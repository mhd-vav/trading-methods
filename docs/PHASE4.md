# Phase 4 — Production Multi-Agent Engine (`services/analysis-api`)

Status: implemented & tested. Builds on the Phase 1 foundation + Phase 3
evidence sources.

## EvidenceSnapshot (the core change)
All analyses now reference an immutable, content-addressed **EvidenceSnapshot**
(`app/evidence.py`) instead of free-form market text:

- `snapshot_id` derived from content hash + timestamp + nonce.
- Typed factors: `CandleWindowEvidence`, `NewsEvidence`, `CalendarEvidence`,
  `OrderFlowEvidence`, `SentimentEvidence`, `OnChainEvidence`.
- `missing_evidence_flags` make degraded/incomplete runs explicit.
- `to_agent_context()` renders a stable evidence block for prompts.

Bundles consume `context` rendered from the snapshot, and their numeric output
is parsed + validated against a strict Pydantic `AgentOutput` schema
(`app/bundles/base.py`) — supporting 100% schema-valid bundle verdicts.

## Engine improvements (`app/engine.py`)
- Runs a frozen snapshot; falls back to building one from legacy `market_data`.
- True parallel bundles with per-bundle timeouts; failures marked `status:error`
  and excluded (no silent neutral votes).
- **Idempotency**: a client `idempotency_key` returns the stored result on retry
  without re-running the LLM pipeline (`app/checkpoint.py`).
- **Checkpointing**: durable per-stage progress via `RunProgressTracker` /
  `CheckpointStore` (pluggable backend — Memory now, Redis/Postgres in prod).
- **Provenance** in every result: `run_id`, `snapshot_id`, `prompt_version`,
  `model_policy_version`, missing-evidence flags, and model-role assignments.
- `progress` (statuses per stage) supports frontend streaming.

## Prompt registry (`app/prompts.py`)
Versioned prompt registry (`PromptRegistry`) + store backend abstraction.
Production backs it with Infisical/DB; prompts are version-tracked, never
inlined in business logic.

## API additions
`POST /api/v1/analyze` accepts an optional `snapshot` and `idempotency_key`.
Invalid snapshots return `400 invalid_snapshot`.

## Verification
- `app` tests: 49 passing (incl. new Phase 4 suite: evidence, idempotency,
  checkpointing, engine provenance/idempotency with stubbed LLM).
- `ruff check` clean, format clean.

## Remaining (prod gating)
- Redis/Postgres checkpointing + streaming (SSE) wiring to frontend.
- Golden evaluation datasets + shadow comparison vs old engine (Phase 7 harness).
- RAG four-index (chunk/sub-chunk/synthetic-query/summary, 3072-dim, pgvector
  HNSW + FTS) — not yet introduced (no RAG scope used).
