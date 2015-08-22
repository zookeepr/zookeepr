"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from person import Person
from funding import Funding

from meta import Session

import datetime
import random

class FundingReview(Base):
    """Stores reviews of funding applications
    """
    __tablename__ = 'funding_review'
    __table_args__ = (
            # Allow only one review for each funding application
            sa.UniqueConstraint('funding_id', 'reviewer_id'),
            {}
            )

    id = sa.Column(sa.types.Integer, primary_key=True)

    funding_id = sa.Column(sa.types.Integer, sa.ForeignKey('funding.id'), nullable=False)
    reviewer_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)

    score = sa.Column(sa.types.Integer)

    comment = sa.Column(sa.types.Text)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    funding = sa.orm.relation(Funding, lazy=True, backref='reviews')
    reviewer = sa.orm.relation(Person, lazy=True, backref='funding_reviews')

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(FundingReview, self).__init__(**kwargs)

    def __repr__(self):
        return '<FundingReview id=%r comment=%r>' % (self.id, self.comment)

    @classmethod
    def find_by_id(cls, id):
        return Session.query(FundingReview).filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return Session.query(FundingReview).order_by(FundingReview.id).all()


