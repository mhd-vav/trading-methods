"""ASGI-style middleware: request-ID, access log, security headers, rate limit.

Kept dependency-light (pure Starlette) so the service boots without extra
packages. An in-process token-bucket rate limiter guards the analyze endpoint;
swap for Redis for multi-instance rate limiting in production.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config import allowed_origin_list, get_settings
from app.observability import (
    get_request_id,
    log_request,
    new_request_id,
    set_request_id,
)

_HEADER_CONTENT_SECURITY = (
    "default-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Assign/propagate request_id and log each request as JSON."""

    def __init__(self, app, dispatch_fn: Callable | None = None, **_kw):
        super().__init__(app)
        self._access_logger = None

    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or new_request_id()
        set_request_id(rid)
        start = time.time()
        try:
            response = await call_next(request)
        except Exception:
            # let the exception handler (errors.py) take over, but still log
            latency = int((time.time() - start) * 1000)
            log_request(request.method, request.url.path, 500, latency, rid)
            raise
        latency = int((time.time() - start) * 1000)
        log_request(request.method, request.url.path, response.status_code, latency, rid)
        response.headers["X-Request-ID"] = rid
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Strict security headers. No raw HTML from this API, so CSP frame/policy is restrictive."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        response.headers["Content-Security-Policy"] = _HEADER_CONTENT_SECURITY
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response


class _TokenBucket:
    def __init__(self, capacity: int, refill_per_sec: float):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_per_sec = refill_per_sec
        self.updated = time.time()

    def take(self) -> bool:
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.refill_per_sec)
        self.updated = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple per-client token bucket. Configure via RATE_LIMIT_PER_MINUTE."""

    def __init__(self, app, **kw):
        super().__init__(app)
        settings = get_settings()
        rpm = max(1, settings.rate_limit_per_minute)
        self._bucket = _TokenBucket(capacity=rpm, refill_per_sec=rpm / 60.0)
        self._protected_paths = {kw.get("protect", "/api/")}

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(p) for p in self._protected_paths) and not self._bucket.take():
            from starlette.responses import JSONResponse

            rid = get_request_id()
            return JSONResponse(
                status_code=429,
                content={
                    "error": {"code": "rate_limited", "message": "Too many requests. Please slow down."},
                    "request_id": rid,
                },
                headers={"Retry-After": "60"},
            )
        return await call_next(request)


class CORSWithOriginValidation(BaseHTTPMiddleware):
    """Allow-list CORS + origin validation for non-safe methods."""

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        allowed = allowed_origin_list()
        # Reject cross-origin state-changing requests not from an allowed origin
        if request.method in ("POST", "PUT", "PATCH", "DELETE") and origin and origin not in allowed:
            from starlette.responses import JSONResponse

            return JSONResponse(
                status_code=403,
                content={
                    "error": {
                        "code": "origin_not_allowed",
                        "message": "This origin is not allowed to perform the request.",
                    },
                    "request_id": get_request_id(),
                },
            )
        response = await call_next(request)
        if origin and origin in allowed:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"
        response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        response.headers.setdefault(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, X-Request-ID"
        )
        return response
