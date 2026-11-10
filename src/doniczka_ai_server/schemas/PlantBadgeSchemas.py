from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from doniczka_ai_server.enums.SeverityEnum import Severity


class PlantBadgeModelOutput(BaseModel):
    title: str = Field(max_length=32)
    content: Optional[str]
    severity: str


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
