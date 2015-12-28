# pytest magic: from .conftest import app_config, db_session$

from zk.model.meta import Session
from zk.model.person import Person
from zk.model.proposal import Proposal, TravelAssistanceType, AccommodationAssistanceType, ProposalStatus, TargetAudience, ProposalType
from zk.model.invoice import Invoice
from zk.model.invoice_item import InvoiceItem
from zk.model.registration import Registration
from zk.model.registration_product import RegistrationProduct
from zk.model.attachment import Attachment
from zk.model.stream import Stream
from zk.model.review import Review
from zk.model.role import Role
from zk.model.config import Config
from zk.model.password_reset_confirmation import PasswordResetConfirmation
from zk.model.url_hash import URLHash
from zk.model.product_category import ProductCategory
from zk.model.product import Product
from zk.model.ceiling import Ceiling
from zk.model.fulfilment import Fulfilment, FulfilmentItem, FulfilmentType, FulfilmentStatus, FulfilmentGroup
from zk.model.event_type import EventType
from zk.model.event import Event
from zk.model.db_content import DbContent, DbContentType
from zk.model.funding_attachment import FundingAttachment
from zk.model.funding import Funding, FundingStatus, FundingType
from zk.model.funding_review import FundingReview
from zk.model.location import Location
from zk.model.time_slot import TimeSlot
from zk.model.schedule import Schedule
from zk.model.rego_note import RegoNote
from zk.model.rego_room import RegoRoom
from zk.model.social_network import SocialNetwork
from zk.model.travel import Travel
from zk.model.voucher import Voucher
from zk.model.special_offer import SpecialOffer

from datetime import datetime, timedelta

import factory
from factory.alchemy import SQLAlchemyModelFactory

from faker import Factory as FakerFactory
faker = FakerFactory.create()

class _ModelFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    # Override _create to get correct session object
    # Passing through Meta didn't work as Session had not yet been initialised
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        obj = model_class(*args, **kwargs)
        Session.add(obj)
        return obj

class _NameIdFactory(_ModelFactory):
    id   = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "name %03d" % n)


class EventTypeFactory(_NameIdFactory):
    class Meta: model = EventType

class TravelAssistanceTypeFactory(_NameIdFactory):
    class Meta: model = TravelAssistanceType

class RoleFactory(_ModelFactory):
    class Meta: model = Role
    name = factory.Sequence(lambda n: "name %03d" % n)

class AccommodationAssistanceTypeFactory(_NameIdFactory):
    class Meta: model = AccommodationAssistanceType

class TargetAudienceFactory(_NameIdFactory):
    class Meta: model = TargetAudience

class ProposalStatusFactory(_NameIdFactory):
    class Meta: model = ProposalStatus

class ProposalTypeFactory(_NameIdFactory):
    class Meta: model = ProposalType

class StreamFactory(_NameIdFactory):
    class Meta: model = Stream

class EventFactory(_ModelFactory):
    class Meta: model = Event

    id        = factory.Sequence(lambda n: n)
    type      = factory.SubFactory(EventTypeFactory)
    exclusive = True


class ConfigFactory(_ModelFactory):
    class Meta: model = Config

    category    = 'general'
    key         = factory.Sequence(lambda n: "autokey %03d" % n)
    value       = factory.LazyAttribute(lambda x: faker.word())
    description = factory.LazyAttribute(lambda x: faker.sentence(nb_words=15))

class CeilingFactory(_ModelFactory):
    class Meta: model = Ceiling
    id        = factory.Sequence(lambda n: n)
    name      = factory.Sequence(lambda n: "name%03d" % n)

class URLHashFactory(_ModelFactory):
    class Meta: model = URLHash
    id        = factory.Sequence(lambda n: n)
    url       = '/'
    url_hash  = factory.Sequence(lambda n: "D00D%03d" % n)
    timestamp = datetime.now()

