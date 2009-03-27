"""The application's model objects"""
import sqlalchemy as sa

from zookeepr.model.meta import metadata

person_role_map = sa.Table('person_role_map', metadata,
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('person.id')),
        sa.Column('role_id',   sa.types.Integer, sa.ForeignKey('role.id'))
)


def setup(meta):
    pass
