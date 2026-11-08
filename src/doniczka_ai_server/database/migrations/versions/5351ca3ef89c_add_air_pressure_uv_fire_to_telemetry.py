"""add air_pressure uv fire to telemetry

Revision ID: 5351ca3ef89c
Revises: 452081350605
Create Date: 2026-11-08 20:47:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5351ca3ef89c"
down_revision: Union[str, Sequence[str], None] = "452081350605"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("telemetry", sa.Column("air_pressure", sa.Integer(), nullable=True))
    op.add_column("telemetry", sa.Column("uv", sa.Float(), nullable=True))
    op.add_column("telemetry", sa.Column("fire", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column("telemetry", "fire")
    op.drop_column("telemetry", "uv")
    op.drop_column("telemetry", "air_pressure")
