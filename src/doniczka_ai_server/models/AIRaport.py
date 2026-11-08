from datetime import datetime
from typing import Any, Optional
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from doniczka_ai_server.database.schemas import Base
from doniczka_ai_server.enums.AIRaportEnums import AIRaportStatus


class AIRaport(Base):
    __tablename__ = "ai_raports"
    __table_args__ = (CheckConstraint("health_score >= 1 AND health_score <= 10"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE")
    )
    photo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("plant_photos.id", ondelete="SET NULL"), nullable=True
    )
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    health_score: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[AIRaportStatus] = mapped_column(
        Enum(AIRaportStatus), nullable=False, default=AIRaportStatus.PENDING, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    raw_response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
