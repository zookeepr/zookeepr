import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from product import Product

from meta import Session

class InvoiceItem(Base):
    """Stores the line items for an invoice
    """
    __tablename__ = 'invoice_item'

    id = sa.Column(sa.types.Integer, primary_key=True)
    invoice_id = sa.Column(sa.types.Integer, sa.ForeignKey('invoice.id'), nullable=False)
    product_id = sa.Column(sa.types.Integer, sa.ForeignKey('product.id'), nullable=True)
    description = sa.Column(sa.types.Text, nullable=False)
    qty = sa.Column(sa.types.Integer, nullable=False)
    free_qty = sa.Column(sa.types.Integer, nullable=False, default=0)
    cost = sa.Column(sa.types.Integer, nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False,
                                            default=sa.func.current_timestamp(),
                                            onupdate=sa.func.current_timestamp())

    # mapped attributes
    total = sa.orm.column_property(cost * qty)

    # relation
    product = sa.orm.relation(Product, lazy=True, backref='invoice_items')

    def __init__(self, **kwargs):
        super(InvoiceItem, self).__init__(**kwargs)

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r qty=%r cost=%r>' % (self.id, self.description, self.qty, self.cost)
