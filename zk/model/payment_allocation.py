import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from invoice_item import InvoiceItem
from payment import Payment
from meta import Session

class PaymentAllocation(Base):
    """Stores details of payments made against invoices
    """
    __tablename__ = 'payment_allocation'

    invoice_item_id = sa.Column(sa.types.Integer, sa.ForeignKey('invoice_item.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    payment_id = sa.Column(sa.types.Integer, sa.ForeignKey('payment.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    amount = sa.Column(sa.types.Integer, nullable=False)

    invoice_item=sa.orm.relation(InvoiceItem, backref=sa.orm.backref('payments', lazy=False, cascade='all, delete-orphan'), lazy=False)
    payment=sa.orm.relation(Payment, backref=sa.orm.backref('invoice_item', lazy=False, cascade='all, delete-orphan'), lazy=False)

    def __init__(self, **kwargs):
        super(PaymentAllocation, self).__init__(**kwargs)
