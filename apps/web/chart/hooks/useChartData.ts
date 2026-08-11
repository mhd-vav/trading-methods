"use client";
/**
 * useChartData — manages the candle series, indicator computation, and derived
 * chart data. Owns error/stale/loading state and streams in updates.
 */
import { useMemo, useRef, useState, useCallback } from "react";
import type { Candle, CandleSeries, IndicatorConfig, IndicatorResult } from "@trading-desk/contracts";
import { computeIndicator, sliceToViewport, clampViewport } from "@trading-desk/chart-core";
import type { ChartViewport } from "@trading-desk/contracts";

export interface UseChartData {
  candles: Candle[];
  series: CandleSeries | null;
  indicators: IndicatorResult[];
  loading: boolean;
  /** Set to true when the last candle is stale (freshness exceeded). */
  stale: boolean;
  error: string | null;
  setSeries(input: CandleSeries): void;
  appendCandles(next: Candle[]): void;
  clear(): void;
  setIndicatorConfigs(configs: IndicatorConfig[]): void;
  viewport: ChartViewport;
  setViewport(v: ChartViewport): void;
  visible: Candle[];
}

const FIT_ALL: ChartViewport = { startIndex: 0, endIndex: Number.MAX_SAFE_INTEGER - 1, candleWidthPx: null };

/** Freshness threshold (ms) past which the marker flags the latest candle stale. */
const STALE_MS = 30_000;

export function useChartData(initial?: CandleSeries, stalenessMs = STALE_MS): UseChartData {
  const [series, setSeriesState] = useState<CandleSeries | null>(initial ?? null);
  const [loading, setLoading] = useState(initial == null);
  const [error, setError] = useState<string | null>(null);
  const [indicatorConfigs, setIndicatorConfigs] = useState<IndicatorConfig[]>([]);
  const [viewport, setViewport] = useState<ChartViewport>(FIT_ALL);
  const staleRef = useRef(false);

  const candles = useMemo(() => series?.candles ?? [], [series]);
  const indicators = useMemo(
    () => indicatorConfigs.map((cfg) => computeIndicator(candles, cfg)),
    [candles, indicatorConfigs],
  );

  // Staleness: derived from the newest candle's freshnessMs (recency of retrieval).
  const stale = useMemo(() => {
    if (!series || series.candles.length === 0) return false;
    const newest = series.candles[series.candles.length - 1];
    return newest.freshnessMs > stalenessMs || staleRef.current;
  }, [series, stalenessMs]);

  const visible = useMemo(() => sliceToViewport(candles, viewport), [candles, viewport]);

  const setSeries = useCallback(
    (input: CandleSeries) => {
      setSeriesState(input);
      setLoading(false);
      setError(null);
      staleRef.current = input.candles.some((c) => c.freshnessMs > stalenessMs);
    },
    [stalenessMs],
  );

  const appendCandles = useCallback((next: Candle[]) => {
    setSeriesState((prev) => {
      if (!prev) return prev;
      const merged = [...prev.candles];
      for (const c of next) {
        const idx = merged.findIndex((m) => m.id === c.id);
        if (idx === -1) merged.push(c);
        else merged[idx] = c;
      }
      return { ...prev, candles: merged };
    });
    staleRef.current = false;
  }, []);

  const clear = useCallback(() => {
    setSeriesState(null);
    setLoading(true);
    setError(null);
    staleRef.current = false;
    setViewport(FIT_ALL);
  }, []);

  const safeSetViewport = useCallback((v: ChartViewport) => {
    setViewport((prev) => clampViewport(v, prev.endIndex === Number.MAX_SAFE_INTEGER ? candles.length : candles.length));
  }, [candles.length]);

  return {
    candles,
    series,
    indicators,
    loading,
    stale,
    error,
    setSeries,
    appendCandles,
    clear,
    setIndicatorConfigs,
    viewport,
    setViewport: safeSetViewport,
    visible,
  };
}
