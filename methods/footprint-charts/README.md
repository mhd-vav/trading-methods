---
title: Footprint Charts
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: 2000s–present (TradeTheSpread, MarketDelta, exocharts)
markets: futures (most), crypto, equities
timeframe: intraday (per-bar)
github_repo: mhd-vav/trading-methods
branch: footprint-charts
---

# Footprint Charts

Footprint charts (cluster charts) decompose each price bar into per-tick-level bid/ask volume, revealing the *internal structure* a candle hides: how much volume traded at each price, split into aggressive-buy vs aggressive-sell. Where a candle shows OHLC, a footprint shows the battle inside the bar — the imbalances, the point of control (POC), and the cumulative delta. It is the primary visualization tool of [Order Flow Trading](order-flow) and the modern successor to [Tape Reading](tape-reading).

## What the Footprint Shows

- **Bid/ask volume per price level** — each row of the bar shows buy-volume vs sell-volume at that tick.
- **Imbalances** — a level where one side dominates massively (e.g., 3× more buys) marks aggressive absorption or initiation.
- **POC (Point of Control)** — the price level with the most volume in the bar; the fairest price, a magnet. Shared with [Market Profile](market-profile).
- **Delta & cumulative delta** — buy minus sell volume per bar; divergence (price up, delta down) signals exhaustion.
- **Stacked imbalances** — 3+ consecutive same-side-dominant levels; institutional footprints, often S/R.

## Key Setups

- **Absorption reversal** — huge sell delta but price holds (buyer absorbing); reversal when sellers exhaust.
- **Delta divergence** — new price high on falling delta; buyers exhausted; short on confirmation.
- **Breakout validation** — breakout with stacked buy imbalances = genuine; weak delta = fakeout.

Footprint trading requires tick data and liquid instruments (futures, crypto majors). It is a *confirmation/trigger* layer best combined with structure ([Supply & Demand](supply-demand), [Smart Money Concepts](smc-ict)) and [Market Profile](market-profile) context.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| murtazayusuf/OrderflowChart | 244 | Plot orderflow footprint charts (plotly, Python) | https://github.com/murtazayusuf/OrderflowChart |
| beinghorizontal/Footprint_Chart_Plotly | 5 | Interactive footprint chart (Plotly), intraday AMT | https://github.com/beinghorizontal/Footprint_Chart_Plotly |
| mahmoud20138/OrderFlow-Analysis-Pro | 16 | Footprint charts, delta analytics, volume profile | https://github.com/mahmoud20138/OrderFlow-Analysis-Pro |
| endegenaassefa/footprint_analyzer | 7 | Python engine for footprint charts from tick data | https://github.com/endegenaassefa/footprint_analyzer |

## Relationships

Primary tool of [Order Flow Trading](order-flow); modern [Tape Reading](tape-reading); shares POC/value-area logic with [Market Profile](market-profile) and [Auction Market Theory](auction-market-theory).
