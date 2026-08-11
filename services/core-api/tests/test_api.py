"""core-api tests — auth, object-level isolation, audit logging."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient

from app import api
from app.database import get_engine


@pytest.fixture()
def client():
    # Fresh in-memory DB per test
    from app import models as m
    m.Base.metadata.drop_all(bind=get_engine())
    m.Base.metadata.create_all(bind=get_engine())
    return TestClient(api.app)


def auth(client, email, password):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_register_and_me(client):
    h = auth(client, "a@example.com", "password123")
    me = client.get("/auth/me", headers=h).json()
    assert me["email"] == "a@example.com"


def test_login_wrong_password_rejected(client):
    auth(client, "a@example.com", "password123")
    r = client.post("/auth/login", json={"email": "a@example.com", "password": "wrongpass1"})
    assert r.status_code == 401


def test_journal_crud(client):
    h = auth(client, "a@example.com", "password123")
    r = client.post("/journal", headers=h, json={"symbol": "BTC/USDT", "direction": "long", "entry_price": 100})
    assert r.status_code == 200
    jid = r.json()["id"]
    got = client.get(f"/journal/{jid}", headers=h).json()
    assert got["symbol"] == "BTC/USDT"
    up = client.patch(f"/journal/{jid}", headers=h, json={"notes": "great trade"})
    assert up.json()["notes"] == "great trade"
    d = client.delete(f"/journal/{jid}", headers=h)
    assert d.status_code == 204
    assert client.get(f"/journal/{jid}", headers=h).status_code == 404


def test_two_users_cannot_access_each_others_journal(client):
    h1 = auth(client, "one@example.com", "password123")
    h2 = auth(client, "two@example.com", "password123")
    r = client.post("/journal", headers=h1, json={"symbol": "ETH/USDT", "direction": "long"})
    jid = r.json()["id"]
    # user2 should not read, update, or delete user1's entry
    assert client.get(f"/journal/{jid}", headers=h2).status_code == 404
    assert client.patch(f"/journal/{jid}", headers=h2, json={"notes": "steal"}).status_code == 404
    assert client.delete(f"/journal/{jid}", headers=h2).status_code == 404


def test_watchlist_and_layout_isolation(client):
    h1 = auth(client, "one@example.com", "password123")
    h2 = auth(client, "two@example.com", "password123")
    w = client.post("/watchlist", headers=h1, json={"symbol": "SOL/USDT"})
    wid = w.json()["id"]
    assert client.delete(f"/watchlist/{wid}", headers=h2).status_code == 404
    assert client.get("/watchlist", headers=h1).json()[0]["symbol"] == "SOL/USDT"
    assert client.get("/watchlist", headers=h2).json() == []

    client.post("/layouts", headers=h1, json={"symbol": "BTC/USDT", "drawings": [{"id": "d1"}]})
    assert client.get("/layouts/BTC/USDT", headers=h1).status_code == 200
    assert client.get("/layouts/BTC/USDT", headers=h2).status_code == 404


def test_alerts_isolated(client):
    h1 = auth(client, "one@example.com", "password123")
    h2 = auth(client, "two@example.com", "password123")
    a = client.post("/alerts", headers=h1, json={"symbol": "BTC", "condition": ">", "price": 50000})
    aid = a.json()["id"]
    assert client.delete(f"/alerts/{aid}", headers=h2).status_code == 404
    assert client.get("/alerts", headers=h1).json()[0]["price"] == 50000


def test_audit_log_recorded(client):
    h = auth(client, "a@example.com", "password123")
    client.post("/journal", headers=h, json={"symbol": "BTC", "direction": "long"})
    logs = client.get("/audit", headers=h).json()
    actions = [log["action"] for log in logs]
    assert "journal.create" in actions


def test_unauthenticated_rejected(client):
    assert client.get("/auth/me").status_code in (401, 403)
    assert client.get("/journal").status_code in (401, 403)
