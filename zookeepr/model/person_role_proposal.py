"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

person__map = sa.Table('person_role_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id')),
        sa.Column('role_id',   sa.types.Integer, sa.ForeignKey('role.id'))
)

# for doing n-n mappings of people and proposals
person_proposal_map = Table('person_proposal_map', metadata,
    Column('person_id', Integer, ForeignKey('person.id'),
        nullable=False),
    Column('proposal_id', Integer, ForeignKey('proposal.id'),
        nullable=False),
    )



def setup(meta):
    pass
