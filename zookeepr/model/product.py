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
                      cost="16000", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Earlybird Hobbyist Ticket",
                      cost="29000", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_earlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Hobbyist Ticket",
                      cost="36500", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Earlybird Professional Ticket",
                      cost="63500", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_earlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Professional Ticket",
                      cost="78500", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    product.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Fairy Penguin Sponsorship",
                      cost="150000", auth=None, validate=None)
    product.ceilings.append(ceiling_conference)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Speaker Ticket",
                      cost="0", auth="AuthFunc('is_speaker').authorise(self)", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Miniconf Organiser Ticket",
                      cost="0", auth="AuthFunc('is_miniconf_org').authorise(self)", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    product = Product(category_id='1', active=True, description="Volunteer Ticket",
                      cost="0", auth="AuthFunc('is_volunteer').authorise(self)", validate=None)
    product.ceilings.append(ceiling_all_conference)
    meta.Session.add(product);

    meta.Session.add_all(
        [
            # Shirts
            Product(category_id='2', active=True, description="Men's Small Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's Medium Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's Large Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's X Large Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's XX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's XXX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's XXXX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Men's XXXXX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Small Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Medium Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's Large Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's X Large Shirt", cost="2000", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's XX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's XXX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's XXXX Large Shirt", cost="2200", auth=None, validate=None),
            Product(category_id='2', active=True, description="Women's XXXXX Large Shirt", cost="2200", auth=None, validate=None),

            # Dinner
            Product(category_id='3', active=True, description="Dinner Tickets", cost="8000", auth=None, validate="ProDinner(dinner_field='product_26_qty',ticket_category='category_1',ticket_id=[5,4])"),
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
            Product(category_id='5', active=True, description="Adult", cost="20000", auth=None, validate="PPEmail(adult_field='product_30_qty',email_field='partner_email')"),
            Product(category_id='5', active=True, description="Child (0-3 years old)", cost="0", auth=None, validate="PPChildrenAdult(current_field='product_31_qty',adult_field='product_30_qty')"),
            Product(category_id='5', active=True, description="Child (4-6 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_32_qty',adult_field='product_30_qty')"),
            Product(category_id='5', active=True, description="Child (7-9 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_33_qty',adult_field='product_30_qty')"),
            Product(category_id='5', active=True, description="Child (10-12 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_34_qty',adult_field='product_30_qty')"),
            Product(category_id='5', active=True, description="Child (13-17 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_35_qty',adult_field='product_30_qty')"),
        ]
    )

    # Product includes
    meta.Session.add_all(
        [
            # Include 1 Shirt in all registration types
            ProductInclude(product_id='1', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='2', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='3', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='4', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='5', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='6', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='7', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='8', include_category_id='2', include_qty='1'),
            ProductInclude(product_id='9', include_category_id='2', include_qty='2'),

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
    description = sa.Column(sa.types.Text, nullable=False, unique=True)
    cost = sa.Column(sa.types.Integer, nullable=False)
    auth = sa.Column(sa.types.Text, nullable=True)
    validate = sa.Column(sa.types.Text, nullable=True)

    # relations
    ceilings = sa.orm.relation(Ceiling, secondary=product_ceiling_map, lazy=True, backref='products')
    category = sa.orm.relation(ProductCategory, lazy=True, backref='products')

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(Product).order_by(Product.cost).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Product).filter_by(id=id).first()

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
