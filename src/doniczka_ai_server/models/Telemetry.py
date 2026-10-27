from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

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
