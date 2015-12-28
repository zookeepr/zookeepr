"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort
from beaker.cache import CacheManager

from role import Role
from person_role_map import person_role_map

from meta import Session

import datetime
import random

class Ceiling(Base):
    """Stores the details of product ceilings which are used to control the sale of itmes with a limited stock
    """

    __tablename__ = 'ceiling'

    id = sa.Column(sa.types.Integer, primary_key=True)
    parent_id = sa.Column(sa.types.Integer, sa.ForeignKey('ceiling.id'), nullable=True)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)
    max_sold = sa.Column(sa.types.Integer, nullable=True)
    available_from = sa.Column(sa.types.DateTime, nullable=True)
    available_until = sa.Column(sa.types.DateTime, nullable=True)
    cache = CacheManager()

    # relations
    parent = sa.orm.relation(lambda: Ceiling, backref='children', remote_side=[id])

    def qty_sold(self):
        qty = 0
        for p in self.products:
            qty += p.qty_sold()
        return qty

    def qty_invoiced(self, date=True):
        # date: bool? only count items that are not overdue

        @self.cache.cache(self.id, expire=600)
        def cached(self, date=True):
            qty = 0

            for p in self.products:
                qty += p.qty_invoiced(date)
            return qty

        return cached(self, date)

    def qty_free(self):
        qty = 0
        for p in self.products:
            qty += p.qty_free()
        return qty

    def percent_sold(self):
        if self.max_sold == None:
            return 0
        else:
            percent = float(self.qty_sold()) / float(self.max_sold)
            return int(percent * 100)

    def percent_invoiced(self):
        if self.max_sold == None:
            return 0
        else:
            percent = float(self.qty_invoiced()) / float(self.max_sold)
            return int(percent * 100)

    def remaining(self):
        return self.max_sold - self.qty_sold()

    def soldout(self):
        if self.max_sold != None:
            return self.qty_invoiced() >= self.max_sold
        return False

    def enough_left(self, qty):
        if self.max_sold != None:
            return (self.qty_invoiced() + qty) > self.max_sold
        return False

    def available(self, stock=True, qty=0):
        # bool stock: care about if the product is in stock (ie sold out?)
        if stock and self.soldout():
            return False
        elif qty > 0 and self.enough_left(qty):
            return False
        elif self.available_from is not None and self.available_from >= datetime.datetime.now():
            return False
        elif self.available_until is not None and self.available_until <= datetime.datetime.now():
            return False
        elif self.parent is not None and self.parent != self and self.parent.available():
            return False
        else:
            return True

    def can_i_sell(self, qty):
        if not self.soldout() and self.remaining() > qty:
            return True
        else:
            return False

    def __repr__(self):
        return '<Ceiling id=%r name=%r max_sold=%r available_from=%r, available_until=%r' % (self.id, self.name, self.max_sold, self.available_from, self.available_until)

    @classmethod
    def find_all(cls):
        return Session.query(Ceiling).order_by(Ceiling.name).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(Ceiling).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(Ceiling).filter_by(name=name).first()
