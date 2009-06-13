"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

def setup(meta):
    pass

# for doing n-n mappings of people and proposals
person_proposal_map = sa.Table('person_proposal_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id'), nullable=False),
        sa.Column('proposal_id',   sa.types.Integer, sa.ForeignKey('proposal.id'), nullable=False)
)
