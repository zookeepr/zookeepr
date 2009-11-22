import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from person import Person
from invoice_item import InvoiceItem
from payment import Payment
from payment_received import PaymentReceived

from zookeepr.model.meta import Session

import datetime

def setup(meta):
    pass

class Invoice(Base):
    """Stores both account login details and personal information.
    """
    # table
    __tablename__ = 'invoice'

    id = sa.Column(sa.types.Integer, primary_key=True)
    person_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'), nullable=False)
    manual = sa.Column(sa.types.Boolean, default=True, nullable=False)
    void = sa.Column(sa.String, default=None, nullable=True)
    issue_date = sa.Column(sa.types.DateTime, default=sa.func.current_timestamp(), nullable=False)
    due_date = sa.Column(sa.types.DateTime, default=sa.func.current_timestamp(), nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    # relations
    payment_received = sa.orm.relation(PaymentReceived, backref='invoice')
    payments = sa.orm.relation(Payment, backref='invoice')
    person = sa.orm.relation(Person,lazy=True,backref=sa.orm.backref('invoices', cascade="all, delete-orphan"))
    items = sa.orm.relation(InvoiceItem, backref='invoice', cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Invoice, self).__init__(**kwargs)

    def is_void(self):
        return (self.void is not None)

    def total(self):
        """Return the total value of this invoice"""
        t = 0
        for ii in self.items:
            t += ii.total()
        return t

    def good_payments(self):
        return Session.query(PaymentReceived).filter_by(approved=True, invoice_id=self.id)

    def bad_payments(self):
        return Session.query(PaymentReceived).filter_by(approved=False, invoice_id=self.id)

    def paid(self):
        """Return whether the invoice is paid (or zero-balance) """
        return bool(! self.is_void() and (self.good_payments().count() > 0 or self.total()==0))

    def status(self):
        if self.is_void() == True:
            return "Invalid"
        elif self.paid():
            return "Paid"
        else:
            return "Unpaid"

    def overdue(self):
        return self.due_date < datetime.datetime.now()

    def __repr__(self):
        return '<Invoice id=%r void=%r person=%r>' % (self.id, self.void, self.person_id)

    @classmethod
    def find_all(cls):
        return Session.query(Invoice).order_by(Invoice.id).all()

    @classmethod
    def find_by_id(cls, id, do_abort=False):
        invoice = Session.query(Invoice).filter_by(id=id).first()
        if do_abort and not invoice:
            abort(404, 'Invalid invoice ID')
        return invoice

    @classmethod
    def find_by_person(cls, person_id):
        return Session.query(Invoice).filter_by(person_id=person_id).first()
