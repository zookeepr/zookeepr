"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from zookeepr.model import meta

import person
import role
import person_role_map
import password_reset_confirmation
import proposal
import person_proposal_map
import attachment
import review
import db_content
import volunteer
import voucher
import invoice
import invoice_item
import payment
import ceiling
import product
import product_ceiling_map
import rego_note

from person import Person
from role import Role
from password_reset_confirmation import PasswordResetConfirmation

from proposal import Proposal, ProposalStatus, ProposalType, TravelAssistanceType, AccommodationAssistanceType, TargetAudience
from attachment import Attachment
from review import Review, Stream

from product import Product, ProductInclude
from product_category import ProductCategory
from ceiling import Ceiling

from invoice import Invoice
from invoice_item import InvoiceItem
from payment import Payment

from registration import Registration
from registration_product import RegistrationProduct

from voucher import Voucher, VoucherProduct

from db_content import DbContentType, DbContent

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine


def setup(meta):
    """Setup any data in the tables"""

    role.setup(meta)
    person_role_map.setup(meta)
    person.setup(meta)

    proposal.setup(meta)
    person_proposal_map.setup(meta)
    attachment.setup(meta)
    review.setup(meta)
    voucher.setup(meta)

    db_content.setup(meta)
    volunteer.setup(meta)

    meta.Session.commit()


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass


