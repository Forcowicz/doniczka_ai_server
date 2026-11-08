"""create initial tables

Revision ID: 9cd0c4ecb0ee
Revises:
Create Date: 2026-10-29 18:07:24.193829

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9cd0c4ecb0ee"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "telemetry",
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("air_humidity", sa.Float(), nullable=True),
        sa.Column("soil_top_humidity", sa.Float(), nullable=True),
        sa.Column("soil_middle_humidity", sa.Float(), nullable=True),
        sa.Column("soil_bottom_humidity", sa.Float(), nullable=True),
        sa.Column("light_intensity", sa.Integer(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.PrimaryKeyConstraint("device_id", "timestamp"),
    )
    # Hypertable bez domyślnego indeksu "telemetry_timestamp_idx" -
    # klucz główny (device_id, timestamp) wystarcza.
    op.execute(
        "SELECT create_hypertable('telemetry', by_range('timestamp'), "
        "create_default_indexes => FALSE);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("telemetry")
    op.drop_table("devices")
