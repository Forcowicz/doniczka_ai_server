from typing import Any, Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from doniczka_ai_server.database.schemas import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    specification: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
