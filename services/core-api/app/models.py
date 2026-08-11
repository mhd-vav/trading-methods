"""core-api database models.

Object-level authorization is fundamental: every mutable record carries an
owner (user) id, and every query scopes by it. No cross-user access is possible
at the data layer regardless of UI exposure.
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _now():
    return dt.datetime.now(dt.UTC)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    telegram_id = Column(String(64), unique=True, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=_now)
    is_active = Column(Boolean, default=True)

    journals = relationship("JournalEntry", back_populates="owner")
    watchlists = relationship("WatchlistEntry", back_populates="owner")
    layouts = relationship("ChartLayout", back_populates="owner")
    alerts = relationship("Alert", back_populates="owner")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(64), nullable=False)
    direction = Column(String(16), nullable=False)  # long | short | flat
    entry_price = Column(Float)
    exit_price = Column(Float)
    size = Column(Float)
    pnl = Column(Float)
    notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)

    owner = relationship("User", back_populates="journals")


class WatchlistEntry(Base):
    __tablename__ = "watchlist_entries"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(64), nullable=False)
    interval = Column(String(8), default="4h")
    created_at = Column(DateTime(timezone=True), default=_now)

    owner = relationship("User", back_populates="watchlists")


class ChartLayout(Base):
    __tablename__ = "chart_layouts"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(64), nullable=False)
    range = Column(JSON, nullable=True)  # {startIndex, endIndex}
    indicators = Column(JSON, default=list)
    drawings = Column(JSON, default=list)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)

    owner = relationship("User", back_populates="layouts")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(64), nullable=False)
    condition = Column(String(32), nullable=False)  # > | < | ==
    price = Column(Float, nullable=False)
    message = Column(String(255), default="")
    active = Column(Boolean, default=True)
    triggered_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now)

    owner = relationship("User", back_populates="alerts")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, nullable=False)  # who acted (user id)
    action = Column(String(64), nullable=False)  # e.g. journal.create
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(64), nullable=True)
    detail = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now)
