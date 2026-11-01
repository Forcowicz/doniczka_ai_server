from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    name: str
    specification: Optional[dict[str, Any]] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
