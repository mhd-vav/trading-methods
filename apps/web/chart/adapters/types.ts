/**
 * Chart adapter interface — the decoupling layer between the app and ECharts.
 *
 * Phase 2 requires keeping Apache ECharts behind an internal adapter so the rest
 * of the app never imports ECharts directly and ECharts could be swapped later.
 * The adapter operates at the application domain level (Candle, IndicatorResult,
 * Drawing, ChartViewport), not at ECharts' option level.
 */
import type {
  Candle,
  ChartViewport,
  Drawing,
  IndicatorResult,
  IndicatorConfig,
} from "@trading-desk/contracts";

/** One subplot of the chart (price main pane, volume pane, indicator panes). */
export type PaneId = "main" | "volume" | string; // indicator panes keyed by name

/** What a cursor/hover currently points at, for crosshair sync + OHLC tooltip. */
export interface CursorInfo {
  /** Candle index under the cursor, or null. */
  index: number | null;
  /** Candle under cursor, or null (e.g. over empty region). */
  candle: Candle | null;
  pricesPx: number | null;
}

export interface ChartSeriesInput {
  candles: Candle[];
  indicators: IndicatorResult[];
  /** Which indicators render in the main vs dedicated pane. */
  paneForIndicator?: (id: string) => PaneId;
}

export interface ChartRenderInput {
  candles: Candle[];
  indicators: IndicatorResult[];
  drawings: Drawing[];
  viewport: ChartViewport;
  /** Candles are rendered as a series of final + live-last candle. */
  symbol: string;
  interval: string;
}

export interface ResizeObserverConfig {
  width: number;
  height: number;
}

/** The mutable handle produced by a concrete adapter over its DOM container. */
export interface ChartHandle {
  render(input: ChartRenderInput): void;
  updateViewport(viewport: ChartViewport): void;
  resize(size: ResizeObserverConfig): void;
  setCursorListener(fn: (info: CursorInfo) => void): void;
  setDrawingListener?(fn: (drawing: Drawing) => void): void;
  dispose(): void;
}

export interface ChartAdapter {
  /** Create an adapter attached to a DOM element. */
  mount(container: HTMLElement, opts?: { theme?: string }): ChartHandle;
  /** Is this adapter implementation available in this runtime? */
  isSupported(): boolean;
}

/** Fake-safe factory type so the app can pick ECharts (or a mock in tests). */
export type ChartAdapterFactory = () => ChartAdapter;

/** Builds the ECharts option from domain data — exposed for unit testing. */
export interface OptionMapper {
  toOption(input: ChartRenderInput, extras?: unknown): unknown;
}
