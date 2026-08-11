/**
 * Deterministic indicator calculations.
 *
 * All functions are PURE: given the same candles + config they return the same
 * result. This is what makes Phase 2's "deterministic calculation tests" (and
 * later golden evaluation datasets) possible.
 *
 * Coordinates: indicator points are indexed by candle position (x = index),
 * which keeps the math simple and lets the ECharts adapter map to timestamps.
 */
import type { Candle, IndicatorConfig, IndicatorPoint, IndicatorResult } from "@trading-desk/contracts";

export type PriceSource = (c: Candle) => number;
export const close: PriceSource = (c) => c.c;
export const high: PriceSource = (c) => c.h;
export const low: PriceSource = (c) => c.l;
export const typical: PriceSource = (c) => (c.h + c.l + c.c) / 3;

/** NaN-guarded arithmetic helpers. */
const clamp01 = (n: number) => (Number.isFinite(n) ? Math.max(0, Math.min(1, n)) : 0);
const round = (n: number, dp = 6) => {
  if (!Number.isFinite(n)) return NaN;
  const f = 10 ** dp;
  return Math.round(n * f) / f;
};

/** Simple Moving Average. Output has (n-1) leading holes (undefined). */
export function sma(values: number[], period: number, dp = 6): (number | null)[] {
  const out: (number | null)[] = new Array(values.length).fill(null);
  if (period <= 0) return out;
  let sum = 0;
  for (let i = 0; i < values.length; i++) {
    sum += values[i];
    if (i >= period) sum -= values[i - period];
    if (i >= period - 1) out[i] = round(sum / period, dp);
  }
  return out;
}

/** Exponential Moving Average. Seed = SMA of first `period` points. */
export function ema(values: number[], period: number, dp = 6): (number | null)[] {
  const out: (number | null)[] = new Array(values.length).fill(null);
  if (period <= 0 || values.length < period) return out;
  const k = 2 / (period + 1);
  let seed = 0;
  for (let i = 0; i < period; i++) seed += values[i];
  out[period - 1] = round(seed / period, dp);
  for (let i = period; i < values.length; i++) {
    out[i] = round(values[i] * k + (out[i - 1] as number) * (1 - k), dp);
  }
  return out;
}

/**
 * Wilder's RSI (using SMA smoothing of gains/losses). Returns values in [0,100]
 * with nulls for the warm-up window.
 */
export function rsi(values: number[], period = 14, dp = 6): (number | null)[] {
  const out: (number | null)[] = new Array(values.length).fill(null);
  if (values.length <= period) return out;
  let avgGain = 0;
  let avgLoss = 0;
  for (let i = 1; i <= period; i++) {
    const change = values[i] - values[i - 1];
    avgGain += Math.max(change, 0);
    avgLoss += Math.max(-change, 0);
  }
  avgGain /= period;
  avgLoss /= period;
  out[period] = round(100 - 100 / (1 + (avgLoss === 0 ? Infinity : avgGain / avgLoss)), dp);
  for (let i = period + 1; i < values.length; i++) {
    const change = values[i] - values[i - 1];
    avgGain = (avgGain * (period - 1) + Math.max(change, 0)) / period;
    avgLoss = (avgLoss * (period - 1) + Math.max(-change, 0)) / period;
    const rs = avgLoss === 0 ? Infinity : avgGain / avgLoss;
    out[i] = round(100 - 100 / (1 + rs), dp);
  }
  return out;
}

/** True Range from consecutive candles; needs high/low/close arrays aligned to candles. */
export function trueRange(highs: number[], lows: number[], closes: number[]): number[] {
  const out: number[] = new Array(highs.length).fill(0);
  for (let i = 0; i < highs.length; i++) {
    if (i === 0) {
      out[i] = highs[i] - lows[i];
    } else {
      const prevClose = closes[i - 1];
      out[i] = Math.max(
        highs[i] - lows[i],
        Math.abs(highs[i] - prevClose),
        Math.abs(lows[i] - prevClose),
      );
    }
  }
  return out;
}

/** Average True Range (Wilder smoothing via EMA). */
export function atr(candles: Candle[], period = 14, dp = 6): (number | null)[] {
  const highs = candles.map(high);
  const lows = candles.map(low);
  const closes = candles.map(close);
  const tr = trueRange(highs, lows, closes);
  // ATR = EMA of TR with Wilder k = 1/period.
  return ema(tr, period, dp);
}

