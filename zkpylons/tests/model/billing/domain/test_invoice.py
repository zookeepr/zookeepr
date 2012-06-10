import datetime

from zkpylons.tests.model import *

class TestInvoiceDomainModel(CRUDModelTest):
    domain = model.billing.Invoice
    samples = [dict(issue_date=datetime.datetime(2006,11,21)),
               dict(issue_date=datetime.datetime(2006,11,22)),
               ]

    def setUp(self):
        super(TestInvoiceDomainModel, self).setUp()

        self.person = model.Person(email_address='testguy@example.org')
        self.dbsession.save(self.person)
        self.dbsession.flush()
        self.pid = self.person.id

        self.dbsession.echo_uow = True

    def tearDown(self):
        p = self.dbsession.query(model.Person).get(self.pid)
        self.dbsession.delete(p)
        self.dbsession.flush()

        super(TestInvoiceDomainModel, self).tearDown()

    def additional(self, invoice):
        invoice.person = self.person
        return invoice

    def test_item_add(self):
        i = model.Invoice(issue_date=datetime.datetime(2006,11,21))
        i.person = self.person
        ii = model.InvoiceItem(description='b', qty=1, cost=2)
        self.dbsession.save(i)
        self.dbsession.save(ii)
        i.items.append(ii)
        self.dbsession.flush()

        self.failUnless(ii in self.dbsession.query(model.InvoiceItem).select())

        # make sure ii gets deleted when i does
        self.dbsession.delete(i)
        self.dbsession.flush()
        self.dbsession.clear()

        iis = self.dbsession.query(model.InvoiceItem).select()
        print "iis:", iis
        self.assertEqual([], iis)
