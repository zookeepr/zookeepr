"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.schedule import Schedule

from meta import Base

class Location(Base):
    __tablename__ = 'location'

    id           = sa.Column(sa.types.Integer, primary_key = True )
    display_name = sa.Column(sa.types.Text,    nullable    = False)

    # relations
    schedule = sa.orm.relation(Schedule, backref='location')

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Location).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such location")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Location).order_by(Location.id).all()

