"""The application's model objects"""
import sqlalchemy as sa

from schedule import Schedule
from meta import Session

from datetime import date, time, datetime

from meta import Base

from pylons.controllers.util import abort

"""Validation"""
import formencode
from formencode import validators, Invalid #, schema

class TimeSlot(Base):
    __tablename__ = 'time_slot'
    __table_args__ = (
            # No duplicate start_time and end_time combinations
            sa.UniqueConstraint('start_time', 'end_time'),
            sa.CheckConstraint('start_time < end_time'),
            {}
            )

    id         = sa.Column(sa.types.Integer , primary_key = True )
    start_time = sa.Column(sa.types.DateTime, nullable = False)
    end_time   = sa.Column(sa.types.DateTime, nullable = False)
    primary    = sa.Column(sa.types.Boolean,  nullable = False, default=False)
    heading    = sa.Column(sa.types.Boolean,  nullable = False, default=False)

    # relations
    schedule = sa.orm.relation(Schedule, backref='time_slot')

    def exclusive_event(self):
        event = None
        for schedule in self.schedule:
            if event == None and schedule.event.exclusive:
                event = schedule.event
            elif event is not None and event != schedule.event:
                return None
        return event

    @property
    def description(self):
        return str(self.start_time) + ' - ' + str(self.end_time)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(TimeSlot).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(TimeSlot).order_by(TimeSlot.start_time).all()

    @classmethod
    def find_by_date(cls, date, primary=False):
        start   = datetime.combine(date, time.min)
        end     = datetime.combine(date, time.max)

        if primary == True:
            return Session.query(TimeSlot).filter(TimeSlot.start_time.between(start,end)).filter(TimeSlot.primary==primary).order_by(TimeSlot.start_time).all()
        else:
            return Session.query(TimeSlot).filter(TimeSlot.start_time.between(start,end)).order_by(TimeSlot.start_time).all()

    @classmethod
    def find_scheduled_dates(cls):
        time_slots = cls.find_all()

        scheduled_dates = []
        for time_slot in time_slots:
            if time_slot.start_time.date() not in scheduled_dates:
                scheduled_dates.append(time_slot.start_time.date())
        return scheduled_dates

class TimeSlotValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return TimeSlot.find_by_id(value)

    def _from_python(self,value, state):
        return value.id
