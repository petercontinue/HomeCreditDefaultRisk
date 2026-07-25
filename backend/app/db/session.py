from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_privacy_columns() -> None:
    """Add privacy/consent columns on existing databases (create_all won't alter)."""
    statements = [
        "ALTER TABLE loan_applications ADD COLUMN IF NOT EXISTS consent_accepted BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE loan_applications ADD COLUMN IF NOT EXISTS privacy_notice_version VARCHAR(32) NOT NULL DEFAULT ''",
        "ALTER TABLE loan_applications ADD COLUMN IF NOT EXISTS consent_accepted_at TIMESTAMPTZ NULL",
    ]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def init_db() -> None:
    from app.models import loan_application  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_privacy_columns()
