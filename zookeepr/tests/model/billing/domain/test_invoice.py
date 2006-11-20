from zookeepr.tests.model import *

class TestInvoiceDomainModel(CRUDModelTest):
    domain = model.billing.Invoice
    samples = [{},
               {},
               ]

    def setUp(self):
        super(TestInvoiceDomainModel, self).setUp()

        self.person = model.Person(email_address='testguy@example.org')
        self.dbsession.save(self.person)
        self.dbsession.flush()
        self.pid = self.person.id

    def tearDown(self):
        self.dbsession.delete(self.dbsession.query(model.Person).get(self.pid))
        self.dbsession.flush()

        super(TestInvoiceDomainModel, self).tearDown()

    def additional(self, invoice):
        invoice.person = self.person
        return invoice
