"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from role import Role
from person_role_map import person_role_map

from zookeepr.model.meta import Session

import datetime
import md5
import random

def setup(meta):
    pass

class Ceiling(Base):
    """Stores the details of product ceilings which are used to control the sale of itmes with a limited stock
    """

    __tablename__ = 'ceiling'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)
    max_sold = sa.Column(sa.types.Integer, nullable=True)
    available_from = sa.Column(sa.types.DateTime, nullable=True)
    available_until = sa.Column(sa.types.DateTime, nullable=True)

    def __init__(self, name=None, max_sold=None, available_from=None, available_until=None):
        self.name = name
        self.max_sold = max_sold
        self.available_from = available_from
        self.available_until = available_until

    def qty_sold(self):
        qty = 0
        for p in self.products:
            qty += p.qty_sold()
        return qty

    def qty_invoiced(self, date=True):
        # date: bool? only count items that are not overdue
        qty = 0
        for p in self.products:
            qty += p.qty_invoiced(date)
        return qty

    def percent_sold(self):
        if self.max_sold == None:
            return 0
        else:
            return self.qty_sold() / self.max_sold * 100

    def percent_invoiced(self):
        if self.max_sold == None:
            return 0
        else:
            return self.qty_invoiced() / self.max_sold * 100

    def remaining(self):
        return self.max_sold - self.qty_sold()

    def soldout(self):
        if self.max_sold != None:
            return self.qty_invoiced() >= self.max_sold
            #return self.qty_sold() >= self.max_sold

    def available(self, stock=True):
        # bool stock: care about if the product is in stock (ie sold out?)
        if stock and self.soldout():
            return False
        elif self.available_from is not None and self.available_from >= datetime.datetime.now():
            return False
        elif self.available_until is not None and self.available_until <= datetime.datetime.now():
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
        return Session.query(Ceiling).order_by(Ceiling.id).all()
