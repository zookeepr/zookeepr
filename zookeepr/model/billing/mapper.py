from sqlalchemy import mapper, relation, backref

from tables import invoice_item, invoice, payment_received, invoice_payment_received_map
from domain import InvoiceItem, Invoice, PaymentReceived
from zookeepr.model.core import Person

mapper(InvoiceItem, invoice_item)

mapper(PaymentReceived, payment_received)

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
    'payment': relation(PaymentReceived, secondary=invoice_payment_received_map,
                        backref='payment_received'
                        ),
    },

    )
