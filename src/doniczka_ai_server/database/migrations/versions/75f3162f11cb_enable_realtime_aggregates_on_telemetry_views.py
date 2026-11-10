"""enable realtime aggregates on telemetry continuous aggregates

Revision ID: 75f3162f11cb
Revises: 9aea589118ed
Create Date: 2026-11-10 15:55:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "75f3162f11cb"
down_revision: Union[str, Sequence[str], None] = "9aea589118ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VIEWS = [
    "telemetry_1hour",
    "telemetry_8hours",
    "telemetry_24hours",
    "telemetry_14days",
]


def upgrade() -> None:
    """Włączenie real-time aggregates dla ciągłych agregatów telemetrii."""
    for view_name in VIEWS:
        op.execute(f"""
            ALTER MATERIALIZED VIEW {view_name}
            SET (timescaledb.materialized_only = false);
        """)


def downgrade() -> None:
    """Przywrócenie trybu materialized_only dla ciągłych agregatów telemetrii."""
    for view_name in reversed(VIEWS):
        op.execute(f"""
            ALTER MATERIALIZED VIEW {view_name}
            SET (timescaledb.materialized_only = true);
        """)