class PersonFactory(_ModelFactory):
    class Meta: model = Person

    id            = factory.Sequence(lambda n: n)
    email_address = factory.Sequence(lambda n: "email%03d@personfactory.com" % n)

    creation_timestamp          = '2000-01-01'
    last_modification_timestamp = '2000-01-01'
    url_hash                    = "A"*64
    activated                   = True
    i_agree                     = True

    # Set default passwords
    # password is set to an encrypted version of password
    # raw_password is set to an unencrypted version of password, but not stored in DB
    post__raw_password          = 'a_swell_password'
    password                    = 'a_swell_password'

    # Some fields are overriden by the Person constructor, so we can't set them
    # So we stash them, generate the object, then override the value
    # This technique takes advantage of the factory_boy post_generation hook
    @classmethod
    def _generate(cls, create, attrs):
        override = ["creation_timestamp", "activated", "badge_printed", "url_hash"]
        for key in override:
            if key in attrs:
                attrs["post__"+key] = attrs.pop(key)

        # Person __init__ function uses Config.get('password_salt')
        try:
            Config.get('password_salt')
        except:
            ConfigFactory.create(key="password_salt", value=23)
        return super(PersonFactory, cls)._generate(create, attrs)

    # post_generation extracts named (post__) elements, presents them after creation
    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        for key in kwargs:
            obj.__dict__[key] = kwargs[key]

class CompletePersonFactory(PersonFactory):
    # Set lots of additional detail to avoid the incomplete profile flag
    firstname = factory.Sequence(lambda n: "jim%03d" % n)
    lastname  = factory.Sequence(lambda n: "kibbles%03d" % n)
    address1  = 'Somewhere',
    city      = 'Over the rainbow',
    postcode  = 'Way up high',

    @classmethod
    def reset_sequence(cls):
        PersonFactory.reset_sequence()

class FulfilmentGroupFactory(_ModelFactory):
    class Meta: model = FulfilmentGroup
    person = factory.SubFactory(PersonFactory)
    code   = factory.Sequence(lambda n: "%s %03d" % (faker.word(), n))

class FulfilmentStatusFactory(_ModelFactory):
    class Meta: model = FulfilmentStatus
    # Can't set id, upsets postgres auto-increment (somehow...)
    name = factory.Sequence(lambda n: "%s%i" % (faker.word(), n))

class FulfilmentTypeFactory(_ModelFactory):
    class Meta: model = FulfilmentType
    initial_status         = factory.SubFactory(FulfilmentStatusFactory)
    name                   = factory.Sequence(lambda n: "type %03d" % n)

class FulfilmentFactory(_ModelFactory):
    class Meta: model = Fulfilment
    person                 = factory.SubFactory(PersonFactory)
    type                   = factory.SubFactory(FulfilmentTypeFactory)
    status                 = factory.SubFactory(FulfilmentStatusFactory)

class ProductCategoryFactory(_ModelFactory):
    class Meta: model = ProductCategory
    id                     = factory.Sequence(lambda n: n)
    name                   = factory.Sequence(lambda n: "product category %03d" % n)
    description            = factory.Sequence(lambda n: "factory generated category %03d" % n)
    display                = factory.LazyAttribute(lambda x: ['radio', 'select', 'checkbox', 'qty'][faker.pyint() % 4])
    display_mode           = factory.LazyAttribute(lambda x: ['grid', 'shirt'][faker.pyint() % 2])
    display_order          = factory.LazyAttribute(lambda x: faker.pyint())
    invoice_free_products  = factory.LazyAttribute(lambda x: faker.boolean())

class ProductFactory(_ModelFactory):
    class Meta: model = Product
    id                     = factory.Sequence(lambda n: n)
    fulfilment_type        = factory.SubFactory(FulfilmentTypeFactory)
    category               = factory.SubFactory(ProductCategoryFactory)
    active                 = True
    description            = factory.Sequence(lambda n: "factory generated product %03d" % n)
    cost                   = factory.Sequence(lambda n: n*100)

class FulfilmentItemFactory(_ModelFactory):
    class Meta: model = FulfilmentItem
    id                     = factory.Sequence(lambda n: n)
    fulfilment             = factory.SubFactory(FulfilmentFactory)
    product                = factory.SubFactory(ProductFactory)
    qty                    = factory.Sequence(lambda n: (n+1)*3)

