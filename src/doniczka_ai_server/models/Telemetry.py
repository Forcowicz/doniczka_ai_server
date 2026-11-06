from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, synonym

from doniczka_ai_server.database.schemas import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    __table_args__ = ({"postgresql_with": {"tsdb.hypertable": True}},)

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )


class Telemetry1Hour(Base):
    __tablename__ = "telemetry_1hour"

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    bucket: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    timestamp = synonym("bucket")

    avg_temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)


TelemetryHourly = Telemetry1Hour


class Telemetry8Hours(Base):
    __tablename__ = "telemetry_8hours"

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    bucket: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    timestamp = synonym("bucket")

    avg_temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)


class Telemetry24Hours(Base):
    __tablename__ = "telemetry_24hours"

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    bucket: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    timestamp = synonym("bucket")

    avg_temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)


class Telemetry14Days(Base):
    __tablename__ = "telemetry_14days"

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), primary_key=True)
    bucket: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    timestamp = synonym("bucket")

    avg_temperature: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_air_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_top_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_middle_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_soil_bottom_humidity: Mapped[Optional[float]] = mapped_column(nullable=True)
    avg_light_intensity: Mapped[Optional[int]] = mapped_column(nullable=True)


type TelemetryBucket = (
    Telemetry1Hour | Telemetry8Hours | Telemetry24Hours | Telemetry14Days
)