/** MACD. Returns macd line, signal line, and histogram. Nulls during warm-up. */
export function macd(
  values: number[],
  fast = 12,
  slow = 26,
  signal = 9,
  dp = 6,
): { macd: (number | null)[]; signal: (number | null)[]; hist: (number | null)[] } {
  const emaFast = ema(values, fast, 12);
  const emaSlow = ema(values, slow, 12);
  const macdLine: (number | null)[] = values.map((_, i) =>
    emaFast[i] != null && emaSlow[i] != null ? round((emaFast[i] as number) - (emaSlow[i] as number), dp) : null,
  );
  // Build signal over non-null macd segment.
  const firstIdx = macdLine.findIndex((v) => v != null);
  const valid = macdLine.slice(firstIdx).map((v) => v as number);
  const sigValid = ema(valid, signal, 12);
  const signalLine: (number | null)[] = new Array(values.length).fill(null);
  for (let i = 0; i < sigValid.length; i++) signalLine[firstIdx + i] = sigValid[i];
  const hist: (number | null)[] = values.map((_, i) =>
    macdLine[i] != null && signalLine[i] != null
      ? Math.round(((macdLine[i] as number) - (signalLine[i] as number)) * 10 ** dp) / 10 ** dp
      : null,
  );
  return { macd: macdLine, signal: signalLine, hist };
}

/** Bollinger Bands: mid = SMA(close), upper/lower = mid ± k*stddev. */
export function bollinger(
  values: number[],
  period = 20,
  k = 2.0,
  dp = 6,
): { mid: (number | null)[]; upper: (number | null)[]; lower: (number | null)[] } {
  const mid = sma(values, period, dp);
  const upper: (number | null)[] = new Array(values.length).fill(null);
  const lower: (number | null)[] = new Array(values.length).fill(null);
  for (let i = period - 1; i < values.length; i++) {
    const slice = values.slice(i - period + 1, i + 1);
    const mean = slice.reduce((a, b) => a + b, 0) / period;
    const variance = slice.reduce((a, b) => a + (b - mean) ** 2, 0) / period;
    const std = Math.sqrt(variance);
    upper[i] = round(mean + k * std, dp);
    lower[i] = round(mean - k * std, dp);
  }
  return { mid, upper, lower };
}

// ---- Unified entry point ---------------------------------------------------

/**
 * Compute an indicator from a candle series using an IndicatorConfig.
 * Returns a normalized IndicatorResult ready for the chart adapter.
 */
export function computeIndicator(candles: Candle[], config: IndicatorConfig): IndicatorResult {
  const n = candles.length;
  const toPoints = (arr: (number | null)[]): IndicatorPoint[] =>
    arr
      .map((y, i) => (y == null ? null : { x: i, y }))
      .filter((p): p is IndicatorPoint => p !== null);

  switch (config.kind) {
    case "sma": {
      const p = config.params["period"] ?? 14;
      return { kind: "sma", config, line: toPoints(sma(candles.map(close), p)) };
    }
    case "ema": {
      const p = config.params["period"] ?? 14;
      return { kind: "ema", config, line: toPoints(ema(candles.map(close), p)) };
    }
    case "rsi": {
      const p = config.params["period"] ?? 14;
      return { kind: "rsi", config, line: toPoints(rsi(candles.map(close), p)) };
    }
    case "macd": {
      const fast = config.params["fast"] ?? 12;
      const slow = config.params["slow"] ?? 26;
      const sig = config.params["signal"] ?? 9;
      const { macd: m, signal: s, hist } = macd(candles.map(close), fast, slow, sig);
      return {
        kind: "macd",
        config,
        line: toPoints(m),
        extraLines: [{ name: "signal", points: toPoints(s) }, { name: "hist", points: toPoints(hist) }],
      };
    }
    case "atr": {
      const p = config.params["period"] ?? 14;
      return { kind: "atr", config, line: toPoints(atr(candles, p)) };
    }
    case "bollinger": {
      const p = config.params["period"] ?? 20;
      const k = config.params["multiplier"] ?? 2.0;
      const { mid, upper, lower } = bollinger(candles.map(close), p, k);
      return {
        kind: "bollinger",
        config,
        line: toPoints(mid),
        bands: { upper: toPoints(upper), lower: toPoints(lower) },
      };
    }
    default:
      return { kind: "sma", config, line: [], warnings: ["invalid-indicator-kind"] };
  }
}

export { clamp01 };
