"""Structured JSON logging, request-ID propagation, and OpenTelemetry.

Phase 1: every log line is JSON, correlation via request_id, spans when an OTel
collector endpoint is configured. All optional — if the OTel SDK is not installed
or no endpoint is set, tracing is a safe no-op that still records request IDs via
logging only.
"""

from __future__ import annotations

import contextvars
import json
import logging
import sys
import uuid
from typing import Any

from app.config import get_settings

# --- Request-ID propagation across async tasks/spans ---
_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


def set_request_id(rid: str) -> None:
    _request_id_var.set(rid)


def get_request_id() -> str:
    return _request_id_var.get()


def new_request_id() -> str:
    return uuid.uuid4().hex


class JsonLogFormatter(logging.Formatter):
    """Emit one JSON object per log record."""

    RESERVED = (
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "taskName",
    )

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        rid = get_request_id()
        if rid:
            payload["request_id"] = rid
        # Extra structured fields
        for key, value in record.__dict__.items():
            if key not in self.RESERVED and not key.startswith("_"):
                payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


class RequestIdFilter(logging.Filter):
    """Attach the active request_id to every record going through our logger."""

    def filter(self, record: logging.LogRecord) -> bool:
        rid = get_request_id()
        if rid and not getattr(record, "request_id", None):
            record.request_id = rid
        return True


def configure_logging(log_level: str | None = None) -> None:
    settings = get_settings()
    level = (log_level or settings.log_level or "INFO").upper()
    root = logging.getLogger()
    root.setLevel(level)
    # Remove duplicate handlers from repeated calls (tests / reloads)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter())
    root.addHandler(handler)
    root.addFilter(RequestIdFilter())

    # Quiet noisy third-party loggers
    for noisy in ("uvicorn.access", "httpcore", "httpx"):
        logging.getLogger(noisy).setLevel(max(logging.WARNING, getattr(logging, level, logging.WARNING)))


class StructuredLogger(logging.LoggerAdapter):
    """Adapter that translates `logger.info("msg", key=value, ...)` into
    structured extra fields on the log record (used by JsonLogFormatter)."""

    def process(self, msg, kwargs):
        # Pull every free keyword out of kwargs into the record's extra dict.
        extra = dict(kwargs.pop("extra", {}))
        for k in list(kwargs.keys()):
            if k not in ("exc_info", "stack_info", "stacklevel"):
                extra[k] = kwargs.pop(k)
        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name: str) -> logging.LoggerAdapter:
    """Return a StructuredLogger so callers can pass structured kwargs."""
    return StructuredLogger(logging.getLogger(name), {})


# ---------------------------------------------------------------------------
# OpenTelemetry (optional)
# ---------------------------------------------------------------------------
_tracer = None


def init_tracing() -> None:
    """Configure OTel resource + tracer provider if an endpoint is configured."""
    global _tracer
    settings = get_settings()
    if not settings.otel_endpoint:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        resource = Resource.create({"service.name": settings.otel_service_name})
        provider = TracerProvider(resource=resource)
        exporter = OTLPSpanExporter(endpoint=settings.otel_endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer(settings.otel_service_name)
        get_logger("app.observability").info("otel_enabled", endpoint=settings.otel_endpoint)
    except Exception as e:  # pragma: no cover - optional dependency
        get_logger("app.observability").warning("otel_init_failed", error=str(e))
        _tracer = None


def start_span(name: str, context: dict | None = None):
    """Convenience wrapper. Returns a no-op tracer when tracing is disabled."""
    if _tracer is not None:
        span = _tracer.start_as_current_span(name)
        if context and hasattr(span, "__enter__"):
            pass
        return span
    return _NopSpan()


class _NopSpan:  # pragma: no cover - fallback
    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        return None

    def set_attribute(self, *a, **kw) -> None:
        return None

    def add_event(self, *a, **kw) -> None:
        return None


_log = get_logger("app.observability")


def log_degraded(dependency: str, error: str) -> None:
    _log.warning("dependency_degraded", dependency=dependency, error=str(error)[:300])


def log_request(method: str, path: str, status: int, latency_ms: int, rid: str) -> None:
    _log.info(
        "http_request",
        method=method,
        path=path,
        status=status,
        latency_ms=latency_ms,
        request_id=rid or get_request_id(),
    )
