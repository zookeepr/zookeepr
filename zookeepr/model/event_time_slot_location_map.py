"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

def setup(meta):
    pass


event_time_slot_location_map = sa.Table('event_time_slot_location_map',metadata,
        sa.Column('time_slot_id',sa.types.Integer, sa.ForeignKey('time_slot.id'), primary_key=True),
        sa.Column('location_id' ,sa.types.Integer, sa.ForeignKey('location.id' ), primary_key=True),
        sa.Column('event_id'    ,sa.types.Integer, sa.ForeignKey('event.id'    ), primary_key=True))
