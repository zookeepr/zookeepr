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

        fields = dict(request.POST)

        valid_mac = self.verify_hmac(fields)
        if not valid_mac:
            redirect_to('/Errors/InvalidPayment')

            


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




