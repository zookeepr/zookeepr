"""The application's model objects"""
import sqlalchemy as sa
import re

from meta import Base
from meta import metadata
#from social_network import SocialNetwork

class PersonSocialNetworkMap(Base):
    """Stores both account login details and personal information.
    """
    __tablename__ = 'person_social_network_map'
    __table_args__ = (
            # A person can have only one of each social network
            sa.UniqueConstraint('person_id', 'social_network_id'),
            {}
            )

    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False)
    social_network_id = sa.Column(sa.types.Integer, sa.ForeignKey('social_network.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False)
    account_name = sa.Column(sa.types.Text, nullable=False)

    #social_network = sa.orm.relation(SocialNetwork, backref='people')

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(PersonSocialNetworkMap, self).__init__(**kwargs)

    def account_url(self):
        p = re.compile('(USER)')
        return p.sub(self.account_name, self.social_network.url)
