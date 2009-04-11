"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.person_role_map import person_role_map

from zookeepr.model.meta import Session

#import datetime
#import md5
#import random

def setup(meta):
    pass

class Attachment(Base):
    __tablename__ = 'attachment'

    id = sa.Column(sa.types.Integer, primary_key=True)

    proposal_id =  sa.Column(sa.types.Integer, sa.ForeignKey('proposal.id'))
    filename = sa.Column(sa.types.Text, key='_filename', nullable=False, default='attachment')
    content_type = sa.Column(sa.types.Text, key='_content_type', nullable=False, default='application/octet-stream')

    content = sa.Column(sa.types.Binary, nullable=False)

    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())


    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Attachment, self).__init__(**kwargs)

    def __repr__(self):
        return '<Attachment id=%r filename="%s">' % (self.id, self.filename)


    @classmethod
    def find_by_id(cls, id):
        return Session.query(Attachment).filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return Session.query(Attachment).order_by(Attachment.id).all()

