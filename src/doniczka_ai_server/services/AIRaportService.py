import os
import tempfile
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from doniczka_ai_server.controllers.AIRaportController import AIRaportController
from doniczka_ai_server.controllers.DeviceController import DeviceController
from doniczka_ai_server.controllers.PlantBadgeController import (
    PlantBadgeController,
)
from doniczka_ai_server.controllers.PlantPhotoController import (
    PlantPhotoController,
)
from doniczka_ai_server.controllers.TelemetryController import (
    TelemetryController,
)
from doniczka_ai_server.enums.AIRaportEnums import AIRaportStatus
from doniczka_ai_server.enums.SeverityEnum import Severity
from doniczka_ai_server.enums.TelemetryEnums import TelemetryPeriod
from doniczka_ai_server.schemas.AIRaportSchemas import (
    AIRaportCreate,
    AIRaportRequest,
    AIRaportResponse,
    AIRaportUpdate,
)
from doniczka_ai_server.schemas.PlantBadgeSchemas import PlantBadgeCreate
from doniczka_ai_server.schemas.TelemetrySchemas import GetAllOptions
from doniczka_ai_server.services.ai_analyzer import AIAnalyzerProtocol
from doniczka_ai_server.services.S3Service import S3Service


class AIRaportService:
    def __init__(self, analyzer: AIAnalyzerProtocol):
        self.analyzer = analyzer

    def analyze(self, device_id: int) -> AIRaportResponse:
        # 1. Pobranie urządzenia i najnowszego zdjęcia przed utworzeniem raportu
        device_controller = DeviceController.get_instance()
        device = device_controller.get_device(device_id)

        photo_controller = PlantPhotoController.get_instance()
        photos = photo_controller.get_all(device_id, GetAllOptions(limit=1))
        latest_photo = photos[0] if photos else None

        period = TelemetryPeriod.WEEK
        period_end = datetime.now(timezone.utc)
        period_start = period_end - timedelta(days=period.value)

        # 2. Utworzenie początkowej encji raportu w bazie danych
        raport_controller = AIRaportController.get_instance()
        raport = raport_controller.store(
            AIRaportCreate(
                device_id=device_id,
                photo_id=latest_photo.id if latest_photo else None,
                period_start=period_start,
                period_end=period_end,
                status=AIRaportStatus.PENDING,
            )
        )

        temp_photo_path: Optional[str] = None
        try:
            plant_data: dict[str, Any] = {
                "id": device.id,
                "name": device.name,
                "specification": device.specification or {},
                **(device.specification or {}),
            }

            # 3. Pobranie danych telemetrycznych (zagregowane wiadra)
            telemetry_controller = TelemetryController.get_instance()
            telemetry_buckets = telemetry_controller.get_time_buckets(
                device_id, GetAllOptions(period=period)
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
                "period": f"{period.value}_days",
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

            # 4. Pobranie najnowszego zdjęcia z S3 na dysk tymczasowy
            if latest_photo and latest_photo.path:
                s3_service = S3Service.get_instance()
                extension = os.path.splitext(latest_photo.path)[1] or ".jpg"
                with tempfile.NamedTemporaryFile(
                    suffix=extension, delete=False
                ) as tmp_file:
                    temp_photo_path = tmp_file.name

                downloaded = s3_service.download_file(
                    latest_photo.path, temp_photo_path
                )
                if not downloaded:
                    raise RuntimeError(
                        f"Failed to download photo {latest_photo.path} from S3."
                    )

            # 5. Pobranie aktywnych odznak (is_active = true) oraz konstrukcja DTO
            badge_controller = PlantBadgeController.get_instance()
            active_badges = list(
                badge_controller.get_all(device_id=device_id, active_only=True)
            )

            ai_request = AIRaportRequest(
                device_id=device_id,
                plant=plant_data,
                telemetry_daily=telemetry_daily,
                active_badges=active_badges,
                photo_path=temp_photo_path or "",
            )

            model_response = self.analyzer.analyze(ai_request)

            # 6. Zapisanie wygenerowanych odznak (plant_badges) w bazie danych
            for badge in model_response.plant_badges:
                badge_severity = (
                    Severity[badge.severity]
                    if badge.severity in Severity.__members__
                    else Severity(int(badge.severity))
                )
                badge_controller.store(
                    PlantBadgeCreate(
                        device_id=device_id,
                        ai_raport_id=raport.id,
                        title=badge.title[:32],
                        content=badge.content[:240] if badge.content else None,
                        severity=badge_severity,
                    )
                )

            # 7. Aktualizacja encji raportu wynikami analizy
            return raport_controller.update(
                raport.id,
                AIRaportUpdate(
                    summary=model_response.summary,
                    recommendations=model_response.recommendations,
                    health_score=model_response.health_score,
                    status=AIRaportStatus.SUCCESS,
                    finished_at=datetime.now(timezone.utc),
                    model_name=model_response.model_name,
                    tokens_used=model_response.tokens_used,
                    raw_response=model_response.raw_response,
                ),
            )
        except Exception as exc:
            # Zapisanie błędu w encji raportu
            raport_controller.update(
                raport.id,
                AIRaportUpdate(
                    status=AIRaportStatus.FAILED,
                    finished_at=datetime.now(timezone.utc),
                    error=str(exc),
                ),
            )
            raise
        finally:
            # 8. Usunięcie tymczasowego pliku ze zdjęciem po wywołaniu analyzera
            if temp_photo_path and os.path.exists(temp_photo_path):
                os.remove(temp_photo_path)
