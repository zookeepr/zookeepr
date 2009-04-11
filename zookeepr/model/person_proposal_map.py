"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

person_proposal_map = sa.Table('person_proposal_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id')),
        sa.Column('proposal_id',   sa.types.Integer, sa.ForeignKey('proposal.id'))
)

def setup(meta):
    pass
