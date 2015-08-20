# pytest magic: from .conftest import app_config, db_session$

from .fixtures import InvoiceFactory, InvoiceItemFactory, PersonFactory
from zk.model.invoice import Invoice
from zk.model.invoice_item import InvoiceItem

class TestInvoice(object):
    def test_item_add(self, db_session):
        invoice_item = InvoiceItemFactory()
        invoice = InvoiceFactory(items=[invoice_item])

        db_session.flush()

        assert invoice_item in db_session.query(InvoiceItem).all()
        assert invoice_item in invoice.items

        # Make sure invoice item gets deleted when invoice does
        db_session.delete(invoice)
        assert len(db_session.query(InvoiceItem).all()) == 0
