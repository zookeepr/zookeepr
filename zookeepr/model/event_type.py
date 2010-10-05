"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

class EventType(Base):
    __tablename__ = 'event_type'

    id           = sa.Column(sa.types.Integer, primary_key = True )
    display_name = sa.Column(sa.types.Text,    nullable    = False)


    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(EventType).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such event type")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(EventType).order_by(EventType.id).all()

