from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
