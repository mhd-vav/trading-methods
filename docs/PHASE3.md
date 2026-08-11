# Phase 3 — Market-Data Platform

Status: implemented & tested in `packages/provider-adapters` + `workers/market-ingestion`.

## Canonical candle contract (in `packages/contracts`)
`Candle` carries: provider, original + canonical symbol, interval, exchange
timezone, OHLCV, `isFinal`, `retrievedAtMs`, `freshnessMs`, adjustment method,
and quality warnings — the full Phase 3 spec. `CandleSeries` wraps candles +
provenance.

## Provider adapters (`packages/provider-adapters`)
- `adapter.ts` — strict `ProviderAdapter` interface (normalized output contract).
- `coingecko.ts` — real CoinGecko adapter (injected fetcher for deterministic tests),
  buckets OHLC into the requested interval, marks the live candle incomplete.
- `forex.ts` — Forex adapter with explicit degraded state when the middleware is
  unavailable (never an endless loading screen).
- `resilience.ts` — `withTimeout`, `withRetry` (exponential backoff + jitter),
  `CircuitBreaker`, `RequestCoalescer` (single-flight).
- `client.ts` — `ResilientMarketClient`: cache → coalesce → provider chain with
  retry/timeout/circuit-breaker → fallback → explicit degraded result.
- `quality.ts` — `auditSeries` detects gaps, duplicate timestamps, invalid OHLC,
  zero volume, clock drift; produces a `degraded` flag + per-warning counts;
  `freshnessScore` for stale-data UI indicators.

## Worker (`workers/market-ingestion`)
`MarketIngestionWorker` — periodic refresher over configured targets using the
resilient client, with per-symbol status tracking (last ok/error time, degraded,
candle count). CLI entry for deployment.

## Verification
- `packages/provider-adapters`: 27 tests passing (quality 11, resilience 11, client 5);
  typecheck clean.
- `workers/market-ingestion`: typecheck clean.

## Notes / gaps
- Redis-backed caching & Timescale-style historical storage are production
  options; the cache is a pluggable interface (`CachePluggable`) with an
  in-memory impl for now.
- The audit's "fallback providers where licensing permits" is modeled (ordered
  provider chain) but only CoinGecko + a Forex stub are concrete.
