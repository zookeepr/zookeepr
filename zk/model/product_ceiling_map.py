"""The application's model objects"""
import sqlalchemy as sa

from meta import metadata

product_ceiling_map = sa.Table('product_ceiling_map', metadata,
        sa.Column('product_id', sa.types.Integer, sa.ForeignKey('product.id'), primary_key=True, nullable=False),
        sa.Column('ceiling_id', sa.types.Integer, sa.ForeignKey('ceiling.id'), primary_key=True, nullable=False)
)
