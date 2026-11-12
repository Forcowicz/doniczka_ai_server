"""make_ai_raport_health_score_nullable

Revision ID: cb432ab9cba5
Revises: a24ce31f7036
Create Date: 2026-11-11 00:13:27.172025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb432ab9cba5'
down_revision: Union[str, Sequence[str], None] = 'a24ce31f7036'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "ai_raports",
        "health_score",
        existing_type=sa.SmallInteger(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "ai_raports",
        "health_score",
        existing_type=sa.SmallInteger(),
        nullable=False,
    )
