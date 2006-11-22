from core import Person, Role, PasswordResetConfirmation
from proposal import Proposal, ProposalType, Attachment, Review
from schedule import Stream, Talk
from registration import Registration, Accommodation
from openday import Openday
from billing import InvoiceItem, Invoice, PaymentReceived, Payment

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

        import core.mapper
        import proposal.mapper
        import schedule.mapper
        import registration.mapper
        import openday.mapper
        import billing.mapper

def create_all(app_conf):
    """This is called from ``websetup`` to create everything."""
    init_model(app_conf)
    metadata.create_all()

def populate_data():
    from sqlalchemy.exceptions import SQLError
    from zookeepr import model

    try:
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Presentation'),
        )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Miniconf'),
            )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Tutorial'),
            )
        model.schedule.tables.stream.insert().execute(
            dict(name='Free Love and Open Sensual Stimulation'),
            )
        model.core.tables.role.insert().execute(
            dict(name='reviewer'),
            )
    except SQLError:
        pass

    try:
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=1,
                 name="New College",
                 beds=125,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="no breakfast",
                 cost_per_night=49.50,
                 accommodation_location_id=1,
                 )
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="",
                 cost_per_night=55.00,
                 accommodation_location_id=1,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=2,
                 name="Shalom",
                 beds=90,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="",
                 cost_per_night=60.00,
                 accommodation_location_id=2,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="with ensuite",
                 cost_per_night=80.00,
                 accommodation_location_id=2,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=3,
                 name="International house",
                 beds=50,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="no breakfast",
                 cost_per_night=35.00,
                 accommodation_location_id=3,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=4,
                 name="Warrane",
                 beds=50,
                 )
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="male only",
                 cost_per_night=58.50,
                 accommodation_location_id=4,
                 )
            )
    except SQLError:
        pass
