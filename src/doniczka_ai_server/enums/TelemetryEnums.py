from enum import IntEnum


class TelemetryPeriod(IntEnum):
    DAY = 1  # days
    WEEK = 7
    MONTH = 30
    YEAR = 365
