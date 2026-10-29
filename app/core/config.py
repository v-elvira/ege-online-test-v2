import os
from functools import lru_cache
from pathlib import Path
from typing import Self
from urllib.parse import quote_plus

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILES = {
    "development": ".env.development",
    "dev": ".env.development",
    "production": ".env.production",
    "prod": ".env.production",
}


def resolve_env_file() -> Path:
    app_env = os.getenv("APP_ENV", "development").strip().lower()
    filename = _ENV_FILES.get(app_env)
    if filename is None:
        allowed = ", ".join(sorted(set(_ENV_FILES)))
        raise ValueError(f"Unknown APP_ENV={app_env!r}. Use one of: {allowed}")
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(
            f"Env file '{filename}' not found for APP_ENV={app_env}. "
            "Copy .env.production.example to .env.production for prod."
        )
    return path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "EGE API"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    secret_key: str = Field(default="change-me-in-production", min_length=8)
    access_token_expire_minutes: int = 60

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "ege"
    database_url: str = ""

    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_pre_ping: bool = True

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
    ]

    @model_validator(mode="after")
    def assemble_postgres_url(self) -> Self:
        url = self.database_url.strip()
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if not url:
            user = quote_plus(self.postgres_user)
            password = quote_plus(self.postgres_password)
            url = (
                f"postgresql+asyncpg://{user}:{password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        if not url.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL must use async PostgreSQL: postgresql+asyncpg://...")
        self.database_url = url
        return self

    @model_validator(mode="after")
    def reject_insecure_production(self) -> Self:
        if self.app_env.lower() not in {"production", "prod"}:
            return self
        if self.debug:
            raise ValueError("DEBUG must be false when APP_ENV=production")
        if self.secret_key == "change-me-in-production":
            raise ValueError("SECRET_KEY must be changed when APP_ENV=production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=resolve_env_file())


settings = get_settings()
