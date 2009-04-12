"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort
from zookeepr.model.meta import Session

class Registration(Base):
    __tablename__ 'registration'

    id = sa.Column('id', Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, ForeignKey('person.id'),
                                                               unique=True)
    over18 = sa.Column(sa.types.Boolean)
    nick = sa.Column(sa.types.Text)
    shell = sa.Column(sa.types.Text)
    editor = sa.Column(sa.types.Text)
    distro = sa.Column(sa.types.Text)
    silly_description = sa.Column(sa.types.Text)
    keyid = sa.Column(sa.types.Text)
    planetfeed = sa.Column(sa.types.Text)
    voucher_code = sa.Column(sa.types.Text, unique=True)
    diet = sa.Column(sa.types.Text)
    special = sa.Column(sa.types.Text)
    partner_email = sa.Column(sa.types.Text)
    checkin = sa.Column(sa.types.Integer)
    checkout = sa.Column(sa.types.Integer)
    prevlca = sa.Column(sa.types.CommaList)
    miniconf = sa.Column(sa.types.CommaList)
    signup = sa.Column(sa.types.CommaList)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    person = sa.orm.relation(Person, backref=sa.orm.backref('registration', cascade="all, delete-orphan", lazy=True, uselist=False)),
    voucher = sa.orm.relation(Voucher, uselist=False,
                                primaryjoin=registration.c.voucher_code==voucher.c.code,
                                foreign_keys=voucher.c.code,
                               )

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return '<Registration id=%r person_id=%r>' % (self.id, self.person_id)

