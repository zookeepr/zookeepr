import hmac
import sha
import smtplib
import string

from zookeepr.lib.base import *
from zookeepr.lib.crud import *

class PaymentController(BaseController, Create, View):
    """This controller receives payment advice from CommSecure.

    the url /payment/new receives the advice
    """

    model = model.PaymentReceived
    individual = 'payment'

    def view(self):
        # hack because we don't use auth:
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])

            if c.signed_in_person != c.payment.payment_sent.invoice.person:
                redirect_to('/account/signin')
                                                    
        c.person = c.payment.payment_sent.invoice.person

        return super(PaymentController, self).view()

    def new(self):
        fields = dict(request.GET)
        
        pr = model.PaymentReceived(**fields)
        self.dbsession.save(pr)
        # save object now to get the id and be sure it's saved in case
        # the validation blows up
        self.dbsession.flush()

        # Start long chain of validation.
        # I'd like to replace this with a "Chain of Command" pattern to do
        # the validation, possibly even using a regular formencode validation
        # chain.
        
        if not self._verify_hmac(fields):
            # Verify the HMAC to be sure that it came from CommSecure.
            pr.result = 'InvalidMac'
            error = '/Errors/InvalidPayment'
            # email seven
            self._mail_warn('Invalid HMAC', pr)
            
        elif pr.payment_sent is None:
            # Check that this data references a payment we sent to CommSecure.
            pr.result = 'NonExistentPayment'
            error = '/Errors/MissingPayment'
            # email seven
            self._mail_warn('Nonexistent Payment', pr)

        elif pr.payment_sent.invoice_id != string.atoi(pr.InvoiceID):
            # check invoices match
            pr.result = 'InvoiceMisMatch'
            error = '/Errors/BadInvoice'

            self._mail_warn("Invoice Numbers Don't Match", pr)

        elif pr.ORIGINAL_AMOUNT is not None and pr.payment_sent.amount != string.atoi(pr.ORIGINAL_AMOUNT):
            # Check amounts match
            pr.result = 'AmountMisMatch'
            error = '/Errors/BadAmount'

            self._mail_warn("Amount Paid Doesn't Match What We Stored", pr)

        elif pr.ORIGINAL_AMOUNT is not None and pr.Amount != pr.ORIGINAL_AMOUNT:
            # Check they paid what we asked
            pr.result = 'DifferentAmountPaid'
            error = '/Errors/UserPaidDifferentAmount'

            self._mail_warn("Amount Paid Doesn't Match What We Asked", pr)
            
        else:
            pr.result = 'OK'
            error = None

        self.dbsession.flush()

        # OK we now have a valid transaction, we redirect the user to the view page
        # so they can see if their transaction was accepted or declined

        if error:
            redirect_to(error)
        else:
            redirect_to(controller='payment', action='view', id=pr.id)

    def _verify_hmac(self, fields):
        merchantid =  request.environ['paste.config']['app_conf'].get('commsecure_merchantid')
        secret =  request.environ['paste.config']['app_conf'].get('commsecure_secret')

        # Check for MAC
        if 'MAC' not in fields:
            print "OATH"
            print ' '.join(fields.keys())
            print "\n\n\n\n"
            return False

        # Generate the MAC
        keys = fields.keys()
        keys.sort()
        stringToMAC = '&'.join(['%s=%s' % (key, fields[key]) for key in keys if key != 'MAC'])
        #print stringToMAC
        mac = hmac.new(secret, stringToMAC, sha).hexdigest()

        # Check the MAC
        if mac.lower() == fields['MAC'].lower():
            return True

        return False


    def _mail_warn(self, msg, pr):
        s = smtplib.SMTP("localhost")
        body = render('payment/warning.myt', fragment=True, subject=msg, pr=pr)
        s.sendmail("seven-contact@lca2007.linux.org.au",
                   "seven-contact@lca2007.linux.org.au",
                   body)
        s.quit()
