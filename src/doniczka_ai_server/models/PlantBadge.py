from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from doniczka_ai_server.database.schemas import Base
from doniczka_ai_server.enums.SeverityEnum import Severity

if TYPE_CHECKING:
    from doniczka_ai_server.models.AIRaport import AIRaport


class PlantBadge(Base):
    __tablename__ = "plant_badges"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE")
    )
    ai_raport_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ai_raports.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    title: Mapped[str] = mapped_column(String(length=32))
    content: Mapped[Optional[str]] = mapped_column(String(length=240), nullable=True)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    ai_raport: Mapped[Optional["AIRaport"]] = relationship(
        back_populates="plant_badges"
    )
