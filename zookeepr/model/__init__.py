from core import Person, Role, PasswordResetConfirmation
from proposal import Proposal, ProposalType, Attachment, Review, AssistanceType
from schedule import Stream, Talk
from registration import *
from openday import Openday
from billing import *
from db_content import DBContentType, DBContent

def init_model(app_conf):
    from paste.deploy.converters import asbool
    from sqlalchemy.schema import MetaData as BoundMetaData

    global metadata

    # Under normal conditions, init_model will only ever get called
    # once.  However when used with paste.fixture, it'll get called
    # multiple times.
    if not globals().get('metadata'):
        metadata = BoundMetaData(app_conf['dburi'])
        #metadata.engine.echo = asbool(app_conf.get('echo_queries', 'false'))

        import core.mapper
        import proposal.mapper
        import schedule.mapper
        import registration.mapper
        import openday.mapper
        import billing.mapper
        import db_content.mapper

def create_all(app_conf):
    """This is called from ``websetup`` to create everything."""
    init_model(app_conf)
    metadata.create_all()

def populate_data():
    from sqlalchemy.exceptions import SQLError
    from zookeepr import model

    try:
        # Proposals
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Presentation'),
            dict(name='Miniconf'),
            dict(name='Tutorial'),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Assistance
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='Can\'t attend without full assistance'),
            dict(name='Can\'t attend without partial assistance'),
            dict(name='May need assistance'),
            dict(name='Don\'t need assistance'),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Stream
        model.schedule.tables.stream.insert().execute(
            dict(name='Free Love and Open Sensual Stimulation'),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Roles
        model.core.tables.role.insert().execute(
            dict(name='reviewer'),
            dict(name='organiser'),
            dict(name='miniconf'),
            dict(name='team'),
            dict(name='tentative_volunteer'),
            dict(name='volunteer')
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Product Categories
        model.billing.tables.product_category.insert().execute(
            dict(name='Ticket', description='Please choose your registration type?', display='radio', min_qty=1, max_qty=1),
            dict(name='Shirt', description='Please choose how many shirts you would like. The first one is free with your registration.', display='qty', min_qty=1, max_qty=10),
            dict(name='Dinner Ticket', description='How many people will be attending the dinner (make sure you include yourself)? One (1) free ticket is included with professional registration but you are still required to accept this in the field below.', display='qty', min_qty=0, max_qty=5),
            dict(name='Accomodation', description='Where would you like to stay during the conference?', display='select', min_qty=0, max_qty=10),
            dict(name='Partners Programme', description='Would your partner like to participate in the partners programme?', display='qty', min_qty=0, max_qty=10),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Products
        model.billing.tables.product.insert().execute(
            dict(category_id='1', active=True, description="Earlybird Student Ticket", cost="16000"),
            dict(category_id='1', active=True, description="Earlybird Hobbiest Ticket", cost="29000"),
            dict(category_id='1', active=True, description="Earlybird Professional Ticket", cost="63500"),
            dict(category_id='1', active=True, description="Student Ticket", cost="16000"),
            dict(category_id='1', active=True, description="Hobbiest Ticket", cost="36500"),
            dict(category_id='1', active=True, description="Professional Ticket", cost="78500"),
            dict(category_id='1', active=True, description="Speaker Ticket", cost="0", auth="AuthFunc('is_speaker').authorise(self)"),
            dict(category_id='1', active=True, description="Volunteer Ticket", cost="0", auth="AuthRole('tentative_volunteer').authorise(self)"),
            dict(category_id='2', active=True, description="Men's Small Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's Medium Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's X Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's XX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's XXX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's XXXX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Men's XXXXX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's Small Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's Medium Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's X Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's XX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's XXX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's XXXX Large Shirt", cost="2000"),
            dict(category_id='2', active=True, description="Women's XXXXX Large Shirt", cost="2000"),
            dict(category_id='3', active=True, description="Dinner Tickets", cost="8000"),
            dict(category_id='4', active=True, description="I will organise my own", cost="0"),
            dict(category_id='4', active=True, description="Wrest Point (Follow this link to book)", cost="0"),
            dict(category_id='4', active=True, description="University Accommodation (price per night)", cost="8000"),
            dict(category_id='5', active=True, description="Adult", cost="20000", validate="PPEmail(adult_field='product_18_qty',email_field='partner_email')"),
            dict(category_id='5', active=True, description="Child (0-3 years old)", cost="20000", validate="PPChildrenAdult(current_field='product_19_qty',adult_field='product_18_qty')"),
            dict(category_id='5', active=True, description="Child (4-6 years old)", cost="20000", validate="PPChildrenAdult(current_field='product_20_qty',adult_field='product_18_qty')"),
            dict(category_id='5', active=True, description="Child (7-9 years old)", cost="20000", validate="PPChildrenAdult(current_field='product_21_qty',adult_field='product_18_qty')"),
            dict(category_id='5', active=True, description="Child (10-12 years old)", cost="20000", validate="PPChildrenAdult(current_field='product_22_qty',adult_field='product_18_qty')"),
            dict(category_id='5', active=True, description="Child (13-17 years old)", cost="20000", validate="PPChildrenAdult(current_field='product_23_qty',adult_field='product_18_qty')"),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Included Products
        model.billing.tables.product_include.insert().execute(
            # Include 1 Shirt in all registration types
            dict(product_id='1', include_category_id='2', include_qty='1'),
            dict(product_id='2', include_category_id='2', include_qty='1'),
            dict(product_id='3', include_category_id='2', include_qty='1'),
            dict(product_id='4', include_category_id='2', include_qty='1'),
            dict(product_id='5', include_category_id='2', include_qty='1'),
            dict(product_id='6', include_category_id='2', include_qty='1'),
            dict(product_id='7', include_category_id='2', include_qty='1'),
            # Include 1 Dinner for Professional and Speaker registrations
            dict(product_id='3', include_category_id='3', include_qty='1'),
            dict(product_id='6', include_category_id='3', include_qty='1'),
            dict(product_id='7', include_category_id='3', include_qty='1'),
            # Include 7 nights of accom for speakers
            dict(product_id='7', include_category_id='4', include_qty='7'),
            # Include 5 partners in the partners program for speakers
            dict(product_id='7', include_category_id='5', include_qty='5'),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Product Ceilings
        model.billing.tables.ceiling.insert().execute(
            dict(name='conference', max_sold=1000),
            dict(name='earlybird', max_sold=400),
            dict(name='uniaccom', max_sold=240),
            )

    except SQLError, inst:
        print inst
        pass

    try:
        # Product Ceiling Map
        model.billing.tables.product_ceiling_map.insert().execute(
            dict(product_id='1', ceiling_id='1'),
            dict(product_id='1', ceiling_id='2'),
            dict(product_id='2', ceiling_id='1'),
            dict(product_id='2', ceiling_id='2'),
            dict(product_id='3', ceiling_id='1'),
            dict(product_id='3', ceiling_id='2'),
            dict(product_id='4', ceiling_id='1'),
            dict(product_id='5', ceiling_id='1'),
            dict(product_id='6', ceiling_id='1'),
            dict(product_id='28', ceiling_id='3'),
            )
    except SQLError, inst:
        print inst
        pass

    try:
        # DB Content
        model.db_content.tables.db_content_type.insert().execute(
            dict(name='Page'),
            dict(name='News'),
            dict(name='In the press'),
            )

    except SQLError, inst:
        print inst
        pass
