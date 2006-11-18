from zookeepr.tests.model import *

class TestInvoiceTable(TableTest):
    """Test the ``invoice`` table.

    """
    table = model.billing.tables.invoice
    samples = [dict(person_id=1,
                    ),
               dict(person_id=2,
                    ),
               ]
    not_nullables = ['person_id']
