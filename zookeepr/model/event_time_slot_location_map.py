"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.time_slot import Time_Slot
from zookeepr.model.location  import Location
from zookeepr.model.event     import Event

from meta import Base

class Event_Time_Slot_Location_map(Base):
    __tablename__ = 'event_time_slot_location_map'
    
    time_slot_id = sa.Column(sa.types.Integer, sa.ForeignKey('time_slot.id'), primary_key=True)
    location_id  = sa.Column(sa.types.Integer, sa.ForeignKey('location.id' ), primary_key=True)
    event_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event.id'    ), primary_key=True)
    
    # relations
    time_slot = sa.orm.relation(Time_Slot)
    location  = sa.orm.relation(Location)
    event     = sa.orm.relation(Event)
                      

    @classmethod
    def find_all(cls):
        return Session.query(Event_Time_Slot_Location_Map).all()

