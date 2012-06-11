from zkpylons.tests.model import *

class TestPaymentTable(TableTest):
    table = model.billing.tables.payment
    samples = [dict(amount=1,
                    invoice_id=1,
                    ),
               dict(amount=2,
                    invoice_id=2,
                    )
               ]
    not_nullables = ['amount', 'invoice_id']
