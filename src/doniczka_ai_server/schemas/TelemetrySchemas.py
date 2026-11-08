from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from doniczka_ai_server.enums.TelemetryEnums import TelemetryPeriod


class TelemetryBase(BaseModel):
    temperature: Optional[float] = None  # Celsius
    air_humidity: Optional[float] = None  # Percentage
    air_pressure: Optional[int] = None
    soil_top_humidity: Optional[float] = None  # Percentage
    soil_middle_humidity: Optional[float] = None  # Percentage
    soil_bottom_humidity: Optional[float] = None  # Percentage
    light_intensity: Optional[int] = None  # LUX
    uv: Optional[float] = None
    fire: Optional[bool] = None
    timestamp: datetime


class TelemetryCreate(TelemetryBase):
    pass


# Query parameters


class GetAllOptions(BaseModel):
    period: TelemetryPeriod = TelemetryPeriod.DAY
    limit: Optional[int] = None
