"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.lib.meta import Session

class Role(Base):
    """Stores the roles used for authorisation
    """
    __tablename__ = 'role'


    id = sa.Column(sa.types.Integer, primary_key=True)

    name = sa.Column(sa.types.Text, unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    @classmethod
    def find_by_name(self, name):
        return Session.query(Role).filter_by(name=name).first()

    @classmethod
    def find_all(self):
        return Session.query(Role).order_by(Role.name)

    def __repr__(self):
        return '<Role id="%s" name="%s">' % (self.id, self.name)

def setup(meta):
    meta.Session.add_all(
        [
            Role(name='organiser'),
            Role(name='team'),
            Role(name='reviewer'),
            Role(name='miniconf'),
        ]
    )
