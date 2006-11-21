from sqlalchemy import mapper, relation, backref

from tables import invoice_item, invoice, invoice_registration_map
from domain import InvoiceItem, Invoice
from zookeepr.model.core import Person
from zookeepr.model.registration import Registration

mapper(InvoiceItem, invoice_item)

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
    },
       )
