import { describe, it, expect } from "vitest";
import {
  sma,
  ema,
  rsi,
  macd,
  atr,
  bollinger,
  trueRange,
  computeIndicator,
} from "../src/indicators";
import type { Candle, IndicatorConfig } from "@trading-desk/contracts";

function candle(i: number, o: number, h: number, l: number, c: number, v = 1): Candle {
  return {
    id: `t:${i}`, provider: "synthetic", originalSymbol: "X", canonicalSymbol: "X/USD",
    interval: "1h", exchangeTimezone: "UTC", startMs: i * 3_600_000, endMs: (i + 1) * 3_600_000,
    o, h, l, c, v, isFinal: true, retrievedAtMs: 0, freshnessMs: 0, adjustment: "none",
    qualityWarnings: [],
  };
}

describe("sma", () => {
  it("produces a correct simple moving average", () => {
    // values 1..10, period 3
    const v = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const res = sma(v, 3);
    expect(res[0]).toBeNull();
    expect(res[1]).toBeNull();
    expect(res[2]).toBe(2);
    expect(res[3]).toBe(3);
    expect(res[9]).toBe(9);
  });

  it("handles period larger than data", () => {
    expect(sma([1, 2], 5)).toEqual([null, null]);
  });

  it("is deterministic", () => {
    const v = [3, 1, 4, 1, 5, 9, 2, 6];
    expect(sma(v, 3)).toEqual(sma(v, 3));
  });
});

describe("ema", () => {
  it("matches a hand-computed example", () => {
    // values [5,6,7,8], period 3 -> seed = SMA(5,6,7) = 6
    const res = ema([5, 6, 7, 8], 3);
    expect(res[0]).toBeNull();
    expect(res[1]).toBeNull();
    // seed at index 2 = 6
    expect(res[2]).toBeCloseTo(6, 6);
    // k = 2/4 = 0.5 ; ema[3] = 8*0.5 + 6*0.5 = 7
    expect(res[3]).toBeCloseTo(7, 6);
  });
});

describe("trueRange / atr", () => {
  // Three candles with easy TR.
  const c = [
    candle(0, 10, 12, 9, 11),   // TR = 12-9 = 3
    candle(1, 11, 13, 8, 12),   // TR = max(13-8=5, |13-11|=2, |8-11|=3) = 5
    candle(2, 12, 14, 10, 13),  // TR = max(14-10=4, |14-12|=2, |10-12|=2) = 4
  ];
  it("computes true range", () => {
    expect(trueRange(c.map((x) => x.h), c.map((x) => x.l), c.map((x) => x.c))).toEqual([3, 5, 4]);
  });
  it("computes ATR", () => {
    const res = atr(c, 2);
    // warm-up: single null for period=2? ema seed at index period-1=1
    expect(res[0]).toBeNull();
    expect(res[1]).toBeCloseTo(4, 6); // SMA(3,5)=4
    // Wilder k = 1/2=0.5: atr[2] = 4*0.5 + 4*0.5 = 4
    expect(res[2]).toBeCloseTo(4, 6);
  });
});

describe("rsi", () => {
  it("gives 100 when all gains, no losses (first segment)", () => {
    const v = [1, 2, 3, 4, 5, 6, 7, 8]; // strictly increasing
    const res = rsi(v, 5);
    // warm-up index 0..4 nulls, first at index 5
    expect(res.slice(0, 5).every((x) => x === null)).toBe(true);
    expect(res[5]).toBe(100);
  });
  it("gives 0 when all losses", () => {
    const v = [10, 9, 8, 7, 6, 5, 4, 3];
    const res = rsi(v, 5);
    expect(res[5]).toBe(0);
  });
  it("is bounded in [0,100] for mixed data", () => {
    const v = [1, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7];
    const res = rsi(v, 3);
    for (const x of res) if (x != null) expect(x).toBeGreaterThanOrEqual(0);
    for (const x of res) if (x != null) expect(x).toBeLessThanOrEqual(100);
  });
});

describe("macd", () => {
  it("has correct lengths and warm-up", () => {
    const v = Array.from({ length: 60 }, (_, i) => 100 + (i % 5));
    const { macd: m, signal, hist } = macd(v, 12, 26, 9);
    expect(m.length).toBe(60);
    expect(signal.length).toBe(60);
    expect(hist.length).toBe(60);
    // macd null until slow warm-up (index 25)
    expect(m.slice(0, 25).every((x) => x === null)).toBe(true);
    expect(m[25]).not.toBeNull();
  });
  it("is deterministic", () => {
    const v = Array.from({ length: 40 }, (_, i) => Math.sin(i));
    expect(macd(v)).toEqual(macd(v));
  });
});

describe("bollinger", () => {
  it("mid equals SMA and bands symmetric", () => {
    const v = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const { mid, upper, lower } = bollinger(v, 5, 2);
    // mid at index 4 = SMA(1..5)=3
    expect(mid[4]).toBe(3);
    expect(upper[4]).toBeGreaterThan(mid[4] as number);
    expect(lower[4]).toBeLessThan(mid[4] as number);
    // symmetric: mid - lower == upper - mid
    expect(upper[4]! - mid[4]!).toBeCloseTo(mid[4]! - lower[4]!, 6);
  });
});

describe("computeIndicator", () => {
  const candles = Array.from({ length: 50 }, (_, i) => candle(i, 100 + i, 101 + i, 99 + i, 100 + i));
  it("computes SMA via config", () => {
    const cfg: IndicatorConfig = { kind: "sma", params: { period: 10 } };
    const res = computeIndicator(candles, cfg);
    expect(res.kind).toBe("sma");
    expect(res.line.length).toBe(41);
    expect(res.line[0].x).toBe(9);
  });
  it("computes MACD with extra signal+hist lines", () => {
    const cfg: IndicatorConfig = { kind: "macd", params: {} };
    const res = computeIndicator(candles, cfg);
    expect(res.extraLines?.length).toBe(2);
    expect(res.extraLines?.map((l) => l.name)).toEqual(["signal", "hist"]);
  });
  it("computes Bollinger with bands", () => {
    const cfg: IndicatorConfig = { kind: "bollinger", params: {} };
    const res = computeIndicator(candles, cfg);
    expect(res.bands).toBeDefined();
    expect(res.bands!.upper.length).toBeGreaterThan(0);
    expect(res.bands!.lower.length).toBe(res.bands!.upper.length);
  });
  it("handles unknown kind gracefully", () => {
    const cfg = { kind: "nope" as never, params: {} };
    const res = computeIndicator(candles, cfg);
    expect(res.warnings).toContain("invalid-indicator-kind");
  });
});
