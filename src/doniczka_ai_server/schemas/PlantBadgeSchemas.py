from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from doniczka_ai_server.enums.SeverityEnum import Severity


class PlantBadgeModelOutput(BaseModel):
    title: str = Field(max_length=32)
    content: Optional[str]
    severity: str


class PlantBadgeCreate(BaseModel):
    device_id: int
    ai_raport_id: Optional[int] = None
    is_active: bool = True
    title: str = Field(..., max_length=32)
    content: Optional[str] = Field(default=None, max_length=240)
    severity: Severity
    timestamp: Optional[datetime] = None

    @field_validator("severity", mode="before")
    @classmethod
    def parse_severity(cls, value: Any) -> Severity:
        if isinstance(value, Severity):
            return value
        if isinstance(value, int):
            return Severity(value)
        if isinstance(value, str):
            normalized = value.strip().upper()
            if normalized in Severity.__members__:
                return Severity[normalized]
            return Severity(int(normalized))
        raise ValueError(f"Invalid severity: {value}")


class PlantBadgeResponse(BaseModel):
    id: int
    device_id: int
    ai_raport_id: Optional[int] = None
    is_active: bool
    title: str
    content: Optional[str] = None
    severity: Severity
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
