"""The application's model objects"""
import datetime
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from zookeepr.model.meta import Session

def setup(meta):
    pass

class Schedule(Base):
    __tablename__ = 'schedule'

    id           = sa.Column(sa.types.Integer, primary_key=True)
    time_slot_id = sa.Column(sa.types.Integer, sa.ForeignKey('time_slot.id'))
    location_id  = sa.Column(sa.types.Integer, sa.ForeignKey('location.id'))

    # We do not allow multiple events to be scheduled at the same time and location
    sa.UniqueConstraint('time_slot_id', 'location_id')

    event_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event.id'), index=True)

    @classmethod
    def find_all(cls):
        return Session.query(Schedule).order_by(Schedule.time_slot_id).all()

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Schedule).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Schedule")
        return result

    @classmethod
    def find_by_start_time(cls, start_time, increment=datetime.timedelta(0), exclusive=False):
        from zookeepr.model.time_slot import TimeSlot
        from zookeepr.model.event import Event
        return Session.query(Schedule).join(TimeSlot).join(Event).filter(TimeSlot.start_time.between(start_time, start_time + increment)).filter(Event.exclusive==exclusive).all()

    @classmethod
    def find_by_start_time_and_location(cls, start_time, location, increment=datetime.timedelta(0)):
        from zookeepr.model.time_slot import TimeSlot
        return Session.query(Schedule).join(TimeSlot).filter(TimeSlot.start_time.between(start_time, start_time + increment)).filter(Schedule.location==location).first()