class ProposalFactory(_ModelFactory):
    class Meta: model = Proposal
    id                     = factory.Sequence(lambda n: n)
    title                  = factory.Sequence(lambda n: "title %03d" % n)
    abstract               = factory.Sequence(lambda n: "abstract %03d" % n)
    private_abstract       = factory.Sequence(lambda n: "private_abstract %03d" % n)
    technical_requirements = factory.Sequence(lambda n: "technical_requirements %03d" % n)
    title                  = factory.Sequence(lambda n: "title %03d" % n)
    project                = factory.Sequence(lambda n: "project %03d" % n)

    video_release  = True
    slides_release = True

    travel_assistance        = factory.SubFactory(TravelAssistanceTypeFactory)
    accommodation_assistance = factory.SubFactory(AccommodationAssistanceTypeFactory)
    status                   = factory.SubFactory(ProposalStatusFactory)
    audience                 = factory.SubFactory(TargetAudienceFactory)
    type                     = factory.SubFactory(ProposalTypeFactory)

#    creation_timestamp = default current_timestamp()
#    last_modification_timestamp = default current_timestamp()


class PasswordResetConfirmationFactory(_ModelFactory):
    class Meta: model = PasswordResetConfirmation
    id            = factory.Sequence(lambda n: n)
    email_address = factory.Sequence(lambda n: "email%03d@passwordresetconfirmationfactory.com" % n)
    url_hash      = "R"*64
    timestamp     = factory.LazyAttribute(lambda o: datetime.now())

    # Some fields are overriden by the constructor, so we can't set them
    # So we stash them, generate the object, then override the value
    # This technique takes advantage of the factory_boy post_generation hook
    @classmethod
    def _generate(cls, create, attrs):
        override = ["timestamp"]
        for key in override:
            if key in attrs:
                attrs["post__"+key] = attrs.pop(key)
        return super(PasswordResetConfirmationFactory, cls)._generate(create, attrs)

    # post_generation extracts named (post__) elements, presents them after creation
    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        for key in kwargs:
            obj.__dict__[key] = kwargs[key]


class AttachmentFactory(_ModelFactory):
    class Meta: model = Attachment
    id      = factory.Sequence(lambda n: n)
    content = factory.Sequence(lambda n: "content %03d" % n)
    # TODO: need to get proposal_id in somehow, there is no smart map


class ReviewFactory(_ModelFactory):
    class Meta: model = Review
    id              = factory.Sequence(lambda n: n)
    miniconf        = factory.Sequence(lambda n: "miniconf %03d" % n)
    comment         = factory.Sequence(lambda n: "comment %03d" % n)
    private_comment = factory.Sequence(lambda n: "private_comment %03d" % n)
    # TODO: not null items
    #proposal_id
    #reviewer_id
    #private_comment
    #creation_timestamp
    #last_modification_timestamp


class InvoiceFactory(_ModelFactory):
    class Meta: model = Invoice
    id = factory.Sequence(lambda n: n)
    person = factory.SubFactory(PersonFactory)


class InvoiceItemFactory(_ModelFactory):
    class Meta: model = InvoiceItem
    id = factory.Sequence(lambda n: n)
    invoice = factory.SubFactory(InvoiceFactory)
    description = factory.Sequence(lambda n: "factory generated item %03d" % n)
    qty         = factory.Sequence(lambda n: n+1)
    cost        = factory.Sequence(lambda n: (n+1)*10)


class RegistrationFactory(_ModelFactory):
    class Meta: model = Registration
    id = factory.Sequence(lambda n: n)
    person = factory.SubFactory(CompletePersonFactory)


class RegistrationProductFactory(_ModelFactory):
    class Meta: model = RegistrationProduct
    registration_id = factory.SubFactory(RegistrationFactory)
    product_id = factory.SubFactory(ProductFactory)
    qty = 1

class DbContentTypeFactory(_NameIdFactory):
    class Meta: model = DbContentType

class DbContentFactory(_ModelFactory):
    class Meta: model = DbContent
    title                       = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    type                        = factory.SubFactory(DbContentTypeFactory)
    url                         = factory.LazyAttribute(lambda x: faker.url())
    body                        = factory.LazyAttribute(lambda x: "\n\n".join(faker.paragraphs(nb=3)))
    creation_timestamp          = factory.LazyAttribute(lambda x: faker.date_time())
    publish_timestamp           = factory.LazyAttribute(lambda x: faker.date_time())
    last_modification_timestamp = factory.LazyAttribute(lambda x: faker.date_time())

class FundingStatusFactory(_NameIdFactory):
    class Meta: model = FundingStatus

class FundingTypeFactory(_NameIdFactory):
    class Meta: model = FundingType
    active       = factory.LazyAttribute(lambda x: faker.boolean())
    note         = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    notify_email = factory.LazyAttribute(lambda x: faker.email())