# FIXME update after pylons upgrade
#from core import PasswordResetConfirmation
#from proposal import Proposal, ProposalType, Attachment, Review, AssistanceType
#from schedule import Stream, Talk
#from registration import *
#from openday import Openday
#from billing import *
#from db_content import DBContentType, DBContent
#
#def init_model(app_conf):
#    from paste.deploy.converters import asbool
#    from sqlalchemy.schema import MetaData as BoundMetaData
#
#    global metadata
#
#    # Under normal conditions, init_model will only ever get called
#    # once.  However when used with paste.fixture, it'll get called
#    # multiple times.
#    if not globals().get('metadata'):
#        metadata = BoundMetaData(app_conf['dburi'])
#        #metadata.engine.echo = asbool(app_conf.get('echo_queries', 'false'))
#
#        import core.mapper
#        import proposal.mapper
#        import schedule.mapper
#        import registration.mapper
#        import openday.mapper
#        import billing.mapper
#        import db_content.mapper
#
#def create_all(app_conf):
#    """This is called from ``websetup`` to create everything."""
#    init_model(app_conf)
#    metadata.create_all()
#
#def populate_data():
#    from sqlalchemy.exceptions import SQLError
#    from zookeepr import model
#
#    try:
#        # Product Categories
#        model.billing.tables.product_category.insert().execute(
#            dict(name='Ticket', description='Please choose your registration type?', display='radio', min_qty=1, max_qty=1),
#            dict(name='Shirt', description='Please choose how many shirts you would like. The first one is free with your registration.', display='qty', min_qty=1, max_qty=100),
#            dict(name='Dinner Ticket', description='Please indicate how many penguin dinner tickets you wish to purchase. You should include yourself in this number, even if you buy a professional registration.', display='qty', min_qty=0, max_qty=5),
#            dict(name='Accommodation', description='Where would you like to stay during the conference?', display='select', min_qty=0, max_qty=10),
#            dict(name='Partners Programme', description='Would your partner like to participate in the partners programme?', display='qty', min_qty=0, max_qty=50),
#            )
#
#    except SQLError, inst:
#        print inst
#        pass
#
#    try:
#        # Products
#        model.billing.tables.product.insert().execute(
#            dict(category_id='1', active=True, description="Concession/Student Ticket", cost="16000", auth=None, validate=None),
#            dict(category_id='1', active=True, description="Earlybird Hobbyist Ticket", cost="29000", auth=None, validate=None)
#            dict(category_id='1', active=True, description="Hobbyist Ticket", cost="36500", auth=None, validate=None),
#            dict(category_id='1', active=True, description="Earlybird Professional Ticket", cost="63500", auth=None, validate=None),
#            dict(category_id='1', active=True, description="Professional Ticket", cost="78500", auth=None, validate=None),
#            dict(category_id='1', active=True, description="Fairy Penguin Sponsorship", cost="150000", auth=None, validate=None),
#            dict(category_id='1', active=True, description="Speaker Ticket", cost="0", auth="AuthFunc('is_speaker').authorise(self)", validate=None),
#            dict(category_id='1', active=True, description="Miniconf Organiser Ticket", cost="0", auth="AuthFunc('is_miniconf_org').authorise(self)", validate=None),
#            dict(category_id='1', active=True, description="Volunteer Ticket", cost="0", auth="AuthFunc('is_volunteer').authorise(self)", validate=None),
#            dict(category_id='2', active=True, description="Men's Small Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's Medium Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's Large Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's X Large Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's XX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's XXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's XXXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Men's XXXXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's Small Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's Medium Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's Large Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's X Large Shirt", cost="2000", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's XX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's XXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's XXXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='2', active=True, description="Women's XXXXX Large Shirt", cost="2200", auth=None, validate=None),
#            dict(category_id='3', active=True, description="Dinner Tickets", cost="8000", auth=None, validate="ProDinner(dinner_field='product_26_qty',ticket_category='category_1',ticket_id=[5,4])"),
#            dict(category_id='4', active=True, description="I will organise my own", cost="0", auth=None, validate=None),
#            dict(category_id='4', active=True, description="Wrest Point (Visit Accommodation page)", cost="0", auth=None, validate=None),
#            dict(category_id='4', active=True, description="University Accommodation - Includes Breakfast! (price per night)", cost="6000", auth=None, validate=None),
#            dict(category_id='5', active=True, description="Adult", cost="20000", auth=None, validate="PPEmail(adult_field='product_30_qty',email_field='partner_email')"),
#            dict(category_id='5', active=True, description="Child (0-3 years old)", cost="0", auth=None, validate="PPChildrenAdult(current_field='product_31_qty',adult_field='product_30_qty')"),
#            dict(category_id='5', active=True, description="Child (4-6 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_32_qty',adult_field='product_30_qty')"),
#            dict(category_id='5', active=True, description="Child (7-9 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_33_qty',adult_field='product_30_qty')"),
#            dict(category_id='5', active=True, description="Child (10-12 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_34_qty',adult_field='product_30_qty')"),
#            dict(category_id='5', active=True, description="Child (13-17 years old)", cost="14000", auth=None, validate="PPChildrenAdult(current_field='product_35_qty',adult_field='product_30_qty')"),
#            )
#
#    except SQLError, inst:
#        print inst
#        pass
#
#    try:
#        # Included Products
#        model.billing.tables.product_include.insert().execute(
#            # Include 1 Shirt in all registration types
#            dict(product_id='1', include_category_id='2', include_qty='1'),
#            dict(product_id='2', include_category_id='2', include_qty='1'),
#            dict(product_id='3', include_category_id='2', include_qty='1'),
#            dict(product_id='4', include_category_id='2', include_qty='1'),
#            dict(product_id='5', include_category_id='2', include_qty='1'),
#            dict(product_id='6', include_category_id='2', include_qty='1'),
#            dict(product_id='7', include_category_id='2', include_qty='1'),
#            dict(product_id='8', include_category_id='2', include_qty='1'),
#            dict(product_id='9', include_category_id='2', include_qty='2'),
#            # Include 1 Dinner for Professional+miniconf and 2 for Speaker registrations
#            dict(product_id='4', include_category_id='3', include_qty='1'), # pro EB
#            dict(product_id='5', include_category_id='3', include_qty='1'), # pro
#            dict(product_id='6', include_category_id='3', include_qty='1'), # fairy
#            dict(product_id='7', include_category_id='3', include_qty='2'), # speaker
#            dict(product_id='8', include_category_id='3', include_qty='1'), # miniconf
#            # Include 5 partners in the partners program for speakers
#            dict(product_id='7', include_category_id='5', include_qty='5'),
#            )
#
#    except SQLError, inst:
#        print inst
#        pass
#
#    try:
#        # Product Ceilings
#        model.billing.tables.ceiling.insert().execute(
#            dict(name='all-conference', max_sold=None, available_from=None, available_until=None),
#            dict(name='conference', max_sold=750, available_from=None, available_until=None),
#            dict(name='earlybird', max_sold=200, available_from=None, available_until="2009-10-28 23:59:59"),
#            dict(name='non-earlybird', max_sold=None, available_from="2009-10-29 00:00:00", available_until=None),
#            dict(name='uniaccom', max_sold=240, available_from=None, available_until=None),
#            )
#
#    except SQLError, inst:
#        print inst
#        pass
#
#    try:
#        # Product Ceiling Map
#        model.billing.tables.product_ceiling_map.insert().execute(
#            # Student
#            dict(product_id='1', ceiling_id='1'),   # all-conference
#            dict(product_id='1', ceiling_id='2'),   # conference
#            # Earlybird Hobbyist
#            dict(product_id='2', ceiling_id='1'),   # all-conference
#            dict(product_id='2', ceiling_id='2'),   # conference
#            dict(product_id='2', ceiling_id='3'),   # earlybird
#            # Hobbyist
#            dict(product_id='3', ceiling_id='1'),   # all-conference
#            dict(product_id='3', ceiling_id='2'),   # conference
#            dict(product_id='3', ceiling_id='4'),   # non-earlybird
#            # Earlybird Professional
#            dict(product_id='4', ceiling_id='1'),   # all-conference
#            dict(product_id='4', ceiling_id='2'),   # conference
#            dict(product_id='4', ceiling_id='3'),   # earlybird
#            # Professional
#            dict(product_id='5', ceiling_id='1'),   # all-conference
#            dict(product_id='5', ceiling_id='2'),   # conference
#            dict(product_id='5', ceiling_id='4'),   # non-earlybird
#            # Fairy
#            dict(product_id='6', ceiling_id='1'),   # all-conference
#            dict(product_id='6', ceiling_id='2'),   # conference
#            # Speaker
#            dict(product_id='7', ceiling_id='1'),   # all-conference
#            # Miniconf
#            dict(product_id='8', ceiling_id='1'),   # all-conference
#            # Volunteer
#            dict(product_id='9', ceiling_id='1'),   # all-conference
#            # University Accommodation
#            dict(product_id='29', ceiling_id='5'),  # uniaccom
#            )
#    except SQLError, inst:
#        print inst
#        pass
#
#    try:
#        # DB Content
#        model.db_content.tables.db_content_type.insert().execute(
#            dict(name='Page'),
#            dict(name='News'),
#            dict(name='In the press'),
#            )
#
#    except SQLError, inst:
#        print inst
#        pass
