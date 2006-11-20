from zookeepr.lib.base import *
from zookeepr.lib.auth import *

class InvoiceController(SecureController, View):
    model = model.Invoice
    permissions = {'view': [AuthFunc('is_payee')],
                   }

    def is_payee(self):
        return c.signed_in_person == self.obj.person
