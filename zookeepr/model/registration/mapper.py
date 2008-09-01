from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.sql import join, and_, select, func, outerjoin

from tables import *
from zookeepr.model.billing.tables import product, voucher_code
from domain import *
from zookeepr.model.billing.domain import Product, VoucherCode
from zookeepr.model.core import Person

mapper(Registration, registration,
       properties = {
            'person': relation(Person,
                               backref=backref('registration', cascade="all, delete-orphan",
                                               lazy=True,
                                               uselist=False),
                              ),
            'voucher': relation(VoucherCode,
                                uselist=False,
                                primaryjoin=registration.c.voucher_code==voucher_code.c.code,
                                foreign_keys=voucher_code.c.code,
                               )
            }
      )

mapper(RegistrationProduct, registration_product,
       properties = {
            'registration': relation(Registration, backref='products', lazy=True),
            'product': relation(Product, backref='registrationse', lazy=False),
            }
      )

mapper(RegoNote, rego_note,
  properties = {
    'rego': relation(Registration,
                     backref=backref('notes', cascade="all, delete-orphan",
                                       lazy=True)),
    'by': relation(Person,
                   backref=backref('notes_made', cascade="all, delete-orphan",
                                       lazy=True)),
  }
)
