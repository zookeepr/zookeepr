import hmac, sha
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *

class InvoiceController(SecureController, Read):
    model = model.Invoice
    individual = 'invoice'
    permissions = {'view': [AuthFunc('is_payee')],
                   }

    def is_payee(self):
        return c.signed_in_person == self.obj.person

    def verify(self):

        # Support GET or POST
        fields = dict(request.POST)
        if 'MAC' not in fields:
            fields = dict(request.GET)


        # If we don't have a valid MAC then we just throw everything away
        # Since someone is being evil
        valid_mac = self.verify_hmac(fields)
        if not valid_mac:
            redirect_to('/Errors/InvalidPayment')

        # TODO Add some field validation
        # I'm just trusting commsecure to do the right thing at the moment

        # Store the payment attempt
        payment_received = model.PaymentReceived(**fields)
        self.dbsession.save(payment_received)
        self.dbsession.flush()

        # TODO Add some field validation
        # I'm just trusting commsecure to do the right thing at the moment
        payment = payment_received.payment
        # check invoices match
        if payment.invoice_id != payment_received.invoice_id:
            payment_recevied.result = 'InvoiceMisMatch'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/BadInvoice')

        # Check amounts match
        if payment.amount != payment_received.original_amount:
            payment_recevied.result = 'AmountMisMatch'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/BadAmount')

        # Check they paid what we asked
        if payment_received.amount != payment_received.original_amount:
            payment_recevied.result = 'DifferentAmountPaid'
            self.dbsession.save(payment_received)
            self.dbsession.flush()
            redirect_to('/Errors/UserPaidDifferentAmount')

        payment_recevied.result = 'OK'
        self.dbsession.save(payment_received)
        self.dbsession.flush()

        # OK we now have a valid transaction, we redirect the user to the view page
        # so they can see if their transaction was accepted or declined

        redirect_to(controller='payment_received', action='view', id=payment_received.id)

    def verify_hmac(self, fields):
        merchantid =  request.environ['paste.config']['app_conf'].get('commsecure_merchantid')
        secret =  request.environ['paste.config']['app_conf'].get('commsecure_secret')

        # Check for MAC
        if 'MAC' not in fields:
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
