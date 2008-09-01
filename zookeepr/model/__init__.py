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
            dict(name='registration', description='Please choose your registration type?', display='radio', min_qty=1, max_qty=1),
            dict(name='shirt', description='Please choose how many shirts you would like. One is included with your registration.', display='qty', min_qty=1, max_qty=10),
            dict(name='dinner', description='Would you like any extra dinner tickets?', display='qty', min_qty=0, max_qty=5),
            dict(name='accomodation', description='Where would you like to stay during the conference?', display='radio', min_qty=0, max_qty=10),
            dict(name='partner', description='Would your partner like to participate in the partners program?', display='qty', min_qty=0, max_qty=10),
            )

        # Product Ceilings
        model.billing.tables.ceiling.insert().execute(
            dict(name='conference'),
            dict(name='earlybird'),
            )

        # DB Content
        model.db_content.tables.db_content_type.insert().execute(
            dict(name='Page'),
            dict(name='News'),
            dict(name='In the press'),
            )
    except SQLError:
        pass
