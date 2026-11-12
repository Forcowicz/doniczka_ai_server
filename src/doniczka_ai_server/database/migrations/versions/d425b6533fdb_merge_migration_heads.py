"""merge migration heads

Revision ID: d425b6533fdb
Revises: 75f3162f11cb, cb432ab9cba5
Create Date: 2026-11-12 02:20:38.055727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd425b6533fdb'
down_revision: Union[str, Sequence[str], None] = ('75f3162f11cb', 'cb432ab9cba5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
