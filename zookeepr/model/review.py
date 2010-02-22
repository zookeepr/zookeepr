"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from person import Person

from zookeepr.model.meta import Session
from zookeepr.model.stream import Stream

import datetime
import random

def setup(meta):
    pass

class Review(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'review'

    id = sa.Column(sa.types.Integer, primary_key=True)

    proposal_id = sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=False)
    reviewer_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)
    sa.UniqueConstraint('proposal_id', 'reviewer_id', name='ux_review_proposal_reviewer')

    score = sa.Column(sa.types.Integer)

    stream_id = sa.Column(sa.types.Integer, sa.ForeignKey('stream.id'))
    miniconf = sa.Column(sa.types.Text)
    comment = sa.Column(sa.types.Text)

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
    def find_all(cls):
        return Session.query(Review).order_by(Review.id).all()


