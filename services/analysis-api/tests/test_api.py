"""Phase 1 tests — API surface, error envelope, readiness, and observable concerns."""
import pytest
from fastapi.testclient import TestClient

from app import api
from app.errors import sanitize_error


@pytest.fixture
def client():
    return TestClient(api.app)


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "request_id" in body


def test_ready_ok(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["ready"] is True


def test_models_never_leak_keys(client):
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    body = r.json()
    for role, cfg in body["roles"].items():
        assert "model" in cfg
        assert "fallback" in cfg
    serialized = r.text
    assert "sk-" not in serialized.lower() and "openrouter" not in serialized.lower()


def test_invalid_asset_class_returns_400_envelope(client):
    r = client.post("/api/v1/analyze", json={"asset": "EUR/USD", "asset_class": "stocks"})
    assert r.status_code == 400
    body = r.json()
    assert body["error"]["code"] == "invalid_asset_class"
    assert "request_id" in body


def test_analyze_missing_asset_returns_422(client):
    r = client.post("/api/v1/analyze", json={"asset_class": "forex"})
    assert r.status_code == 422


def test_market_data_too_large(client):
    big = "x" * 20_000
    r = client.post("/api/v1/analyze", json={"asset": "EUR/USD", "market_data": big})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "market_data_too_large"


def test_security_headers_present(client):
    r = client.get("/health")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert r.headers.get("Content-Security-Policy")
    assert r.headers.get("X-Request-ID")


def test_sanitize_error_hides_internals():
    msg = sanitize_error(RuntimeError("connection closed to db at internal-host:5432"))
    assert "internal-host" not in msg
    assert "connection closed" not in msg


def test_request_id_header_echoed(client):
    r = client.get("/health", headers={"X-Request-ID": "test-rid-123"})
    assert r.headers.get("X-Request-ID") == "test-rid-123"