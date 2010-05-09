"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.proposal import ProposalType

from meta import Base

class TimeSlot(Base):
    __tablename__ = 'time_slot'

    id         = sa.Column(sa.types.Integer , primary_key = True )
    start_time = sa.Column(sa.types.DateTime, nullable    = False)
    end_time   = sa.Column(sa.types.DateTime, nullable    = False)
    type       = sa.Column(sa.types.Text)  
        
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(TimeSlot).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(TimeSlot).order_by(TimeSlot.start_time).all()
