from enum import StrEnum


class AIRaportStatus(StrEnum):
    CREATED = "created"
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
