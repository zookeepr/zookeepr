"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

def setup(meta):
    pass

person_role_map = sa.Table('person_role_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id'), primary_key=True, nullable=False),
        sa.Column('role_id',   sa.types.Integer, sa.ForeignKey('role.id'), primary_key=True, nullable=False)
)
