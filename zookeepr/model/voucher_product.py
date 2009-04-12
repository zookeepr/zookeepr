"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from role import Role
from person import Person
from person_role_map import person_role_map

from zookeepr.model.meta import Session

class VoucherProduct(Base):
    __tablename__ = 'voucher_product'

    voucher_id = sa.Column(sa.Integer, sa.ForeignKey('voucher.id'), primary_key=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
    qty = sa.Column(sa.Integer, nullable=False)
    percentage = sa.Column(sa.Integer, nullable=False)


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Voucher, self).__init__(**kwargs)

    def __repr__(self):
        return '<VoucherProduct>'

    @classmethod
    def find_all(cls):
        return Session.query(VoucherProduct).order_by(VoucherProduct.id).all()
