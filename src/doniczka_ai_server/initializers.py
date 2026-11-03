import os

from sqlalchemy import Engine

from doniczka_ai_server.controllers import (
    DeviceController,
    EventLogEntryController,
    PlantPhotoController,
    TelemetryController,
)
from doniczka_ai_server.database.postgres_client import PostgresClient
from doniczka_ai_server.database.schemas import Base

# Model imports
from doniczka_ai_server.models import Device, EventLogEntry, PlantPhoto, Telemetry
from doniczka_ai_server.services.S3Service import S3Service


def initialize_database(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def initialize_controllers(engine: Engine) -> None:
    DeviceController.initialize(engine)
    TelemetryController.initialize(engine)
    PlantPhotoController.initialize(engine)
    EventLogEntryController.initialize(engine)


def initialize_s3() -> None:
    S3Service.initialize(os.getenv("AWS_BUCKET_NAME"))
