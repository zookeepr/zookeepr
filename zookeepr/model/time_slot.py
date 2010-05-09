"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.proposal import ProposalType

from meta import Base

class Time_Slot(Base):
    __tablename__ = 'time_slot'

    id               = sa.Column(sa.types.Integer,  primary_key=True )
    start_time       = sa.Column(sa.types.DateTime, nullable   =False)
    end_time         = sa.Column(sa.types.DateTime, nullable   =False)
    proposal_type_id = sa.Column(sa.types.Integer,  sa.ForeignKey('proposal_type.id'), nullable   =False)
    
    # relations
    type = sa.orm.relation(ProposalType)
    
    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Time_Slot).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Time Slot")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Time_Slot).order_by(Time_Slot.start_time).all()
