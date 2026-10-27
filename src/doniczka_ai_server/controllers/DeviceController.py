from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from doniczka_ai_server.errors.controller_errors import (
    ControllerNotInstantiatedException,
)
from doniczka_ai_server.errors.model_errors import InstanceNotFoundException
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

    def get_device(self, id: int) -> Device:
        stmt = select(Device).where(Device.id == id)

        with Session(self.db_client) as session:
            result = session.scalars(stmt).first()
            if result is None:
                raise InstanceNotFoundException()
            return result

    def store_device(self, device_data: DeviceCreate):
        device = Device(**device_data.model_dump())

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(device)

        return device

    def update_device(self, id: int, device_data: DeviceCreate):
        device = self.get_device(id)

        for key, value in device_data.model_dump().items():
            setattr(device, key, value)

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.add(device)

        return device

    def delete_device(self, id: int):
        device = self.get_device(id)

        with Session(
            self.db_client, expire_on_commit=False
        ) as session, session.begin():
            session.delete(device)
