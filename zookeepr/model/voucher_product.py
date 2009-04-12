"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from voucher import Voucher
from product import Product

from zookeepr.model.meta import Session

class VoucherProduct(Base):
    # table definitions
    __tablename__ = 'voucher_product'

    voucher_id = sa.Column(sa.Integer, sa.ForeignKey('voucher.id'), primary_key=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
    qty = sa.Column(sa.Integer, nullable=False)
    percentage = sa.Column(sa.Integer, nullable=False)

    # relations
    voucher = sa.orm.relation(Voucher, lazy=True, backref=sa.orm.backref('products', lazy=False), cascade="all, delete-orphan")
    product = sa.orm.relation(Product, lazy=True, backref=sa.orm.backref('vouchers', cascade="all, delete-orphan"))

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Voucher, self).__init__(**kwargs)

    def __repr__(self):
        return '<VoucherProduct>'

    @classmethod
    def find_all(cls):
        return Session.query(VoucherProduct).order_by(VoucherProduct.id).all()
