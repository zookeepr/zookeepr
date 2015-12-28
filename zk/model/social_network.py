"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection

from meta import Base
from pylons.controllers.util import abort
from meta import Session
from person_social_network_map import PersonSocialNetworkMap

class SocialNetwork(Base):
    """Stores the social networks that people might be members of
    """
    __tablename__ = 'social_network'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)
    url = sa.Column(sa.types.Text, nullable=False)
    logo = sa.Column(sa.types.Text, nullable=False)

    by_person = sa.orm.relation(PersonSocialNetworkMap,
      collection_class=attribute_mapped_collection('person'),
      cascade="all, delete-orphan",
      backref='social_network')
    people = association_proxy('by_person', 'account_name')
    # Note: You can't set via the people attribute


    def __init__(self, **kwargs):
        super(SocialNetwork, self).__init__(**kwargs)

    @classmethod
    def find_by_name(self, name, abort_404 = True):
        result = Session.query(SocialNetwork).filter_by(name=name).first()
        if result is None and abort_404:
            abort(404, "No such social network object")
        return result

    @classmethod
    def find_by_id(self, id, abort_404 = True):
        result = Session.query(SocialNetwork).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such social network object")
        return result

    @classmethod
    def find_all(self):
        return Session.query(SocialNetwork).order_by(SocialNetwork.name).all()

    def __repr__(self):
        return '<SocialNetwork id="%s" name="%s">' % (self.id, self.name)
