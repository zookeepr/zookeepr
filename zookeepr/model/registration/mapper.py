from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.sql import join, and_, select, func, outerjoin

from tables import *
from zookeepr.model.billing.tables import voucher
from domain import *
from zookeepr.model.billing.domain import Product, Voucher
from zookeepr.model.core import Person

mapper(RegoNote, rego_note,
       properties = {
            'rego': relation(Registration, backref=backref('notes', cascade="all, delete-orphan", lazy=True)),
            'by': relation(Person, backref=backref('notes_made', cascade="all, delete-orphan", lazy=True)),
            }
      )

mapper(Volunteer, volunteer,
       properties = {
            'person': relation(Person, backref=backref('volunteer', cascade="all, delete-orphan", lazy=True, uselist=False)),
            }
      )
