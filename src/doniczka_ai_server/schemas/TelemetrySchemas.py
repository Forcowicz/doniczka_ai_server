from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from doniczka_ai_server.enums.TelemetryEnums import TelemetryPeriod


class TelemetryBase(BaseModel):
    device_id: int
    temperature: Optional[float] = None  # Celsius
    air_humidity: Optional[float] = None  # Percentage
    soil_top_humidity: Optional[float] = None  # Percentage
    soil_middle_humidity: Optional[float] = None  # Percentage
    soil_bottom_humidity: Optional[float] = None  # Percentage
    light_intensity: Optional[int] = None  # LUX
    timestamp: datetime


class TelemetryCreate(TelemetryBase):
    pass


# Query parameters


class GetAllOptions(BaseModel):
    period: TelemetryPeriod = TelemetryPeriod.DAY
    limit: Optional[int] = None
