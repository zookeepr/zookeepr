import datetime

from zkpylons.tests.model import *

class TestInvoiceTable(TableTest):
    """Test the ``invoice`` table.

    """
    table = model.billing.tables.invoice
    samples = [dict(person_id=1,
                    issue_date=datetime.datetime(2006, 11, 21),
                    ),
               dict(person_id=2,
                    issue_date=datetime.datetime(2006, 11, 22),
                    ),
               ]
    not_nullables = ['person_id']
