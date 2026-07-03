---
title: VWAP Trading
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: 1990s (institutional execution) → retail 2010s
markets: equities (most), futures, crypto
timeframe: intraday (session-based)
github_repo: mhd-vav/trading-methods
branch: vwap-trading
---

# VWAP Trading

VWAP (Volume-Weighted Average Price) is the intraday benchmark of institutional execution and a dynamic support/resistance for discretionary intraday traders. It is the ratio of value traded (price × volume) to total volume, cumulated over a session, producing a single line that represents the day's average price weighted by where the most volume occurred. Institutional desks execute large orders to *minimize slippage vs VWAP* (benchmark execution); intraday traders read VWAP as the day's "fair value" — price above VWAP is bullish (buyers paying up), below is bearish, and VWAP itself is a magnet and S/R that mean-reverts.

## The VWAP Line

- Session VWAP resets each day; it's the cumulative value/volume from the open.
- It is *volume-weighted*, so it's pulled toward high-volume price levels (the day's accepted value) — unlike a simple MA.
- **Standard-deviation bands** (VWAP ±1σ, ±2σ) act as dynamic overbought/oversold and S/R.

## Trading VWAP

- **Mean reversion to VWAP** — price stretched to ±2σ bands tends to revert to VWAP (the fair-value magnet). Fade extremes toward VWAP.
- **VWAP as S/R** — VWAP holding as support (price above, dips bought at VWAP) = bullish intraday; VWAP as resistance = bearish.
- **VWAP reclaim/lose** — reclaiming VWAP after losing it is an intraday trend-change; losing VWAP after holding is bearish.
- **VWAP bounce** — in a trend, pullbacks to VWAP that hold are continuation entries.
- **Anchored VWAP** — reset from a specific event (earnings, swing high/low) rather than the session open; tracks the average price *since* the anchor, used by [Smart Money Concepts](smc-ict) and [Supply & Demand](supply-demand) traders to find institutional cost basis.

## Uses & Cautions

VWAP is the gold-standard intraday benchmark and S/R on liquid equities/futures. Cautions: it's *session-based* (resets daily) so it's intraday-only; on illiquid instruments it's noisy; and it lags (cumulative), so it's a reference magnet, not a leading signal. Best combined with [Market Profile](market-profile)/[Auction Market Theory](auction-market-theory) (value area) and [Order Flow](order-flow).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| naimkatiman/tradeclaw | 34 | Self-hosted AI trading signals, VWAP strategy presets | https://github.com/naimkatiman/tradeclaw |
| Taqhee/BTC_TradingBot | 20 | Bot using KVO/Signal and VWAP strategies | https://github.com/Taqhee/BTC_TradingBot |
| J232005/5-Indicator-trading-tool | 0 | Intraday engine: Market Structure, VWAP, Volume Profile | https://github.com/J232005/5-Indicator-trading-tool |
| bukosabino/ta | 5106 | TA library with VWAP support | https://github.com/bukosabino/ta |

## Relationships

Intraday value benchmark shared with [Market Profile](market-profile) and [Auction Market Theory](auction-market-theory); anchored VWAP used in [Smart Money Concepts](smc-ict) and [Supply & Demand](supply-demand); execution benchmark for [TWAP/VWAP/POV execution](execution-algorithms).
