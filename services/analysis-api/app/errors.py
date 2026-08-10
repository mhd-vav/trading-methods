"""HTTP error contract — never leak internal details to clients.

Phase 1: the API returns stable, sanitized error envelopes and logs the raw
exception server-side only.
"""

from __future__ import annotations

from fastapi.responses import JSONResponse


class ApiError(Exception):
    """Carry an HTTP status + a code + a sanitized (already-safe) message."""

    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


def api_error_response(status_code: int, code: str, message: str, request_id: str = "") -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
            },
            "request_id": request_id,
        },
    )


def sanitize_error(exc: BaseException) -> str:
    """Return a stable client-safe description for an unexpected exception."""
    return f"Internal error processing the request (type={exc.__class__.__name__})."
