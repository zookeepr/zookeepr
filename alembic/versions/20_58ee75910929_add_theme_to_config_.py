"""Add theme to config

Revision ID: 58ee75910929
Revises: 1c22ceb384a7
Create Date: 2015-08-28 15:15:47.971807

"""

# revision identifiers, used by Alembic.
revision = '58ee75910929'
down_revision = '1c22ceb384a7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("INSERT INTO config (category, key, value, description) VALUES ('general', 'theme', '\"zkpylons\"', 'The enabled theme to use. Should match the theme folder name (requires a server restart to take effect)')")


def downgrade():
    op.execute("DELETE FROM config WHERE category='general' AND key='theme'")

