"""Audit logging — record every mutation (Phase 5 requirement)."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app import models


def audit(
    db: Session,
    actor_id: int,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    detail: dict[str, Any] | None = None,
) -> models.AuditLog:
    entry = models.AuditLog(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        detail=detail,
    )
    db.add(entry)
    return entry
