"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.role import Role
from zookeepr.model.person_role_map import person_role_map

import datetime
import md5
import random

def setup(meta):
    person = Person(
        email_address="admin@zookeepr.org",
        activated=True,
        firstname="Admin",
        lastname="User"
    )
    person.password = 'password'

    role = meta.Session.query(Role).filter_by(name='organiser').first()
    person.roles.append(role)

    meta.Session.add(person)

class Person(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'person'

    id = sa.Column(sa.types.Integer, primary_key=True)

    email_address = sa.Column(sa.types.Text, nullable=False, unique=True)
    password_hash = sa.Column(sa.types.Text)

    # creation timestamp of the registration
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False)
    url_hash = sa.Column(sa.types.String(32), nullable=False, index=True)


    # flag that the account has been activated by the user
    # (responded to their confirmation email)
    activated = sa.Column(sa.types.Boolean, nullable=False, default=False)

    # other personal details
    # the lengths of the fields are chosen arbitrarily
    firstname = sa.Column(sa.types.Text)
    lastname = sa.Column(sa.types.Text)
    address1 = sa.Column(sa.types.Text)
    address2 = sa.Column(sa.types.Text)
    city = sa.Column(sa.types.Text)
    state = sa.Column(sa.types.Text)
    postcode = sa.Column(sa.types.Text)
    country = sa.Column(sa.types.Text)
    company = sa.Column(sa.types.Text)
    phone = sa.Column(sa.types.Text)
    mobile = sa.Column(sa.types.Text)

    url = sa.Column(sa.types.Text)

    # Proposal bits
    experience = sa.Column(sa.types.Text)
    bio = sa.Column(sa.types.Text)

    badge_printed = sa.Column(sa.types.Boolean, default='False')

    # relations
    roles = sa.orm.relation(Role, secondary=person_role_map, backref='people', order_by=Role.name)
    # FIXME invoice = sa.orm.relation(Invoice)


    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

        if not 'creation_timestamp' in kwargs:
            self.creation_timestamp = datetime.datetime.now()

        # url_hash should never be modifiable by the caller directly
        self._update_url_hash()

    def _set_password(self, value):
        if value is not None:
            self.password_hash = md5.new(value).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

    def check_password(self, value):
        """Check the given password is equal to the stored one"""
        return self.password_hash == md5.new(value).hexdigest()

    def is_speaker(self):
        return reduce(lambda a, b: a or (b.accepted and b.type.name != 'Miniconf'), self.proposals, False)

    def is_miniconf_org(self):
        return reduce(lambda a, b: a or (b.accepted and b.type.name == 'Miniconf'), self.proposals, False)

    def is_volunteer(self):
        if self.volunteer and self.volunteer.accepted is not None:
            return self.volunteer.accepted
        return False

    def _set_creation_timestamp(self, value):
        if value is None:
            self._creation_timestamp = datetime.datetime.now()
        else:
            self._creation_timestamp = value
        self._update_url_hash()

    def _get_creation_timestamp(self):
        return self._creation_timestamp

    creation_timestamp = property(_get_creation_timestamp, _set_creation_timestamp)

    def _get_url_hash(self):
        return self._url_hash

    url_hash = property(_get_url_hash)

    def _update_url_hash(self):
        """Update the stored URL hash for this person.

        Call this when an element of the URL hash has changed
        (i.e. either the email address or timestamp)
        """
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address,
                              self.creation_timestamp,
                              nonce)
        self._url_hash = md5.new(magic).hexdigest()

    def valid_invoice(self):
        for invoice in self.invoices:
            if not invoice.void and not invoice.manual:
                return invoice
        return None

    def paid(self):
        status = False
        for invoice in self.invoices:
            if not invoice.void:
                if invoice.paid():
                    status = True
                else:
                    return False
        return status

    def __repr__(self):
        return '<Person id="%s" email="%s">' % (self.id, self.email_address)

    def find_by_email(self, email):
        return sa.meta.Session.query(Person).filter_by(email=email.lower()).first()

    def find_all(self):
        return sa.meta.Session.query(Person).order_by(Person.id)


class PasswordResetConfirmation(object):
    def __init__(self, email_address=None):
        self.email_address = email_address
        self.timestamp = datetime.datetime.now()
        self._update_url_hash()

    def _update_url_hash(self):
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address,
            self.timestamp,
            nonce)
        self.url_hash = md5.new(magic).hexdigest()

    def __repr__(self):
        return '<PasswordResetConfirmation email_address=%r timestamp=%r>' % (self.email_address, self.timestamp)

