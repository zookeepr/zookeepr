# coding=utf-8
"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

from ceiling import Ceiling
from product_category import ProductCategory
from product_ceiling_map import product_ceiling_map

def setup(meta):
    ceiling_conference = Ceiling.find_by_name('conference')
    ceiling_all_conference = Ceiling.find_by_name('all-conference')
    ceiling_earlybird = Ceiling.find_by_name('earlybird')
    ceiling_nonearlybird = Ceiling.find_by_name('non-earlybird')
    ceiling_uniaccom = Ceiling.find_by_name('uniaccom')

    # Tickets
    product = Product(category_id='1', active=True, description="Concession/Student Ticket",
                      cost="24900", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Earlybird Hobbyist Ticket",
                      cost="39900", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_earlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Hobbyist Ticket",
                      cost="49900", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Earlybird Professional Ticket",
                      cost="79900", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_earlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Professional Ticket",
                      cost="99900", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Kororā Little Blue Penguin Sponsorship",
                      cost="225000", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Speaker Ticket",
                      cost="0", auth="self.is_speaker()", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Miniconf Organiser Ticket",
                      cost="0", auth="self.is_miniconf_org()", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Volunteer Ticket",
                      cost="0", auth="self.is_volunteer()", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    meta.Session.add_all(
        [
            # Shirts
            Product(category_id='2', active=True, description="Men's XS", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's Small", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's Medium", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's Large", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's XL", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's 2XL", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's 3XL", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's 5XL", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's 7XL", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 6", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 8", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 10", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 12", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 14", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 16", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 18", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 20", cost="2500", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Size 22", cost="2500", auth=None, validate=None),

            # Dinner
            Product(category_id='3', active=True, description="Adult", cost="11500", auth=None, validate="ProDinner(dinner_field='product_Penguin Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[8,7,6,5,4])"),
            Product(category_id='3', active=True, description="Child", cost="2000", auth=None, validate=None),
            Product(category_id='3', active=True, description="Infant", cost="0", auth=None, validate=None),

            # Speakers Dinner
            Product(category_id='6', active=True, description="Adult", cost="0", validate="ProDinner(dinner_field='product_Speakers Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[7,8])", auth="self.is_speaker() or self.is_miniconf_org()"),
            Product(category_id='6', active=True, description="Child", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org()"),
            Product(category_id='6', active=True, description="Infant", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org()"),
        ]
    )

    # Accommodation
    product = Product(category_id='4', active=True, description="I will organise my own",
                      cost="0", auth=None, validate=None)
    meta.Session.add(product);
    product = Product(category_id='4', active=True, description="Wrest Point (Visit Accommodation page)",
                      cost="0", auth=None, validate=None)
    meta.Session.add(product);
    product = Product(category_id='4', active=True, description="University Accommodation - Includes Breakfast! (price per night)",
                      cost="6000", auth=None, validate=None)
    product.ceilings.append(ceiling_uniaccom)
    meta.Session.add(product);

    # Partner's Programme
    meta.Session.add_all(
        [
            Product(category_id='5', active=True, description="Adult", cost="28000", auth=None, validate="PPDetails(adult_field='product_Partners Programme_Adult_qty', email_field='partner_email', name_field='partner_name', mobile_field='partner_mobile')"),
            Product(category_id='5', active=True, description="Child (3-14 years old)", cost="21000", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (3_14 years old)_qty',adult_field='product_Partners Programme_Adult_qty')"),
            Product(category_id='5', active=True, description="Infant (0-2 years old)", cost="0", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (0_2 years old)_qty',adult_field='product_Partners Programme_Adult_qty')"),
        ]
    )

    # Product includes
    meta.Session.add_all(
        [
            # Include 1 Shirt in all registration types
            ProductInclude(product_id='1', include_category_id='2', include_qty='1'), # Student
            ProductInclude(product_id='2', include_category_id='2', include_qty='1'), # Hobbyist EB
            ProductInclude(product_id='3', include_category_id='2', include_qty='1'), # Hobbyist
            ProductInclude(product_id='4', include_category_id='2', include_qty='1'), # Pro EB
            ProductInclude(product_id='5', include_category_id='2', include_qty='1'), # Pro
            ProductInclude(product_id='6', include_category_id='2', include_qty='1'), # Fairy
            ProductInclude(product_id='7', include_category_id='2', include_qty='1'), # Speaker
            ProductInclude(product_id='8', include_category_id='2', include_qty='1'), # Miniconf
            ProductInclude(product_id='9', include_category_id='2', include_qty='2'), # Volunteer
            ProductInclude(product_id='37', include_category_id='2', include_qty='1'), # Partner's Programme get a t-shirt

            # Include 1 Dinner for Professional+miniconf and 2 for Speaker registrations
            ProductInclude(product_id='4', include_category_id='3', include_qty='1'), # pro EB
            ProductInclude(product_id='5', include_category_id='3', include_qty='1'), # pro
            ProductInclude(product_id='6', include_category_id='3', include_qty='1'), # fairy
            ProductInclude(product_id='7', include_category_id='3', include_qty='2'), # speaker
            ProductInclude(product_id='8', include_category_id='3', include_qty='1'), # miniconf

            # Include 5 partners in the partners program for speakers
            ProductInclude(product_id='7', include_category_id='5', include_qty='5'),
        ]
    )

class Product(Base):
    """Stores the products used for registration
    """
    # table
    __tablename__ = 'product'

    id = sa.Column(sa.types.Integer, primary_key=True)
    category_id = sa.Column(sa.types.Integer, sa.ForeignKey('product_category.id'), nullable=False)
    active = sa.Column(sa.types.Boolean, nullable=False)
    description = sa.Column(sa.types.Text, nullable=False)
    cost = sa.Column(sa.types.Integer, nullable=False)
    auth = sa.Column(sa.types.Text, nullable=True)
    validate = sa.Column(sa.types.Text, nullable=True)

    # relations
    ceilings = sa.orm.relation(Ceiling, secondary=product_ceiling_map, lazy=True, backref='products')
    category = sa.orm.relation(ProductCategory, lazy=True, backref='products')

    # Descriptions should be unique within a category
    sa.UniqueConstraint(category_id, description, name='category_description');

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(Product).order_by(Product.cost).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Product).filter_by(id=id).first()

    @classmethod
    def find_by_category(cls, id):
        return Session.query(Product).filter_by(category_id=id)

    def qty_sold(self):
        qty = 0
        for ii in self.invoice_items:
            if not ii.invoice.void and ii.invoice.paid():
                if self.category.name == 'Accommodation':
                    qty += 1
                else:
                    qty += ii.qty
        return qty

    def qty_invoiced(self, date=True):
        # date: bool? only count items that are not overdue
        qty = 0
        for ii in self.invoice_items:
            # also count sold items as invoiced since they are valid
            if not ii.invoice.void and ((ii.invoice.paid() or not ii.invoice.overdue() or not date)):
                if self.category.name == 'Accommodation':
                    qty += 1
                else:
                    qty += ii.qty
        return qty

    def remaining(self):
        max_ceiling = None
        for c in self.ceilings:
            if c.remaining() > max_ceiling:
                max_ceiling = c.remaining
        return max_ceiling

    def available(self, stock=True):
    # bool stock: care about if the product is in stock (ie sold out?)
        if self.active:
           for c in self.ceilings:
                if not c.available(stock):
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

    def clean_description(self):
        return self.description.replace('-','_');

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
