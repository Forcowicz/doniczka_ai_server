from collections.abc import Sequence
from typing import Optional

from sqlalchemy import Engine, select, update
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.errors.model_errors import InstanceNotFoundException
from doniczka_ai_server.models import PlantBadge
from doniczka_ai_server.schemas.PlantBadgeSchemas import (
    PlantBadgeCreate,
    PlantBadgeResponse,
)
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions


class PlantBadgeController:
    _instance = None

    def __init__(self, db_client: Engine) -> None:
        self.db_client = db_client

    @classmethod
    def initialize(cls, db_client: Engine) -> None:
        if cls._instance is not None:
            return

        cls._instance = cls(db_client)

    @classmethod
    def get_instance(cls) -> "PlantBadgeController":
        if cls._instance is None:
            raise ControllerNotInstantiatedException()
        return cls._instance

    @staticmethod
    def _to_orm(badge_data: PlantBadgeCreate) -> PlantBadge:
        payload = badge_data.model_dump()
        if payload.get("timestamp") is None:
            payload.pop("timestamp", None)
        return PlantBadge(**payload)

    def get_all(
        self,
        device_id: Optional[int] = None,
        active_only: bool = True,
        options: Optional[GetAllOptions] = None,
    ) -> Sequence[PlantBadgeResponse]:
        stmt = select(PlantBadge).order_by(PlantBadge.timestamp.desc())

        if device_id is not None:
            stmt = stmt.where(PlantBadge.device_id == device_id)

        if active_only:
            stmt = stmt.where(PlantBadge.is_active.is_(True))

        if options and options.limit:
            stmt = stmt.limit(options.limit)

        with Session(self.db_client) as session:
            results = session.scalars(stmt).all()
            return [PlantBadgeResponse.model_validate(badge) for badge in results]

    def get_one(self, id: int, device_id: Optional[int] = None) -> PlantBadgeResponse:
        stmt = select(PlantBadge).where(PlantBadge.id == id)

        if device_id is not None:
            stmt = stmt.where(PlantBadge.device_id == device_id)

        with Session(self.db_client) as session:
            result = session.scalars(stmt).first()
            if result is None:
                raise InstanceNotFoundException()
            return PlantBadgeResponse.model_validate(result)

    def store(self, badge_data: PlantBadgeCreate) -> PlantBadgeResponse:
        badge = self._to_orm(badge_data)

        with Session(self.db_client) as session, session.begin():
            session.add(badge)
            session.flush()
            session.refresh(badge)
            return PlantBadgeResponse.model_validate(badge)

    def store_many(
        self, badges_data: Sequence[PlantBadgeCreate]
    ) -> Sequence[PlantBadgeResponse]:
        if not badges_data:
            return []

        badges = [self._to_orm(badge_data) for badge_data in badges_data]

        with Session(self.db_client) as session, session.begin():
            session.add_all(badges)
            session.flush()
            for badge in badges:
                session.refresh(badge)
            return [PlantBadgeResponse.model_validate(badge) for badge in badges]

    def deactivate_by_device(self, device_id: int) -> None:
        stmt = (
            update(PlantBadge)
            .where(PlantBadge.device_id == device_id, PlantBadge.is_active.is_(True))
            .values(is_active=False)
        )

        with Session(self.db_client) as session, session.begin():
            session.execute(stmt)
