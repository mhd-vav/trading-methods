import { describe, it, expect } from "vitest";
import {
  candleQualityWarnings,
  auditSeries,
  findGaps,
  findDuplicates,
  freshnessScore,
} from "../src/quality";
import type { Candle, CandleSeries } from "@trading-desk/contracts";

function c(i: number, o = 100, h = 101, l = 99, cc = 100, v = 10, opts: Partial<Candle> = {}): Candle {
  const step = 3_600_000;
  const start = i * step;
  return {
    id: `c:${i}`, provider: "synthetic", originalSymbol: "X", canonicalSymbol: "X/USD",
    interval: "1h", exchangeTimezone: "UTC", startMs: start, endMs: start + step,
    o, h, l, c: cc, v, isFinal: true, retrievedAtMs: 0, freshnessMs: 0, adjustment: "none",
    qualityWarnings: [], ...opts,
  };
}

describe("candleQualityWarnings", () => {
  it("flags broken OHLC relationship", () => {
    const bad = c(0, 100, 90, 95, 100); // high < max(o,c)
    expect(candleQualityWarnings(bad)).toContain("invalid-ohlc-relationship");
  });
  it("flags zero volume", () => {
    expect(candleQualityWarnings(c(0, 100, 101, 99, 100, 0))).toContain("zero-volume");
  });
  it("flags incomplete candles", () => {
    expect(candleQualityWarnings(c(0, 100, 101, 99, 100, 10, { isFinal: false }))).toContain("incomplete");
  });
  it("passes a clean candle", () => {
    expect(candleQualityWarnings(c(0))).toEqual([]);
  });
});

describe("auditSeries", () => {
  it("detects a gap", () => {
    const candles = [c(0), c(1), c(3), c(4)]; // missing index 2
    const series: CandleSeries = { candles, symbol: "X/USD", interval: "1h", provider: "synthetic", generatedAtMs: 0 };
    const report = auditSeries(series);
    expect(report.totals.gap).toBeGreaterThan(0);
    expect(report.degraded).toBe(true);
  });
  it("detects duplicates", () => {
    const candles = [c(0), c(1), { ...c(1), id: "dup" }]; // same startMs
    const series: CandleSeries = { candles, symbol: "X/USD", interval: "1h", provider: "synthetic", generatedAtMs: 0 };
    const report = auditSeries(series);
    expect(report.totals["duplicate-timestamp"]).toBeGreaterThan(0);
  });
  it("counts per-candle warnings", () => {
    const candles = [c(0, 100, 95, 99, 100, 10), c(1)]; // first has invalid OHLC + maybe zero? v=10
    const series: CandleSeries = { candles, symbol: "X/USD", interval: "1h", provider: "synthetic", generatedAtMs: 0 };
    const report = auditSeries(series);
    expect(report.totals["invalid-ohlc-relationship"]).toBeGreaterThan(0);
  });
});

describe("findGaps", () => {
  it("finds missing bars", () => {
    const candles = [c(0), c(1), c(3)];
    const gaps = findGaps(candles, "1h");
    expect(gaps.length).toBe(1);
    expect(gaps[0].fromMs).toBe(candles[1].startMs);
    expect(gaps[0].toMs).toBe(candles[2].startMs);
  });
});

describe("findDuplicates", () => {
  it("finds duplicate timestamps", () => {
    const candles = [c(0), c(0), c(1)];
    const dups = findDuplicates(candles);
    expect(dups.some((d) => d.count === 2)).toBe(true);
  });
});

describe("freshnessScore", () => {
  it("is 1 for current data", () => {
    const candles = [c(0), c(1)];
    const series: CandleSeries = { candles, symbol: "X/USD", interval: "1h", provider: "synthetic", generatedAtMs: 0 };
    // newest candle end = 2h; now = 2h => age 0
    expect(freshnessScore(series, 2 * 3_600_000)).toBe(1);
  });
  it("decays with age", () => {
    const candles = [c(0), c(1)];
    const series: CandleSeries = { candles, symbol: "X/USD", interval: "1h", provider: "synthetic", generatedAtMs: 0 };
    // 10 bars stale -> score 0
    expect(freshnessScore(series, 2 * 3_600_000 + 50 * 3_600_000)).toBe(0);
  });
});
