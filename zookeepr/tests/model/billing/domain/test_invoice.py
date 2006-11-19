from zookeepr.tests.model import *

class TestInvoiceDomainModel(CRUDModelTest):
    domain = model.billing.Invoice
    samples = [{},
               {},
               ]

    def setUp(self):
        self.person = model.Person(email_address='testguy@example.org')
        objectstore.save(self.person)
        objectstore.flush()
        self.pid = self.person.id

    def tearDown(self):
        objectstore.delete(Query(model.Person).get(self.pid))
        objectstore.flush()

    def additional(self, invoice):
        invoice.person = self.person
        return invoice
