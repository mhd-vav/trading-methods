"""Database session + config for core-api."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Settings(BaseSettings):
    app_name: str = "core-api"
    app_version: str = "0.1.0"
    app_env: str = "development"
    database_url: str = "sqlite:///./core-api.db"
    jwt_secret: str = "change-me-in-production"  # REQUIRED via env in prod
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 60
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        url = get_settings().database_url
        connect_args = {}
        poolclass = None
        if url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
            if url == "sqlite:///:memory:":
                from sqlalchemy.pool import StaticPool
                poolclass = StaticPool
        kwargs = {"connect_args": connect_args}
        if poolclass:
            kwargs["poolclass"] = poolclass
        _engine = create_engine(url, **kwargs)
    return _engine


def SessionLocal():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), expire_on_commit=False, class_=Session)
    return _SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app import models  # noqa: F401
    Base = models.Base
    Base.metadata.create_all(bind=get_engine())
