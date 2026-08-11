"""Prompt registry — versioned, auditable prompts for each agent role.

Phase 4: prompts are versioned and stored in a registry so runs are reproducible
and prompt changes can be diffed/rolled back. The engine references prompt
versions (e.g. "v1") rather than embedding prompt text in code paths.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# The actual prompt templates live in the bundles. This registry maps a logical
# prompt key + version to a deterministic content hash and the concrete template.
# A production implementation reads these from Infisical/DB; here we keep the
# registry in code but versioned and changelog-tracked.

# Registry entry: {role: {version: {text, hash}}}
_PROMPT_VERSIONS: dict[str, dict[str, dict[str, str]]] = {}


class PromptRegistry(ABC):
    @abstractmethod
    def resolve(self, role: str, version: str = "v1") -> str:
        """Return the concrete prompt template for role+version."""

    @abstractmethod
    def register(self, role: str, version: str, text: str) -> None: ...


class InMemoryPromptRegistry(PromptRegistry):
    """Default registry. In production, back this with Infisical or the DB."""

    def resolve(self, role: str, version: str = "v1") -> str:
        entry = _PROMPT_VERSIONS.get(role, {}).get(version)
        if not entry:
            raise KeyError(f"prompt {role}@{version} not registered")
        return entry["text"]

    def register(self, role: str, version: str, text: str) -> None:
        import hashlib

        h = hashlib.sha256(text.encode()).hexdigest()[:12]
        _PROMPT_VERSIONS.setdefault(role, {})[version] = {"text": text, "hash": h}

    def versions(self, role: str) -> dict[str, str]:
        return {v: e["hash"] for v, e in _PROMPT_VERSIONS.get(role, {}).items()}


_default_registry = InMemoryPromptRegistry()


def get_prompt_registry() -> InMemoryPromptRegistry:
    return _default_registry


def prompt_version_for(role: str, version: str = "v1") -> str:
    """Resolve a prompt and return a version stamp for provenance."""
    try:
        _default_registry.resolve(role, version)
    except KeyError:
        version = "v1"  # fallback
    return version


# ---------------------------------------------------------------------------
# Idempotency + checkpoint store
# ---------------------------------------------------------------------------
class StoreBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> bytes | None: ...

    @abstractmethod
    def set(self, key: str, value: bytes, ttl_seconds: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...


class MemoryStoreBackend(StoreBackend):
    """Thread-safe in-process store (tests/local single-instance)."""

    def __init__(self) -> None:
        self._d: dict[str, bytes] = {}

    def get(self, key: str) -> bytes | None:
        return self._d.get(key)

    def set(self, key: str, value: bytes, ttl_seconds: int | None = None) -> None:
        self._d[key] = value

    def delete(self, key: str) -> None:
        self._d.pop(key, None)
