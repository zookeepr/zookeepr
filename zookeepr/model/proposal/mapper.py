from sqlalchemy import mapper, relation

from zookeepr.model.core import Person
from zookeepr.model.proposal.tables import proposal, proposal_type, person_proposal_map
from zookeepr.model.proposal.domain import Proposal, ProposalType

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
