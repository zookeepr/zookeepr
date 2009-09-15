"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort
from zookeepr.model.meta import Session
#from person_social_network_map import PersonSocialNetworkMap

def setup(meta):
    meta.Session.add_all(
        [
            SocialNetwork(name='Twitter', url='http://twitter.com/USER',
                          logo='tag_twitter.png'),
            SocialNetwork(name='Identi.ca', url='http://identi.ca/USER',
                          logo='tag_identica.png'),
            SocialNetwork(name='Flickr', url='http://www.flickr.com/photos/USER',
                          logo='tag_flickr.png'),
        ]
    )

class SocialNetwork(Base):
    """Stores the social networks that people might be members of
    """
    __tablename__ = 'social_network'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)
    url = sa.Column(sa.types.Text, nullable=False)
    logo = sa.Column(sa.types.Text, nullable=False)

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
