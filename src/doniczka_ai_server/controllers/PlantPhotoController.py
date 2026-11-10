import os
import uuid
from collections.abc import Sequence

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.models import PlantPhoto
from doniczka_ai_server.schemas.PlantPhotoSchemas import PlantPhotoCreate
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions



class PlantPhotoController:
    _instance = None

    def __init__(self, db_client: Engine) -> None:
        self.db_client = db_client

    @classmethod
    def initialize(cls, db_client: Engine) -> None:
        if cls._instance is not None:
            return

        cls._instance = cls(db_client)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise ControllerNotInstantiatedException()
        return cls._instance

    def get_all(self, device_id: int, options: GetAllOptions) -> Sequence[PlantPhoto]:
        stmt = (
            select(PlantPhoto)
            .where(PlantPhoto.device_id == device_id)
            .order_by(PlantPhoto.timestamp.desc())
        )

        if options.limit is not None:
            stmt = stmt.limit(options.limit)

        with Session(self.db_client, expire_on_commit=False) as session:
            return session.scalars(stmt).all()

    def store(self, device_id: int, data: PlantPhotoCreate) -> PlantPhoto:
        from doniczka_ai_server.services.S3Service import S3Service

        s3_service = S3Service.get_instance()

        extension = (
            os.path.splitext(data.photo.filename)[1] if data.photo.filename else ""
        )
        object_name = f"{uuid.uuid4()}{extension}"

        uploaded = s3_service.upload_fileobj(data.photo.file, object_name)
        if not uploaded:
            raise RuntimeError("Failed to upload photo to S3.")

        plant_photo = PlantPhoto(
            device_id=device_id,
            timestamp=data.timestamp,
            path=object_name,
        )

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(plant_photo)

        return plant_photo
