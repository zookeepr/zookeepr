from zookeepr.tests.model import *

class TestInvoiceItemTable(TableTest):
    """Test the ``invoice_item`` table.

    This table contains items in an invoice.
    """
    table = model.billing.tables.invoice_item
    samples = [dict(description='desc1',
                    cost=1),
               dict(description='desc2',
                    cost=2),
               ]
    not_nullables = ['description', 'cost']
