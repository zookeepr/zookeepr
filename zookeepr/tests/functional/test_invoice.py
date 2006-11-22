import datetime

from zookeepr.tests.functional import *

class TestInvoiceController(SignedInCRUDControllerTest):
    def setUp(self):
        super(TestInvoiceController, self).setUp()
                                                 
        self.invoice = model.Invoice(issue_date=datetime.datetime(2006,11,21))
        self.dbsession.save(self.invoice)
        self.person.invoices.append(self.invoice)

        ii1 = model.InvoiceItem(description='line 1', qty=2, cost=100)
        self.invoice.items.append(ii1)
        self.dbsession.save(ii1)
        
        ii2 = model.InvoiceItem(description="awesomeness", qty=1, cost=250)
        self.invoice.items.append(ii2)
        self.dbsession.save(ii2)
        
        self.dbsession.flush()
        self.iid = self.invoice.id

    def tearDown(self):
        invoice = self.dbsession.query(model.Invoice).get(self.iid)
        self.dbsession.delete(invoice)
        self.dbsession.flush()

        super(TestInvoiceController, self).tearDown()

    def test_invoice_view(self):
        resp = self.app.get('/invoice/%d' % self.iid)
        print resp

        resp.mustcontain("Linux Australia")
        resp.mustcontain("ABN")
        resp.mustcontain("line 1")
        resp.mustcontain("$2.00")
        resp.mustcontain("$4.50")
