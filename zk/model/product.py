"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

from ceiling import Ceiling
from product_category import ProductCategory
from product_ceiling_map import product_ceiling_map

def setup(meta):
    category_ticket = ProductCategory.find_by_name('Ticket')

    ceiling_conference = Ceiling.find_by_name('conference-paid')
    ceiling_all_conference = Ceiling.find_by_name('conference-all')
    ceiling_earlybird = Ceiling.find_by_name('conference-earlybird')
    ceiling_nonearlybird = Ceiling.find_by_name('conference-non-earlybird')

    # Tickets
    ticket_student = Product(category=category_ticket, active=True, description="Student Ticket",
                      cost="12500", auth=None, validate=None)
    ticket_student.ceilings.append(ceiling_conference)
    ticket_student.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_student);

    ticket_hobbyist_eb = Product(category=category_ticket, active=True, description="Earlybird Hobbyist Ticket",
                      cost="29900", auth=None, validate=None)
    ticket_hobbyist_eb.ceilings.append(ceiling_conference)
    ticket_hobbyist_eb.ceilings.append(ceiling_all_conference)
    ticket_hobbyist_eb.ceilings.append(ceiling_earlybird)
    meta.Session.add(ticket_hobbyist_eb);

    ticket_hobbyist = Product(category=category_ticket, active=True, description="Hobbyist Ticket",
                      cost="37500", auth=None, validate=None)
    ticket_hobbyist.ceilings.append(ceiling_conference)
    ticket_hobbyist.ceilings.append(ceiling_all_conference)
    ticket_hobbyist.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(ticket_hobbyist);

    ticket_professional_eb = Product(category=category_ticket, active=True, description="Earlybird Professional Ticket",
                      cost="63500", auth=None, validate=None)
    ticket_professional_eb.ceilings.append(ceiling_conference)
    ticket_professional_eb.ceilings.append(ceiling_all_conference)
    ticket_professional_eb.ceilings.append(ceiling_earlybird)
    meta.Session.add(ticket_professional_eb);

    ticket_professional = Product(category=category_ticket, active=True, description="Professional Ticket",
                      cost="79500", auth=None, validate=None)
    ticket_professional.ceilings.append(ceiling_conference)
    ticket_professional.ceilings.append(ceiling_all_conference)
    ticket_professional.ceilings.append(ceiling_nonearlybird)
    meta.Session.add(ticket_professional);

    ticket_fairy_penguin = Product(category=category_ticket, active=True, description="Fairy Penguin Sponsor",
                      cost="150000", auth=None, validate=None)
    ticket_fairy_penguin.ceilings.append(ceiling_conference)
    ticket_fairy_penguin.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_fairy_penguin);

    ticket_speaker = Product(category=category_ticket, active=True, description="Speaker Ticket",
                      cost="0", auth="self.is_speaker()", validate=None)
    ticket_speaker.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_speaker);

    ticket_miniconf = Product(category=category_ticket, active=True, description="Miniconf Organiser Ticket",
                      cost="0", auth="self.is_miniconf_org()", validate=None)
    ticket_miniconf.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_miniconf);

    ticket_volunteer_free = Product(category=category_ticket, active=True, description="Volunteer Ticket (Free)",
                      cost="0", auth="self.is_volunteer(product)", validate=None)
    ticket_volunteer_free.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_volunteer_free);

    ticket_volunteer_paid = Product(category=category_ticket, active=True, description="Volunteer Ticket (paid)",
                      cost="12500", auth="self.is_volunteer(product)", validate=None)
    ticket_volunteer_paid.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_volunteer_paid);

    ticket_press = Product(category=category_ticket, active=True, description="Press Ticket",
                      cost="0", auth="self.is_role('press')", validate=None)
    ticket_press.ceilings.append(ceiling_all_conference)
    meta.Session.add(ticket_press)

    ticket_team = Product(category=category_ticket, active=True, description="Team Ticket",
                      cost="0", auth="self.is_role('team')", validate=None)

    # Miniconfs
    category_miniconf = ProductCategory.find_by_name('Miniconfs')

    ceiling_miniconf_all = Ceiling.find_by_name('miniconf-all')
    ceiling_miniconf_monday = Ceiling.find_by_name('miniconf-monday')
    ceiling_miniconf_tuesday = Ceiling.find_by_name('miniconf-tuesday')
    ceiling_rocketry = Ceiling.find_by_name('miniconf-rocketry')

    product = Product(category=category_miniconf, active=True, description="Monday Southern Plumbers",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday Haecksen",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday Multimedia + Music",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday Arduino",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday Open Programming",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday The Business of Open Source",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Monday Freedom in the cloud",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Multicore and Parallel Computing",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Rocketry",
                      cost="20000", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    product.ceilings.append(ceiling_rocketry)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Systems Administration",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Open in the public sector ",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Mobile FOSS",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Data Storage",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Research and Student Innovation",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_tuesday)
    meta.Session.add(product)

    product = Product(category=category_miniconf, active=True, description="Tuesday Libre Graphics Day",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_miniconf_all)
    product.ceilings.append(ceiling_miniconf_monday)
    meta.Session.add(product)

    # Shirts
    category_shirt = ProductCategory.find_by_name('T-Shirt')

    ceiling_shirt_all = Ceiling.find_by_name('shirt-all')
    ceiling_shirt_men = Ceiling.find_by_name('shirt-men')
    ceiling_shirt_women = Ceiling.find_by_name('shirt-women')

    product = Product(category=category_shirt, active=True, description="Men's Small", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's Medium", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)


    product = Product(category=category_shirt, active=True, description="Men's Large", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's XL", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's 2XL", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's 3XL", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's 5XL", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Men's 7XL", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_men)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 6", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 8", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 10", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 12", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 14", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 16", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 18", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 20", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    product = Product(category=category_shirt, active=True, description="Women's Size 22", cost="2500", auth=None, validate=None)
    product.ceilings.append(ceiling_shirt_all)
    product.ceilings.append(ceiling_shirt_women)
    meta.Session.add(product)

    # Penguin Dinner
    category_penguin = ProductCategory.find_by_name('Penguin Dinner Ticket')

    ceiling_penguin_all = Ceiling.find_by_name('penguindinner-all')

    product = Product(category=category_penguin, active=True, description="Adult", cost="9000", auth=None, validate="ProDinner(dinner_field='product_Penguin Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[4,5,6,7,8,11,12])")
    product.ceilings.append(ceiling_penguin_all)
    meta.Session.add(product)

    product = Product(category=category_penguin, active=True, description="Child", cost="2000", auth=None, validate=None)
    product.ceilings.append(ceiling_penguin_all)
    meta.Session.add(product)

    Product(category=category_penguin, active=True, description="Infant", cost="0", auth=None, validate=None)
    meta.Session.add(product)

    # Speakers Dinner
    category_speakers = ProductCategory.find_by_name('Speakers Dinner Ticket')

    ceiling_speakers_all = Ceiling.find_by_name('speakersdinner-all')

    product = Product(category=category_speakers, active=True, description="Adult", cost="0", validate="ProDinner(dinner_field='product_Speakers Dinner Ticket_Adult_qty',ticket_category='category_Ticket',ticket_id=[7,8,12])", auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
    product.ceilings.append(ceiling_speakers_all)
    meta.Session.add(product)

    product = Product(category=category_speakers, active=True, description="Child", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
    product.ceilings.append(ceiling_speakers_all)
    meta.Session.add(product)

    product = Product(category=category_speakers, active=True, description="Infant", cost="0", validate=None , auth="self.is_speaker() or self.is_miniconf_org() or self.is_role('team')")
    meta.Session.add(product)

    # Accommodation
    category_accomodation = ProductCategory.find_by_name('Accommodation')
    ceiling_accom_all = Ceiling.find_by_name('accomodation-all')
    ceiling_accom_selfbook = Ceiling.find_by_name('accomodation-selfbook')
    product = Product(category=category_accomodation, active=True, description="I will organise my own",
                      cost="0", auth=None, validate=None)
    product.ceilings.append(ceiling_accom_all)
    product.ceilings.append(ceiling_accom_selfbook)
    meta.Session.add(product);

    # Partners' Programme
    category_partners = ProductCategory.find_by_name('Partners\' Programme')
    ceiling_partners_all = Ceiling.find_by_name('partners-all')

    partners_adult = Product(category=category_partners, active=True, description="Adult", cost="23500", auth=None, validate="PPDetails(adult_field='product_Partners Programme_Adult_qty', email_field='partner_email', name_field='partner_name', mobile_field='partner_mobile')")
    partners_adult.ceilings.append(ceiling_partners_all)
    meta.Session.add(partners_adult);

    product = Product(category=category_partners, active=True, description="Child (3-14 years old)", cost="16500", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (3_14 years old)_qty',adult_field='product_Partners Programme_Adult_qty')")
    product.ceilings.append(ceiling_partners_all)
    meta.Session.add(product);

    product = Product(category=category_partners, active=True, description="Infant (0-2 years old)", cost="0", auth=None, validate="PPChildrenAdult(current_field='product_Partners Programme_Child (0_2 years old)_qty',adult_field='product_Partners Programme_Adult_qty')")
    product.ceilings.append(ceiling_partners_all)
    meta.Session.add(product);

    # Product includes
    meta.Session.add_all(
        [
            # Include 1 Shirt in all registration types
            ProductInclude(product=ticket_student, include_category=category_shirt, include_qty='1'),           # Student
            ProductInclude(product=ticket_hobbyist_eb, include_category=category_shirt, include_qty='1'),       # Hobbyist EB
            ProductInclude(product=ticket_hobbyist, include_category=category_shirt, include_qty='1'),          # Hobbyist
            ProductInclude(product=ticket_professional_eb, include_category=category_shirt, include_qty='1'),   # Pro EB
            ProductInclude(product=ticket_professional, include_category=category_shirt, include_qty='1'),      # Pro
            ProductInclude(product=ticket_fairy_penguin, include_category=category_shirt, include_qty='1'),     # Fairy
            ProductInclude(product=ticket_speaker, include_category=category_shirt, include_qty='1'),           # Speaker
            ProductInclude(product=ticket_miniconf, include_category=category_shirt, include_qty='1'),          # Miniconf
            ProductInclude(product=ticket_volunteer_free, include_category=category_shirt, include_qty='2'),    # Volunteer
            ProductInclude(product=ticket_volunteer_paid, include_category=category_shirt, include_qty='2'),    # Volunteer
            ProductInclude(product=ticket_press, include_category=category_shirt, include_qty='1'),             # Press
            ProductInclude(product=ticket_team, include_category=category_shirt, include_qty='6'),              # Team
            #ProductInclude(product=partners_adult, include_category=category_shirt, include_qty='1'),           # Partner's Programme get a t-shirt

            # Include 1 Dinner for Professional+miniconf and for Speaker registrations
            ProductInclude(product=ticket_professional_eb, include_category=category_penguin, include_qty='1'), # Pro EB
            ProductInclude(product=ticket_professional, include_category=category_penguin, include_qty='1'),    # Pro
            ProductInclude(product=ticket_fairy_penguin, include_category=category_penguin, include_qty='1'),   # Fairy
            ProductInclude(product=ticket_speaker, include_category=category_penguin, include_qty='1'),         # Speaker
            ProductInclude(product=ticket_miniconf, include_category=category_penguin, include_qty='1'),        # Miniconf
            ProductInclude(product=ticket_press, include_category=category_penguin, include_qty='1'),           # Press
            ProductInclude(product=ticket_team, include_category=category_penguin, include_qty='2'),            # Team

            # Include 2 partners in the partners program for speakers
            ProductInclude(product=ticket_speaker, include_category=category_partners, include_qty='2'),
        ]
    )

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
    display_order = sa.Column(sa.types.Integer, nullable=False)
    active = sa.Column(sa.types.Boolean, nullable=False)
    description = sa.Column(sa.types.Text, nullable=False)
    cost = sa.Column(sa.types.Integer, nullable=False)
    auth = sa.Column(sa.types.Text, nullable=True)
    validate = sa.Column(sa.types.Text, nullable=True)

    # relations
    category = sa.orm.relation(ProductCategory, lazy=True, backref=sa.orm.backref('products', order_by=lambda: [Product.display_order, Product.cost]))
    ceilings = sa.orm.relation(Ceiling, secondary=product_ceiling_map, lazy=True, order_by=Ceiling.name, backref='products')


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
