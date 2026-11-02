from fastapi import FastAPI
from fastapi.params import Form, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Sequence
from doniczka_ai_server.controllers import (
    DeviceController,
    PlantPhotoController,
    TelemetryController,
)
from doniczka_ai_server.database.postgres_client import PostgresClient
from contextlib import asynccontextmanager

from doniczka_ai_server.initializers import (
    initialize_controllers,
    initialize_database,
    initialize_s3,
)
from doniczka_ai_server.models import Device, Telemetry, PlantPhoto
from doniczka_ai_server.schemas.DeviceSchemas import DeviceCreate, DeviceResponse
from doniczka_ai_server.schemas.PlantPhotoSchemas import (
    PlantPhotoCreate,
    PlantPhotoResponse,
)
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions
from doniczka_ai_server.services.S3Service import S3Service


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres_client = PostgresClient.get_instance()

    initialize_database(postgres_client)
    initialize_controllers(postgres_client)
    initialize_s3()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub ["*"] na czas lokalnego developmentu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    pass


@app.get("/devices/{id}")
def get_device(id: int):
    controller: DeviceController = DeviceController.get_instance()

    device: Device = controller.get_device(id)

    return {
        "status": "success",
        "data": {"device": DeviceResponse.model_validate(device)},
    }


@app.post("/devices")
def store_device(device_data: DeviceCreate):
    controller: DeviceController = DeviceController.get_instance()

    device: Device = controller.store_device(device_data)

    return {
        "status": "success",
        "data": {"device": DeviceResponse.model_validate(device)},
    }


@app.patch("/devices/{id}")
def update_device(id: int, device_data: DeviceCreate):
    controller: DeviceController = DeviceController.get_instance()

    device: Device = controller.update_device(id, device_data)

    return {
        "status": "success",
        "data": {"device": DeviceResponse.model_validate(device)},
    }


@app.delete("/devices/{id}")
def delete_device(id: int):
    controller: DeviceController = DeviceController.get_instance()

    controller.delete_device(id)

    return {
        "status": "success",
        "message": f"Device with id {id} has been deleted.",
    }


@app.get("/devices/{id}/telemetry")
def get_telemetry(id: int, options: Annotated[GetAllOptions, Query()]):
    controller: TelemetryController = TelemetryController.get_instance()

    telemetry: Sequence[Telemetry] = controller.get_all(id, options)

    return {
        "status": "success",
        "data": {"telemetry": telemetry},
    }


@app.get("/devices/{id}/photos")
def get_plant_photos(
    id: int,
    options: Annotated[GetAllOptions, Query()] = GetAllOptions(),
):
    controller: PlantPhotoController = PlantPhotoController.get_instance()
    s3_service: S3Service = S3Service.get_instance()

    photos: Sequence[PlantPhoto] = controller.get_all(id, options)

    photo_responses = [
        PlantPhotoResponse(
            id=photo.id,
            device_id=photo.device_id,
            path=photo.path,
            timestamp=photo.timestamp,
            url=s3_service.get_url(photo.path),
        )
        for photo in photos
    ]

    return {
        "status": "success",
        "data": {"photos": photo_responses},
    }


@app.post("/devices/{id}/photos")
def store_plant_photo(
    id: int,
    photo_data: Annotated[PlantPhotoCreate, Form()],
):
    controller: PlantPhotoController = PlantPhotoController.get_instance()

    controller.store(id, photo_data)

    return {
        "status": "success",
        "message": "Plant photo stored successfully.",
    }
