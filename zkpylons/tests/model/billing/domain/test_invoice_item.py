import datetime

from zkpylons.tests.model import *

class TestInvoiceItemDomainModel(CRUDModelTest):
    domain = model.billing.InvoiceItem
    samples = [dict(description='desc1',
                    qty=1,
                    cost=1),
               dict(description='desc2',
                    qty=2,
                    cost=2),
               ]

    def setUp(self):
        super(TestInvoiceItemDomainModel, self).setUp()
        self.person = model.Person(email_address='testguy@example.org')
        self.dbsession.save(self.person)
        self.invoice = model.Invoice(issue_date=datetime.datetime(2006,11,21))
        self.dbsession.save(self.invoice)
        self.invoice.person = self.person
        self.dbsession.flush()

        self.pid = self.person.id
        self.iid = self.invoice.id

    def tearDown(self):
        person = self.dbsession.query(model.Person).get(self.pid)
        invoice = self.dbsession.query(model.Invoice).get(self.iid)
        self.dbsession.delete(invoice)
        self.dbsession.delete(person)
        self.dbsession.flush()
        super(TestInvoiceItemDomainModel, self).tearDown()

    def additional(self, ii):
        ii.invoice = self.invoice
        return ii
