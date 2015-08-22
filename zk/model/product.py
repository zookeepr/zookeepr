"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

from ceiling import Ceiling
from product_category import ProductCategory
from product_ceiling_map import product_ceiling_map

class Product(Base):
    """Stores the products used for registration
    """
    # table
    __tablename__ = 'product'
    __table_args__ = (
            # Descriptions should be unique within a category
            sa.UniqueConstraint('category_id', 'description'),
            {}
            )

    id = sa.Column(sa.types.Integer, primary_key=True)
    category_id = sa.Column(sa.types.Integer, sa.ForeignKey('product_category.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    fulfilment_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('fulfilment_type.id'), nullable=True)
    display_order = sa.Column(sa.types.Integer, nullable=False, default=10)
    active = sa.Column(sa.types.Boolean, nullable=False)
    description = sa.Column(sa.types.Text, nullable=False)
    badge_text = sa.Column(sa.types.Text, nullable=True)
    cost = sa.Column(sa.types.Integer, nullable=False)
    auth = sa.Column(sa.types.Text, nullable=True)
    validate = sa.Column(sa.types.Text, nullable=True)

    # relations
    category = sa.orm.relation(ProductCategory, lazy=True, backref=sa.orm.backref('products', order_by=lambda: [Product.display_order, Product.cost]))
    ceilings = sa.orm.relation(Ceiling, secondary=product_ceiling_map, lazy=True, order_by=Ceiling.name, backref='products')
    fulfilment_type = sa.orm.relation('FulfilmentType')


    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(Product).order_by(Product.display_order).order_by(Product.cost).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Product).filter_by(id=id).first()

    @classmethod
    def find_by_category(cls, id):
        return Session.query(Product).filter_by(category_id=id).order_by(Product.display_order).order_by(Product.cost)

    def qty_free(self):
        qty = 0
        for ii in self.invoice_items:
            if not ii.invoice.void and ii.invoice.is_paid:
                qty += ii.free_qty
        return qty

    def qty_sold(self):
        qty = 0
        for ii in self.invoice_items:
            if not ii.invoice.void and ii.invoice.is_paid:
                qty += (ii.qty - ii.free_qty)
        return qty

    def qty_invoiced(self, date=True):
        # date: bool? only count items that are not overdue
        qty = 0
        for ii in self.invoice_items:
            # also count sold items as invoiced since they are valid
            if not ii.invoice.void and ((ii.invoice.is_paid or not ii.invoice.is_overdue or not date)):
                qty += ii.qty
        return qty

    def remaining(self):
        max_ceiling = None
        for c in self.ceilings:
            if c.remaining() > max_ceiling:
                max_ceiling = c.remaining
        return max_ceiling

    def available(self, stock=True, qty=0):
    # bool stock: care about if the product is in stock (ie sold out?)
        if self.active:
           for c in self.ceilings:
                if not c.available(stock, qty):
                    return False
           return True
        else:
            return False

    def can_i_sell(self, person, qty):
        if not self.available():
            return False
        if not self.category.can_i_sell(person, qty):
            return False
        for c in self.ceiling:
            if not c.can_i_sell(qty):
                return False
        return True

    def available_until(self):
        until = []
        for ceiling in self.ceilings:
            if ceiling.available_until != None:
                until.append(ceiling.available_until)
        if len(until) > 0:
            return max(until)

    def clean_description(self, category=False):
        if category == True:
            return self.category.clean_name() + '_' + self.description.replace('-','_').replace("'",'')
        else:
            return self.description.replace('-','_').replace("'",'');

    def __repr__(self):
        return '<Product id=%r active=%r description=%r cost=%r auth=%r validate%r>' % (self.id, self.active, self.description, self.cost, self.auth, self.validate)

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
        super(ProductInclude, self).__init__(**kwargs)

    @classmethod
    def find_by_category(cls, id):
        return Session.query(ProductInclude).filter_by(include_category_id=id)

    @classmethod
    def find_by_product(cls, id):
        return Session.query(ProductInclude).filter_by(product_id=id)
