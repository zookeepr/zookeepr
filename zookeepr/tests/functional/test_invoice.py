import datetime

from zookeepr.tests.functional import *

class TestInvoiceController(SignedInCRUDControllerTest):
    def setUp(self):
        super(TestInvoiceController, self).setUp()
                                                 
        self.invoice = model.Invoice(issue_date=datetime.date(2006,11,21))
        ii1 = model.InvoiceItem(description='line 1', cost=1)
        self.invoice.items.append(ii1)
        self.person.invoices.append(self.invoice)
        self.dbsession.save(ii1)
        ii2 = model.InvoiceItem(description="awesomeness", cost=2.50)
        self.invoice.items.append(ii2)
        self.dbsession.save(ii2)
        self.dbsession.save(self.invoice)
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
        resp.mustcontain("$1.00")
        resp.mustcontain("Total: $3.50")
