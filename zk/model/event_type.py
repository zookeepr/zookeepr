"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort

from meta import Session

"""Validation"""
import formencode
from formencode import validators, Invalid #, schema

class EventType(Base):
    __tablename__ = 'event_type'

    id = sa.Column(sa.types.Integer, primary_key = True )
    name = sa.Column(sa.types.Text, unique=True, nullable = False)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(EventType).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such event type")
        return result

    @classmethod
    def find_by_name(cls, name):
        return Session.query(EventType).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(EventType).order_by(EventType.id).all()


class EventTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return EventType.find_by_id(value)

    def _from_python(self,value, state):
        return value.id
