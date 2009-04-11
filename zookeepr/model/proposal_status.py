"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            ProposalStatus(name='Accepted'),
            ProposalStatus(name='Rejected'),
            ProposalStatus(name='Pending'),
            ProposalStatus(name='Withdrawn'),
            ProposalStatus(name='Backup'),
        ]
    )

class ProposalStatus(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'proposal_status'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    name = sa.Column(sa.types.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(ProposalStatus, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(ProposalStatus).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(ProposalStatus).filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return Session.query(ProposalStatus).order_by(ProposalStatus.name).all()

