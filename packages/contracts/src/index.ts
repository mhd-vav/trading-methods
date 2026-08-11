/**
 * Canonical market-data & chart contracts (Phase 3 foundation, used by Phase 2).
 *
 * The Candle contract follows the audit's Phase 3 spec: provider, canonical
 * symbol, interval, exchange timezone, OHLCV, final/incomplete state, retrieval
 * time, freshness, adjustment method, quality warnings.
 */

/** GRANULARITY: candle intervals. */
export const Timeframes = [
  "1m", "5m", "15m", "1h", "4h", "1d", "1w",
] as const;
export type Timeframe = (typeof Timeframes)[number];

/** Providers the platform can source candles from. */
export type CandleProvider =
  | "coingecko"
  | "binance"
  | "oanda"
  | "forex-brs"
  | "manual-import"
  | "synthetic";

/** How a historical series was adjusted (drifts copyright/quality semantics). */
export type AdjustmentMethod =
  | "none"
  | "split"
  | "dividend"
  | "total-return"
  | "back-adjust";

/** Quality warnings surfaced per candle or per series. */
export type QualityWarning =
  | "gap"
  | "duplicate-timestamp"
  | "invalid-ohlc-relationship"
  | "zero-volume"
  | "possible-clock-drift"
  | "incomplete";

/** Canonical OHLCV candle. `id` is deterministic: `${provider}:${canonicalSymbol}:${interval}:${startMs}`. */
export interface Candle {
  id: string;
  provider: CandleProvider;
  /** The symbol as originally received from the provider. */
  originalSymbol: string;
  /** Normed symbol, e.g. "BTC/USDT", "EUR/USD". */
  canonicalSymbol: string;
  interval: Timeframe;
  exchangeTimezone: string;
  /** Unix epoch milliseconds of the candle open. */
  startMs: number;
  /** Unix epoch milliseconds of the candle close (usually startMs + interval). */
  endMs: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
  /** True when the candle is the current, still-forming one. */
  isFinal: boolean;
  /** When the data was retrieved from the provider. */
  retrievedAtMs: number;
  /** Freshness (ms since retrieval) — consumers flag stale data from this. */
  freshnessMs: number;
  adjustment: AdjustmentMethod;
  qualityWarnings: QualityWarning[];
}

/** A chart series is candles + the provenance header that produced them. */
export interface CandleSeries {
  candles: Candle[];
  symbol: string;
  interval: Timeframe;
  provider: CandleProvider;
  /** Epoch ms when the series was produced / last updated. */
  generatedAtMs: number;
}

// ---- Indicators ------------------------------------------------------------

export type IndicatorKind = "sma" | "ema" | "rsi" | "macd" | "atr" | "bollinger";

export interface IndicatorConfig {
  kind: IndicatorKind;
  /** Per-kind params, e.g. { period: 14 } or { fast: 12, slow: 26, signal: 9 }. */
  params: Record<string, number>;
}

/** A single point on an indicator output line. */
export interface IndicatorPoint {
  /** X axis — aligns to candle startMs (or its index when index-based). */
  x: number;
  y: number;
}

export interface IndicatorResult {
  kind: IndicatorKind;
  config: IndicatorConfig;
  /** Primary line. */
  line: IndicatorPoint[];
  /** Optional extra lines (e.g. signal line for MACD, mid for Bollinger). */
  extraLines?: { name: string; points: IndicatorPoint[] }[];
  /** Optional bands (e.g. Bollinger upper/lower). */
  bands?: { upper: IndicatorPoint[]; lower: IndicatorPoint[] };
  /** Quality / computation warnings. */
  warnings?: (QualityWarning | string)[];
}

// ---- Drawings --------------------------------------------------------------

export type DrawingTool =
  | "trendline"
  | "horizontal-line"
  | "ray"
  | "fibonacci"
  | "rectangle"
  | "text"
  | "arrow";

export interface Drawing {
  id: string;
  tool: DrawingTool;
  /** Anchor points, in chart (index, price) coordinates. */
  points: { x: number; y: number }[];
  label?: string;
  color?: string;
  locked?: boolean;
  visible?: boolean;
  createdAtMs: number;
  updatedAtMs: number;
}

// ---- Layout / viewport / presets -------------------------------------------

/** Persisted visible range + indicator set for a symbol. */
export interface ChartLayout {
  id: string;
  symbol: string;
  /** Visible candle range [startIndex, endIndex] (nullable = fit all). */
  range: { startIndex: number | null; endIndex: number | null } | null;
  indicators: IndicatorConfig[];
  drawings: Drawing[];
  updatedAtMs: number;
}

export interface ChartViewport {
  startIndex: number;
  endIndex: number;
  /** Candle width in px, or null for auto. */
  candleWidthPx: number | null;
}

/** A saved, named indicator preset (persisted server-side in Phase 5). */
export interface IndicatorPreset {
  id: string;
  name: string;
  indicators: IndicatorConfig[];
}

export interface WatchlistEntry {
  symbol: string;
  interval: Timeframe;
}

// ---- Market replay ---------------------------------------------------------

export interface ReplayState {
  active: boolean;
  cursorIndex: number;
  playheadMs: number;
  speed: number;
}
