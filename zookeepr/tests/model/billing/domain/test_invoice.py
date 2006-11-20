from zookeepr.tests.model import *

class TestInvoiceDomainModel(CRUDModelTest):
    domain = model.billing.Invoice
    samples = [{},
               {},
               ]

    def setUp(self):
        self.person = model.Person(email_address='testguy@example.org')
        self.dbsession.save(self.person)
        self.dbsession.flush()
        self.pid = self.person.id

    def tearDown(self):
        self.dbsession.delete(Query(model.Person).get(self.pid))
        self.dbsession.flush()

    def additional(self, invoice):
        invoice.person = self.person
        return invoice
