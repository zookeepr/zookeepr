"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from zookeepr.model.meta import Session

def setup(meta):
    pass

class Schedule(Base):
    __tablename__ = 'schedule'

    time_slot_id = sa.Column(sa.types.Integer, sa.ForeignKey('time_slot.id'), primary_key=True)
    location_id  = sa.Column(sa.types.Integer, sa.ForeignKey('location.id' ), primary_key=True)
    event_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event.id'    ), primary_key=True)
