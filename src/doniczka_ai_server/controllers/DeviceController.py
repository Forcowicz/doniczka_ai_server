from sqlalchemy import Engine
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.models import Device
from doniczka_ai_server.schemas.DeviceSchemas import DeviceCreate


class DeviceController:
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

    def store_device(self, device_data: DeviceCreate):
        device = Device(**device_data.model_dump())

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(device)

        return device
