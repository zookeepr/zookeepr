"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from zookeepr.model.meta import Session

def setup(meta):
    pass

class Schedule(Base):
    __tablename__ = 'schedule'

    # We do not allow multiple events to be scheduled at the same time and location
    time_slot_id = sa.Column(sa.types.Integer, sa.ForeignKey('time_slot.id'), primary_key=True)
    location_id  = sa.Column(sa.types.Integer, sa.ForeignKey('location.id'), primary_key=True, index=True)

    event_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event.id'), index=True)

    @classmethod
    def find_all(cls):
        return Session.query(Schedule).order_by(Schedule.time_slot_id).all()
