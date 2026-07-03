---
title: Heikin-Ashi
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: Japan (popularized West 2000s)
markets: all
timeframe: any (trend smoothing)
github_repo: mhd-vav/trading-methods
branch: heikin-ashi
---

# Heikin-Ashi

Heikin-Ashi ("average bar") is a modified candlestick charting method that smooths price into a synthetic series, dampening noise so trends read more clearly. Each Heikin-Ashi candle is computed from the prior candle and current OHLC, producing a continuous series where strong trends appear as long runs of same-colored bodies with small lower (uptrend) or upper (downtrend) wicks, and consolidation appears as doji-laden chop. It is a *visualization* technique — not a new data source — that makes trend regime and reversal points easier to spot than on raw [Candlestick Patterns](candlestick-patterns).

## The Formula

- HA Close = (Open + High + Low + Close) / 4
- HA Open = (prior HA Open + prior HA Close) / 2
- HA High = max(High, HA Open, HA Close)
- HA Low = min(Low, HA Open, HA Close)

The HA Open averages the prior HA values, introducing *lag* — the smoothing. The series is path-dependent (each candle depends on the previous).

## Reading Heikin-Ashi

- **Strong uptrend** — long green bodies, no lower wicks (gaps-down filled by the smoothing). Hold longs.
- **Strong downtrend** — long red bodies, no upper wicks.
- **Reversal warning** — small bodies with wicks on both sides (indecision) appearing after a run; a color change follows.
- **Consolidation** — alternating small bodies with both wicks; stand aside.

## Uses & Cautions

Heikin-Ashi is excellent as a trend filter and for reducing whipsaw exits (trail using HA color flips rather than raw candles). The critical caveat: **HA prices are synthetic and lag real price** — entries/exits must reference actual price levels, not HA values, and HA hides volatility (gaps/wicks) that matter for risk. It's a trend-reading overlay, not a replacement for the real chart. Pairs well with [Ichimoku Cloud](ichimoku) (fellow Japanese trend method) and [Moving Average](moving-average-crossover) systems.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| emreturan/heikin-ashi | 49 | Heikin-Ashi candlesticks for pandas DataFrame | https://github.com/emreturan/heikin-ashi |
| aprilyye/heikin-ashi-algo-trading | 20 | Algo trading utilizing Heikin-Ashi plotting | https://github.com/aprilyye/heikin-ashi-algo-trading |
| techietrader/Trading-indicators-and-Chart-patterns | 173 | ATR, SuperTrend, Heiken Ashi, Renko | https://github.com/techietrader/Trading-indicators-and-Chart-patterns |

## Relationships

Smoothing cousin of [Candlestick Patterns](candlestick-patterns); trend-filter for [Price Action](price-action), [Trend Following](trend-following), [Ichimoku Cloud](ichimoku), [Renko Trading](renko-trading).
