import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from doniczka_ai_server.enums.AIRaportEnums import AIRaportStatus
from doniczka_ai_server.schemas.PlantBadgeSchemas import (
    PlantBadgeModelOutput,
    PlantBadgeResponse,
)


class AIRaportRequest(BaseModel):
    device_id: int
    plant: Dict[str, Any] = Field(default_factory=dict)
    telemetry_daily: Dict[str, Any] = Field(default_factory=dict)
    photo_path: str = ""


AIResponseRequest = AIRaportRequest


class AIRaportModelOutput(BaseModel):
    summary: str
    recommendations: str
    health_score: int = Field(..., ge=1, le=10)

    plant_badges: List["PlantBadgeModelOutput"]


class AIRaportModelResponse(AIRaportModelOutput):
    device_id: int
    raw_response: str
    tokens_used: int
    timestamp: datetime
    model_name: str


class AIRaportResponse(BaseModel):
    id: int
    device_id: int
    photo_id: Optional[int] = None
    period_start: datetime
    period_end: datetime
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    health_score: int
    status: AIRaportStatus
    created_at: datetime
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None
    raw_response: Optional[dict[str, Any] | str] = None

    plant_badges: List[PlantBadgeResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


def _parse_raw_response(value: Any) -> Optional[dict[str, Any]]:
    if value is None or isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {"value": parsed}
        except json.JSONDecodeError:
            return {"raw": value}
    return value


class AIRaportCreate(BaseModel):
    device_id: int
    period_start: datetime
    period_end: datetime
    health_score: int = Field(..., ge=1, le=10)
    photo_id: Optional[int] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    status: AIRaportStatus = AIRaportStatus.PENDING
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None
    raw_response: Optional[dict[str, Any] | str] = None

    @field_validator("raw_response", mode="before")
    @classmethod
    def validate_raw_response(cls, value: Any) -> Optional[dict[str, Any]]:
        return _parse_raw_response(value)


class AIRaportUpdate(BaseModel):
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    health_score: Optional[int] = Field(default=None, ge=1, le=10)
    status: Optional[AIRaportStatus] = None
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None
    raw_response: Optional[dict[str, Any] | str] = None

    @field_validator("raw_response", mode="before")
    @classmethod
    def validate_raw_response(cls, value: Any) -> Optional[dict[str, Any]]:
        return _parse_raw_response(value)
