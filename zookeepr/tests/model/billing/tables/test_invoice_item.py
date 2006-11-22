from zookeepr.tests.model import *

class TestInvoiceItemTable(TableTest):
    """Test the ``invoice_item`` table.

    This table contains items in an invoice.
    """
    table = model.billing.tables.invoice_item
    samples = [dict(description='desc1',
                    invoice_id=1,
                    qty=1,
                    cost=1),
               dict(description='desc2',
                    invoice_id=2,
                    qty=2,
                    cost=2),
               ]
    not_nullables = ['description', 'cost', 'invoice_id', 'qty']
