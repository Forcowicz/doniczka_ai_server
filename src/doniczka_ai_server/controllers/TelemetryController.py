from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.errors.model_errors import InstanceNotFoundException
from doniczka_ai_server.models import Telemetry
from doniczka_ai_server.schemas.TelemetrySchemas import TelemetryCreate


class TelemetryController:
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

    def store_telemetry(self, telemetry_data: TelemetryCreate):
        telemetry = Telemetry(**telemetry_data.model_dump())

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(telemetry)

        return telemetry
