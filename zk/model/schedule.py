"""The application's model objects"""
from datetime import datetime, date, time
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from meta import Session

class Schedule(Base):
    __tablename__ = 'schedule'
    __table_args__ = (
            # Only allow one Event to be scheduled in any TimeSlot and Location
            sa.UniqueConstraint('time_slot_id', 'location_id'),
            {}
            )

    id           = sa.Column(sa.types.Integer, primary_key=True)
    time_slot_id = sa.Column(sa.types.Integer, sa.ForeignKey('time_slot.id'), nullable=False)
    location_id  = sa.Column(sa.types.Integer, sa.ForeignKey('location.id'), nullable=False)
    event_id     = sa.Column(sa.types.Integer, sa.ForeignKey('event.id'), nullable=False)

    overflow  = sa.Column(sa.types.Boolean, nullable=True)
    video_url = sa.Column(sa.types.Text)
    audio_url = sa.Column(sa.types.Text)
    slide_url = sa.Column(sa.types.Text)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    @classmethod
    def find_all(cls):
        return Session.query(Schedule).order_by(Schedule.id).all()

    @classmethod

    def find_by_id(cls, id, abort_404 = True, published = True):
        if published:
            #I can't see why this exists as events as published, not schedules
            #Original: result = Session.query(Schedule).filter_by(id=id).filter_by(published=published).first()
            result = Session.query(Schedule).filter_by(id=id).first()
        else:
            result = Session.query(Schedule).filter_by(id=id).first()

        if result is None and abort_404:
            abort(404, "No such Schedule")
        return result

    @classmethod
    def find_by_date(cls, date, primary=False):
        from time_slot import TimeSlot
        start   = datetime.combine(date,time.min)
        end     = datetime.combine(date,time.max)

        return Session.query(Schedule).options(sa.orm.eagerload_all('time_slot.schedule'), sa.orm.eagerload('location'), sa.orm.eagerload_all('event.proposal.people')).join(TimeSlot).filter(TimeSlot.start_time.between(start,end)).order_by(TimeSlot.start_time).all()
