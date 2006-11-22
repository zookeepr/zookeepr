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
        payment_received = model.PaymentReceived()
        payment_received.map_fields(fields)
        self.dbsession.save(payment_received)
        self.dbsession.flush()


        redirect_to('/ShouldntGetHere')


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
