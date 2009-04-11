"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            ProposalType(name='Presentation'),
            ProposalType(name='Miniconf'),
            ProposalType(name='Tutorial'),
        ]
    )

class ProposalType(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'proposal_type'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    name = sa.Column(sa.types.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(ProposalType, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(ProposalType).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(ProposalType).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(ProposalType).order_by(ProposalType.name).all()

