from sqlalchemy import mapper, relation, backref

from tables import invoice_item, invoice
from domain import InvoiceItem, Invoice
from zookeepr.model.core import Person

mapper(InvoiceItem, invoice_item)

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
    },
       )
