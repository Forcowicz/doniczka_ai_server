"""update telemetry continuous aggregates with avg_air_pressure and avg_uv

Revision ID: 9aea589118ed
Revises: 5351ca3ef89c
Create Date: 2026-11-08 20:55:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9aea589118ed"
down_revision: Union[str, Sequence[str], None] = "5351ca3ef89c"
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
        # 1. Usunięcie polityki automatycznego odświeżania (job policy)
        op.execute(
            f"SELECT remove_continuous_aggregate_policy('{view_name}', if_exists => TRUE);"
        )
        # 2. Zrzucenie starego widoku Continuous Aggregate wraz z chunkami
        op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {view_name} CASCADE;")

        # 3. Utworzenie widoku z nowymi kolumnami (avg_air_pressure, avg_uv)
        op.execute(f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {view_name}
            WITH (timescaledb.continuous) AS
            SELECT
                device_id,
                time_bucket('{bucket_interval}', timestamp) AS bucket,
                avg(temperature) AS avg_temperature,
                avg(air_humidity) AS avg_air_humidity,
                avg(air_pressure)::int AS avg_air_pressure,
                avg(soil_top_humidity) AS avg_soil_top_humidity,
                avg(soil_middle_humidity) AS avg_soil_middle_humidity,
                avg(soil_bottom_humidity) AS avg_soil_bottom_humidity,
                avg(light_intensity)::int AS avg_light_intensity,
                avg(uv) AS avg_uv
            FROM telemetry
            GROUP BY device_id, bucket
            WITH NO DATA;
        """)

        # 4. Ponowne dodanie polityki automatycznego odświeżania
        op.execute(f"""
            SELECT add_continuous_aggregate_policy(
                continuous_aggregate => '{view_name}',
                start_offset => INTERVAL '{start_offset}',
                end_offset => INTERVAL '{bucket_interval}',
                schedule_interval => INTERVAL '{schedule_interval}'
            );
        """)


def downgrade() -> None:
    for view_name, bucket_interval, schedule_interval, start_offset in reversed(VIEWS):
        # 1. Usunięcie nowej polityki
        op.execute(
            f"SELECT remove_continuous_aggregate_policy('{view_name}', if_exists => TRUE);"
        )
        # 2. Zrzucenie nowego widoku
        op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {view_name} CASCADE;")

        # 3. Przywrócenie widoku w wersji z f4aee1e99d4a
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

        # 4. Przywrócenie polityki automatycznego odświeżania
        op.execute(f"""
            SELECT add_continuous_aggregate_policy(
                continuous_aggregate => '{view_name}',
                start_offset => INTERVAL '{start_offset}',
                end_offset => INTERVAL '{bucket_interval}',
                schedule_interval => INTERVAL '{schedule_interval}'
            );
        """)
