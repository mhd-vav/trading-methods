"use client";
/**
 * useChartViewport — manages the visible candle range and smooths ECharts
 * dataZoom events into React state, avoiding render-on-every-pixel.
 * Optimistic updates + (optional) persistence callback.
 */
import { useCallback, useRef, useState } from "react";
import type { ChartLayout, ChartViewport } from "@trading-desk/contracts";
import { clampViewport } from "@trading-desk/chart-core";

export interface UseChartViewport {
  viewport: ChartViewport;
  setRange(startIndex: number, endIndex: number): void;
  /** Debounced callback to notify persistence (Phase 5 server-save). */
  persist: () => void;
  fitAll(length: number): void;
}

export interface ViewportOptions {
  onPersist?: (viewport: ChartViewport) => void;
  debounceMs?: number;
}

export function useChartViewport(
  length: number,
  initial: ChartViewport = { startIndex: 0, endIndex: length - 1 || 0, candleWidthPx: null },
  opts: ViewportOptions = {},
): UseChartViewport {
  const [viewport, setViewport] = useState<ChartViewport>(() => clampViewport(initial, Math.max(length, 1)));
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const setRange = useCallback(
    (startIndex: number, endIndex: number) => {
      setViewport((prev) => clampViewport({ ...prev, startIndex, endIndex }, Math.max(length, 1)));
    },
    [length],
  );

  const fitAll = useCallback(
    (len: number) => {
      setViewport({ startIndex: 0, endIndex: Math.max(0, len - 1), candleWidthPx: null });
    },
    [],
  );

  const persist = useCallback(() => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      opts.onPersist?.(viewport);
    }, opts.debounceMs ?? 300);
  }, [opts, viewport]);

  return { viewport, setRange, persist, fitAll };
}

/** Helper to read a persisted viewport back from a stored ChartLayout. */
export function viewportFromLayout(layout: ChartLayout | null, length: number): ChartViewport {
  if (!layout?.range) return { startIndex: 0, endIndex: Math.max(0, length - 1), candleWidthPx: null };
  const start = layout.range.startIndex ?? 0;
  const end = layout.range.endIndex ?? Math.max(0, length - 1);
  return clampViewport({ startIndex: start, endIndex: end, candleWidthPx: null }, Math.max(length, 1));
}
