# Trading Desk — Runbook & Acceptance Checklist (Phase 7)

## Prerequisites

- Docker 24+ and Docker Compose v2
- Node.js 20+ (for local TS development)
- Python 3.12+ (for local Python development)
- 4 GB RAM minimum for full stack

## Quick start (local dev)

```bash
# 1. Clone and enter
git clone <repo-url> trading-desk
cd trading-desk
git checkout feat/phase0-phase1-foundation

# 2. Copy env
cp services/core-api/.env.example services/core-api/.env
# Edit .env: set JWT_SECRET to a strong random value

# 3. Start data layer
docker compose up -d postgres redis

# 4. Start APIs
docker compose up -d core-api analysis-api

# 5. Start web + edge
docker compose up -d web nginx

# 6. Start worker (optional)
docker compose up -d market-ingestion

# 7. Start observability (optional)
docker compose up -d otel-collector
```

## Health checks

```bash
# Core API
curl http://localhost:8001/health
# Expected: {"status":"ok","service":"core-api","version":"0.1.0"}

# Analysis API
curl http://localhost:8000/health
# Expected: {"status":"ok",...}

# Via nginx edge
curl http://localhost:8080/health
# Expected: {"status":"ok","service":"core-api","version":"0.1.0"}

# PostgreSQL
docker compose exec postgres pg_isready -U td -d tradingdesk
# Expected: /var/run/postgresql:5432 - accepting connections

# Redis
docker compose exec redis redis-cli ping
# Expected: PONG
```

## Test suite

### Unit tests (no services needed)

```bash
# TypeScript packages
npm test                           # all workspaces
npm run test --workspace @trading-desk/chart-core
npm run test --workspace @trading-desk/provider-adapters
npm run test --workspace @trading-desk/web

# Python services
cd services/analysis-api
. .venv/bin/activate
pytest -q tests/
ruff check app/

cd services/core-api
. .venv/bin/activate
pytest -q tests/
ruff check app/ tests/
```

### Integration tests (requires running stack)

```bash
# Start the stack first
docker compose up -d postgres redis core-api analysis-api

# Run integration tests
cd tests/integration
npx vitest run
```

### E2E tests (requires full stack + nginx)

```bash
# Start the full stack
docker compose up -d

# Run E2E tests
cd tests/e2e
npx vitest run
```

### Contract tests (no services needed)

```bash
cd tests/contracts
npx vitest run
```

## Acceptance checklist

### Phase 2 — Charting
- [x] `packages/contracts` defines Candle, Indicator, Drawing, ChartLayout schemas
- [x] `packages/chart-core` has pure SMA/EMA/RSI/MACD/ATR/Bollinger + transforms
- [x] 25 unit tests passing
- [x] ECharts adapter behind interface (no direct ECharts imports outside adapter)
- [x] 6 web chart component tests passing

### Phase 3 — Market-data platform
- [x] `packages/provider-adapters` with resilience (timeout/retry/circuit-breaker/coalescing)
- [x] CoinGecko + Forex adapters
- [x] `ResilientMarketClient` with cache → coalesce → fallback → degradation
- [x] `auditSeries` quality checks (gaps/dupes/OHLC/drift/freshness)
- [x] 27 unit tests passing
- [x] `workers/market-ingestion` scheduler scaffold

### Phase 4 — Production engine
- [x] `EvidenceSnapshot` (immutable, content-addressed)
- [x] Prompt registry
- [x] Idempotency + checkpointing stores
- [x] Typed Pydantic `AgentOutput` validation
- [x] Provenance in every result
- [x] 49 analysis-api tests passing

### Phase 5 — Core persistence
- [x] `services/core-api` with SQLAlchemy models (User/Journal/Watchlist/ChartLayout/Alert/AuditLog)
- [x] JWT auth (bcrypt + PyJWT)
- [x] Every query scoped by `owner_id`
- [x] Audit logging on all mutations
- [x] 8 core-api tests passing
- [x] ruff clean
- [x] Dockerfile (multi-stage: test + runtime)
- [x] `.env.example`
- [x] `docs/PHASE5.md`

### Phase 6 — Infrastructure
- [x] `docker-compose.yml` with all services
- [x] Per-service compose files (`infra/compose/`)
- [x] Nginx reverse proxy with rate limiting + security headers
- [x] PostgreSQL init script with extensions + indexes
- [x] OTel collector config
- [x] Dockerfiles for web, market-ingestion
- [x] Network segmentation (trading-app / trading-data)
- [x] `docs/PHASE6.md`

### Phase 7 — Integration & acceptance
- [x] Integration test scaffolds (`tests/integration/`)
- [x] Contract test scaffolds (`tests/contracts/`)
- [x] E2E test scaffolds (`tests/e2e/`)
- [x] Evaluation test scaffolds (`tests/evaluation/`)
- [x] Runbook (this document)
- [x] Acceptance checklist (this document)

## Troubleshooting

### "no such table: users"
The database hasn't been initialized. `init_db()` runs on import, but if
using PostgreSQL ensure the server is up first:
```bash
docker compose up -d postgres
docker compose up -d core-api
```

### "Connection refused" on analysis-api
Redis must be healthy first:
```bash
docker compose up -d redis
docker compose restart analysis-api
```

### "bcrypt version error"
If passlib is accidentally reinstalled, it conflicts with bcrypt 4.x.
The project uses `bcrypt` directly (not passlib). Ensure requirements.txt
has `bcrypt==4.3.0` and not `passlib[bcrypt]`.

### Nginx 502 Bad Gateway
Check that the upstream services are running:
```bash
docker compose ps
docker compose logs core-api --tail 20
docker compose logs analysis-api --tail 20
```

## Security notes

- JWT secret MUST be changed from the default in production
- PostgreSQL password MUST be changed from the default in production
- Use Infisical or a secrets manager for all API keys
- Nginx rate limits are per-IP; consider a WAF for production
- All ports bind to 127.0.0.1 (localhost only) by default
