"""FastAPI endpoint for the Multi-Agent Trading Desks (analysis-api).

Phase 1:
- /health (liveness) and /ready (readiness incl. optional dependency probe)
- request IDs on every response and log line
- sanitized error envelope (no raw exceptions leaked to clients)
- required-field / enum validation with 4xx responses
- the engine's run is registered with a run_id for traceability
"""

from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from app.config import get_settings
from app.errors import ApiError, api_error_response, sanitize_error
from app.middleware import (
    CORSWithOriginValidation,
    RateLimitMiddleware,
    RequestContextMiddleware,
    SecurityHeadersMiddleware,
)
from app.observability import configure_logging, get_logger, get_request_id, init_tracing

configure_logging()
log = get_logger("app.api")

app = FastAPI(
    title="analysis-api — Multi-Agent Trading Desks",
    description="Explainable multi-agent deliberation for Forex and Crypto — educational analysis only.",
    version=get_settings().app_version,
    docs_url="/docs" if get_settings().app_env != "production" else None,
    redoc_url="/redoc" if get_settings().app_env != "production" else None,
)

# Middleware order matters: outermost runs first.
app.add_middleware(RequestContextMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, protect="/api/")
app.add_middleware(CORSWithOriginValidation)

init_tracing()

# --- Schemas -----------------------------------------------------------------


class AnalysisRequest(BaseModel):
    asset: str = Field(min_length=1, max_length=64)
    asset_class: str = "forex"
    timeframe: str = "4h"
    market_data: str = ""
    include_onchain: bool | None = None


# --- Dependency probes --------------------------------------------------------


def _redis_available() -> bool:
    """Optional readiness probe. Returns True when no Redis is configured."""
    settings = get_settings()
    if not settings.redis_url:
        return True
    try:
        import redis

        r = redis.from_url(settings.redis_url, socket_timeout=settings.redis_timeout_s)
        return r.ping()
    except Exception:
        return False


@app.get("/health")
async def health(_: Request = None):
    return {
        "status": "ok",
        "service": get_settings().app_name,
        "version": get_settings().app_version,
        "request_id": get_request_id(),
    }


@app.get("/ready")
async def ready(_: Request = None):
    """Readiness: true when the service can accept analysis work."""
    deps = {"redis": "ok" if _redis_available() else "unavailable"}
    healthy = all(v == "ok" for v in deps.values())
    return {
        "status": "ready" if healthy else "degraded",
        "ready": healthy,
        "dependencies": deps,
        "request_id": get_request_id(),
    }


# --- Handlers ------------------------------------------------------------------


@app.post("/api/v1/analyze")
async def analyze(req: AnalysisRequest, request: Request = None):
    """Run full MAS analysis for an asset. Educational analysis only."""
    run_id = uuid.uuid4().hex

    if req.asset_class not in ("forex", "crypto"):
        raise ApiError(400, "invalid_asset_class", "asset_class must be forex or crypto")

    settings = get_settings()
    if len(req.market_data) > settings.max_market_data_chars:
        raise ApiError(
            400, "market_data_too_large", f"market_data exceeds {settings.max_market_data_chars} characters"
        )

    from app.engine import run_analysis

    started = time.time()
    try:
        result = run_analysis(
            asset=req.asset,
            asset_class=req.asset_class,
            timeframe=req.timeframe,
            market_data=req.market_data or "No market data provided - analyze based on general knowledge.",
            include_onchain=req.include_onchain,
        )
    except ApiError as e:
        raise e
    except Exception as e:
        # Log the full detail server-side; reply with a sanitized envelope only.
        log.error("analyze_failed", run_id=run_id, error=str(e)[:2000])
        raise ApiError(500, "analysis_failed", sanitize_error(e)) from None

    latency_ms = int((time.time() - started) * 1000)
    result.setdefault("request_meta", {})
    result["request_meta"]["run_id"] = run_id
    result["request_meta"]["latency_ms"] = latency_ms
    return result


@app.get("/api/v1/models")
async def list_models(_: Request = None):
    """List effective role->model assignments (no keys are ever returned)."""
    from app.models import get_all_role_configs

    cfg = get_all_role_configs()
    return {
        "roles": {role: {"model": c["model"], "fallback": c.get("fallback")} for role, c in cfg.items()},
        "disclaimer": "Educational analysis only. Not financial advice.",
    }


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError):
    log.info("api_error", code=exc.code, status=exc.status_code)
    return api_error_response(exc.status_code, exc.code, exc.message, get_request_id())


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    # Never leak internals. Log full detail here.
    log.error("unhandled_exception", error=str(exc)[:2000], type=exc.__class__.__name__)
    rid = get_request_id()
    return api_error_response(500, "internal_error", sanitize_error(exc), rid)
