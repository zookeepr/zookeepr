"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from zookeepr.model.meta import Session

from proposal_type import ProposalType
from person import Person
from person_proposal_map import person_proposal_map
from attachment import Attachment
from review import Review
from accommodation_assistance_type import AccommodationAssistanceType
from travel_assistance_type import TravelAssistanceType
from proposal_status import ProposalStatus
from target_audience import TargetAudience

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
    proposal_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal_type.id'))

    # type, enumerated in the assistance_type table
    travel_assistance_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('travel_assistance_type.id'))
    accommodation_assistance_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('accommodation_assistance_type.id'))
    status_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal_status.id'))
    target_audience_id = sa.Column(sa.types.Integer, sa.ForeignKey('target_audience.id'))

    video_release = sa.Column(sa.types.Boolean)
    slides_release = sa.Column(sa.types.Boolean)

    # name and url of the project
    project = sa.Column(sa.types.Text)
    url = sa.Column(sa.types.Text)

    # url to a short video
    abstract_video_url = sa.Column(sa.types.Text)

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
    accommodation_assistance = sa.orm.relation(AccommodationAssistanceType)
    travel_assistance = sa.orm.relation(TravelAssistanceType)
    status = sa.orm.relation(ProposalStatus)
    audience = sa.orm.relation(TargetAudience)
    people = sa.orm.relation(Person, secondary=person_proposal_map, backref='proposals')
    attachments = sa.orm.relation(Attachment, lazy=True, cascade='all, delete-orphan')
    reviews = sa.orm.relation(Review, backref='proposal', cascade='all, delete-orphan')


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Proposal, self).__init__(**kwargs)

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

    def _get_accepted(self):
        return self.status.name == 'Accepted'
    accepted = property(_get_accepted)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such object")
        return result
        
    @classmethod
    def find_all(cls):
        return Session.query(Proposal).order_by(Proposal.id).all()

    @classmethod
    def find_all_by_accommodation_assistance_type_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(accommodation_assistance_type_id=id).all()
        if result is None and abort_404:
            abort(404, "No such object")
        return result

    @classmethod
    def find_all_by_travel_assistance_type_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(travel_assistance_type_id=id).all()
        if result is None and abort_404:
            abort(404, "No such object")
        return result

    @classmethod
    def find_all_by_proposal_type_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(proposal_type_id=id).all()
        if result is None and abort_404:
            abort(404, "No such object")
        return result
