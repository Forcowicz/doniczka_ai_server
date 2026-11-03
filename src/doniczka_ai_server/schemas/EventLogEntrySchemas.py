from datetime import datetime

from pydantic import BaseModel, ConfigDict

from doniczka_ai_server.enums.SeverityEnum import Severity


class EventLogEntryBase(BaseModel):
    content: str
    severity: Severity
    timestamp: datetime


class EventLogEntryCreate(EventLogEntryBase):
    pass


class EventLogEntryResponse(EventLogEntryBase):
    id: int
    device_id: int

    model_config = ConfigDict(from_attributes=True)

