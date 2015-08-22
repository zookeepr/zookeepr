"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

from registration import Registration
from product import Product

class RegistrationProduct(Base):
    __tablename__ = 'registration_product_map'

    registration_id = sa.Column(sa.types.Integer, sa.ForeignKey('registration.id'), primary_key=True)
    product_id = sa.Column(sa.types.Integer, sa.ForeignKey('product.id'), primary_key=True)
    qty = sa.Column(sa.types.Integer, nullable=False)

    registration=sa.orm.relation(Registration, backref=sa.orm.backref('products', lazy=False, cascade='all, delete-orphan'), lazy=False)
    product=sa.orm.relation(Product, backref=sa.orm.backref('registrations', lazy=True, cascade='all, delete-orphan'), lazy=False)

    def __init__(self, **kwargs):
        super(RegistrationProduct, self).__init__(**kwargs)

    def __repr__(self):
        return '<RegistrationProduct registration_id=%r product_id=%r qty=%r>' % (self.registration_id, self.product_id, self.qty)
