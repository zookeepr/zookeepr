"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.proposal import Proposal
from zookeepr.model.event_type import EventType
from zookeepr.model.schedule import Schedule
from zookeepr.model.meta import Session

from meta import Base

"""Validation"""
import formencode
from formencode import validators, Invalid #, schema

class Event(Base):
    __tablename__ = 'event'

    id          = sa.Column(sa.types.Integer, primary_key=True)
    type_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event_type.id'), nullable=False)
    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), unique=True, nullable=True)
    title       = sa.Column(sa.types.Text, nullable=True)     # Should not be set if there is a proposal_id
    url         = sa.Column(sa.types.Text, nullable=True)     # Should not be set if there is a proposal_id
    publish     = sa.Column(sa.types.Boolean, nullable=False, default=True)
    exclusive   = sa.Column(sa.types.Boolean, nullable=False) # No other event may be scheduled at the same
                                                              # time as this event.  There can be only one.
    sequence    = sa.Column(sa.types.Integer, nullable=False, default=1, onupdate='+1')

    # relations
    type     = sa.orm.relation(EventType, backref='events')
    proposal = sa.orm.relation(Proposal, backref=sa.orm.backref('event', uselist=False))
    schedule = sa.orm.relation(Schedule, backref='event')

    # properties


    # object methods
    def increment_sequence(self):
        sequence += 1

    def location_by_time_slot(self, time_slot):
        from zookeepr.model.location import Location
        return Session.query(Location).join(Schedule).filter(Schedule.event==self).filter(Schedule.time_slot==time_slot).all()

    # class methods

    @classmethod
    def find_all(cls):
        return Session.query(Event).order_by(Event.id).all()

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Event).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Event")
        return result

    def find_all_published(cls):
        return Session.query(Event).filter(Event.publish==True).order_by(Event.id).all()

    @classmethod
    def find_published_by_id(cls, id):
        return Session.query(Event).filter(Event.id==id).filter(Event.publish==True).first()

class EventValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Event.find_by_id(value)

    def _from_python(self,value, state):
        return value.id
