"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            TravelAssistanceType(name='I do not require travel assistance.'),
            TravelAssistanceType(name='I request that linux.conf.au book and pay for air travel.'),
        ]
    )

class TravelAssistanceType(Base):
    __tablename__ = 'travel_assistance_type'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    name = sa.Column(sa.types.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(TravelAssistanceType, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(TravelAssistanceType).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(TravelAssistanceType).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(TravelAssistanceType).order_by(TravelAssistanceType.name).all()

