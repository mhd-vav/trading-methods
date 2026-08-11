"use client";
/**
 * ChartRenderer — owns one ECharts instance (via the adapter) and its full
 * lifecycle: mount, render, resize (ResizeObserver), cursor events, dispose.
 * It is the ONLY component that touches the adapter.
 */
import { useEffect, useRef, useCallback } from "react";
import type { Candle, ChartViewport, Drawing, IndicatorResult } from "@trading-desk/contracts";
import type { ChartAdapter, CursorInfo } from "./adapters/types";
import { createEChartsAdapter } from "./adapters/echarts";

export interface ChartRendererProps {
  candles: Candle[];
  indicators: IndicatorResult[];
  drawings: Drawing[];
  viewport: ChartViewport;
  symbol: string;
  interval: string;
  onCursor?: (info: CursorInfo) => void;
  adapter?: ChartAdapter; // injectable for tests/mocks
  className?: string;
}

export function ChartRenderer({
  candles,
  indicators,
  drawings,
  viewport,
  symbol,
  interval,
  onCursor,
  adapter,
  className,
}: ChartRendererProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const adapterRef = useRef<ChartAdapter>(adapter ?? createEChartsAdapter());
  const handleRef = useRef<ReturnType<ChartAdapter["mount"]> | null>(null);
  const onCursorRef = useRef(onCursor);
  onCursorRef.current = onCursor;

  // Mount once.
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const handle = adapterRef.current.mount(el, { theme: "dark" });
    handleRef.current = handle;
    handle.setCursorListener((info) => onCursorRef.current?.(info));

    const ro = new ResizeObserver(() => {
      if (handleRef.current && el.clientWidth && el.clientHeight) {
        handleRef.current.resize({ width: el.clientWidth, height: el.clientHeight });
      }
    });
    ro.observe(el);

    return () => {
      ro.disconnect();
      handleRef.current?.dispose();
      handleRef.current = null;
    };
  }, [adapterRef]);

  // Render on data/viewport change.
  useEffect(() => {
    handleRef.current?.render({ candles, indicators, drawings, viewport, symbol, interval });
  }, [candles, indicators, drawings, viewport, symbol, interval]);

  return <div ref={containerRef} className={className} style={{ width: "100%", height: "100%" }} />;
}
