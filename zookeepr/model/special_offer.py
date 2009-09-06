import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

from special_registration import SpecialRegistration

def setup(meta):
    meta.Session.add_all(
        [
            SpecialOffer(name='NZOSS', description='<p>Welcome to members of the New Zealand Open Source Society!</p><p>We are happy to invite you to register for LCA before we open registrations to the general public. To take advantage of this special offer, simply enter the username you use on the NZOSS website.</p>', id_name='NZOSS Account name', enabled=False),
            SpecialOffer(name='LinuxAustralia', description='<p>Welcome to Linux Australia members!</p><p>We are happy to invite you to register for LCA before we open registrations to the general public. To take advantage of this special offer, simply enter your LA member number (which you can see on your <a href="https://www.linux.org.au/membership/index.php?page=edit-member">details page</a> once you are logged in).</p>', id_name='LA member number', enabled=False),
            SpecialOffer(name='NZCS', description='<p>Welcome to members of the New Zealand Computer Society!</p><p>We are happy to invite you to register for LCA before we open registrations to the general public. To take advantage of this special offer, simply enter your NZCS member number (which you can see on your <a href="http://www.nzcs.org.nz/members">details page</a>).</p>', id_name='NZCS member number', enabled=False),
        ]
    )

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
