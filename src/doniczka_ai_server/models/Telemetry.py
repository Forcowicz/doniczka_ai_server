from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, synonym

from doniczka_ai_server.database.schemas import Base, ViewBase


class Telemetry(Base):
    __tablename__ = "telemetry"

    __table_args__ = ({"postgresql_with": {"tsdb.hypertable": True}},)

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    air_pressure: Mapped[Optional[int]] = mapped_column(nullable=True)
    soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)
    uv: Mapped[Optional[float]] = mapped_column(nullable=True)
    fire: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )


class _TelemetryBucketColumns:
    """Shared columns of TimescaleDB continuous aggregates (read-only views
    created in migration f4aee1e99d4a). No ForeignKey here - views have no
    constraints and `devices` lives in a different MetaData."""

    device_id: Mapped[int] = mapped_column(primary_key=True)
    bucket: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)

    @declared_attr
    def timestamp(cls):
        return synonym("bucket")

    avg_temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_pressure: Mapped[Optional[int]] = mapped_column(nullable=True)
    avg_soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)
    avg_uv: Mapped[Optional[float]] = mapped_column(nullable=True)


class Telemetry1Hour(_TelemetryBucketColumns, ViewBase):
    __tablename__ = "telemetry_1hour"


TelemetryHourly = Telemetry1Hour


class Telemetry8Hours(_TelemetryBucketColumns, ViewBase):
    __tablename__ = "telemetry_8hours"


class Telemetry24Hours(_TelemetryBucketColumns, ViewBase):
    __tablename__ = "telemetry_24hours"


class Telemetry14Days(_TelemetryBucketColumns, ViewBase):
    __tablename__ = "telemetry_14days"


type TelemetryBucket = (
    Telemetry1Hour | Telemetry8Hours | Telemetry24Hours | Telemetry14Days
)
