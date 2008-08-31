from sqlalchemy.orm import mapper, relation, backref

from tables import *
from domain import *
from zookeepr.model.core import Person
from zookeepr.model.registration import Registration
from zookeepr.model.registration.tables import registration

mapper(Ceiling, ceiling)

mapper(Product, product,
       properties = {
             'ceilings': relation(Ceiling, secondary=product_ceiling_map, lazy=False,
                                 backref='products'),
            },
     )

mapper(InvoiceItem, invoice_item,
       properties = {
             'product': relation(Product, lazy=True,
                                 backref='invoice_items'),
            },
      )

mapper(Payment, payment,
       properties = {
             'invoice': relation(Invoice)
            },
      )

mapper(PaymentReceived, payment_received,
       properties = {
             'invoice': relation(Invoice),
             'payment_sent': relation(Payment,
                                      backref='payments_received'
                                     ),
            },
      )

mapper(Invoice, invoice,
       properties = {
             'person': relation(Person,
                                lazy=True,
                                backref=backref('invoices', cascade="all, delete-orphan"),
                               ),
             'items': relation(InvoiceItem,
                               backref='invoice',
                               cascade="all, delete-orphan",
                              ),
             # All payments
             'payments': relation(PaymentReceived),
             # Good payments, we got the money
             'good_payments': relation(PaymentReceived,
                              primaryjoin=and_(payment_received.c.InvoiceID == invoice.c.id,
                                               payment_received.c.result == 'OK',
                                               payment_received.c.Status == 'Accepted'
                                      )
                            ),
             # Bad payments, something went wrong
             'bad_payments': relation(PaymentReceived,
                             primaryjoin=and_(payment_received.c.InvoiceID == invoice.c.id,
                                              payment_received.c.result != 'OK'
                                             )
                                     )
            },
       )

mapper(VoucherCode, voucher_code,
        properties = {
             'registrations': relation(Registration,
                                       uselist=True,
                                       primaryjoin=registration.c.voucher_code==voucher_code.c.code,
                                       foreign_keys=voucher_code.c.code,
                                      ),
             'leader': relation(Person,
                                lazy=True,
                                backref=backref('voucher_codes', cascade="all, delete-orphan"),
                               ),
            },
      )
