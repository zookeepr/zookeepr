"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from zookeepr.model.proposal import Proposal
from zookeepr.model.timeSlot import TimeSlot
from zookeepr.model.location import Location

class Event(Base):
    __tablename__ = 'event'

    id          = sa.Column(sa.types.Integer, primary_key=True)
    title       = sa.Column(sa.types.Text,    nullable=False  )
    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=True )
    exclusive   = sa.Column(sa.types.Boolean, nullable=False  ) # No other event may be scheduled at the same 
                                                                # time as this event.  There can be only one.

    # relations

    proposal = sa.orm.relation(Proposal)
    time     = sa.orm.relation(TimeSlot, secondary='event_time_slot_location_map', backref = 'time_slot')
    location = sa.orm.relation(Location, secondary='event_time_slot_location_map', backref = 'location' )
    
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Event).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Event).order_by(Event.id).all()

    
