from core import Person, Role, PasswordResetConfirmation
from proposal import Proposal, ProposalType, Attachment, Review, AssistanceType
from schedule import Stream, Talk
from registration import Registration, Accommodation
from openday import Openday
from billing import InvoiceItem, Invoice, PaymentReceived, Payment, VoucherCode
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
        )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Miniconf'),
            )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Tutorial'),
            )

        # Assistance
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='Can\'t attend without full assistance'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='Can\'t attend without partial assistance'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='May need assistance'),
            )
        model.proposal.tables.assistance_type.insert().execute(
            dict(name='Don\'t need assistance'),
            )

        model.schedule.tables.stream.insert().execute(
            dict(name='Free Love and Open Sensual Stimulation'),
            )
        model.core.tables.role.insert().execute(
            dict(name='reviewer'),
            )
        model.core.tables.role.insert().execute(
            dict(name='organiser'),
            )
        model.core.tables.role.insert().execute(
            dict(name='miniconf'),
            )
        model.core.tables.role.insert().execute(
            dict(name='team'),
            )
            
        model.db_content.tables.db_content_type.insert().execute(
            dict(name='Page'),
            )
        model.db_content.tables.db_content_type.insert().execute(
            dict(name='News'),
            )
    except SQLError:
        pass
