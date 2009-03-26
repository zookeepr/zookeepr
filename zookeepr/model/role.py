"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

class Role(Base):
    """Stores the roles used for authorisation
    """
    __tablename__ = 'role'


    id = sa.Column(sa.types.Integer, primary_key=True)

    name = sa.Column(sa.types.Text, unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def find_by_name(self, name):
        return sa.meta.Session.query(Role).filter_by(name=name).first()

    def find_all(self):
        return sa.meta.Session.query(Role).order_by(Role.name)

    def __repr__(self):
        return '<Role id="%s" name="%s">' % (self.id, self.name)

