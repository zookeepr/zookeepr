"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            AccommodationAssistanceType(name='I do not require accomodation assistance.'),
            AccommodationAssistanceType(name='I request that linux.conf.au provide student-style single room accommodation for the length of the conference.'),
        ]
    )

class AccommodationAssistanceType(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'accommodation_assistance_type'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    name = sa.Column(sa.types.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(AccommodationAssistanceType, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(AccommodationAssistanceType).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(AccommodationAssistanceType).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(AccommodationAssistanceType).order_by(AccommodationAssistanceType.name).all()

