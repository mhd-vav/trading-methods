/**
 * Provider adapter interface (Phase 3).
 *
 * Every provider implements the same strict contract: take a symbol + interval
 * + window and return a normalized `CandleSeries`. Normalization includes the
 * canonical symbol, provider identification, exchange timezone, final/incomplete
 * flag, retrieval time, freshness, adjustment method, and quality warnings —
 * exactly the canonical Candle contract.
 */
import type { CandleSeries, Timeframe } from "@trading-desk/contracts";

export interface ProviderFetchOptions {
  symbol: string;
  interval: Timeframe;
  /** Number of candles to fetch. */
  limit: number;
  /** Optional end anchor (default now). */
  endMs?: number;
  signal?: AbortSignal;
}

export interface ProviderAdapter {
  readonly provider: string;
  /**
   * Fetch and normalize. MUST NOT throw on provider-transient errors only — it
   * may throw TimeoutError / ProviderTransientError which caller resilience
   * layers retry/circuit-break. Returns a normal series on success.
   */
  fetchCandles(opts: ProviderFetchOptions): Promise<CandleSeries>;
  /** Normalize a provider symbol to the canonical form, or null if unsupported. */
  canNormalize(symbol: string): boolean;
}
