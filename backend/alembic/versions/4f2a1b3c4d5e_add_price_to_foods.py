"""add price to foods

Revision ID: 4f2a1b3c4d5e
Revises: 10c7115345f7
Create Date: 2025-12-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f2a1b3c4d5e'
down_revision = '10c7115345f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('foods', sa.Column('price', sa.Float(), nullable=False, server_default='0.0'))


def downgrade() -> None:
    op.drop_column('foods', 'price')
