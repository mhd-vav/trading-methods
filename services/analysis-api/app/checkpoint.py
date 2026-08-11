"""Idempotency and run-checkpointing for the analysis engine (Phase 4).

- Idempotency: a client-supplied idempotency key lets a retried request return
  the same stored result without re-running the expensive LLM pipeline.
- Checkpointing: durable progress for long runs so they can be resumed and
  streamed. The store backend is pluggable (Memory for tests/local, Redis/Postgres
  in production).
"""

from __future__ import annotations

import json
import time
from typing import Any

from app.prompts import MemoryStoreBackend, StoreBackend


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------
class IdempotencyStore:
    def __init__(self, backend: StoreBackend | None = None, ttl_seconds: int = 3600) -> None:
        self.backend = backend or MemoryStoreBackend()
        self.ttl_seconds = ttl_seconds

    def _key(self, idem_key: str) -> str:
        return f"idem:{idem_key}"

    def get(self, idem_key: str) -> dict[str, Any] | None:
        raw = self.backend.get(self._key(idem_key))
        if not raw:
            return None
        try:
            return json.loads(raw.decode())
        except Exception:
            return None

    def put(self, idem_key: str, result: dict[str, Any]) -> None:
        payload = json.dumps(result, default=str).encode()
        self.backend.set(self._key(idem_key), payload, self.ttl_seconds)

    def try_resume(self, idem_key: str) -> dict[str, Any] | None:
        """Return a stored completed result for an idempotency key, if any."""
        return self.get(idem_key)


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------
class CheckpointStore:
    """Durable progress store keyed by run/thread id."""

    def __init__(self, backend: StoreBackend | None = None) -> None:
        self.backend = backend or MemoryStoreBackend()

    def _key(self, run_id: str, stage: str) -> str:
        return f"run:{run_id}:{stage}"

    def checkpoint(self, run_id: str, stage: str, data: dict[str, Any]) -> None:
        payload = json.dumps({"ts": time.time(), **data}, default=str).encode()
        self.backend.set(self._key(run_id, stage), payload)

    def read(self, run_id: str, stage: str) -> dict[str, Any] | None:
        raw = self.backend.get(self._key(run_id, stage))
        if not raw:
            return None
        try:
            return json.loads(raw.decode())
        except Exception:
            return None

    def list_checkpointed_stages(self, run_id: str) -> list[str]:
        # Memory backend stores stages independently; return known ones.
        # In Redis/Postgres this would scan keys/rows for the run.
        return []


class RunProgressTracker:
    """Stores per-stage status so progress can be streamed to the frontend."""

    def __init__(self, run_id: str, store: CheckpointStore | None = None) -> None:
        self.run_id = run_id
        self.store = store or CheckpointStore()
        self.statuses: dict[str, str] = {}

    def mark(self, stage: str, status: str, detail: Any = None) -> None:
        self.statuses[stage] = status
        self.store.checkpoint(
            self.run_id, "progress", {"statuses": self.statuses, "stage": stage, "detail": detail}
        )

    def snapshot(self) -> dict[str, Any]:
        return {"run_id": self.run_id, "statuses": self.statuses}


# Keep a single shared idempotency store for the app process.
_idem_store: IdempotencyStore | None = None


def get_idempotency_store() -> IdempotencyStore:
    global _idem_store
    if _idem_store is None:
        _idem_store = IdempotencyStore()
    return _idem_store
