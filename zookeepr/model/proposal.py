"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

from proposal_type import ProposalType
from assistance_type import AssistanceType
from person import Person
#from person_proposal_map import person_proposal_map

def setup(meta):
    pass

class Proposal(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'proposal'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    title = sa.Column(sa.types.Text)
    # abstract or description
    abstract = sa.Column(sa.types.Text)

    # type, enumerated in the proposal_type table
    #proposal_type_id = sa.Column(sa.types.Integer
    #       ForeignKey('proposal_type.id'))

    # type, enumerated in the assistance_type table
    #sa.Column('assistance_type_id', Integer
    #       ForeignKey('assistance_type.id'))

    # name and url of the project
    project = sa.Column(sa.types.Text)
    url = sa.Column(sa.types.Text)

    # url to a short video
    abstract_video_url = sa.Column(sa.types.Text)

    # Is it accepted?
    accepted = sa.Column(sa.types.Boolean)

    code = sa.Column(sa.types.Integer)
    scheduled = sa.Column(sa.types.DateTime)
    finished = sa.Column(sa.types.DateTime)
    theatre = sa.Column(sa.types.Text)
    building = sa.Column(sa.types.Text)

    recorded_ogg = sa.Column(sa.types.Text)
    recorded_spx = sa.Column(sa.types.Text)
    wiki_name = sa.Column(sa.types.Text)
    slides_link = sa.Column(sa.types.Text)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    type = sa.orm.relation(ProposalType)
    assistance = sa.orm.relation(AssistanceType)
    # FIXME
    #people = sa.orm.relation(Person, secondary=person_proposal_map, backref='proposals')
    #attachements = sa.orm.relation(Attachement, lazy=True, cascade='all, delete-orphan')
    #reviews = sa.orm.relation(Review, backref='proposal', cascade='all, delete-orphan')


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Proposal, self).__init__(**kwargs)

        self.acceppted = False
        self.code = None
        self.scheduled = None
        self.finished = None
        self.theatre = None
        self.building = None
        self.recorded_ogg = None
        self.recorded_spx = None
        self.wiki_name = None
        self.slides_link = None


    def __repr__(self):
        return '<Proposal id="%r" title="%s">' % (self.id, self.title)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Proposal).filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return Session.query(Proposal).order_by(Proposal.id).all()

