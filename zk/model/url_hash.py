"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

import hashlib
import datetime
import random

class URLHash(Base):
    """ Stores a unique has for various access """
    __tablename__ = 'url_hash'

    id = sa.Column(sa.types.Integer, primary_key=True)

    url = sa.Column(sa.types.Text, nullable=False, unique=True)
    url_hash = sa.Column(sa.types.Text, nullable=False, unique=True)

    timestamp = sa.Column(sa.types.DateTime, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(URLHash, self).__init__(**kwargs)

        self.timestamp = datetime.datetime.now()
        self._update_url_hash()

    def _update_url_hash(self):
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.url, self.timestamp, nonce)
        m = hashlib.md5()
        m.update(magic)
        self.url_hash = m.hexdigest()

    def __repr__(self):
        return '<URLHash url=%r timestamp=%r>' % (self.url, self.timestamp)

    @classmethod
    def find_by_url(cls, url):
        return Session.query(URLHash).filter_by(url=url).first()

    @classmethod
    def find_by_hash(cls, url_hash):
        return Session.query(URLHash).filter_by(url_hash=url_hash).first()

