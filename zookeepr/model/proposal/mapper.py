from sqlalchemy import mapper, relation

from zookeepr.model.core import Person
from tables import proposal, proposal_type, person_proposal_map, review
from domain import Proposal, ProposalType, Review

# Map the ProposalType object onto the submision_type table
mapper(ProposalType, proposal_type)

# Map the Proposal object onto the proposal table
mapper(Proposal, proposal,
    properties = {
        'type': relation(ProposalType, lazy=True),
        'people': relation(Person, secondary=person_proposal_map,
            backref='proposals')
    }
    )

# Map the Review domain model onto the review table
mapper(Review, review)
