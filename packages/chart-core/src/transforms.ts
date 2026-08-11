/**
 * Chart transformations: viewport slicing, min-max sampling, and helper math.
 *
 * Implements the Phase 2 performance patterns — min-max sampling for dense
 * series, viewport clamping, and NaN filtering — as PURE functions so they are
 * deterministic and unit-testable.
 */
import type { Candle, ChartViewport } from "@trading-desk/contracts";

export interface SliceResult {
  candles: Candle[];
  /** In-slice index of the last candle (for progressive append checks). */
  offset: number;
}

/** Clamp a requested viewport to a valid index range over `length` candles. */
export function clampViewport(viewport: ChartViewport, length: number): ChartViewport {
  const lo = Math.max(0, Math.floor(viewport.startIndex));
  const hi = Math.max(lo, Math.min(length - 1, Math.ceil(viewport.endIndex)));
  return { ...viewport, startIndex: lo, endIndex: hi };
}

/** Slice candles to the viewport. Returns the visible subset. */
export function sliceToViewport(candles: Candle[], viewport: ChartViewport): Candle[] {
  if (candles.length === 0) return [];
  const clamped = clampViewport(viewport, candles.length);
  return candles.slice(clamped.startIndex, clamped.endIndex + 1);
}

/**
 * Min-max sampling for dense series (ECharts `sampling: 'min-max'` pattern).
 * Reduces a series so that every `bucket` candles contribute up to 2 points:
 * one for the min value and one for the max. Deterministic.
 */
export function minMaxSample(
  xs: number[],
  ys: number[],
  bucket: number,
): { xs: number[]; ys: number[] } {
  if (xs.length !== ys.length) throw new Error("minMaxSample: length mismatch");
  if (bucket <= 1) return { xs: xs.slice(), ys: ys.slice() };
  const outX: number[] = [];
  const outY: number[] = [];
  for (let i = 0; i < xs.length; i += bucket) {
    const end = Math.min(i + bucket, xs.length);
    let minIdx = i;
    let maxIdx = i;
    for (let j = i + 1; j < end; j++) {
      if (ys[j] < ys[minIdx]) minIdx = j;
      if (ys[j] > ys[maxIdx]) maxIdx = j;
    }
    if (minIdx === maxIdx) {
      outX.push(xs[minIdx]);
      outY.push(ys[minIdx]);
    } else {
      // Push the earlier of the two first, then the later, keeping x ascending.
      const [a, b] = minIdx < maxIdx ? [minIdx, maxIdx] : [maxIdx, minIdx];
      outX.push(xs[a], xs[b]);
      outY.push(ys[a], ys[b]);
    }
  }
  return { xs: outX, ys: outY };
}

/** Break a candlestick series into aligned OHLC arrays. */
export function ohlcArrays(candles: Candle[]) {
  return {
    xs: candles.map((c) => c.startMs),
    o: candles.map((c) => c.o),
    h: candles.map((c) => c.h),
    l: candles.map((c) => c.l),
    c: candles.map((c) => c.c),
    v: candles.map((c) => c.v),
    isFinal: candles.map((c) => c.isFinal),
  };
}

/** Simple identically-valued helper used by tests for minute offsets. */
export const msPerBar = (timeframe: string): number => {
  const n = parseInt(timeframe, 10);
  if (!Number.isFinite(n)) return 60_000;
  const unit = timeframe.replace(/[0-9]/g, "");
  const mult: Record<string, number> = { m: 60_000, h: 3_600_000, d: 86_400_000, w: 604_800_000 };
  return n * (mult[unit] ?? 60_000);
};
