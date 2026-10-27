import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from doniczka_ai_server.controllers import DeviceController
from doniczka_ai_server.database.postgres_client import PostgresClient
from contextlib import asynccontextmanager

from doniczka_ai_server.initializers import initialize_controllers, initialize_database
from doniczka_ai_server.models import Device
from doniczka_ai_server.schemas.DeviceSchemas import DeviceCreate, DeviceResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres_client = PostgresClient.get_instance()

    initialize_database(postgres_client)
    initialize_controllers(postgres_client)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    pass


@app.post("/devices")
def store_device(device_data: DeviceCreate):
    controller: DeviceController = DeviceController.get_instance()

    device: Device = controller.store_device(device_data)

    return {
        "status": "success",
        "data": {"device": DeviceResponse.model_validate(device)},
    }
