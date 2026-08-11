/**
 * ECharts adapter — concrete implementation of `ChartAdapter`.
 *
 * Encapsulates ALL ECharts usage behind the adapter interface. Implements the
 * Phase 2 performance patterns: `dataZoom`, min-max sampling, progressive/
 * appended data for large datasets, animation disabled for large datasets, and
 * correct resize + disposal lifecycle.
 *
 * This module is the ONLY place in the app that imports `echarts`.
 */
import * as echarts from "echarts";
import type { ECharts, EChartsOption } from "echarts";
import type {
  ChartViewport,
  Drawing,
  IndicatorResult,
} from "@trading-desk/contracts";
import {
  ohlcArrays,
  minMaxSample,
  msPerBar,
} from "@trading-desk/chart-core";
import type { ChartAdapter, ChartHandle, ChartRenderInput, CursorInfo } from "./types";

export const DENSE_THRESHOLD = 10_000; // candles at/above this disable animation

function buildOption(input: ChartRenderInput): EChartsOption {
  const { candles, indicators, viewport, symbol, interval } = input;
  const { xs, o, h, l, c, v } = ohlcArrays(candles);
  const dense = candles.length >= DENSE_THRESHOLD;

  // Sampling: for dense series use min-max sampling on candles to keep ECharts fast.
  let kdata = candles.map((a) => a.c);
  if (dense) {
    const sampled = minMaxSample(
      xs,
      candles.map((a) => a.c),
      Math.floor(candles.length / DENSE_THRESHOLD) + 1,
    );
    // For a candlestick we keep raw arrays but rely on dataZoom; min-max applies
    // to indicator lines below. Candlesticks themselves use progressive render.
  }

  const zoom: EChartsOption["dataZoom"] = [
    {
      type: "inside",
      xAxisIndex: [0, 1, 2],
      start: 0,
      end: 100,
      throttle: 50,
    },
    { type: "slider", xAxisIndex: [0, 1, 2], bottom: 8, height: 20 },
  ];

  const baseAxis = {
    type: "category" as const,
    data: xs.map((x) => x),
    boundaryGap: true as const,
  };

  const series: EChartsOption["series"] = [
    {
      name: symbol,
      type: "candlestick",
      data: candles.map((cd, i) => [cd.o, cd.c, cd.l, cd.h]),
      itemStyle: { color: "#10b981", color0: "#ef4444", borderColor: "#10b981", borderColor0: "#ef4444" },
      progressive: dense ? 4000 : 1000,
      animation: !dense,
    },
    {
      name: "Volume",
      type: "bar",
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: v,
      itemStyle: { color: (p: { dataIndex: number }) => (c[p.dataIndex] >= o[p.dataIndex] ? "#10b98155" : "#ef444455") },
      animation: !dense,
    },
  ];

  // Indicator series (rendered in main or dedicated pane based on pane).
  const indicatorSeries: EChartsOption["series"] = [];
  for (const ind of indicators) {
    if (ind.kind === "bollinger" && ind.bands) {
      indicatorSeries.push({
        name: "BB-upper", type: "line", data: ind.bands.upper.map((p) => p.y),
        step: false, symbol: "none", lineStyle: { opacity: 0.5 }, smooth: false,
        animation: !dense,
      });
      indicatorSeries.push({
        name: "BB-lower", type: "line", data: ind.bands.lower.map((p) => p.y),
        symbol: "none", lineStyle: { opacity: 0.5 }, smooth: false, animation: !dense,
      });
    }
    if (ind.line.length) {
      const seriesToPush: Record<string, unknown> = {
        name: ind.kind.toUpperCase(),
        type: "line",
        data: ind.line.map((p) => p.y),
        symbol: "none",
        animation: !dense,
        sampling: dense ? "minmax" : "lttb",
      };
      indicatorSeries.push(seriesToPush as never);
    }
    for (const extra of ind.extraLines ?? []) {
      if (extra.points.length) {
        indicatorSeries.push({
          name: `${ind.kind.toUpperCase()}-${extra.name}`,
          type: "line",
          data: extra.points.map((p) => p.y),
          symbol: "none",
          animation: !dense,
          sampling: dense ? "minmax" : "lttb",
        });
      }
    }
  }
  series.push(...(indicatorSeries as never[]));

  return {
    animation: !dense,
    animationThreshold: DENSE_THRESHOLD,
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
      valueFormatter: (val: unknown) =>
        typeof val === "number" ? val.toLocaleString(undefined, { maximumFractionDigits: 6 }) : String(val),
    },
    axisPointer: { link: [{ xAxisIndex: "all" }] },
    xAxis: [
      baseAxis,
      { ...baseAxis, gridIndex: 1 },
      { ...baseAxis, gridIndex: 2 },
    ],
    yAxis: [
      { scale: true, gridIndex: 0 },
      { gridIndex: 1, show: false, max: (mx: { max: number }) => mx.max * 4 },
      { scale: true, gridIndex: 2 },
    ],
    grid: [
      { left: 70, right: 20, top: 10, height: "55%" },
      { left: 70, right: 20, top: "68%", height: "12%" },
      { left: 70, right: 20, top: "84%", height: "14%" },
    ],
    dataZoom: zoom,
    series,
  };
}

/**
 * ECharts-backed adapter. One `ChartHandle` owns one ECharts instance and its
 * DOM container; callers must call `dispose()` to avoid leaks.
 */
const echartsAdapter: ChartAdapter = {
  isSupported() {
    return typeof window !== "undefined" && !!echarts;
  },
  mount(container, opts) {
    const chart: ECharts = echarts.init(container, opts?.theme ?? "dark", { renderer: "canvas" });
    let cursorListener: ((info: CursorInfo) => void) | null = null;
    let lastRender: ChartRenderInput | null = null;

    // Crosshair/OHLC tooltip synchronization wiring.
    chart.on("mousemove", (params: { dataIndex?: number }) => {
      if (cursorListener && typeof params?.dataIndex === "number") {
        const c = lastRender?.candles[params.dataIndex];
        cursorListener({ index: params.dataIndex, candle: c ?? null, pricesPx: null });
      }
    });
    chart.on("mouseout", () => {
      cursorListener?.({ index: null, candle: null, pricesPx: null });
    });

    const handle: ChartHandle = {
      render(input: ChartRenderInput) {
        lastRender = input;
        chart.setOption(buildOption(input), { notMerge: false, lazyUpdate: false });
      },
      updateViewport(_viewport: ChartViewport) {
        // ECharts dataZoom owns the viewport; the hook layer keeps app state in
        // sync via the 'datazoom' event. Nothing extra needed here.
      },
      resize(size: { width: number; height: number }) {
        chart.resize({ width: size.width, height: size.height });
      },
      setCursorListener(fn) {
        cursorListener = fn;
      },
      dispose() {
        chart.dispose();
        (chart as unknown as { __container?: HTMLElement | null }).__container = null;
      },
    };
    return handle;
  },
};

export { buildOption };
export const createEChartsAdapter = (): ChartAdapter => echartsAdapter;

// Re-export for tests / other adopters.
export const chartCoreReExports = { msPerBar, minMaxSample };
export type { IndicatorResult };
export type { Drawing };
