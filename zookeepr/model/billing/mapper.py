from sqlalchemy import mapper

from tables import invoice_item
from domain import InvoiceItem

mapper(InvoiceItem, invoice_item)
