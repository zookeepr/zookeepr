"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort
from zookeepr.model.meta import Session

class RegistrationProduct(Base):
    __tablename__ 'registration_product'

    registration_id = sa.Column(sa.types.Integer, ForeignKey('registration.id'), primary_key=True),
    product_id = sa.Column(sa.types.Integer, ForeignKey('product.id'), primary_key=True),
    qty = sa.Column(sa.types.Integer, nullable=False),

    registration=sa.orm.relation(Registration, backref=backref('products', lazy=False, cascade='all, delete-orphan'), lazy=False)
    product=sa.orm.relation(Product, backref=backref('registrations', lazy=True, cascade='all, delete-orphan'), lazy=False)

    def __repr__(self):
        return '<RegistrationProduct registration_id=%r product_id=%r qty=%r>' % (self.registration_id, self.product_id, self.qty)
