import sqlalchemy as sa

from meta import Base

from meta import Session

class SpecialRegistration(Base):
    """Stores details of a person who used a special offer to register early
    """
    __tablename__ = 'special_registration'

    id = sa.Column(sa.types.Integer, primary_key=True)
    member_number = sa.Column(sa.types.Text, nullable=True, unique=False)
    special_offer_id = sa.Column(sa.types.Integer, sa.ForeignKey('special_offer.id'), nullable=False)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)

    def __init__(self, **kwargs):
        super(SpecialRegistration, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(SpecialRegistration).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(SpecialRegistration).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(SpecialRegistration).filter_by(name=name).first()

    @classmethod
    def find_by_offer(cls, offer):
        return Session.query(SpecialRegistration).filter_by(special_offer_id=offer)

    @classmethod
    def find_by_person_and_offer(cls, person, offer):
        return Session.query(SpecialRegistration).filter_by(person_id=person, special_offer_id=offer).first()

    def __repr__(self):
        return '<SpecialRegistration id=%r member_number=%r person=%r special_offer=%r>' % (self.id, self.member_number, self.person.id, self.special_offer.id)
