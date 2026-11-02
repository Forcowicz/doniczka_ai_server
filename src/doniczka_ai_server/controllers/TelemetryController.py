from datetime import datetime, timedelta
from collections.abc import Sequence

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.models import Telemetry
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions, TelemetryCreate


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

    def get_all(self, device_id: int, options: GetAllOptions) -> Sequence[Telemetry]:
        stmt = select(Telemetry).where(Telemetry.device_id == device_id).limit(20)

        # if options.limit is not None:
        #     stmt = stmt.limit(options.limit)
        # else:
        #     stmt.where(
        #         Telemetry.timestamp > datetime.now() - timedelta(options.period.value)
        #     )

        with Session(self.db_client, expire_on_commit=False) as session:
            return session.scalars(stmt).all()

    def store_telemetry(self, telemetry_data: TelemetryCreate):
        telemetry = Telemetry(**telemetry_data.model_dump())

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(telemetry)

        return telemetry
