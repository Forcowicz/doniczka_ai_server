from __future__ import annotations

import math
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from doniczka_ai_server.database.postgres_client import PostgresClient
from doniczka_ai_server.models import Device, Telemetry

DEVICE_ID = 1
BATCH_SIZE = 10_000
START = datetime(2025, 10, 28, tzinfo=timezone.utc)
END = datetime(2026, 10, 28, tzinfo=timezone.utc)
MINUTE = timedelta(minutes=1)


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def _telemetry_row(timestamp: datetime, minute_index: int) -> dict[str, object]:
    """Create a smooth, deterministic synthetic reading for one minute."""
    rng = random.Random(minute_index)
    day_fraction = (minute_index % (24 * 60)) / (24 * 60)
    year_fraction = minute_index / (365 * 24 * 60)

    daily_cycle = math.sin(2 * math.pi * (day_fraction - 0.25))
    seasonal_cycle = math.sin(2 * math.pi * (year_fraction - 0.25))
    daylight = max(0.0, math.sin(math.pi * (day_fraction - 0.25) / 0.5))

    temperature = 20.0 + 3.5 * daily_cycle + 4.0 * seasonal_cycle
    temperature += rng.uniform(-0.2, 0.2)

    air_humidity = 58.0 - 8.0 * daily_cycle - 3.0 * seasonal_cycle
    air_humidity += rng.uniform(-0.8, 0.8)

    soil_trend = 48.0 + 4.0 * seasonal_cycle
    soil_top_humidity = soil_trend + 4.0 * daily_cycle + rng.uniform(-0.3, 0.3)
    soil_middle_humidity = soil_trend + 9.0 + 2.0 * daily_cycle
    soil_middle_humidity += rng.uniform(-0.25, 0.25)
    soil_bottom_humidity = soil_trend + 14.0 + 1.0 * daily_cycle
    soil_bottom_humidity += rng.uniform(-0.2, 0.2)

    light_intensity = int(_clamp(850.0 * daylight + rng.uniform(-20.0, 20.0), 0.0, 1_000.0))

    return {
        "device_id": DEVICE_ID,
        "temperature": round(_clamp(temperature, 10.0, 35.0), 2),
        "air_humidity": round(_clamp(air_humidity, 20.0, 90.0), 2),
        "soil_top_humidity": round(_clamp(soil_top_humidity, 20.0, 80.0), 2),
        "soil_middle_humidity": round(_clamp(soil_middle_humidity, 20.0, 85.0), 2),
        "soil_bottom_humidity": round(_clamp(soil_bottom_humidity, 20.0, 90.0), 2),
        "light_intensity": light_intensity,
        "timestamp": timestamp,
    }


def seed_telemetry() -> int:
    engine = PostgresClient.get_instance()
    inserted = 0

    with Session(engine) as session, session.begin():
        device_exists = session.scalar(
            select(Device.id).where(Device.id == DEVICE_ID)
        )
        if device_exists is None:
            raise RuntimeError(f"Device with id={DEVICE_ID} does not exist")

        batch: list[dict[str, object]] = []
        timestamp = START
        minute_index = 0

        while timestamp < END:
            batch.append(_telemetry_row(timestamp, minute_index))
            if len(batch) == BATCH_SIZE:
                session.execute(insert(Telemetry), batch)
                inserted += len(batch)
                batch.clear()

            timestamp += MINUTE
            minute_index += 1

        if batch:
            session.execute(insert(Telemetry), batch)
            inserted += len(batch)

    return inserted


def main() -> None:
    count = seed_telemetry()
    print(f"Inserted {count} telemetry records for device {DEVICE_ID}.")


if __name__ == "__main__":
    main()
