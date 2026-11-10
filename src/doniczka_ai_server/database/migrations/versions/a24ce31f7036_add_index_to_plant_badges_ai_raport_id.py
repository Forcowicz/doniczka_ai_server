"""add index to plant_badges ai_raport_id

Revision ID: a24ce31f7036
Revises: 9aea589118ed
Create Date: 2026-11-09 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a24ce31f7036"
down_revision: Union[str, Sequence[str], None] = "9aea589118ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        op.f("ix_plant_badges_ai_raport_id"),
        "plant_badges",
        ["ai_raport_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_plant_badges_ai_raport_id"), table_name="plant_badges")
