import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from meta import Session

from lib.model import CommaList

from person import Person
from product import Product

class Volunteer(Base):
    """Information about a potential volunteer
    """
    __tablename__ = 'volunteer'

    id = sa.Column(sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), unique=True, nullable=False)
    areas = sa.Column(CommaList, nullable=False)
    other = sa.Column(sa.types.Text, nullable=False)
    experience = sa.Column(sa.types.Text)
    accepted = sa.Column(sa.types.Boolean)
    ticket_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('product.id'), nullable=True)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    person = sa.orm.relation(Person, backref=sa.orm.backref('volunteer', cascade="all, delete-orphan", lazy=True, uselist=False))
    ticket_type = sa.orm.relation(Product)

    def __init__(self, **kwargs):
        super(Volunteer, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Volunteer).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such volunteer object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Volunteer).order_by(Volunteer.id).all()
