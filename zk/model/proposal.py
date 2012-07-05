"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from meta import Session

from person import Person
from person_proposal_map import person_proposal_map
from attachment import Attachment
from review import Review
from stream import Stream

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
    meta.Session.add_all(
        [
            ProposalType(name='Presentation'),
            ProposalType(name='Miniconf'),
            ProposalType(name='Tutorial - 1 hour and 45 minutes'),
            ProposalType(name='Tutorial - 3 hours and 30 minutes'),
            ProposalType(name='Poster'),
        ]
    )
    meta.Session.add_all(
        [
            TravelAssistanceType(name='I do not require travel assistance.'),
            TravelAssistanceType(name='I request that linux.conf.au book and pay for air travel.'),
        ]
    )
    meta.Session.add_all(
        [
            TargetAudience(name='Community'),
            TargetAudience(name='User'),
            TargetAudience(name='Developer'),
            TargetAudience(name='Business'),
        ]
    )
    meta.Session.add_all(
        [
            AccommodationAssistanceType(name='I do not require accommodation assistance.'),
            AccommodationAssistanceType(name='I request that linux.conf.au provide student-style single room accommodation for the duration of the conference.'),
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

class TravelAssistanceType(Base):
    __tablename__ = 'travel_assistance_type'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.String(60), unique=True, nullable=False)

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

class AccommodationAssistanceType(Base):
    __tablename__ = 'accommodation_assistance_type'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    name = sa.Column(sa.types.String(120), unique=True, nullable=False)

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

class Proposal(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'proposal'

    id = sa.Column(sa.types.Integer, primary_key=True)

    # title of proposal
    title = sa.Column(sa.types.Text, nullable=False)
    # abstract or description
    abstract = sa.Column(sa.types.Text, nullable=False)
    private_abstract = sa.Column(sa.types.Text, nullable=False)
    technical_requirements = sa.Column(sa.types.Text, nullable=False)

    # type, enumerated in the proposal_type table
    proposal_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal_type.id'), nullable=False)

    # allocated stream of talk
    stream_id = sa.Column(sa.types.Integer, sa.ForeignKey('stream.id'))

    # type, enumerated in the assistance_type table
    travel_assistance_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('travel_assistance_type.id'), nullable=False)
    accommodation_assistance_type_id = sa.Column(sa.types.Integer, sa.ForeignKey('accommodation_assistance_type.id'), nullable=False)
    status_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal_status.id'), nullable=False)
    target_audience_id = sa.Column(sa.types.Integer, sa.ForeignKey('target_audience.id'), nullable=False)

    video_release = sa.Column(sa.types.Boolean, nullable=False)
    slides_release = sa.Column(sa.types.Boolean, nullable=False)

    # name and url of the project
    project = sa.Column(sa.types.Text, nullable=False)
    url = sa.Column(sa.types.Text, nullable=False)

    # url to a short video
    abstract_video_url = sa.Column(sa.types.Text, nullable=False)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    type = sa.orm.relation(ProposalType, backref='proposals')
    stream = sa.orm.relation(Stream)
    accommodation_assistance = sa.orm.relation(AccommodationAssistanceType)
    travel_assistance = sa.orm.relation(TravelAssistanceType)
    status = sa.orm.relation(ProposalStatus)
    audience = sa.orm.relation(TargetAudience)
    people = sa.orm.relation(Person, secondary=person_proposal_map, backref='proposals')
    attachments = sa.orm.relation(Attachment, cascade='all, delete-orphan')
    reviews = sa.orm.relation(Review, backref='proposal', cascade='all, delete-orphan')


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Proposal, self).__init__(**kwargs)

        stream_id = None

    def __repr__(self):
        return '<Proposal id="%r" title="%s">' % (self.id, self.title)

    def _get_accepted(self):
        return self.status.name == 'Accepted'
    accepted = property(_get_accepted)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such proposal object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Proposal).order_by(Proposal.id).all()

    @classmethod
    def find_all_by_accommodation_assistance_type_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(accommodation_assistance_type_id=id).all()
        if result is None and abort_404:
            abort(404, "No such proposal object")
        return result

    @classmethod
    def find_all_by_travel_assistance_type_id(cls, id, abort_404 = True):
        result = Session.query(Proposal).filter_by(travel_assistance_type_id=id).all()
        if result is None and abort_404:
            abort(404, "No such proposal object")
        return result

    # TODO: add an optional filter for removing the signed in user's proposals
    @classmethod
    def find_all_by_proposal_type_id(cls, id, abort_404 = True, include_withdrawn=True):
        result = Session.query(Proposal).filter_by(proposal_type_id=id)
        if not include_withdrawn:
            withdrawn = ProposalStatus.find_by_name('Withdrawn')
            result = result.filter(Proposal.status_id != withdrawn.id)

        result = result.all()
        if result is None and abort_404:
            abort(404, "No such proposal object")
        return result

    @classmethod
    def find_all_accepted(cls):
        #status = ProposalStatus.find_by_name('Accepted')
        #result = Session.query(Proposal).filter_by(status_id=status.id)

        # Optimisation: assume that ProposalStatus of ID=1 is Accepted
        result = Session.query(Proposal).filter_by(status_id=1)
        return result

    @classmethod
    def find_all_accepted_without_event(cls):
        status = ProposalStatus.find_by_name('Accepted')

        return Session.query(Proposal).filter_by(status=status).filter_by(event=None).all()

    @classmethod
    def find_accepted_by_id(cls, id):
        #status = ProposalStatus.find_by_name('Accepted')
        #result = Session.query(Proposal).filter_by(id=id,status_id=status.id)

        # Optimisation: assume that ProposalStatus of ID=1 is Accepted
        result = Session.query(Proposal).filter_by(id=id,status_id=1).one()
        return result

    # TODO: add an optional filter for removing the signed in user's proposals
    @classmethod
    def find_next_proposal(cls, id, type_id, signed_in_person_id):
        withdrawn = ProposalStatus.find_by_name('Withdrawn')
        next = Session.query(Proposal).from_statement("""
              SELECT
                  p.id
              FROM
                  (SELECT id
                   FROM proposal
                   WHERE id <> %d
                     AND status_id <> %d
                     AND proposal_type_id = %d
                   EXCEPT
                       SELECT proposal_id AS id
                       FROM review
                       WHERE review.reviewer_id = %d) AS p
              LEFT JOIN
                      review AS r
                              ON(p.id=r.proposal_id)
              GROUP BY
                      p.id
              ORDER BY COUNT(r.reviewer_id), RANDOM()
              LIMIT 1
        """ % (id, withdrawn.id, type_id, signed_in_person_id))
        next = next.first()
        if next is not None:
            return next.id
        else:
            # looks like you've reviewed everything!
            return None

    @classmethod
    def find_review_summary(cls):
        from review import Review
        return Review.stats_query().join(cls).add_entity(cls).group_by(cls)
