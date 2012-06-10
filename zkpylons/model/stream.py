"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from meta import Session

class Stream(Base):
    __tablename__ = 'stream'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Stream, self).__init__(**kwargs)

    @classmethod
    def find_by_name(self, name):
        return Session.query(Stream).filter_by(name=name).first()

    @classmethod
    def find_by_id(self, id):
        return Session.query(Stream).filter_by(id=id).first()

    @classmethod
    def find_all(self):
        return Session.query(Stream).order_by(Stream.name).all()

    @classmethod
    def select_values(self):
        streams = Session.query(Stream).order_by(Stream.name).all()
        values = [ (None, '(none)') ]
        for stream in streams:
            v = (stream.id, stream.name)
            values.append(v)
        return values

    def __repr__(self):
        return '<Stream name=%r>' % self.name
