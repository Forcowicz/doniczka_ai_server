from collections.abc import Sequence
from typing import Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.errors.model_errors import InstanceNotFoundException
from doniczka_ai_server.models import EventLogEntry
from doniczka_ai_server.schemas.EventLogEntrySchemas import EventLogEntryCreate
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions


class EventLogEntryController:
    _instance = None

    def __init__(self, db_client: Engine) -> None:
        self.db_client = db_client

    @classmethod
    def initialize(cls, db_client: Engine) -> None:
        if cls._instance is not None:
            return

        cls._instance = cls(db_client)

    @classmethod
    def get_instance(cls) -> "EventLogEntryController":
        if cls._instance is None:
            raise ControllerNotInstantiatedException()
        return cls._instance

    def get_all(
        self,
        device_id: Optional[int] = None,
        limit: Optional[int] = None,
        options: Optional[GetAllOptions] = None,
    ) -> Sequence[EventLogEntry]:
        stmt = select(EventLogEntry).order_by(EventLogEntry.timestamp.desc())

        if device_id is not None:
            stmt = stmt.where(EventLogEntry.device_id == device_id)

        effective_limit = (
            limit if limit is not None else (options.limit if options else None)
        )
        if effective_limit is not None:
            stmt = stmt.limit(effective_limit)

        with Session(self.db_client, expire_on_commit=False) as session:
            return session.scalars(stmt).all()

    def get_all_logs(
        self, limit: Optional[int] = None, device_id: Optional[int] = None
    ) -> Sequence[EventLogEntry]:
        return self.get_all(device_id=device_id, limit=limit)

    def get_log(self, id: int) -> EventLogEntry:
        stmt = select(EventLogEntry).where(EventLogEntry.id == id)

        with Session(self.db_client) as session:
            result = session.scalars(stmt).first()
            if result is None:
                raise InstanceNotFoundException()
            return result

    def store(self, data: EventLogEntryCreate) -> EventLogEntry:
        event_log = EventLogEntry(
            device_id=1,
            **data.model_dump(),
        )

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(event_log)

        return event_log

    def delete_log(self, id: int) -> None:
        event_log = self.get_log(id)

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.delete(event_log)

