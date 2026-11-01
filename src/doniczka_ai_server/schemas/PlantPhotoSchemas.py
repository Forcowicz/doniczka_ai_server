from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class PlantPhotoBase(BaseModel):
    timestamp: datetime


class PlantPhotoCreate(PlantPhotoBase):
    photo: UploadFile
