"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.proposal import Proposal
from zookeepr.model.event_type import EventType
from zookeepr.model.schedule import Schedule

from meta import Base

class Event(Base):
    __tablename__ = 'event'

    id          = sa.Column(sa.types.Integer, primary_key=True)
    title       = sa.Column(sa.types.Text,    nullable=True  )
    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=True )
    exclusive   = sa.Column(sa.types.Boolean, nullable=False  ) # No other event may be scheduled at the same 
                                                                # time as this event.  There can be only one.
    url         = sa.Column(sa.types.Text, nullable=True)
    publish     = sa.Column(sa.types.Boolean, nullable=False, default=True)
    sequence    = sa.Column(sa.types.Integer, nullable=False, default=1)
    type_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event_type.id'), nullable=False)

    # relations

    proposal = sa.orm.relation(Proposal, backref='events')
    type     = sa.orm.relation(EventType, backref='events');   
    schedule = sa.orm.relation(Schedule, backref='event')

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Event).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Event).order_by(Event.id).all()

