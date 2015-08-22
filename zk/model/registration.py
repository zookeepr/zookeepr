"""The application's model objects"""
import sqlalchemy as sa

from meta import Base
from pylons.controllers.util import abort
from meta import Session
from lib.model import CommaList

from person import Person
from voucher import Voucher

class Registration(Base):
    __tablename__ = 'registration'

    id = sa.Column('id', sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'),
                                                               unique=True)
    over18 = sa.Column(sa.types.Boolean)
    nick = sa.Column(sa.types.Text)
    shell = sa.Column(sa.types.Text)
    editor = sa.Column(sa.types.Text)
    distro = sa.Column(sa.types.Text)
    vcs = sa.Column(sa.types.Text)
    silly_description = sa.Column(sa.types.Text)
    keyid = sa.Column(sa.types.Text)
    planetfeed = sa.Column(sa.types.Text)
    voucher_code = sa.Column(sa.types.Text, sa.ForeignKey('voucher.code'), unique=True)
    diet = sa.Column(sa.types.Text)
    special = sa.Column(sa.types.Text)
    partner_name = sa.Column(sa.types.Text)
    partner_email = sa.Column(sa.types.Text)
    partner_mobile = sa.Column(sa.types.Text)
#    checkin = sa.Column(sa.types.Integer)
#    checkout = sa.Column(sa.types.Integer)
    prevlca = sa.Column(CommaList)
    signup = sa.Column(CommaList)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False,
                                       default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime,
        nullable=False, default=sa.func.current_timestamp(),
        onupdate=sa.func.current_timestamp())

    person = sa.orm.relation(Person, backref=sa.orm.backref('registration', cascade="all, delete-orphan", lazy=True, uselist=False))
    voucher = sa.orm.relation(Voucher, uselist=False,
                                primaryjoin='Registration.voucher_code==Voucher.code',
                                foreign_keys=Voucher.code,
                                backref = 'registration',
                               )

    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)

    def __repr__(self):
        return '<Registration id=%r person_id=%r>' % (self.id, self.person_id)

    def ticket_description(self):
        for p in self.products:
            if p.product.category.name.lower() == "ticket":
                return p.product.description
        return ""

    @classmethod
    def find_by_id(cls, id, abort_404 = True):
        result = Session.query(Registration).filter_by(id=id).first()
        if result is None and abort_404:
            abort(404, "No such Registration object")
        return result

    @classmethod
    def find_by_ids(cls, id_list):
        return Session.query(Registration).filter(Registration.id.in_(id_list)).all()

    @classmethod
    def find_all(cls):
        return Session.query(Registration).order_by(Registration.id).all()
