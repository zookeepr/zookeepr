"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy 
from sqlalchemy.orm.collections import attribute_mapped_collection

from meta import Base

from pylons.controllers.util import abort

from role import Role
from person_role_map import person_role_map
from social_network import SocialNetwork
from person_social_network_map import PersonSocialNetworkMap
from special_registration import SpecialRegistration

from zookeepr.model.meta import Session

import datetime
import hashlib
import random
from libravatar import libravatar_url

def setup(meta):
    person = Person(
        email_address="admin@zookeepr.org",
        activated=True,
        firstname="Admin",
        lastname="User"
    )
    person.password = 'password'
    person.activated = True

    role = Role.find_by_name('organiser')
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
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
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

    def _create_social_network_map(network, account_name):
       """Constructs SocialNetworkMaps from the SocialNetowkr and the
          account_name."""
       return PersonSocialNetworkMap(social_network=network, account_name=account_name)

    # relations
    roles = sa.orm.relation(Role, secondary=person_role_map, backref='people', order_by=Role.name)
    by_social_network = sa.orm.relation(PersonSocialNetworkMap, 
      collection_class=attribute_mapped_collection('social_network'),
      cascade="all, delete-orphan", backref='person')
    social_networks = association_proxy('by_social_network', 'account_name', creator=_create_social_network_map)
    special_registration = sa.orm.relation(SpecialRegistration, backref='person')

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Person, self).__init__(**kwargs)

        self.creation_timestamp = datetime.datetime.now()
        self.activated = False
        self.badge_printed = False

        # url_hash should never be modifiable by the caller directly
        self._update_url_hash()

    def gen_password(self, value):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()

    def _set_password(self, value):
        if value is not None:
            self.password_hash = self.gen_password(value)

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

    def check_password(self, value):
        """Check the given password is equal to the stored one"""
        return self.password_hash == self.gen_password(value)

    def is_professional(self):
        """We treat speakers, miniconf orgs, Little Blue sponsors and
           professionals as professionals."""
        for invoice in self.invoices:
            if invoice.paid() and not invoice.is_void():
                if self.is_speaker() or self.is_miniconf_org():
                    return True
                else:
                    for item in invoice.items:
                        if (item.description.find('Professional') > -1 or item.description.find('Little Blue') > -1):
                            return True
        return False

    def is_speaker(self):
        # Check is they have the 'copresenter' role, this means they are not a 'real' speaker
        if self.has_role("copresenter"): return False
        return reduce(lambda a, b: a or (b.accepted and b.type.name != 'Miniconf'), self.proposals, False) or False
        # note: the "or False" at the end converts a None into a False

    def is_miniconf_org(self):
        return reduce(lambda a, b: a or (b.accepted and b.type.name == 'Miniconf'), self.proposals, False) or False
        # note: the "or False" at the end converts a None into a False

    def has_role(self, name):
        name = name.lower()
        for role in self.roles:
          if role.name.lower() == name:
            return True
        return False

    def is_volunteer(self):
        if self.volunteer and self.volunteer.accepted is not None:
            return self.volunteer.accepted
        return False

    def is_from_common_country(self):
        # People registering from these countries will not require extra verification
        common_countries = ['australia', 'new zealand', 'united states', 'canada',
                            'germany', 'france', 'spain', 'italy', 'switzerland',
                            'austria', 'united kingdom', 'ireland', 'japan', 'norway',
                            'denmark', 'sweden', 'finland', 'iceland', 'belgium',
                            'brazil', 'mexico', 'argentina', 'chile', 'columbia',
                            'estonia', 'greece', 'hong kong', 'israel', 'luxembourg', 
                            'monaco', 'netherlands', 'portugal', 'south africa']

        if self.country.strip().lower() in common_countries:
            return True
        else:
            return False

    def _update_url_hash(self):
        """Update the stored URL hash for this person.

        Call this when an element of the URL hash has changed
        (i.e. either the email address or timestamp)
        """
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address,
                              self.creation_timestamp,
                              nonce)
        self.url_hash = self.gen_password(magic)

    def valid_invoice(self):
        for invoice in self.invoices:
            if not invoice.is_void() and not invoice.manual:
                return invoice
        return None

    def has_valid_invoice(self):
        for invoice in self.invoices:
            if not invoice.is_void():
                return True
        return False

    def has_paid_ticket(self):
        for invoice in self.invoices:
            if invoice.paid() and not invoice.is_void():
                for item in invoice.items:
                    if item.product is not None and item.product.category.name == 'Ticket':
                        return True
        return False

    def ticket_type(self):
        for invoice in self.invoices:
            if not invoice.is_void():
                for item in invoice.items:
                    if item.product is not None and item.product.category.name == 'Ticket':
                        # Strip off any mention of "Ticket".
                        str = item.description
                        str = str.replace('Ticket - ', '')
                        str = str.replace(' Ticket', '')
                        return str

    def paid(self):
        status = False
        for invoice in self.invoices:
            if not invoice.is_void():
                if invoice.paid():
                    status = True
                else:
                    return False
        return status

    def fetch_social_networks(self):
        self.social_network = dict()

        for sn in self.social_networks:
            self.social_network[sn.name] = self.social_networks[sn]

        for sn in SocialNetwork.find_all():
            if sn.name not in self.social_network:
                self.social_network[sn.name] = ''

    def fullname(self):
        return "%s %s" % (self.firstname, self.lastname)

    def __repr__(self):
        return '<Person id="%s" email="%s">' % (self.id, self.email_address)

    @classmethod
    def find_by_email(cls, email, abort_404 = False):
        result = Session.query(Person).filter_by(email_address=email.lower()).first()
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Person).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(Person).order_by(Person.id).all()

    @classmethod
    def find_by_url_hash(cls, url_hash, abort_404 = True):
        result = Session.query(Person).filter_by(url_hash=url_hash).first()
        if result is None and abort_404:
            abort(404, "No such person object")
        return result

    def avatar_url(self):
        return libravatar_url(email=self.email_address, https=True, default='mm')
