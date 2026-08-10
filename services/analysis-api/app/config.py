"""Application configuration — loaded from environment (no hardcoded secrets).

Phase 1: config moves toward a GapGPT OpenAI-compatible gateway. Role-to-model
assignments are intended to be supplied from a secret/vault (Infisical) in
production; whatever is not provided falls back to the defaults below.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "analysis-api"
    app_version: str = "0.1.0"
    app_env: str = "development"  # development | test | staging | production
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # --- LLM gateway ---
    # Default: OpenRouter. Swap LLM_BASE_URL to a GapGPT-compatible gateway.
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_default_key: str = ""  # single gateway key; else per-role keys below
    llm_api_key_code: str = ""
    llm_api_key_eval: str = ""
    llm_request_timeout_s: float = 120.0  # hard per-call timeout
    llm_total_budget_usd: float = 0.0  # 0 = no budget cap

    # --- Observable dependency endpoints (readiness) ---
    redis_url: str = ""  # optional; empty disables dependency probe
    redis_timeout_s: float = 1.5

    # --- Request security ---
    allowed_origins: str = "http://localhost:3000"  # comma-separated
    rate_limit_per_minute: int = 60

    # --- Analysis limits ---
    max_market_data_chars: int = 16_000
    max_assets_per_request: int = 1

    # --- OpenTelemetry ---
    otel_endpoint: str = ""  # e.g. http://otel-collector:4317 ; empty = disabled
    otel_service_name: str = "analysis-api"

    # --- LangFuse (optional tracing backend) ---
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""
    langfuse_base_url: str = "https://us.cloud.langfuse.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def is_production() -> bool:
    return get_settings().app_env in ("staging", "production")


# Convenience: parsed allowed-origin list
def allowed_origin_list() -> list[str]:
    s = get_settings().allowed_origins
    return [o.strip() for o in s.split(",") if o.strip()]


# Locate the analysis-api package root (for path-safe imports in scripts/tests)
def package_root() -> Path:
    return Path(__file__).resolve().parent.parent
