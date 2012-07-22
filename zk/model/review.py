"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from person import Person

from meta import Session
from stream import Stream

import datetime
import random

def setup(meta):
    pass

class Review(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'review'
    __table_args__ = (
            # Only one Review of each Proposal for each Reviewer
            sa.UniqueConstraint('proposal_id', 'reviewer_id', name='ux_review_proposal_reviewer'),
            {}
            )

    id = sa.Column(sa.types.Integer, primary_key=True)

    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=False)
    reviewer_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)
    stream_id = sa.Column(sa.types.Integer, sa.ForeignKey('stream.id'))

    miniconf = sa.Column(sa.types.Text, nullable=False)
    score = sa.Column(sa.types.Integer)
    comment = sa.Column(sa.types.Text, nullable=False)
    private_comment = sa.Column(sa.types.Text, nullable=False)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    reviewer = sa.orm.relation(Person, lazy=True, backref='reviews')
    stream = sa.orm.relation(Stream, lazy=True)


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Review, self).__init__(**kwargs)

    def __repr__(self):
        return '<Review id=%r comment=%r>' % (self.id, self.comment)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Review).filter_by(id=id).first()

    @classmethod
    def find_by_proposal_reviewer(cls, proposal_id, reviewer_id, abort_404 = True):
        result = Session.query(Review).filter_by(proposal_id=proposal_id).filter_by(reviewer_id=reviewer_id).first()
        if result is None and abort_404:
            abort(404, "No such review object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Review).order_by(Review.id).all()

    @classmethod
    def query(cls):
        return Session.query(Review).order_by(Review.id)

    @classmethod
    def by_reviewer(cls, reviewer):
        return cls.query().filter_by(reviewer=reviewer)

    @classmethod
    def stats_query(cls):
        return Session.query(sa.func.count(cls.score).label('reviews'), (sa.func.count(1)-sa.func.count(cls.score)).label('declined'), sa.func.avg(cls.score).label('average'))
