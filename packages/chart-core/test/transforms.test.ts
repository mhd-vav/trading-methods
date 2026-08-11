import { describe, it, expect } from "vitest";
import { minMaxSample, sliceToViewport, clampViewport, ohlcArrays, msPerBar } from "../src/transforms";
import type { Candle, ChartViewport } from "@trading-desk/contracts";

function candle(i: number, c: number): Candle {
  return {
    id: `c:${i}`, provider: "synthetic", originalSymbol: "X", canonicalSymbol: "X/USD",
    interval: "1m", exchangeTimezone: "UTC", startMs: i * 60_000, endMs: (i + 1) * 60_000,
    o: c, h: c, l: c, c, v: 1, isFinal: true, retrievedAtMs: 0, freshnessMs: 0,
    adjustment: "none", qualityWarnings: [],
  };
}

describe("clampViewport", () => {
  it("clamps negatives and overflow", () => {
    const v = clampViewport({ startIndex: -5, endIndex: 1000, candleWidthPx: null }, 10);
    expect(v.startIndex).toBe(0);
    expect(v.endIndex).toBe(9);
  });
});

describe("sliceToViewport", () => {
  it("returns only the visible window", () => {
    const c = [candle(0, 1), candle(1, 2), candle(2, 3), candle(3, 4), candle(4, 5)];
    const out = sliceToViewport(c, { startIndex: 1, endIndex: 3, candleWidthPx: null });
    expect(out.map((x) => x.c)).toEqual([2, 3, 4]);
  });
  it("returns empty for empty input", () => {
    expect(sliceToViewport([], { startIndex: 0, endIndex: 9, candleWidthPx: null })).toEqual([]);
  });
});

describe("minMaxSample", () => {
  it("returns identical series when bucket <= 1", () => {
    const { xs, ys } = minMaxSample([0, 1, 2], [5, 6, 7], 1);
    expect(xs).toEqual([0, 1, 2]);
    expect(ys).toEqual([5, 6, 7]);
  });
  it("samples min and max per bucket of 3", () => {
    // bucket=3 windows: [9,1,5] (min 1, max 9), [3,8,2] (min 2, max 8), [7] lone
    const ys = [9, 1, 5, 3, 8, 2, 7];
    const xs = ys.map((_, i) => i);
    const { xs: ox, ys: oy } = minMaxSample(xs, ys, 3);
    // window0: min at 1 (y=1), max at 0 (y=9) -> ordered [0,1]
    // window1: min at 5 (y=2), max at 4 (y=8) -> ordered [4,5]
    // window2: single 7 -> [6]
    expect(ox).toEqual([0, 1, 4, 5, 6]);
    expect(oy).toEqual([9, 1, 8, 2, 7]);
  });
  it("throws on length mismatch", () => {
    expect(() => minMaxSample([1, 2], [1], 2)).toThrow();
  });
  it("is deterministic", () => {
    const xs = [0, 1, 2, 3, 4, 5, 6, 7];
    const ys = [3, 1, 4, 1, 5, 9, 2, 6];
    expect(minMaxSample(xs, ys, 2)).toEqual(minMaxSample(xs, ys, 2));
  });
});

describe("ohlcArrays", () => {
  it("splits candles into aligned arrays", () => {
    const c = [candle(0, 1), candle(1, 2), candle(2, 3)];
    const a = ohlcArrays(c);
    expect(a.o).toEqual([1, 2, 3]);
    expect(a.h).toEqual([1, 2, 3]);
    expect(a.c).toEqual([1, 2, 3]);
    expect(a.xs).toEqual([0, 60000, 120000]);
  });
});

describe("msPerBar", () => {
  it("returns correct ms per timeframe", () => {
    expect(msPerBar("1h")).toBe(3_600_000);
    expect(msPerBar("4h")).toBe(14_400_000);
    expect(msPerBar("5m")).toBe(300_000);
    expect(msPerBar("1d")).toBe(86_400_000);
  });
});
