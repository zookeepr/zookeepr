from sqlalchemy.orm import mapper, relation

from zookeepr.model.core import Person
from zookeepr.model.schedule import Stream
from tables import assistance_type, proposal, proposal_type, person_proposal_map, attachment, review
from domain import AssistanceType, Proposal, ProposalType, Attachment, Review

# Map the ProposalType object onto the submision_type table
mapper(ProposalType, proposal_type)

mapper(AssistanceType, assistance_type)

# Map the Attachment object onto the attachment table
mapper(Attachment, attachment)

# Map the Proposal object onto the proposal table
mapper(Proposal, proposal,
    properties = {
        'type': relation(ProposalType),
        'assistance': relation(AssistanceType),
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
