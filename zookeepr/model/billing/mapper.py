from sqlalchemy import mapper, relation

from tables import invoice_item, invoice
from domain import InvoiceItem, Invoice
from zookeepr.model.core import Person

mapper(InvoiceItem, invoice_item)

mapper(Invoice, invoice,
       properties = {
    'person': relation(Person)
    },
       )
