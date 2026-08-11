"""Pydantic request/response schemas for core-api."""
from __future__ import annotations

import datetime as dt
from typing import Any

from pydantic import BaseModel, Field, field_validator


# --- Auth ---
class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=255)
    telegram_id: str | None = None

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    telegram_id: str | None = None

    model_config = {"from_attributes": True}


# --- Journal ---
class JournalCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=64)
    direction: str = Field(pattern="^(long|short|flat)$")
    entry_price: float | None = None
    exit_price: float | None = None
    size: float | None = None
    pnl: float | None = None
    notes: str = ""


class JournalUpdate(BaseModel):
    symbol: str | None = None
    direction: str | None = Field(default=None, pattern="^(long|short|flat)$")
    entry_price: float | None = None
    exit_price: float | None = None
    size: float | None = None
    pnl: float | None = None
    notes: str | None = None


class JournalOut(BaseModel):
    id: int
    symbol: str
    direction: str
    entry_price: float | None = None
    exit_price: float | None = None
    size: float | None = None
    pnl: float | None = None
    notes: str = ""
    created_at: dt.datetime

    model_config = {"from_attributes": True}


# --- Watchlist ---
class WatchlistCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=64)
    interval: str = "4h"


class WatchlistOut(BaseModel):
    id: int
    symbol: str
    interval: str

    model_config = {"from_attributes": True}


# --- Chart layout (persisted server-side: Phase 5) ---
class LayoutCreate(BaseModel):
    symbol: str
    range: dict[str, Any] | None = None
    indicators: list[dict[str, Any]] = []
    drawings: list[dict[str, Any]] = []


class LayoutOut(BaseModel):
    id: int
    symbol: str
    range: dict[str, Any] | None = None
    indicators: list[dict[str, Any]] = []
    drawings: list[dict[str, Any]] = []
    updated_at: dt.datetime

    model_config = {"from_attributes": True}


# --- Alerts ---
class AlertCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=64)
    condition: str = Field(pattern="^(>|<|==)$")
    price: float
    message: str = ""


class AlertOut(BaseModel):
    id: int
    symbol: str
    condition: str
    price: float
    message: str
    active: bool
    triggered_at: dt.datetime | None = None

    model_config = {"from_attributes": True}


# --- Audit ---
class AuditOut(BaseModel):
    id: int
    actor_id: int
    action: str
    resource_type: str
    resource_id: str | None = None
    detail: dict[str, Any] | None = None
    created_at: dt.datetime

    model_config = {"from_attributes": True}
