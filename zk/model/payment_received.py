import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from payment import Payment

from meta import Session

class PaymentReceived(Base):
    """Stores details of payments as returned by the payment gateway
    """
    __tablename__ = 'payment_received'

    id = sa.Column(sa.types.Integer, primary_key=True)
    approved = sa.Column(sa.types.Boolean, nullable=False)
    validation_errors = sa.Column(sa.types.String, nullable=True)
    payment_id = sa.Column(sa.types.Integer, sa.ForeignKey('payment.id'), nullable=True)
    invoice_id = sa.Column(sa.types.Integer, sa.ForeignKey('invoice.id'), nullable=True)

    # various details returned by the payment gateway
    success_code = sa.Column(sa.types.String, nullable=False)
    amount_paid = sa.Column(sa.types.Integer, nullable=True)
    currency_used = sa.Column(sa.types.String, nullable=True)
    auth_code = sa.Column(sa.types.String, nullable=True)
    card_name = sa.Column(sa.types.String, nullable=True)
    card_type = sa.Column(sa.types.String, nullable=True)
    card_number = sa.Column(sa.types.String, nullable=True)
    card_expiry = sa.Column(sa.types.String, nullable=True)
    card_mac = sa.Column(sa.types.String, nullable=True)
    gateway_ref = sa.Column(sa.types.String, nullable=True)
    response_text = sa.Column(sa.types.String, nullable=False)
    client_ip_zookeepr = sa.Column(sa.types.String, nullable=False)
    client_ip_gateway = sa.Column(sa.types.String, nullable=False)
    email_address = sa.Column(sa.types.String, nullable=False)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    payment = sa.orm.relation(Payment, backref='payment_received')

    def __init__(self, **kwargs):
        super(PaymentReceived, self).__init__(**kwargs)

    def __repr__(self):
        return '<PaymentReceived id=%r>' % (self.id)

    @classmethod
    def find_all(cls):
        return Session.query(PaymentReceived).order_by(PaymentReceived.id).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(PaymentReceived).filter_by(id=id).first()

    @classmethod
    def find_by_payment(cls, id):
        return Session.query(PaymentReceived).filter_by(payment_id=id).first()

    @classmethod
    def find_by_invoice(cls, id):
        return Session.query(PaymentReceived).filter_by(invoice_id=id)

    @classmethod
    def find_by_email(cls, id):
        return Session.query(PaymentReceived).filter_by(email_address=id)
