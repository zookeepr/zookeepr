import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from person import Person
from invoice_item import InvoiceItem
from payment import Payment
from payment_received import PaymentReceived

from meta import Session

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

    # mapped attributes
    """
    These are currently defined outside of the class because correlate(Invoice) will not work within the class. SQL Alchemy 0.8 is supposed to add a new correlate_except() function which will get around this issue
    """
    # relations
    payment_received = sa.orm.relation(PaymentReceived, lazy='subquery', backref='invoice')
    good_payments = sa.orm.relation(PaymentReceived, lazy='subquery', primaryjoin=sa.and_(PaymentReceived.invoice_id == id, PaymentReceived.approved == True))
    bad_payments = sa.orm.relation(PaymentReceived, lazy='subquery', primaryjoin=sa.and_(PaymentReceived.invoice_id == id, PaymentReceived.approved == False))
    payments = sa.orm.relation(Payment, lazy='subquery', backref='invoice')
    person = sa.orm.relation(Person, lazy='subquery', backref=sa.orm.backref('invoices', cascade="all, delete-orphan"))
    items = sa.orm.relation(InvoiceItem, lazy='subquery', backref=sa.orm.backref('invoice', lazy='subquery'), cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        self.due_date = datetime.datetime.now() + datetime.timedelta(+1)
        super(Invoice, self).__init__(**kwargs)

    @property
    def status(self):
        if self.is_void:
            return "Invalid"
        elif self.is_paid:
            return "Paid"
        else:
            return "Unpaid"

    def __repr__(self):
        return '<Invoice id=%r void=%r person=%r>' % (self.id, self.void, self.person_id)

    @classmethod
    def find_all(cls):
        return Session.query(Invoice).order_by(Invoice.id).options(sa.orm.subqueryload('person.registration')).all()

    @classmethod
    def find_by_id(cls, id, do_abort=False):
        invoice = Session.query(Invoice).filter_by(id=id).first()
        if do_abort and not invoice:
            abort(404, 'Invalid invoice ID')
        return invoice

    @classmethod
    def find_by_person(cls, person_id):
        return Session.query(Invoice).filter_by(person_id=person_id).first()

total_query = sa.select([sa.case([(sa.func.count(InvoiceItem.id) == 0, 0)], else_=sa.func.sum(InvoiceItem.total))]).where(InvoiceItem.invoice_id==Invoice.id).correlate(Invoice.__table__)
payment_query = sa.select([sa.case([(sa.func.count(PaymentReceived.id) == 0, 0)], else_=sa.func.sum(PaymentReceived.amount_paid))]).where(sa.and_(PaymentReceived.invoice_id==Invoice.id, PaymentReceived.approved==True)).correlate(Invoice.__table__)

Invoice.total = sa.orm.column_property(total_query)
Invoice.payment = sa.orm.column_property(payment_query)
Invoice.is_void = sa.orm.column_property(Invoice.void != None)
Invoice.is_paid = sa.orm.column_property(sa.and_(Invoice.void == None, total_query.as_scalar() == payment_query.as_scalar()))
Invoice.is_overdue = sa.orm.column_property(Invoice.due_date < datetime.datetime.now())
