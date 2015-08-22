import sqlalchemy as sa

from meta import Base

from meta import Session

from lib.model import CommaList

from person import Person
from registration import Registration
from registration_product import RegistrationProduct
from event import Event

class Vote(Base):
    """Votes from registered delegates on events
    """
    __tablename__ = 'vote'

    id = sa.Column(sa.types.Integer, primary_key=True)
    rego_id = sa.Column(sa.types.Integer)
    vote_value = sa.Column(sa.types.Integer)
    comment = sa.Column(sa.types.Text)
    event_id = sa.Column(sa.types.Integer)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations

    def __init__(self, **kwargs):
        super(Vote, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Vote).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such vote object")
        return result

    @classmethod
    def find_by_event_rego(cls,event,rego):
        result = Session.query(Vote).filter_by(event_id=event,rego_id=rego).first()
        return result
        
    @classmethod
    def find_by_event(cls,id):
        result = Session.query(Vote).filter_by(event_id=id)
        return result

    @classmethod
    def find_by_rego(cls,id):
        result = Session.query(Vote).filter_by(rego_id=id)
        return result
    
    @classmethod
    def find_all(cls):
        return Session.query(Vote).order_by(Vote.id).all()
