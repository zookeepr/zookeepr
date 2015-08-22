"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from person import Person
from product import Product

from meta import Session

class Voucher(Base):
    __tablename__ = 'voucher'

    id = sa.Column(sa.types.Integer, primary_key=True)
    code = sa.Column(sa.types.Text, nullable=False, unique=True)
    comment = sa.Column(sa.types.Text, nullable=False)
    leader_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    leader = sa.orm.relation(Person, backref=sa.orm.backref('vouchers', cascade="all, delete-orphan"))

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Voucher, self).__init__(**kwargs)

    def __repr__(self):
        return '<Voucher id=%r code=%r comment=%r leader_id=%r>' % (self.id, self.code, self.comment, self.leader_id)

    @classmethod
    def find_all(cls):
        return Session.query(Voucher).order_by(Voucher.id).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Voucher).filter_by(id=id).first()

    @classmethod
    def find_by_code(cls, code):
        return Session.query(Voucher).filter_by(code=code).first()

class VoucherProduct(Base):
    # table definitions
    __tablename__ = 'voucher_product'

    voucher_id = sa.Column(sa.Integer, sa.ForeignKey('voucher.id'), primary_key=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
    qty = sa.Column(sa.Integer, nullable=False)
    percentage = sa.Column(sa.Integer, nullable=False)

    # relations
    voucher = sa.orm.relation(Voucher, lazy=True, backref=sa.orm.backref('products', cascade="all, delete-orphan"))
    product = sa.orm.relation(Product, lazy=True, backref=sa.orm.backref('vouchers', cascade="all, delete-orphan"))

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(VoucherProduct, self).__init__(**kwargs)

    def __repr__(self):
        return '<VoucherProduct>'

    @classmethod
    def find_all(cls):
        return Session.query(VoucherProduct).order_by(VoucherProduct.id).all()
