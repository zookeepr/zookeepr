from core import Person, Role, PasswordResetConfirmation
from proposal import Proposal, ProposalType, Attachment, Review
from schedule import Stream, Talk
from registration import Registration, Accommodation
from openday import Openday
from billing import InvoiceItem, Invoice

def init_model(app_conf):
    from paste.deploy.converters import asbool
    from sqlalchemy import BoundMetaData

    global metadata

    # Under normal conditions, init_model will only ever get called
    # once.  However when used with paste.fixture, it'll get called
    # multiple times.
    if not globals().get('metadata'):
        metadata = BoundMetaData(app_conf['dburi'])
        metadata.engine.echo = asbool(app_conf.get('echo_queries', 'false'))

def create_all(app_conf):
    """This is called from ``websetup`` to create everything."""
    init_model(app_conf)
    metadata.create_all()
