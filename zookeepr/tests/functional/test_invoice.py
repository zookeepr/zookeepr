import datetime

from zookeepr.tests.functional import *

class TestInvoiceController(SignedInCRUDControllerTest):
    def setUp(self):
        super(TestInvoiceController, self).setUp()
                                                 
        self.invoice = model.Invoice(issue_date=datetime.date(2006,11,21))
        ii1 = model.InvoiceItem(description='line 1', cost=1)
        self.invoice.items.append(ii1)
        self.dbsession.save(ii1)
        self.dbsession.save(self.invoice)
        self.dbsession.flush()

    def tearDown(self):
        self.dbsession.delete(self.invoice)
        self.dbsession.flush()

        super(TestInvoiceController, self).tearDown()

    def test_invoice_view(self):
        self.fail("not really")
