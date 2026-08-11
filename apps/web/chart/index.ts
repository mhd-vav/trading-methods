"use client";
/**
 * Chart package barrel — the Phase 2 chart-facing public API.
 *
 * Consumers (pages/other components) import from here. ECharts themselves are
 * only reachable through `adapters/echarts`, keeping the rest of the app
 * decoupled from the rendering library.
 */
export { ChartContainer } from "./ChartContainer";
export { ChartRenderer } from "./ChartRenderer";
export { ChartToolbar } from "./ChartToolbar";
export { DrawingLayer } from "./DrawingLayer";
export { IndicatorPane } from "./IndicatorPane";
export { VolumePane } from "./VolumePane";

export { useChartData } from "./hooks/useChartData";
export { useChartViewport, viewportFromLayout } from "./hooks/useChartViewport";
export { useDrawingState } from "./hooks/useDrawingState";

export * from "./adapters/types";
export { createEChartsAdapter, buildOption } from "./adapters/echarts";
