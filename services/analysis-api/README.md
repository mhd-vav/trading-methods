# analysis-api — Multi-Agent Trading Desks analysis engine

FastAPI + LangGraph explainable multi-agent deliberation for Forex and Crypto.
**Educational analysis only. Not financial advice.**

Imported from the Hostinger backend and hardened under Phase 1 (production
foundation). Six bundles (technical, orderflow, macro, sentiment, onchain,
quant), each running a thesis/antithesis/referee debate, orchestrated by a
regime-weighted aggregate and constrained by a risk governor.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness |
| GET | `/ready` | Readiness (incl. optional Redis dependency probe) |
| POST | `/api/v1/analyze` | Run full MAS analysis for an asset |
| GET | `/api/v1/models` | Effective role→model assignments (never returns keys) |

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in LLM_API_KEY_CODE / LLM_API_KEY_EVAL
uvicorn app.api:app --reload
```

## Test / lint

```bash
pytest tests/ -q        # 39 unit + API tests
ruff check app/ && ruff format --check app/
```

## Build

```bash
docker build -t analysis-api:dev -f Dockerfile .
# multi-stage: base -> test (runs tests/lint/compile) -> runtime (minimal, non-root)
```

## Phase 1 hardening notes

- Structured JSON logging with `request_id` correlation
- Sanitized error envelope (no raw exceptions leak to clients)
- Hard per-call LLM timeout + explicit retry policy
- True parallel bundle execution with per-bundle timeouts
- Failed bundles marked `status:error` and excluded from aggregation
- Rate limiting, security headers, CORS allow-list + origin validation
- Optional OpenTelemetry tracing (`OTEL_ENDPOINT`)

See `docs/PRESERVE.md`, `docs/PHASE1.md`, `docs/SECURITY.md` at the repo root.
