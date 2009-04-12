"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
    )

class Product(Base):
    """Stores the products used for registration
    """
    __tablename__ = 'product'


    id = sa.Column(sa.types.Integer, primary_key=True)

    category_id = sa.Column(sa.types.Integer, sa.ForeignKey('product_category.id'), nullable=False)

    active = sa.Column(sa.types.Boolean, nullable=False)

    description = sa.Column(sa.types.Text, nullable=False, unique=True)

    cost = sa.Column(sa.types.Integer, nullable=False)

    auth = sa.Column(sa.types.Text, nullable=True)

    validate = sa.Column(sa.types.Text, nullable=True)


    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(Product).order_by(Product.cost).all()

    def qty_sold(self):
        qty = 0
        for ii in self.invoice_items:
            if not ii.invoice.void and ii.invoice.paid():
                if self.category.name == 'Accomodation':
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
                if self.category.name == 'Accomodation':
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
