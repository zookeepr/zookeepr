"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort
from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            Role(name='organiser', comment='Has full access to management pages'),
            Role(name='team', comment='Member of core team'),
            Role(name='reviewer', pretty_name='Paper Reviewer', comment='Has access to the paper review system'),
            Role(name='miniconf', pretty_name='Miniconf Organiser', comment='Is a miniconference organiser'),
            Role(name='papers_chair', pretty_name='Papers Chair', comment='Has access to paper review system management functions'),
            Role(name='late_submitter', comment='Is allowed to submit paper proposals late'),
            Role(name='funding_reviewer', pretty_name='Funding Reviewer', comment='Has access to the funding review system'),
        ]
    )

class Role(Base):
    """Stores the roles used for authorisation
    """
    __tablename__ = 'role'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)
    pretty_name = sa.Column(sa.types.Text, nullable=True)
    display_order = sa.Column(sa.types.Integer, nullable=True)
    comment = sa.Column(sa.types.Text, nullable=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    @classmethod
    def find_by_name(self, name, abort_404 = True):
        result = Session.query(Role).filter_by(name=name).first()
        return result

    @classmethod
    def find_by_id(self, id, abort_404 = True):
        result = Session.query(Role).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such role object")
        return result

    @classmethod
    def find_all(self):
        return Session.query(Role).order_by(Role.name).all()

    def __repr__(self):
        return '<Role id="%s" name="%s" pretty_name="%s" display_order="%s">' % (self.id, self.name, self.pretty_name, self.display_order)
