import sqlalchemy as sa

from meta import Base

from meta import Session

from lib.model import CommaList

from person import Person
from registration import Registration
from registration_product import RegistrationProduct

def setup(meta):
    pass

class RegoNote(Base):
    """Misc notes from the organising team on a person
    """
    __tablename__ = 'rego_note'

    id = sa.Column(sa.types.Integer, primary_key=True)
    rego_id = sa.Column(sa.types.Integer, sa.ForeignKey('registration.id'))
    note = sa.Column(sa.types.Text)
    block = sa.Column(sa.types.Boolean, nullable=False)
    by_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    by = sa.orm.relation(Person, backref=sa.orm.backref('notes_made', cascade="all, delete-orphan", lazy=True))
    rego = sa.orm.relation(Registration, backref=sa.orm.backref('notes', cascade="all, delete-orphan", lazy=True))

    def __init__(self, **kwargs):
        super(RegoNote, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(RegoNote).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such rego note object")
        return result

    @classmethod
    def find_all(cls):
        return Session.query(RegoNote).order_by(RegoNote.id).all()
