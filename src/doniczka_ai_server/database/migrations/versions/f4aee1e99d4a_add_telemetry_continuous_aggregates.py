"""add_telemetry_continuous_aggregates

Revision ID: f4aee1e99d4a
Revises: fa189b6c9200
Create Date: 2026-11-06 21:46:45.264124

"""

from typing import Sequence, Union
from alembic import op

revision: str = "..."
down_revision: Union[str, Sequence[str], None] = "..."
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
# Konfiguracja widoków: (nazwa_widoku, bucket_interval, refresh_schedule, start_offset)
VIEWS = [
    ("telemetry_1hour", "1 hour", "1 hour", "1 month"),
    ("telemetry_8hours", "8 hours", "8 hours", "3 months"),
    ("telemetry_24hours", "24 hours", "24 hours", "1 year"),
    ("telemetry_14days", "14 days", "1 day", "5 years"),
]


def upgrade() -> None:
    for view_name, bucket_interval, schedule_interval, start_offset in VIEWS:
        # 1. Tworzenie Continuous Aggregate
        op.execute(f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {view_name}
            WITH (timescaledb.continuous) AS
            SELECT
                device_id,
                time_bucket('{bucket_interval}', timestamp) AS bucket,
                avg(temperature) AS avg_temperature,
                avg(air_humidity) AS avg_air_humidity,
                avg(soil_top_humidity) AS avg_soil_top_humidity,
                avg(soil_middle_humidity) AS avg_soil_middle_humidity,
                avg(soil_bottom_humidity) AS avg_soil_bottom_humidity,
                avg(light_intensity)::int AS avg_light_intensity
            FROM telemetry
            GROUP BY device_id, bucket
            WITH NO DATA;
        """)
        # 2. Polityka automatycznego odświeżania w tle przez TimescaleDB
        op.execute(f"""
            SELECT add_continuous_aggregate_policy(
                continuous_aggregate => '{view_name}',
                start_offset => INTERVAL '{start_offset}',
                end_offset => INTERVAL '{bucket_interval}',
                schedule_interval => INTERVAL '{schedule_interval}'
            );
        """)


def downgrade() -> None:
    for view_name, _, _, _ in reversed(VIEWS):
        op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {view_name} CASCADE;")
