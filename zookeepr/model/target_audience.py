"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            TargetAudience(name='Community'),
            TargetAudience(name='User'),
            TargetAudience(name='Developer'),
            TargetAudience(name='Business'),
        ]
    )

class TargetAudience(Base):
    __tablename__ = 'target_audience'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(TargetAudience, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(TargetAudience).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(TargetAudience).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(TargetAudience).order_by(TargetAudience.name).all()

