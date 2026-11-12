from collections.abc import Sequence

from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session

from doniczka_ai_server.enums import TELEMETRY_PERIOD_TO_POSTGRES_INTERVAL
from doniczka_ai_server.enums.TelemetryEnums import TELEMETRY_PERIOD_TO_POSTGRES_VIEW
from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.models import TelemetryBucket, Telemetry
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

    def get_latest(self, device_id: int) -> Telemetry:
        stmt = (
            select(Telemetry)
            .where(Telemetry.device_id == device_id)
            .order_by(Telemetry.timestamp.desc())
            .limit(1)
        )

        with Session(self.db_client, expire_on_commit=False) as session:
            return session.scalars(stmt).first()

    def get_time_buckets(
        self, device_id: int, options: GetAllOptions
    ) -> Sequence[TelemetryBucket]:
        interval = TELEMETRY_PERIOD_TO_POSTGRES_INTERVAL.get(
            options.period, f"{options.period.value} days"
        )

        TelemetryView: type[TelemetryBucket] = TELEMETRY_PERIOD_TO_POSTGRES_VIEW.get(
            options.period
        )

        stmt = (
            select(TelemetryView)
            .where(
                TelemetryView.device_id == device_id,
                TelemetryView.bucket >= text(f"NOW() - INTERVAL '{interval}'"),
            )
            .order_by(TelemetryView.bucket.asc())
        )

        if options.limit is not None:
            stmt = stmt.limit(options.limit)

        with Session(self.db_client, expire_on_commit=False) as session:
            return session.scalars(stmt).all()

    def store_telemetry(self, telemetry_data: TelemetryCreate):
        telemetry = Telemetry(**telemetry_data.model_dump(), device_id=1)

        try:
            with Session(
                self.db_client, expire_on_commit=False
            ) as session, session.begin():
                session.add(telemetry)

            return telemetry
        except Exception as e:
            print(f"An error has occurred when saving a Telemetry entity: {e}")
