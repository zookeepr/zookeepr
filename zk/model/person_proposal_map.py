"""The application's model objects"""
import sqlalchemy as sa

from meta import metadata

# for doing n-n mappings of people and proposals
person_proposal_map = sa.Table('person_proposal_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
        sa.Column('proposal_id',   sa.types.Integer, sa.ForeignKey('proposal.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)
