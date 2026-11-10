from typing import Protocol

from doniczka_ai_server.schemas import AIRaportRequest
from doniczka_ai_server.schemas.AIRaportSchemas import AIRaportModelResponse


class AIAnalyzerProtocol(Protocol):
    def analyze(self, dto: AIRaportRequest) -> AIRaportModelResponse:
        pass
