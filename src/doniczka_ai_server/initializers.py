from sqlalchemy import Engine

from doniczka_ai_server.controllers import DeviceController, TelemetryController
from doniczka_ai_server.database.postgres_client import PostgresClient
from doniczka_ai_server.database.schemas import Base

# Model imports
from doniczka_ai_server.models import Device, Telemetry


def initialize_database(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def initialize_controllers(engine: Engine) -> None:
    DeviceController.initialize(engine)
    TelemetryController.initialize(engine)
