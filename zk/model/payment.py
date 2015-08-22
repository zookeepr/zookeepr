import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from meta import Session

class Payment(Base):
    """Stores details of payments made against invoices
    """
    __tablename__ = 'payment'

    id = sa.Column(sa.types.Integer, primary_key=True)
    invoice_id = sa.Column(sa.types.Integer, sa.ForeignKey('invoice.id'), nullable=False)
    amount = sa.Column(sa.types.Integer, nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    def __init__(self, **kwargs):
        super(Payment, self).__init__(**kwargs)

    def __repr__(self):
        return '<Payment id=%r>' % (self.id)

    @classmethod
    def find_all(cls):
        return Session.query(Payment).order_by(Payment.id).all()

    @classmethod
    def find_by_id(cls, id, abort_404 = False):
        result =  Session.query(Payment).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such payment object")
        return result

