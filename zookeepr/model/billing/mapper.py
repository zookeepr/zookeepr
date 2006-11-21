from sqlalchemy import mapper, relation, backref

from tables import invoice_item, invoice, payment_received, invoice_payment_received_map, invoice_registration_map, payment_sent
from domain import InvoiceItem, Invoice, PaymentReceived, PaymentSent
from zookeepr.model.core import Person
from zookeepr.model.registration import Registration

mapper(InvoiceItem, invoice_item)

mapper(PaymentSent, payment_sent)

mapper(PaymentReceived, payment_received,
       properties = {
            'payment': relation(PaymentSent,
                                backref='payment_sent'
                       ),
            },
      )

mapper(Invoice, invoice,
       properties = {
    'person': relation(Person,
                       lazy=True,
                       backref=backref('invoices', cascade="all, delete-orphan"),
                       ),
    'registration': relation(Registration, secondary=invoice_registration_map,
                             backref='invoice'),
    'items': relation(InvoiceItem,
                      backref='invoice',
                      cascade="all, delete-orphan",
                      ),
    'payment': relation(PaymentReceived, secondary=invoice_payment_received_map,
                        backref='payment_received'
                        ),
    },

    )
