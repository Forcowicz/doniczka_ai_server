from enum import IntEnum, StrEnum

from doniczka_ai_server.models.Telemetry import (
    Telemetry14Days,
    Telemetry1Hour,
    Telemetry24Hours,
    Telemetry8Hours,
    TelemetryBucket,
)


class PumpBlock(StrEnum):
    NONE = "NONE"
    NO_WATER = "NO_WATER"
    FIRE = "FIRE"
    COOLDOWN = "COOLDOWN"


class TelemetryPeriod(IntEnum):
    DAY = 1  # days
    WEEK = 7
    MONTH = 30
    YEAR = 365

    @property
    def postgres_interval(self) -> str:
        return TELEMETRY_PERIOD_TO_POSTGRES_INTERVAL[self]


TELEMETRY_PERIOD_TO_POSTGRES_INTERVAL: dict[TelemetryPeriod, str] = {
    TelemetryPeriod.DAY: "1 day",
    TelemetryPeriod.WEEK: "7 days",
    TelemetryPeriod.MONTH: "30 days",
    TelemetryPeriod.YEAR: "1 year",
}

TELEMETRY_PERIOD_TO_POSTGRES_VIEW: dict[TelemetryPeriod, type[TelemetryBucket]] = {
    TelemetryPeriod.DAY: Telemetry1Hour,
    TelemetryPeriod.WEEK: Telemetry8Hours,
    TelemetryPeriod.MONTH: Telemetry24Hours,
    TelemetryPeriod.YEAR: Telemetry14Days,
}
