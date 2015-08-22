import sqlalchemy as sa

from meta import Base

from meta import Session

from special_registration import SpecialRegistration

class SpecialOffer(Base):
    """Stores details about a special offer for pre-registration
    """
    __tablename__ = 'special_offer'

    id = sa.Column(sa.types.Integer, primary_key=True)
    enabled = sa.Column(sa.types.Boolean, nullable=False)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)
    description = sa.Column(sa.types.Text, nullable=False)
    id_name = sa.Column(sa.types.Text)

    special_registrations = sa.orm.relation(SpecialRegistration, backref='special_offer')

    def __init__(self, **kwargs):
        super(SpecialOffer, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(SpecialOffer).order_by(SpecialOffer.name).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(SpecialOffer).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(SpecialOffer).filter_by(name=name).first()

    def __repr__(self):
        return '<SpecialOffer id=%r name=%r description=%r id_name=%r>' % (self.id, self.name, self.description, self.id_name)
