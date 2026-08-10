"""Model registry — role-to-model assignment and the LLM factory.

Phase 1 hardening:
- Reads the gateway base URL + keys from config (env), not literals.
- Applies a hard per-call timeout on every provider call.
- Supports fallback models per role.
- Enforces an optional total per-run cost budget via usage accounting (see engine).
- Role-to-model assignments are environment-driven; a secrets/vault (Infisical)
  can override them — nothing is baked into source.
"""

from __future__ import annotations

import os
from typing import Any

from langchain_openai import ChatOpenAI
from pydantic_settings import BaseSettings

from app.config import get_settings

# Default role -> {model, fallback}. Environment overrides win:
#   LLM_MODEL_<ROLE_UC>  and  LLM_FALLBACK_<ROLE_UC>
_DEFAULT_MODELS: dict[str, dict[str, str]] = {
    "orchestrator": {"model": "moonshotai/kimi-k2", "fallback": "z-ai/glm-5.2"},
    "technical_deep": {"model": "openai/gpt-4o", "fallback": "z-ai/glm-5.2"},
    "technical_quick": {"model": "openai/gpt-4o-mini", "fallback": "z-ai/glm-5.2"},
    "orderflow_deep": {"model": "deepseek/deepseek-chat", "fallback": "z-ai/glm-5.2"},
    "macro_deep": {"model": "moonshotai/kimi-k2", "fallback": "z-ai/glm-5.2"},
    "sentiment_quick": {"model": "google/gemini-2.5-flash", "fallback": "z-ai/glm-5.2"},
    "onchain_deep": {"model": "deepseek/deepseek-chat", "fallback": "z-ai/glm-5.2"},
    "quant_deep": {"model": "deepseek/deepseek-r1", "fallback": "z-ai/glm-5.2"},
    "quant_quick": {"model": "openai/gpt-4o-mini", "fallback": "z-ai/glm-5.2"},
    "risk_review": {"model": "moonshotai/kimi-k2", "fallback": "z-ai/glm-5.2"},
    "eval": {"model": "openai/gpt-4o-mini", "fallback": "z-ai/glm-5.2"},
}


class RoleModelConfig(BaseSettings):
    """Per-role overrides injected from environment (LLM_MODEL_<ROLE>, LLM_FALLBACK_<ROLE>)."""

    model_config_settings: dict[str, str] = {}

    class Config:
        env_prefix = ""
        extra = "ignore"


def _env_overrides() -> dict[str, dict[str, str]]:
    """Read LLM_MODEL_<ROLE> and LLM_FALLBACK_<ROLE> from the environment."""
    overrides: dict[str, dict[str, str]] = {}
    for role in _DEFAULT_MODELS:
        key = "LLM_MODEL_" + role.upper()
        fbk = "LLM_FALLBACK_" + role.upper()
        model = os.getenv(key)
        fb = os.getenv(fbk)
        if model or fb:
            overrides[role] = {
                "model": model or _DEFAULT_MODELS[role]["model"],
                "fallback": fb or _DEFAULT_MODELS[role]["fallback"],
            }
    return overrides


def get_all_role_configs() -> dict[str, dict[str, str]]:
    cfg: dict[str, dict[str, str]] = {}
    for role, base in _DEFAULT_MODELS.items():
        cfg[role] = base.copy()
    for role, delta in _env_overrides().items():
        cfg[role].update(delta)
    return cfg


def _key_for(role: str) -> str:
    """Key selection: a single gateway key, else a role-specific key, else default command key."""
    settings = get_settings()
    if settings.llm_default_key:
        return settings.llm_default_key
    if role == "eval":
        return settings.llm_api_key_eval or settings.llm_api_key_code
    return settings.llm_api_key_code


def _build_chat(model: str, api_key: str, temperature: float) -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=model,
        openai_api_base=settings.llm_base_url,
        openai_api_key=api_key,
        temperature=temperature,
        request_timeout=settings.llm_request_timeout_s,  # hard per-call timeout
        max_retries=1,  # explicit, no silent infinite retry
    )


def get_llm(role: str, temperature: float = 0.3) -> ChatOpenAI:
    role = role if role in _DEFAULT_MODELS else "technical_quick"
    cfg = get_all_role_configs()[role]
    return _build_chat(cfg["model"], _key_for(role), temperature)


def get_fallback_llm(role: str, temperature: float = 0.3) -> ChatOpenAI:
    role = role if role in _DEFAULT_MODELS else "technical_quick"
    cfg = get_all_role_configs()[role]
    return _build_chat(cfg["fallback"] or cfg["model"], _key_for(role), temperature)


# Exposed for tests / compatibility
MODEL_ASSIGNMENTS: dict[str, dict[str, Any]] = get_all_role_configs()
