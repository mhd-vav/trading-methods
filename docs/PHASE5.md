# Phase 5 — Core Persistence

Status: **implemented & tested**.

## Goal

Server-side persistence for users, auth, trading journals, watchlists, chart
layouts, alerts, and audit logs. Every mutable record is scoped to its owner;
cross-user access is impossible at the data layer.

## What was built

### `services/core-api/`

A FastAPI service with SQLAlchemy models and JWT auth:

| Resource     | Endpoints                                         | Owner-scoped |
|--------------|---------------------------------------------------|--------------|
| Auth         | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` | —       |
| Health       | `GET /health`                                     | —            |
| Journal      | `POST /journal`, `GET /journal`, `GET /journal/{id}`, `PATCH /journal/{id}`, `DELETE /journal/{id}` | yes |
| Watchlist    | `POST /watchlist`, `GET /watchlist`, `DELETE /watchlist/{id}` | yes    |
| Layouts      | `POST /layouts`, `GET /layouts/{symbol:path}`     | yes          |
| Alerts       | `POST /alerts`, `GET /alerts`, `DELETE /alerts/{id}` | yes       |
| Audit        | `GET /audit`                                      | yes (own logs) |

### Key design decisions

- **Object-level authorization**: every query filters by `owner_id == user.id`.
  A user cannot read, update, or delete another user's records — the query
  returns 404 before any mutation.
- **bcrypt password hashing** via the `bcrypt` library directly (not passlib,
  which has a version-incompatibility with bcrypt 4.x).
- **JWT tokens** via PyJWT (`HS256`), with configurable TTL.
- **Audit trail**: every mutating action writes an `AuditLog` row with the
  actor, action name, resource type/id, and optional detail JSON.
- **In-memory SQLite tests**: `StaticPool` ensures the shared in-memory engine
  is used consistently across the test client and the app's `get_db` dependency.
- **Path symbols**: chart layouts use `{symbol:path}` so trading pairs with
  slashes (e.g. `BTC/USDT`) work as URL parameters.
- **Pydantic v2**: `SettingsConfigDict` (not legacy `class Config`) for
  `BaseSettings`, `model_config = {"from_attributes": True}` on response models.

### Dependencies

```
fastapi, uvicorn, sqlalchemy, psycopg[binary], pydantic, pydantic-settings,
python-dotenv, bcrypt, PyJWT, itsdangerous
test: pytest, httpx, ruff
```

## Test results

```
tests/test_api.py — 8 passed
ruff check app/ tests/ — All checks passed
```

Tests cover:
1. `test_register_and_me` — register + token + `/auth/me`
2. `test_login_wrong_password_rejected` — 401 on bad password
3. `test_journal_crud` — full create/read/update/delete cycle
4. `test_two_users_cannot_access_each_others_journal` — cross-user 404s
5. `test_watchlist_and_layout_isolation` — watchlist + layout isolation
6. `test_alerts_isolated` — alert cross-user 404
7. `test_audit_log_recorded` — `journal.create` appears in audit trail
8. `test_unauthenticated_rejected` — 401 without a token

## Deployment artifacts

- `services/core-api/Dockerfile` — multi-stage (test + runtime)
- `infra/compose/core-api.yml` — deployment definition (not deployed in this phase)
- `services/core-api/.env.example` — env vars reference

## What's NOT here (intentional)

- No server deployment (constraint: implement, don't deploy)
- No Infisical integration yet (secrets are env vars for now)
- No rate limiting on auth endpoints (planned for Phase 6)
- No admin-scoped audit log access (currently returns the actor's own logs)
