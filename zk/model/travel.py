"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from person import Person

from pylons.controllers.util import abort
from beaker.cache import CacheManager

from meta import Session

import datetime
import random

class Travel(Base):
    """Stores the details of an individuals travel to and from the conference
    """

    __tablename__ = 'travel'

    id = sa.Column(sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), unique=True, nullable=False)
    origin_airport = sa.Column(sa.types.Text, nullable=False)
    destination_airport = sa.Column(sa.types.Text, nullable=False)
    flight_details = sa.Column(sa.types.Text, nullable=False)

    # relations
    #person = sa.orm.relation(Person, backref=sa.orm.backref('travel', cascade="all, delete-orphan", uselist=False))
    person = sa.orm.relation(lambda: Person, backref='travel', lazy='subquery')


    def __init__(self, **kwargs):
        super(Travel, self).__init__(**kwargs)

    def __repr__(self):
        return '<Travel id=%r person=%s origin_airport=%s destination_airport=%s' % (self.id, self.person, self.origin_airport, self.destination_airport)

    @classmethod
    def find_all(self):
        return Session.query(Travel).all()

    @classmethod
    def find_by_id(self, id):
        return Session.query(Travel).get(id)
