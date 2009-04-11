from sqlalchemy.orm import mapper, relation
from sqlalchemy.sql import select

from tables import stream
from domain import Stream, Talk
from zookeepr.model.proposal.tables import proposal, person_proposal_map
from zookeepr.model.proposal.domain import ProposalType
from zookeepr.model.core.domain import Person

# map the Stream domain object onto the stream table
mapper(Stream, stream)
