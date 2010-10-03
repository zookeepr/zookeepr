"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from zookeepr.model.proposal import Proposal
from zookeepr.model.time_slot import TimeSlot
from zookeepr.model.location import Location

class Event(Base):
    __tablename__ = 'event'

    id          = sa.Column(sa.types.Integer, primary_key=True)
    title       = sa.Column(sa.types.Text,    nullable=True  )
    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=True )
    exclusive   = sa.Column(sa.types.Boolean, nullable=False  ) # No other event may be scheduled at the same 
                                                                # time as this event.  There can be only one.
    url                = sa.Column(sa.types.Text, nullable=True)
    publish    = sa.Column(sa.types.Boolean, nullable=False, default=True)
    sequence    = sa.Column(sa.types.Integer, nullable=False, default=1)

    # relations

    proposal = sa.orm.relation(Proposal)
    time     = sa.orm.relation(TimeSlot, secondary='event_time_slot_location_map', backref = 'event')
    location = sa.orm.relation(Location, secondary='event_time_slot_location_map', backref = 'event')

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Event).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Event).order_by(Event.id).all()

