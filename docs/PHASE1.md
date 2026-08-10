# Phase 1 — Production Foundation (analysis-api)

Status: **implemented and verified in this pass (2026-08-10)** for
`services/analysis-api`. Items that depend on the local Next.js repo or on
deployment to platform-01 are flagged.

## Done & verified

| Concern | Implementation | Verified |
|---|---|---|
| Multi-stage Dockerfile | `Dockerfile` (base → test → runtime), non-root runtime user, healthcheck | Parsed & structure-validated; every command it runs was executed locally |
| `.dockerignore` | excludes `.env`, caches, `.next`, `node_modules`, venvs | written |
| Standalone-ish runtime | `uvicorn app.api:app` single-worker container CMD | local boot OK |
| Image tagging w/ SHA | CI tags images with `git sha` (see CI workflow) | written |
| Health | `GET /health` (liveness) | 200 OK, returns status/service/version/request_id |
| Readiness | `GET /ready` (readiness + optional Redis dependency probe) | returns `ready:true` |
| Structured JSON logging | every log line JSON, `request_id` correlation | observed in `/tmp/uvicorn.log` |
| Request IDs | `X-Request-ID` set + echoed; propagates to logs | observed |
| OpenTelemetry traces | optional via `OTEL_ENDPOINT`; safe no-op when unset | guarded import |
| Provider timeouts | `LLM_REQUEST_TIMEOUT_S` on every ChatOpenAI; `max_retries=1` | code |
| Bundle parallelism | true parallel execution via ThreadPoolExecutor + per-bundle timeout | code + tests |
| Explicit failure states | failed bundles `status:error` and excluded from aggregation | code + tests |
| Error sanitation | sanitized error envelope; raw detail logged server-side only | 400/500 tests + live curl |
| Rate limiting | token-bucket on `/api/*` | code + tests |
| Security headers | CSP, nosniff, frame-deny, referrer, perms-policy, cache | live curl |
| Origin validation / CORS | allow-list + reject cross-origin state-changers | code |
| Cost/run ID | `run_id`, provisional provenance/metadata in result | code |

**Test result:** `39 passed` (unit + API). **Lint:** `ruff check` clean, format clean.

## In repo, not yet run

- **CI** (`.github/workflows/ci.yml`): TS, ESLint, Next build, Python fmt+type+tests,
  C++ tests/sanitizers, container builds, dependency + secret scanning — to run on
  the GitHub Actions runners once the canonical remote exists.
- **Infra compose** (`infra/compose/analysis-api.yml`) for Phase 6 deployment.

## Blocked (no local/server deployment in this pass, per task constraint)

- **Next.js `apps/web`**: standalone `output: "standalone"` step and the TS/ESLint/
  production-build CI jobs can only run against the real local checkout — it was not
  transferred (and intentionally not moved to a server). The CI jobs are written and
  will activate when the web app is imported in Phase 0 follow-up.
- **C++ engine** (13 tests): not imported (local ChromePath). CI C++ job written.
- **Docker image build/run on a server**: intentionally not performed (no copying to
  servers). The Dockerfile is validated structurally and by local execution of its
  commands.

## Next steps

Phase 2 (charting), Phase 3 (market-data platform), Phase 4 (production engine:
evidence snapshot, checkpoints, idempotency, streaming) build on this foundation.
