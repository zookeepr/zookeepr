# pytest magic: from .conftest import app_config, db_session$

from zk.model.meta import Session
from zk.model.person import Person
from zk.model.proposal import Proposal, TravelAssistanceType, AccommodationAssistanceType, ProposalStatus, TargetAudience, ProposalType
from zk.model.invoice import Invoice
from zk.model.invoice_item import InvoiceItem
from zk.model.registration import Registration
from zk.model.attachment import Attachment
from zk.model.stream import Stream
from zk.model.review import Review
from zk.model.role import Role

import factory
from factory.alchemy import SQLAlchemyModelFactory

class _ModelFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session
        abstract = True

class _NameIdFactory(_ModelFactory):
    id   = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "name %03d" % n)



class TravelAssistanceTypeFactory(_NameIdFactory):
    class Meta: model = TravelAssistanceType

class RoleFactory(_NameIdFactory):
    class Meta: model = Role

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


class PersonFactory(_ModelFactory):
    class Meta: model = Person

    id            = factory.Sequence(lambda n: n)
    email_address = factory.Sequence(lambda n: "email%03d@example.com" % n)

    creation_timestamp          = '2000-01-01'
    last_modification_timestamp = '2000-01-01'
    url_hash                    = "A"*64
    activated                   = True
    i_agree                     = True

    # Some fields are overriden by the Person constructor, so we can't set them
    # So we stash them, generate the object, then override the value
    # This technique takes advantage of the factory_boy post_generation hook
    @classmethod
    def _generate(cls, create, attrs):
        override = ["creation_timestamp", "activated", "badge_printed", "url_hash"]
        for key in override:
            if key in attrs:
                attrs["post__"+key] = attrs.pop(key)
        return super(PersonFactory, cls)._generate(create, attrs)

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
    person = factory.SubFactory(PersonFactory)


class InvoiceItemFactory(_ModelFactory):
    class Meta: model = InvoiceItem
    id = factory.Sequence(lambda n: n)
    # TODO: invoice is required
    description = factory.Sequence(lambda n: "factory generated item %03d" % n)
    qty         = factory.Sequence(lambda n: n+1)
    cost        = factory.Sequence(lambda n: (n+1)*10)


class RegistrationFactory(_ModelFactory):
    class Meta: model = Registration
    id = factory.Sequence(lambda n: n)
