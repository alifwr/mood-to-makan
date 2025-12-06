"""merge heads

Revision ID: 569c44855b4a
Revises: 3ae053fca305, 4f2a1b3c4d5e
Create Date: 2025-12-06 23:18:52.627426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '569c44855b4a'
down_revision: Union[str, Sequence[str], None] = ('3ae053fca305', '4f2a1b3c4d5e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
