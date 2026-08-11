/**
 * Market-data quality checks (Phase 3):
 * - gaps / missing intervals
 * - duplicate timestamps
 * - invalid OHLC relationships (h<max(o,c), l>min(o,c), negative prices)
 * - zero/non-positive volume
 * - clock drift (retrieval time far from candle window)
 * - freshness scoring for stale-data indications
 *
 * Pure and deterministic — unit-tested.
 */
import type { Candle, CandleSeries, QualityWarning } from "@trading-desk/contracts";
import { msPerBar } from "@trading-desk/chart-core";

export interface QualityReport {
  symbol: string;
  candleCount: number;
  warnings: Record<string, QualityWarning[]>;
  /** True when any candle has a blocking-quality warning. */
  degraded: boolean;
  /** Summary counts for monitoring/UI. */
  totals: Record<QualityWarning, number>;
}

/** Validate one candle's OHLC internal consistency. */
export function candleQualityWarnings(c: Candle): QualityWarning[] {
  const out: QualityWarning[] = [];
  if (c.h < Math.max(c.o, c.c)) out.push("invalid-ohlc-relationship");
  if (c.l > Math.min(c.o, c.c)) out.push("invalid-ohlc-relationship");
  if (c.o < 0 || c.h < 0 || c.l < 0 || c.c < 0) out.push("invalid-ohlc-relationship");
  if (c.v <= 0) out.push("zero-volume");
  if (!c.isFinal) out.push("incomplete");
  return out;
}

/** Detect gaps in a series given the expected bar duration. */
export function findGaps(candles: Candle[], interval: string): { fromMs: number; toMs: number }[] {
  const step = msPerBar(interval);
  const gaps: { fromMs: number; toMs: number }[] = [];
  for (let i = 1; i < candles.length; i++) {
    const expected = candles[i - 1].startMs + step;
    if (candles[i].startMs > expected) {
      gaps.push({ fromMs: candles[i - 1].startMs, toMs: candles[i].startMs });
    }
  }
  return gaps;
}

/** Detect duplicate start timestamps. */
export function findDuplicates(candles: Candle[]): { startMs: number; count: number }[] {
  const seen = new Map<number, number>();
  for (const c of candles) seen.set(c.startMs, (seen.get(c.startMs) ?? 0) + 1);
  return [...seen.entries()]
    .filter(([, n]) => n > 1)
    .map(([startMs, count]) => ({ startMs, count }));
}

/** Detect clock drift: retrieval far outside the candle's own window. */
export function findClockDrift(candles: Candle[], toleranceMs = 90_000): number[] {
  const idx: number[] = [];
  for (let i = 0; i < candles.length; i++) {
    const c = candles[i];
    if (c.retrievedAtMs > 0 && Math.abs(c.retrievedAtMs - c.endMs) > toleranceMs) idx.push(i);
  }
  return idx;
}

export const ALL_WARNINGS: QualityWarning[] = [
  "gap", "duplicate-timestamp", "invalid-ohlc-relationship", "zero-volume",
  "possible-clock-drift", "incomplete",
];

/** Run the full quality audit over a series. */
export function auditSeries(series: CandleSeries, opts?: {
  gapToleranceBars?: number;
  clockDriftToleranceMs?: number;
  minutesGapThreshold?: number;
}): QualityReport {
  const candles = series.candles;
  const perCandle: Record<string, QualityWarning[]> = {};
  const totals: Record<QualityWarning, number> = {
    gap: 0, "duplicate-timestamp": 0, "invalid-ohlc-relationship": 0,
    "zero-volume": 0, "possible-clock-drift": 0, incomplete: 0,
  };
  let degraded = false;

  // per-candle checks
  for (const c of candles) {
    const w = candleQualityWarnings(c);
    if (w.length) {
      perCandle[c.id] = w;
      for (const x of w) totals[x] += 1;
      degraded = degraded || w.some((x) => x !== "incomplete");
    }
  }

  // gaps: flag any intervals missing more than `gapToleranceBars` bars
  const step = msPerBar(series.interval);
  const gapThresholdMs = (opts?.gapToleranceBars ?? 0) * step;
  const gaps = findGaps(candles, series.interval).filter((g) => g.toMs - g.fromMs > step + gapThresholdMs);
  if (gaps.length) {
    perCandle["__series__"] = perCandle["__series__"] ?? [];
    perCandle["__series__"].push("gap");
    totals.gap += gaps.length;
    degraded = true;
  }

  // duplicates
  const dups = findDuplicates(candles);
  if (dups.length) {
    perCandle["__series__"] = perCandle["__series__"] ?? [];
    perCandle["__series__"].push("duplicate-timestamp");
    totals["duplicate-timestamp"] += dups.length;
    degraded = true;
  }

  // clock drift
  const drift = findClockDrift(candles, opts?.clockDriftToleranceMs);
  if (drift.length) totals["possible-clock-drift"] += drift.length;

  return { symbol: series.symbol, candleCount: candles.length, warnings: perCandle, degraded, totals };
}

/** Freshness scoring: 0..1 recency of the newest candle. */
export function freshnessScore(series: CandleSeries, nowMs = Date.now()): number {
  if (!series.candles.length) return 0;
  const newest = series.candles[series.candles.length - 1];
  const age = nowMs - newest.endMs;
  // Fully fresh if retrieved/ended within one bar; decays to 0 over 5 bars.
  const bar = msPerBar(series.interval);
  const spans = age / (bar * 5);
  return Math.max(0, Math.min(1, 1 - spans));
}