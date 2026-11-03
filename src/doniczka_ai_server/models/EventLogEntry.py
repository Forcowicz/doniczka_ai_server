from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from doniczka_ai_server.database.schemas import Base
from doniczka_ai_server.enums.SeverityEnum import Severity


class EventLogEntry(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    content: Mapped[str] = mapped_column(Text)
    severity: Mapped[Severity] = mapped_column(SAEnum(Severity))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
