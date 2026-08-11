"use client";
/**
 * ChartContainer — composition root for the chart. Wires the data hook, viewport
 * hook, and drawing hook together and renders the toolbar + renderer + panes.
 * This replaces the previous monolithic component.
 */
import { useMemo, useCallback } from "react";
import type { CandleSeries, IndicatorConfig, IndicatorKind, Timeframe } from "@trading-desk/contracts";
import { useChartData } from "./hooks/useChartData";
import { useChartViewport } from "./hooks/useChartViewport";
import { useDrawingState } from "./hooks/useDrawingState";
import { ChartRenderer } from "./ChartRenderer";
import { ChartToolbar } from "./ChartToolbar";
import { VolumePane } from "./VolumePane";
import { IndicatorPane } from "./IndicatorPane";
import { DrawingLayer } from "./DrawingLayer";
import type { CursorInfo } from "./adapters/types";

export interface ChartContainerProps {
  initialSeries?: CandleSeries;
  initialSymbol?: string;
  initialInterval?: Timeframe;
  onPersistViewport?: (v: ReturnType<typeof useChartViewport>["viewport"]) => void;
  onPersistDrawings?: (d: ReturnType<typeof useDrawingState>["drawings"]) => void;
  /** Streaming updater (SSE/WebSocket) — Phase 3/4 wires this to providers. */
  onSubscribe?: (symbol: string, interval: Timeframe) => () => void;
}

export function ChartContainer({
  initialSeries,
  initialSymbol = "BTC/USDT",
  initialInterval = "4h",
  onPersistViewport,
  onPersistDrawings,
  onSubscribe,
}: ChartContainerProps) {
  const data = useChartData(initialSeries);
  const viewportModel = useChartViewport(data.candles.length, undefined, { onPersist: onPersistViewport });
  const drawings = useDrawingState({ onPersist: onPersistDrawings });

  // Indicator panes to render (distinct kinds among current configs).
  const mainIndicators = useMemo(() => data.indicators.filter((i) => i.kind !== "atr"), [data.indicators]);
  const volumeIndicators = useMemo(() => data.indicators.filter((i) => i.kind === "atr"), [data.indicators]);

  const handleCursor = useCallback((info: CursorInfo) => {
    // Optionally surface the OHLC tooltip elsewhere (e.g. a readout bar).
    void info;
  }, []);

  const addIndicator = useCallback(
    (kind: IndicatorKind) => {
      const params: Record<string, number> =
        kind === "macd" ? { fast: 12, slow: 26, signal: 9 }
        : kind === "bollinger" ? { period: 20, multiplier: 2 }
        : { period: kind === "rsi" || kind === "atr" ? 14 : 20 };
      const cfg: IndicatorConfig = { kind, params };
      data.setIndicatorConfigs([...data.indicators.map((i) => i.config).filter((c) => c.kind !== kind), cfg]);
    },
    [data],
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", minHeight: 0 }}>
      <ChartToolbar
        symbol={initialSymbol}
        interval={initialInterval}
        onInterval={(iv) => onSubscribe?.(initialSymbol, iv)}
        drawingTool={drawings.tool}
        onDrawingTool={drawings.setTool}
        onAddIndicator={addIndicator}
        onClearIndicator={() => data.setIndicatorConfigs([])}
        onFitAll={() => viewportModel.fitAll(data.candles.length)}
        hasDrawingChanges={drawings.hasChanges}
        onSaveDrawings={drawings.persist}
      />
      <div style={{ position: "relative", flex: 1, minHeight: 0 }}>
        <ChartRenderer
          candles={data.candles}
          indicators={data.indicators}
          drawings={drawings.drawings}
          viewport={viewportModel.viewport}
          symbol={initialSymbol}
          interval={initialInterval}
          onCursor={handleCursor}
        />
        <DrawingLayer
          drawings={drawings.drawings}
          selectedId={drawings.selectedId}
          onSelect={drawings.select}
          onAdd={drawings.addDrawing}
          tool={drawings.tool}
        />
      </div>
      {mainIndicators.length > 0 && <IndicatorPane indicators={mainIndicators} />}
      {volumeIndicators.length > 0 && <VolumePane indicators={volumeIndicators} />}
    </div>
  );
}