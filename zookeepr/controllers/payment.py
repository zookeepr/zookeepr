import hmac, sha
import string

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *

class PaymentController(SecureController, Create, View):
    """This controller receives payment advice from CommSecure.

    the url /payment/new receives the advice
    """

    model = model.PaymentReceived
    individual = 'payment'
    permissions = {'view': [AuthFunc('is_payee')],
                   }

    def is_payee(self):
        return c.payment.payment_received.invoice.person == c.signed_in_person

    def view(self):

        # TODO Needs auth

        c.person = c.payment.payment_sent.invoice.person

        return super(PaymentController, self).view()

    def new(self):
        fields = dict(request.GET)
        c.payment = model.PaymentReceived(**fields)
        payment_received = c.payment
        self.dbsession.save(payment_received)
        self.dbsession.flush()

        # Verify it really came from Commsecure
        valid_mac = self.verify_hmac(fields)
        if not valid_mac:
            payment_received.result = 'InvalidMac'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/InvalidPayment')

        # What we sent
        payment_sent = payment_received.payment
        if payment_sent is None:
            payment_received.result = 'NonExistentPayment'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/MissingPayment')

        # check invoices match
        if payment_sent.invoice_id != string.atoi(payment_received.InvoiceID):
            payment_received.result = 'InvoiceMisMatch'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/BadInvoice')

        # Check amounts match
        if payment_sent.amount != string.atoi(payment_received.ORIGINAL_AMOUNT):
            payment_received.result = 'AmountMisMatch'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/BadAmount')

        # Check they paid what we asked
        if payment_received.Amount != payment_received.ORIGINAL_AMOUNT:
            payment_received.result = 'DifferentAmountPaid'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/UserPaidDifferentAmount')

        payment_received.result = 'OK'
        self.dbsession.save(payment_received)
        self.dbsession.flush()

        # OK we now have a valid transaction, we redirect the user to the view page
        # so they can see if their transaction was accepted or declined

        redirect_to(controller='payment', action='view', id=payment_received.id)


    def verify_hmac(self, fields):
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
        mac = hmac.new(secret, stringToMAC, sha).hexdigest()

        # Check the MAC
        if mac.lower() == fields['MAC'].lower():
            return True

        return False

