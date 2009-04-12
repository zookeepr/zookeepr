"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from product import Product
from product_category import ProductCategory

from zookeepr.model.meta import Session

def setup(meta):
    pass

class ProductInclude(Base):
    """Stores the product categories that are included in another product
    """
    __tablename__ = 'product_include'

    product_id = sa.Column(sa.types.Integer, sa.ForeignKey('product.id'), primary_key=True)
    include_category_id = sa.Column(sa.types.Integer, sa.ForeignKey('product_category.id'), primary_key=True)
    include_qty = sa.Column(sa.types.Integer, nullable=False)

    product = sa.orm.relation(Product, backref='included', lazy=False)
    include_category = sa.orm.relation(ProductCategory)

    def __init__(self, **kwargs):
        super


