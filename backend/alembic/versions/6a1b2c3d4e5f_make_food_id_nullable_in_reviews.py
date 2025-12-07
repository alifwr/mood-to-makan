"""make food_id nullable in reviews

Revision ID: 6a1b2c3d4e5f
Revises: 569c44855b4a
Create Date: 2025-12-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a1b2c3d4e5f'
down_revision: Union[str, Sequence[str], None] = '569c44855b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('reviews', 'food_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('reviews', 'food_id',
               existing_type=sa.INTEGER(),
               nullable=False)
