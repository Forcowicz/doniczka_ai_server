from collections.abc import Sequence
from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, selectinload

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.errors.model_errors import InstanceNotFoundException
from doniczka_ai_server.models import AIRaport
from doniczka_ai_server.schemas.AIRaportSchemas import (
    AIRaportCreate,
    AIRaportResponse,
    AIRaportUpdate,
)
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions


class AIRaportController:
    _instance = None
    IMMUTABLE_FIELDS = frozenset(
        {
            "id",
            "device_id",
            "period_start",
            "period_end",
            "created_at",
            "photo_id",
        }
    )

    def __init__(self, db_client: Engine) -> None:
        self.db_client = db_client

    @classmethod
    def initialize(cls, db_client: Engine) -> None:
        if cls._instance is not None:
            return

        cls._instance = cls(db_client)

    @classmethod
    def get_instance(cls) -> "AIRaportController":
        if cls._instance is None:
            raise ControllerNotInstantiatedException()
        return cls._instance

    def get_all(
        self,
        device_id: Optional[int] = None,
        options: Optional[GetAllOptions] = None,
    ) -> Sequence[AIRaportResponse]:
        stmt = (
            select(AIRaport)
            .options(selectinload(AIRaport.plant_badges))
            .order_by(AIRaport.created_at.desc())
        )

        if device_id is not None:
            stmt = stmt.where(AIRaport.device_id == device_id)

        if options and options.limit:
            stmt = stmt.limit(options.limit)

        with Session(self.db_client) as session:
            results = session.scalars(stmt).all()
            return [AIRaportResponse.model_validate(raport) for raport in results]

    def get_one(self, id: int, device_id: Optional[int] = None) -> AIRaportResponse:
        stmt = (
            select(AIRaport)
            .options(selectinload(AIRaport.plant_badges))
            .where(AIRaport.id == id)
        )

        if device_id is not None:
            stmt = stmt.where(AIRaport.device_id == device_id)

        with Session(self.db_client) as session:
            result = session.scalars(stmt).first()
            if result is None:
                raise InstanceNotFoundException()
            return AIRaportResponse.model_validate(result)

    def store(self, raport_data: AIRaportCreate) -> AIRaportResponse:
        raport = AIRaport(**raport_data.model_dump())

        with Session(self.db_client) as session, session.begin():
            session.add(raport)
            session.flush()
            session.refresh(raport)
            return AIRaportResponse.model_validate(raport)

    def update(self, id: int, raport_data: AIRaportUpdate) -> AIRaportResponse:
        stmt = (
            select(AIRaport)
            .options(selectinload(AIRaport.plant_badges))
            .where(AIRaport.id == id)
        )

        with Session(self.db_client) as session, session.begin():
            raport = session.scalars(stmt).first()
            if raport is None:
                raise InstanceNotFoundException()

            for key, value in raport_data.model_dump(exclude_unset=True).items():
                if key not in self.IMMUTABLE_FIELDS:
                    setattr(raport, key, value)

            session.flush()
            return AIRaportResponse.model_validate(raport)
