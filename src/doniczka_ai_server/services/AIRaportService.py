import os
import tempfile
from typing import Any, Optional

from doniczka_ai_server.controllers.DeviceController import DeviceController
from doniczka_ai_server.controllers.PlantPhotoController import (
    PlantPhotoController,
)
from doniczka_ai_server.controllers.TelemetryController import (
    TelemetryController,
)
from doniczka_ai_server.enums.TelemetryEnums import TelemetryPeriod
from doniczka_ai_server.schemas.AIRaportSchemas import (
    AIRaportRequest,
    AIRaportModelResponse,
)
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions
from doniczka_ai_server.services.ai_analyzer import AIAnalyzerProtocol
from doniczka_ai_server.services.S3Service import S3Service


class AIRaportService:
    def __init__(self, analyzer: AIAnalyzerProtocol):
        self.analyzer = analyzer

    def analyze(self, device_id: int) -> AIRaportModelResponse:
        # 1. Pobranie danych urządzenia i rośliny
        device_controller = DeviceController.get_instance()
        device = device_controller.get_device(device_id)

        plant_data: dict[str, Any] = {
            "id": device.id,
            "name": device.name,
            "specification": device.specification or {},
            **(device.specification or {}),
        }

        # 2. Pobranie danych telemetrycznych (dobowe zagregowane wiadra)
        telemetry_controller = TelemetryController.get_instance()
        telemetry_buckets = telemetry_controller.get_time_buckets(
            device_id, GetAllOptions(period=TelemetryPeriod.WEEK)
        )

        buckets_data = [
            {
                "bucket": (
                    b.bucket.isoformat()
                    if hasattr(b.bucket, "isoformat")
                    else str(b.bucket)
                ),
                "avg_temperature": b.avg_temperature,
                "avg_air_humidity": b.avg_air_humidity,
                "avg_air_pressure": b.avg_air_pressure,
                "avg_soil_top_humidity": b.avg_soil_top_humidity,
                "avg_soil_middle_humidity": b.avg_soil_middle_humidity,
                "avg_soil_bottom_humidity": b.avg_soil_bottom_humidity,
                "avg_light_intensity": b.avg_light_intensity,
                "avg_uv": b.avg_uv,
            }
            for b in telemetry_buckets
        ]

        telemetry_daily: dict[str, Any] = {
            "period": "1_day",
            "buckets": buckets_data,
        }

        latest_telemetry = telemetry_controller.get_latest(device_id)
        if latest_telemetry:
            telemetry_daily["latest"] = {
                "timestamp": (
                    latest_telemetry.timestamp.isoformat()
                    if hasattr(latest_telemetry.timestamp, "isoformat")
                    else str(latest_telemetry.timestamp)
                ),
                "temperature": latest_telemetry.temperature,
                "air_humidity": latest_telemetry.air_humidity,
                "air_pressure": latest_telemetry.air_pressure,
                "soil_top_humidity": latest_telemetry.soil_top_humidity,
                "soil_middle_humidity": latest_telemetry.soil_middle_humidity,
                "soil_bottom_humidity": latest_telemetry.soil_bottom_humidity,
                "light_intensity": latest_telemetry.light_intensity,
                "uv": latest_telemetry.uv,
            }

        # 3. Pobranie najnowszego zdjęcia z bazy i pobranie z S3 na dysk
        photo_controller = PlantPhotoController.get_instance()
        photos = photo_controller.get_all(device_id, GetAllOptions(limit=1))
        latest_photo = photos[0] if photos else None

        temp_photo_path: Optional[str] = None
        if latest_photo and latest_photo.path:
            s3_service = S3Service.get_instance()
            extension = os.path.splitext(latest_photo.path)[1] or ".jpg"
            with tempfile.NamedTemporaryFile(
                suffix=extension, delete=False
            ) as tmp_file:
                temp_photo_path = tmp_file.name

            downloaded = s3_service.download_file(latest_photo.path, temp_photo_path)
            if not downloaded:
                if os.path.exists(temp_photo_path):
                    os.remove(temp_photo_path)
                raise RuntimeError(
                    f"Failed to download photo {latest_photo.path} from S3."
                )

        try:
            # 4. Konstrukcja DTO
            ai_request = AIRaportRequest(
                device_id=device_id,
                plant=plant_data,
                telemetry_daily=telemetry_daily,
                photo_path=temp_photo_path or "",
            )

            # 5. Wywołanie analyzera
            return self.analyzer.analyze(ai_request)
        finally:
            # 6. Usunięcie tymczasowego pliku ze zdjęciem po wywołaniu analyzera
            if temp_photo_path and os.path.exists(temp_photo_path):
                os.remove(temp_photo_path)
