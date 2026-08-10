# Security Policy — Trading Desk

## Reporting

If you find a vulnerability, report it privately. **Do not** open a public
issue. Email the maintainers or file a private advisory for this repository.

## Supported scope

| Component | Security-relevant behavior |
|---|---|
| `services/analysis-api` | LLM input handling, error envelopes, model/key config, rate limiting, security headers |
| `apps/web` | AuthZ (backend-enforced, not UI-hidden), CSP, input validation |
| `services/core-api` | User identity, journal, layout persistence — object-level access control |
| `services/backtest-api` | Execution of user-supplied data ranges — timeouts + resource caps |

## Key commitments (from the audit)

- **Never** return raw exception details to clients. Unexpected errors are
  logged server-side with full detail and returned to clients as a sanitized
  envelope (`{"error":{"code","message"},"request_id"}`).
- **Never** bake secrets into source. Keys come from the environment / a vault
  (Infisical in production). Role→model assignments are env-overridable, never
  hardcoded credentials.
- **Authentication & authorization** are enforced by the backend, not merely
  hidden in the UI. Two users must not be able to read each other's records.
- **Every mutation is audited** (audit-log storage in Phase 5).
- **All provider/LLM calls have timeouts and cancellation.** A hard per-call
  timeout is applied (`LLM_REQUEST_TIMEOUT_S`, default 120s); `max_retries=1` is
  explicit (no silent infinite retry).

## Rate limiting & headers (Phase 1, analysis-api)

- Per-client token-bucket rate limit on `/api/*` (`RATE_LIMIT_PER_MINUTE`).
  In-memory for single-instance; swap for Redis for multi-instance production.
- Security headers on every response: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`,
  `Permissions-Policy`, a restrictive `Content-Security-Policy`,
  `Cache-Control: no-store`, `X-Robots-Tag: noindex`.
- CORS allow-list + origin validation for state-changing methods.

## Deployment guardrails

- Build from **immutable SHA-tagged images** only.
- Run DB migrations as an explicit one-shot job, never inline at startup.
- Keep the old backend available read-only during a rollback window.
- No `node_modules`, `.next`, `.env`, or caches are ever copied to a server.

## Dependency & secret scanning

CI runs dependency and secret scanning on every push (see CI workflow). A
baseline secret scan must pass before the first consolidated push to a remote.
