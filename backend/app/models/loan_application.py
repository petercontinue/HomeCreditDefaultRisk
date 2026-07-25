from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    input_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    requested_amount: Mapped[float] = mapped_column(Float, nullable=False)
    default_probability: Mapped[float] = mapped_column(Float, nullable=False)
    approved: Mapped[bool] = mapped_column(Boolean, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False)
    max_approved_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    feedback_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    client_meta: Mapped[str | None] = mapped_column(Text, nullable=True)
