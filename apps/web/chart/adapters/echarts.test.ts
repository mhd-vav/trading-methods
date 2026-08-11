import { describe, it, expect } from "vitest";
import { buildOption } from "./echarts";
import { viewportFromLayout } from "../hooks/useChartViewport";
import type { Candle, ChartLayout, ChartViewport } from "@trading-desk/contracts";

function candle(i: number, price: number): Candle {
  return {
    id: `c:${i}`, provider: "synthetic", originalSymbol: "BTC", canonicalSymbol: "BTC/USDT",
    interval: "4h", exchangeTimezone: "UTC", startMs: i * 14_400_000, endMs: (i + 1) * 14_400_000,
    o: price, h: price + 1, l: price - 1, c: price, v: 100 + i, isFinal: true,
    retrievedAtMs: 0, freshnessMs: 0, adjustment: "none", qualityWarnings: [],
  };
}

describe("buildOption (pure ECharts option mapper)", () => {
  const candles = Array.from({ length: 100 }, (_, i) => candle(i, 100 + i * 0.1));
  const viewport: ChartViewport = { startIndex: 0, endIndex: 99, candleWidthPx: null };

  it("produces a candlestick series with volume", () => {
    const opt = buildOption({ candles, indicators: [], drawings: [], viewport, symbol: "BTC/USDT", interval: "4h" }) as any;
    const kinds = opt.series.map((s: any) => s.type);
    expect(kinds).toContain("candlestick");
    expect(kinds).toContain("bar");
  });

  it("adds indicator series when provided", () => {
    const indicators = [
      {
        kind: "sma", config: { kind: "sma" as const, params: { period: 20 } },
        line: [{ x: 0, y: 100 }, { x: 1, y: 101 }],
        extraLines: [],
      },
    ];
    const opt = buildOption({ candles, indicators, drawings: [], viewport, symbol: "S", interval: "1d" }) as any;
    const names = opt.series.map((s: any) => s.name);
    expect(names).toContain("SMA");
  });

  it("disables animation for ≥ DENSE_THRESHOLD candles", () => {
    const big = Array.from({ length: 10_000 }, (_, i) => candle(i, 100 + Math.sin(i) * 5));
    const opt = buildOption({ candles: big, indicators: [], drawings: [], viewport, symbol: "B", interval: "1m" }) as any;
    expect(opt.animation).toBe(false);
    expect(opt.series[0].animation).toBe(false);
  });

  it("keeps raw candle count in dataZoom regardless of sampling", () => {
    const opt = buildOption({ candles, indicators: [], drawings: [], viewport, symbol: "X", interval: "1m" }) as any;
    expect(opt.dataZoom.length).toBeGreaterThanOrEqual(2);
  });
});

describe("viewportFromLayout", () => {
  it("fits all when layout range is null or missing", () => {
    const v = viewportFromLayout(null, 50);
    expect(v.startIndex).toBe(0);
    expect(v.endIndex).toBe(49);
  });
  it("reads persisted range and clamps", () => {
    const layout: ChartLayout = {
      id: "l", symbol: "BTC/USDT", range: { startIndex: 10, endIndex: 30 }, indicators: [], drawings: [],
      updatedAtMs: 0,
    };
    const v = viewportFromLayout(layout, 20);
    expect(v.endIndex).toBeLessThanOrEqual(19);
  });
});