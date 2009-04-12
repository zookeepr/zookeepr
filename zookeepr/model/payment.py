import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from invoice import Invoice

from zookeepr.model.meta import Session

class Payment(Base):
    """Stores details of payments made against invoices
    """
    __tablename__ = 'payment'

    id = sa.Column(sa.types.Integer, primary_key=True)
    invoice_id = sa.Column(sa.types.Integer, sa.ForeignKey('invoice.id'), nullable=False)
    amount = sa.Column(sa.types.Integer, nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relation
    invoice = sa.orm.relation(Invoice, backref='payments')

    def __repr__(self):
        return '<Payment id=%r>' % (self.id)
