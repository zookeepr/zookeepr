"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

import hashlib
import datetime
import random

class PasswordResetConfirmation(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'password_reset_confirmation'

    id = sa.Column(sa.types.Integer, primary_key=True)

    email_address = sa.Column(sa.types.Text, nullable=False, unique=True)
    url_hash = sa.Column(sa.types.Text, nullable=False, unique=True)

    timestamp = sa.Column(sa.types.DateTime, nullable=False)

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(PasswordResetConfirmation, self).__init__(**kwargs)

        self.timestamp = datetime.datetime.now()
        self._update_url_hash()

    def _update_url_hash(self):
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address, self.timestamp, nonce)
        m = hashlib.md5()
        m.update(magic)
        self.url_hash = m.hexdigest()

    def __repr__(self):
        return '<PasswordResetConfirmation email_address=%r timestamp=%r>' % (self.email_address, self.timestamp)

    @classmethod
    def find_by_email(cls, email):
        return Session.query(PasswordResetConfirmation).filter_by(email_address=email.lower()).first()

    @classmethod
    def find_by_url_hash(cls, url_hash):
        return Session.query(PasswordResetConfirmation).filter_by(url_hash=url_hash).first()

