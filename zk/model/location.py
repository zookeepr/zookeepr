"""The application's model objects"""
import sqlalchemy as sa

from time_slot import TimeSlot
from schedule import Schedule
from meta import Session

from datetime import date, time, datetime

from meta import Base

from pylons.controllers.util import abort

"""Validation"""
import formencode
from formencode import validators, Invalid #, schema

class Location(Base):
    __tablename__ = 'location'

    id            = sa.Column(sa.types.Integer, primary_key = True)
    display_name  = sa.Column(sa.types.Text, nullable = False)
    display_order = sa.Column(sa.types.Integer)
    capacity      = sa.Column(sa.types.Integer)

    # relations
    schedule = sa.orm.relation(Schedule, backref='location')

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Location).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such location")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Location).order_by(Location.id).all()

    # This is to get a list of all the rooms that have talks (event.type_id=1) scheduled in them, for a given day
    # The purpose is to produce columns in the schedule for the rooms
    @classmethod
    def find_scheduled_by_date_and_type(cls, date, event_type):
        from schedule import Schedule
        from event import Event
        from time_slot import TimeSlot

        start   = datetime.combine(date,time(0,0,0))
        end     = datetime.combine(date,time(23,59,59))
        return Session.query(Location).join(Schedule).join(Event).join(TimeSlot).filter(Event.type==event_type).filter(TimeSlot.start_time.between(start, end)).order_by(Location.display_order).all()

class LocationValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Location.find_by_id(value)

    def _from_python(self,value, state):
        return value.id
