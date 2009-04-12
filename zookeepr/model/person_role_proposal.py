"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

def setup(meta):
    pass

# for doing n-n mappings of people and proposals
person_proposal_map = Table('person_proposal_map', metadata,
    Column('person_id', Integer, ForeignKey('person.id'),
        nullable=False),
    Column('proposal_id', Integer, ForeignKey('proposal.id'),
        nullable=False),
    )
