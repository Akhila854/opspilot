from sqlalchemy import String, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InvestigationDB(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    request: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="created",
    )

    severity: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    diagnosis: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    evidence: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    recommended_action: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    requires_human_approval: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )
