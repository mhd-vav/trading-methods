# Phase 2 — Charting Architecture

Status: **implemented & tested** for the framework-agnostic core + ECharts adapter
in this pass. ECharts 6.1.0 is kept behind an internal adapter; no code outside
`chart/adapters/echarts.ts` imports ECharts.

## What was built

### Contracts (`packages/contracts`)
Canonical `Candle`, `CandleSeries`, `IndicatorConfig/Result`, `Drawing`,
`ChartLayout`, `ChartViewport`, `IndicatorPreset`, `WatchlistEntry`,
`ReplayState` — the Phase 3 candle contract lives here too.

### Chart core (`packages/chart-core`) — deterministic & pure
- Indicators: **SMA, EMA, RSI, MACD, ATR, Bollinger Bands** (`indicators.ts`)
- Transforms: viewport clamps/slicing, **min-max sampling** (ECharts dense-series
  pattern), OHLC array split (`transforms.ts`)
- **25 tests passing**, all deterministic (hand-computed + property assertions).

### Web chart (`apps/web/chart`) — replaces the 1,212-line monolith
```
chart/
├── ChartContainer.tsx      composition root
├── ChartRenderer.tsx       owns adapter instance + lifecycle
├── ChartToolbar.tsx        intervals, tools, indicator add, fit, save
├── DrawingLayer.tsx        interactive SVG markup overlay
├── IndicatorPane.tsx       main-pane indicator readouts
├── VolumePane.tsx          volume/ATR readout
├── hooks/
│   ├── useChartData.ts     candles + indicator computation + stale/loading
│   ├── useChartViewport.ts viewport + debounced persistence
│   └── useDrawingState.ts  drawings CRUD/select/lock/visibility + persistence
└── adapters/
    ├── types.ts            ChartAdapter/ChartHandle interface (framework-agnostic)
    └── echarts.ts          concrete ECharts 6.1.0 implementation
```
- **6 tests** for the pure option mapper + viewport helpers.

## ECharts performance patterns applied
- `dataZoom` (inside + slider) for navigation.
- Min-max sampling + `progressive` rendering for dense series.
- Animation **disabled** at/above `DENSE_THRESHOLD = 10,000` candles.
- Correct `ResizeObserver` resize + `dispose()` lifecycle (no leaks).
- Crosshair axis linking + precise OHLC tooltip.

## Distributed across later phases (per plan)
- Server persistence of layouts/drawings → Phase 5 (`core-api`).
- Historical pagination/progressive loading, SSE/WebSocket streaming, replay,
  PNG export → Phase 3 (provider/ingestion) + Phase 4 (streaming).
- Playwright e2e (drawing/zoom/symbol/persistence) → Phase 7 harness
  (`tests/e2e`), gated on the real `apps/web` being imported.

## Verification
- `packages/chart-core`: `npm test` → 25 passed; `npm run typecheck` clean.
- `apps/web`: `npm test` → 6 passed; `npm run typecheck` clean.

## Note on the replaced file
`MarketChart.tsx` (1,212 lines) lives only on the local Windows checkout
(blocked). This directory is the reconciled replacement and will supercede it
when `apps/web` is imported in Phase 0 follow-up.
