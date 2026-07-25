from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "postgresql+psycopg2://hcdr:hcdr_pass@127.0.0.1:6436/hcdr"
    )
    model_dir: str = str(PROJECT_ROOT / "ml" / "artifacts")
    approval_threshold: float | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def model_dir_path(self) -> Path:
        path = Path(self.model_dir)
        if not path.is_absolute():
            path = (BACKEND_ROOT / path).resolve()
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()
