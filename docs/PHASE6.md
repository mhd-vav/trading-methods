# Phase 6 — Infrastructure & Deployment

Status: **defined (not deployed)**.

## Goal

Define the full-stack deployment topology: data layer, edge, APIs, web, worker,
and observability — all as Docker Compose services. Committed so the contract
evolves with the code; no server is touched.

## Topology

```
                    ┌──────────┐
       :8080        │  nginx   │  (reverse proxy + rate limiting)
  User ───────────►│  edge    │
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ core-api  │ │analysis-api│ │   web    │
    │   :8001   │ │   :8000   │ │  :3000   │
    └─────┬─────┘ └─────┬─────┘ └──────────┘
          │              │
    ┌─────▼─────┐ ┌─────▼─────┐ ┌───────────┐
    │ postgres  │ │  redis    │ │ market-   │
    │   :5432   │ │  :6379    │ │ ingestion │
    └───────────┘ └───────────┘ └───────────┘
                         │              │
                    ┌────▼──────────────▼────┐
                    │  otel-collector        │
                    │  :4317 (OTLP gRPC)     │
                    └────────────────────────┘
```

## Artifacts

### `docker-compose.yml` (root)

The single entry point for local dev and production parity. Services:

| Service           | Image                  | Port  | Depends on        |
|-------------------|------------------------|-------|--------------------|
| `postgres`        | postgres:16-alpine     | 5432  | —                  |
| `redis`           | redis:7-alpine         | 6379  | —                  |
| `nginx`           | nginx:alpine           | 8080  | core-api, analysis-api, web |
| `core-api`        | built from `services/core-api` | 8001 | postgres  |
| `analysis-api`    | built from `services/analysis-api` | 8000 | redis   |
| `web`             | built from `apps/web`  | 3000  | core-api, analysis-api |
| `market-ingestion`| built from `workers/market-ingestion` | — | redis |
| `otel-collector`  | otel/opentelemetry-collector-contrib | 4317 | — |

### Per-service compose files (`infra/compose/`)

- `analysis-api.yml` — standalone definition for selective deployment
- `core-api.yml` — standalone definition for selective deployment

### Edge (`infra/edge/`)

- `nginx.conf` — reverse proxy with:
  - Rate limiting: 10 req/min on auth, 60 req/min on API
  - Security headers: X-Frame-Options, X-Content-Type-Options, Referrer-Policy
  - WebSocket upgrade for Next.js HMR
  - Route mapping: `/api/auth/` → core-api (auth rate limit), `/api/` → core-api,
    `/analysis/` → analysis-api, `/` → web

### Database (`infra/database/`)

- `init.sql` — PostgreSQL extensions and indexes:
  - `uuid-ossp` for future UUID PKs
  - `pg_trgm` + GIN index for fuzzy symbol search
  - Composite indexes on `(owner_id, created_at)` for journal and audit logs
  - Partial index on `alerts WHERE active = true`

### Monitoring (`infra/monitoring/`)

- `otel-collector.yaml` — OTLP receiver on :4317, batch processor, debug exporter
  (swap for Jaeger/Tempo in production)

### Dockerfiles

| Service           | Dockerfile                               | Stages           |
|-------------------|------------------------------------------|------------------|
| `analysis-api`    | `services/analysis-api/Dockerfile`       | test, runtime    |
| `core-api`        | `services/core-api/Dockerfile`           | test, runtime    |
| `web`             | `apps/web/Dockerfile`                    | builder, runtime |
| `market-ingestion`| `workers/market-ingestion/Dockerfile`    | builder, runtime |

## Networks

- `trading-app` — frontend + edge + APIs (application tier)
- `trading-data` — APIs + postgres + redis + worker (data tier)

Services are on the minimum networks needed. `web` and `nginx` are only on
`trading-app`; `postgres` and `redis` are only on `trading-data`; APIs bridge
both.

## Secrets

- **Development**: env vars in `docker-compose.yml` with safe defaults
- **Production**: inject via Infisical or `--env-file .env.production`
- **Never committed**: `.env`, `.env.production`, API keys, JWT secrets

## What's NOT here (intentional)

- No server deployment (constraint: implement, don't deploy)
- No Terraform/IaC (future phase if needed)
- No CI/CD pipeline (the `.github/` directory has basic workflows from Phase 1)
- No backtest-api Dockerfile (placeholder service — defined when implemented)
- No horizontal scaling config (single instance per service for now)
