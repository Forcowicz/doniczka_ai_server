from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class PlantPhotoBase(BaseModel):
    timestamp: datetime


class PlantPhotoCreate(PlantPhotoBase):
    photo: UploadFile


class PlantPhotoResponse(PlantPhotoBase):
    id: int
    device_id: int
    path: str
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
