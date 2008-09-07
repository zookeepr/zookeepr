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

        # Assistance
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='Can\'t attend without full assistance'),
            dict(name='Can\'t attend without partial assistance'),
            dict(name='May need assistance'),
            dict(name='Don\'t need assistance'),
            )

        # Stream
        model.schedule.tables.stream.insert().execute(
            dict(name='Free Love and Open Sensual Stimulation'),
            )

        # Roles
        model.core.tables.role.insert().execute(
            dict(name='reviewer'),
            dict(name='organiser'),
            dict(name='miniconf'),
            dict(name='team'),
            )

        # Product Categories
        model.billing.tables.product_category.insert().execute(
            dict(name='Tickets', description='Please choose your registration type?', display='radio', min_qty=1, max_qty=1),
            dict(name='Shirts', description='Please choose how many shirts you would like. The first one is free with your registration.', display='qty', min_qty=1, max_qty=10),
            dict(name='Dinner Tickets', description='Would you like any dinner tickets? (The first one is free with professional registrations)', display='qty', min_qty=0, max_qty=5),
            dict(name='Accomodation', description='Where would you like to stay during the conference?', display='radio', min_qty=0, max_qty=10),
            dict(name='Partners Program', description='Would your partner like to participate in the partners program?', display='qty', min_qty=0, max_qty=10),
            )

        model.billing.tables.product.insert().execute(
            dict(category_id='1', active=True, description="Earlybird Student Ticket", cost="160"),
            dict(category_id='1', active=True, description="Earlybird Hobbiest Ticket", cost="290"),
            dict(category_id='1', active=True, description="Earlybird Professional Ticket", cost="635"),
            dict(category_id='1', active=False, description="Student Ticket", cost="160"),
            dict(category_id='1', active=False, description="Hobbiest Ticket", cost="365"),
            dict(category_id='1', active=False, description="Professional Ticket", cost="785"),
            dict(category_id='2', active=True, description="Men's Small Shirt", cost="20"),
            dict(category_id='2', active=True, description="Men's Medium Shirt", cost="20"),
            dict(category_id='2', active=True, description="Men's Large Shirt", cost="20"),
            dict(category_id='2', active=True, description="Women's Small Shirt", cost="20"),
            dict(category_id='2', active=True, description="Women's Medium Shirt", cost="20"),
            dict(category_id='2', active=True, description="Women's Large Shirt", cost="20"),
            dict(category_id='3', active=True, description="Dinner Tickets", cost="80"),
            dict(category_id='4', active=True, description="I will organise my own", cost="0"),
            dict(category_id='4', active=True, description="University Accommodation (price per night)", cost="80"),
            dict(category_id='4', active=True, description="Wrest Point (Follow this link to book)", cost="0"),
            dict(category_id='5', active=True, description="Adult", cost="200"),
            dict(category_id='5', active=True, description="Child (0-3 years old)", cost="200"),
            dict(category_id='5', active=True, description="Child (4-6 years old)", cost="200"),
            dict(category_id='5', active=True, description="Child (7-9 years old)", cost="200"),
            dict(category_id='5', active=True, description="Child (10-12 years old)", cost="200"),
            dict(category_id='5', active=True, description="Child (13-17 years old)", cost="200"),
            )

        model.billing.tables.product_include.insert().execute(
            dict(product_id='3', include_category_id='2', include_qty='1'),
            dict(product_id='3', include_category_id='3', include_qty='1'),
            )

        # Product Ceilings
        model.billing.tables.ceiling.insert().execute(
            dict(name='conference', max_sold=1000),
            dict(name='earlybird', max_sold=400),
            )

        # DB Content
        model.db_content.tables.db_content_type.insert().execute(
            dict(name='Page'),
            dict(name='News'),
            dict(name='In the press'),
            )
    except SQLError:
        pass
