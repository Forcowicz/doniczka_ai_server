import json
import os
from datetime import datetime
from typing import Any, List

from google.genai import Client, types

from doniczka_ai_server.enums.SeverityEnum import Severity
from doniczka_ai_server.schemas.AIRaportSchemas import (
    AIRaportModelOutput,
    AIRaportRequest,
    AIRaportModelResponse,
)
from doniczka_ai_server.services.ai_analyzer import AIAnalyzerProtocol


class GeminiAIAnalyzer(AIAnalyzerProtocol):
    MODEL_ID = "gemini-3.8-flash"

    SYSTEM_INSTRUCTION = """Jesteś ekspertem botaniki, fizjologii roślin i agronomii, działającym jako silnik analityczny dla inteligentnej doniczki (Smart Plant Pot).

Twoim zadaniem jest przeprowadzenie rzetelnej, wielomodalnej analizy kondycji rośliny domowej na podstawie dostarczonych danych specyfikacji rośliny, dobowych pomiarów telemetrycznych z czujników, aktualnie aktywnych odznak (is_active = true) oraz załączonego zdjęcia (o ile jest dostępne).

ZASADY ANALIZY:
1. SPECYFIKACJA ROŚLINY:
   - Zwróć uwagę na gatunek rośliny oraz jej specyficzne preferencje środowiskowe (zapotrzebowanie na światło, tolerancję wilgotności podłoża i powietrza, zakres temperatur).

2. KORELACJA Z TELEMETRIĄ (OSTATNIE 24 GODZINY):
   - Wilgotność podłoża: przeanalizuj wilgotność na trzech poziomach (górna, środkowa, dolna). Zwróć uwagę na ryzyko przelania (zastój wody na dole doniczki) lub przesuszenia podłoża.
   - Oświetlenie: oceń, czy natężenie światła (w luksach) w ciągu dnia jest wystarczające dla danego gatunku i czy roślina nie jest narażona na poparzenia słoneczne lub zbyt ciemne stanowisko.
   - Temperatura i wilgotność powietrza: oceń, czy warunki termiczne i wilgotnościowe nie wywołują stresu fizjologicznego u rośliny.

3. ANALIZA ZDJĘCIA (JEŚLI ZAŁĄCZONE):
   - Oceń turgor liści, ich wybarwienie, obecność plam, nekroz, przebarwień, usychania końcówek, chlorozy lub oznak szkodników.
   - Połącz obserwacje wizualne z danymi telemetrycznymi (np. żółknięcie liści + wysoka wilgotność dolna = objaw przelania i gnicia korzeni).

4. OCENA STANU ZDROWIA (health_score):
   - Przyznaj ocenę w skali od 1 do 10 (liczba całkowita):
     * 1-3: Stan krytyczny (roślina obumiera, pilna potrzeba ratunku, zaawansowane gnicie korzeni lub skrajne uschnięcie).
     * 4-6: Stan zły / wymagający interwencji (wyraźne objawy stresu, nieodpowiednie nawodnienie lub oświetlenie).
     * 7-8: Stan dobry (roślina zdrowa, prawidłowy rozwój, drobne uwagi pielęgnacyjne).
     * 9-10: Stan doskonały (wzorcowy wigor, optymalne parametry środowiskowe).

5. PODSUMOWANIE I ZALECENIA:
   - summary: Zwięzłe, rzeczowe podsumowanie aktualnej kondycji rośliny w języku polskim.
   - recommendations: Konkretne, praktyczne instrukcje pielęgnacyjne w punktach dla właściciela (np. dawka wody, przestawienie, zraszanie).

6. ODZNAKI (plant_badges) I KONTEKST AKTYWNYCH ODZNAK:
   - W danych wejściowych otrzymujesz listę aktualnie aktywnych odznak rośliny (is_active = true). Wykorzystaj je, aby zachować ciągłość analizy (np. sprawdzić, czy poprzedni problem nadal występuje, czy ustąpił) oraz nie dublować zbędnie tych samych odznak.
   - Wygeneruj do 6 krótkich odznak (najlepiej 4–6, o ile pozwalają na to dane), obejmujących różne kluczowe obszary stanu rośliny (np. nawodnienie gleby, oświetlenie, temperatura, wilgotność powietrza, kondycja wizualna liści).
   - title: Zwięzły tytuł (bezwzględnie MAKSYMALNIE 32 znaki!), np. "Dobre nawodnienie", "Za mało światła", "Zastój wody w glebie".
   - content: Krótkie (1-2 zdania) wyjaśnienie przyczyny nadania odznaki.
   - severity: Poziom istotności odznaki. MUSI być jedną z poniższych dopuszczalnych wartości enuma Severity:
     * POSITIVE (1) - Stan optymalny, wzorcowy (np. właściwe nawodnienie, idealne oświetlenie).
     * INFO (2) - Stan neutralny / obserwacja (np. faza spoczynku, stabilna temperatura).
     * WARNING (3) - Ostrzeżenie, umiarkowane odchylenie od normy (np. przesychające podłoże, niedostateczne światło).
     * CRITICAL (4) - Stan krytyczny, bezpośrednie zagrożenie dla rośliny (np. przelanie i gnicie korzeni, skrajna susza, niebezpieczna temperatura)."""

    def analyze(self, dto: AIRaportRequest) -> AIRaportModelResponse:
        active_badges_data = [
            {
                "id": badge.id,
                "title": badge.title,
                "content": badge.content,
                "severity": f"{badge.severity.name} ({badge.severity.value})",
                "timestamp": badge.timestamp.isoformat(),
            }
            for badge in dto.active_badges
        ]

        prompt_text = (
            "DANE WEJŚCIOWE DO ANALIZY:\n\n"
            "1. SPECYFIKACJA ROŚLINY:\n"
            f"{json.dumps(dto.plant, indent=2, ensure_ascii=False)}\n\n"
            "2. DOBOWE DANE TELEMETRYCZNE (OSTATNIE 24 GODZINY):\n"
            f"{json.dumps(dto.telemetry_daily, indent=2, ensure_ascii=False)}\n\n"
            "3. AKTYWNE ODZNAKI ROŚLINY (is_active = true):\n"
            f"{json.dumps(active_badges_data, indent=2, ensure_ascii=False)}\n"
        )

        uploaded_file = None
        with Client() as client:
            try:
                contents: List[Any] = [prompt_text]

                if dto.photo_path and os.path.exists(dto.photo_path):
                    uploaded_file = client.files.upload(file=dto.photo_path)
                    contents.append(uploaded_file)

                response = client.models.generate_content(
                    model=self.MODEL_ID,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=AIRaportModelOutput,
                        temperature=0.3,
                        system_instruction=self.SYSTEM_INSTRUCTION,
                    ),
                )
            finally:
                if uploaded_file:
                    try:
                        client.files.delete(name=uploaded_file.name)  # type: ignore
                    except Exception:
                        pass

        parsed_data = response.parsed
        if parsed_data is None:
            if not response.text:
                raise ValueError("Gemini returned an empty response.")
            parsed_data = AIRaportModelOutput.model_validate_json(response.text)

        # Walidacja i normalizacja pól odpowiedzi, w szczególności enuma Severity
        self._validate_and_normalize_output(parsed_data)  # type: ignore

        result = AIRaportModelResponse(
            **parsed_data.model_dump(),  # type: ignore
            device_id=dto.device_id,
            raw_response=response.text or "",
            tokens_used=response.usage_metadata.total_token_count,  # type: ignore
            timestamp=datetime.now(),
            model_name=response.model_version or self.MODEL_ID,
        )

        return result

    def _validate_and_normalize_output(self, output: AIRaportModelOutput) -> None:
        output.plant_badges = output.plant_badges[:5]

        valid_severity_names = set(Severity.__members__.keys())
        valid_severity_values = {str(s.value): s.name for s in Severity}

        for badge in output.plant_badges:
            # 1. Walidacja i normalizacja enuma Severity
            raw_severity = str(badge.severity).strip().upper()
            if raw_severity in valid_severity_names:
                badge.severity = raw_severity
            elif raw_severity in valid_severity_values:
                badge.severity = valid_severity_values[raw_severity]
            else:
                badge.severity = Severity.INFO.name

            # 2. Walidacja długości tytułu odznaki (maksymalnie 32 znaki)
            if len(badge.title) > 32:
                badge.title = badge.title[:32].strip()

        # 3. Walidacja oceny zdrowia (zakres 1 - 10)
        output.health_score = max(1, min(10, output.health_score))
