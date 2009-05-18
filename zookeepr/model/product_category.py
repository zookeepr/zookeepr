"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
    )

class ProductCategory(Base):
    """Stores the product categories used for registration
    """
    __tablename__ = 'product_category'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)
    description = sa.Column(sa.types.Text, nullable=False)
    
    # display is used to determine the type of field to collect input with (see templates/registration/form.mako)
    # display is also used to validate the output (see controllers/registration.py)
    # available types so far: radio, select, checkbox, qty
    # The first three are self explanatory and act as the HTML counterpart
    # qty is an interger validated text box
    display = sa.Column(sa.types.Text, nullable=False) 
    
    min_qty = sa.Column(sa.types.Integer, nullable=True)
    max_qty = sa.Column(sa.types.Integer, nullable=True)

    def __init__(self, **kwargs):
        super(ProductCategory, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(ProductCategory).order_by(ProductCategory.name).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(ProductCategory).filter_by(id=id).one()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(ProductCategory).filter_by(name=name).first()

    def available_products(self, person, stock=True):
        # bool stock: care about if the product is in stock (ie sold out?)
        products = []
        for product in self.products:
            if product.available(stock):
                products.append(product)
        return products

    def qty_person_sold(self, person):
        qty = 0
        for i in person.invoices:
            for ii in i.invoice_items:
                if ii.product.category == self:
                    qty += ii.qty
        return qty

    def can_i_sell(self, person, qty):
        if self.qty_person_sold(person) + qty <= self.max_qty:
            return True
        else:
            return False

    def __repr__(self):
        return '<ProductCategory id=%r name=%r description=%r display=%r min_qty=%r max_qty=%r>' % (self.id, self.name, self.description, self.display, self.min_qty, self.max_qty)
