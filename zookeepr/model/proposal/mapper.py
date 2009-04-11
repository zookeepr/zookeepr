from sqlalchemy.orm import mapper, relation

from zookeepr.model.core import Person
from zookeepr.model.schedule import Stream
from tables import accommodation_assistance_type, travel_assistance_type, proposal, proposal_type, proposal_status, target_audience, person_proposal_map, attachment, review
from domain import AccommodationAssistanceType, TravelAssistanceType, Proposal, ProposalType, TargetAudience, ProposalStatus, Attachment, Review

# Map the ProposalType object onto the submision_type table
mapper(ProposalType, proposal_type)
mapper(TargetAudience, target_audience)
mapper(ProposalStatus, proposal_status)

mapper(AccommodationAssistanceType, accommodation_assistance_type)
mapper(TravelAssistanceType, travel_assistance_type)

# Map the Attachment object onto the attachment table
mapper(Attachment, attachment)

# Map the Proposal object onto the proposal table
mapper(Proposal, proposal,
    properties = {
        'type': relation(ProposalType),
        'audience': relation(TargetAudience),
        'accommodation_assistance': relation(AccommodationAssistanceType),
        'travel_assistance': relation(TravelAssistanceType),
        'status': relation(ProposalStatus),
        'people': relation(Person, secondary=person_proposal_map,
            backref='proposals'),
        'attachments': relation(Attachment, lazy=True,
            cascade="all, delete-orphan"),
        'reviews' : relation(Review, cascade="all, delete-orphan",
             backref='proposal'),
    }
    )

# Map the Review domain model onto the review table
mapper(Review, review,
       properties = {
    'reviewer': relation(Person, lazy=True, backref='reviews'),
    'stream': relation(Stream, lazy=True),
    }
       )
