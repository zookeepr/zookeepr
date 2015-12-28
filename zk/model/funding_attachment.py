"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from person_role_map import person_role_map

from meta import Session

#import datetime
#import random

class FundingAttachment(Base):
    __tablename__ = 'funding_attachment'

    id = sa.Column(sa.types.Integer, primary_key=True)
    funding_id =  sa.Column(sa.types.Integer, sa.ForeignKey('funding.id'))

    filename = sa.Column(sa.types.Text, key='_filename', nullable=False, default='attachment')
    content_type = sa.Column(sa.types.Text, key='_content_type', nullable=False, default='application/octet-stream')

    content = sa.Column(sa.types.Binary, nullable=False)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    funding = sa.orm.relation('Funding')


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(FundingAttachment, self).__init__(**kwargs)

    def __repr__(self):
        return '<FundingAttachment id=%r filename="%s">' % (self.id, self.filename)

    @classmethod
    def find_by_filename(cls, filename):
        return Session.query(FundingAttachment).filter_by(filename=filename).first()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(FundingAttachment).filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return Session.query(FundingAttachment).order_by(FundingAttachment.id).all()