class FundingFactory(_ModelFactory):
    class Meta: model = Funding
    person                  = factory.SubFactory(CompletePersonFactory)
    status                  = factory.SubFactory(FundingStatusFactory)
    type                    = factory.SubFactory(FundingTypeFactory)
    male                    = factory.LazyAttribute(lambda x: faker.boolean())
    why_attend              = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    how_contribute          = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    financial_circumstances = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    diverse_groups          = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    supporting_information  = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    prevlca                 = factory.LazyAttribute(lambda x: " ".join([faker.word() for i in range(5)]))


class FundingAttachmentFactory(_ModelFactory):
    class Meta: model = FundingAttachment
    funding  = factory.SubFactory(FundingFactory)
    filename = factory.LazyAttribute(lambda x: faker.word())
    content  = factory.LazyAttribute(lambda x: bytes(faker.word()))

class FundingReviewFactory(_ModelFactory):
    class Meta: model = FundingReview
    funding  = factory.SubFactory(FundingFactory)
    reviewer = factory.SubFactory(CompletePersonFactory)
    score    = factory.LazyAttribute(lambda x: faker.pyint())
    comment  = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))

class TimeSlotFactory(_ModelFactory):
    class Meta: model = TimeSlot
    id   = factory.Sequence(lambda n: n)
    start_time      = factory.LazyAttribute(lambda x: faker.date_time())
    end_time        = factory.LazyAttribute(lambda x: faker.date_time_between_dates(datetime_start=x.start_time, datetime_end=x.start_time+timedelta(days=1)))
    primary         = factory.LazyAttribute(lambda x: faker.boolean())
    heading         = factory.LazyAttribute(lambda x: faker.boolean())

class LocationFactory(_ModelFactory):
    class Meta: model = Location
    display_name  = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    display_order = factory.LazyAttribute(lambda x: faker.pyint())
    capacity      = factory.LazyAttribute(lambda x: faker.pyint())

class ScheduleFactory(_ModelFactory):
    class Meta: model = Schedule
    overflow     = factory.LazyAttribute(lambda x: faker.boolean())
    video_url    = factory.LazyAttribute(lambda x: faker.url())
    audio_url    = factory.LazyAttribute(lambda x: faker.url())
    slide_url    = factory.LazyAttribute(lambda x: faker.url())
    time_slot    = factory.SubFactory(TimeSlotFactory)
    location     = factory.SubFactory(LocationFactory)
    event        = factory.SubFactory(EventFactory)

class RegoNoteFactory(_ModelFactory):
    class Meta: model = RegoNote
    rego = factory.SubFactory(RegistrationFactory)
    by   = factory.SubFactory(PersonFactory)
    note = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    block = factory.LazyAttribute(lambda x: faker.boolean())
    # creation_timestamp & last_modification_timestamp auto-set

class RegoRoomFactory(_ModelFactory):
    class Meta: model = RegoRoom
    rego = factory.SubFactory(RegistrationFactory)
    by   = factory.SubFactory(CompletePersonFactory)
    room = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    # creation_timestamp & last_modification_timestamp auto-set

class SocialNetworkFactory(_ModelFactory):
    class Meta: model = SocialNetwork
    name = factory.Sequence(lambda n: "%s%i" % (faker.word(), n))
    logo = factory.LazyAttribute(lambda x: faker.word())
    url  = factory.LazyAttribute(lambda x: faker.url())

class TravelFactory(_ModelFactory):
    class Meta: model = Travel
    person = factory.SubFactory(PersonFactory)
    origin_airport = factory.LazyAttribute(lambda x: faker.word())
    destination_airport = factory.LazyAttribute(lambda x: faker.word())
    flight_details = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))

class VoucherFactory(_ModelFactory):
    class Meta: model = Voucher

    code = factory.Sequence(lambda n: "%s%i" % (faker.word(), n))
    comment = factory.LazyAttribute(lambda x: faker.sentence(nb_words=8))
    leader = factory.SubFactory(PersonFactory)
    # creation_timestamp & last_modification_timestamp auto-set

class SpecialOfferFactory(_ModelFactory):
    class Meta: model = SpecialOffer

    enabled = factory.LazyAttribute(lambda x: faker.boolean())
    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda x: faker.sentence(nb_words=10))
    id_name = factory.LazyAttribute(lambda x: faker.word())
