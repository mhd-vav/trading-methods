---
title: Moving Average Crossover
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
era: 1970s–present
markets: all
timeframe: any (swing/position most common)
github_repo: mhd-vav/trading-methods
branch: moving-average-crossover
---

# Moving Average Crossover

Moving average crossover is the simplest systematic trend-following method: trade when a fast moving average crosses a slow one — a "golden cross" (fast above slow, bullish) or "death cross" (fast below slow, bearish). It is the canonical example of a trend-following rule and the gateway strategy for most algorithmic traders. Its appeal is mechanical objectivity and the fact that it is, by construction, always in the market and always aligned with the trend. Its weakness — shared by all trend-following — is whipsaw losses in ranging markets, where crossovers fire repeatedly without a trend developing.

## The Mechanics

- **Simple MA (SMA)** — arithmetic mean of last N closes; equal weight.
- **Exponential MA (EMA)** — weighted toward recent prices; faster reaction, less lag.
- **Crossover signal** — fast MA (e.g., 20/50) crosses slow MA (e.g., 50/200). The 50/200 crossover on daily charts is the famous golden/death cross.
- **Price-vs-MA** — price crossing an MA (e.g., price > 200-day MA = bullish regime) is a simpler variant.

## Strategy Variants

- **Dual-MA crossover** — fast crosses slow; enter on cross, exit on opposite cross. Always in market.
- **Triple-MA** (e.g., 4/9/18) — adds a filter; trade only when fast and medium align above/below slow.
- **MA ribbon** — multiple MAs; trend strength read by their spread/fan.
- **EMA vs SMA** — EMA reduces lag, gives earlier signals but more false ones; SMA smoother but later.

## The Core Tradeoff: Lag vs Whipsaw

MA length is a lag/whipsaw dial. Long MAs (200) lag badly (late entries/exits) but filter noise. Short MAs (10/20) react fast but whipsaw in chop. No length is "best" — it's regime-dependent. The profitability of crossover systems depends almost entirely on the fraction of trending vs ranging market in the backtest; they bleed in ranges and profit in trends. This is why they're paired with regime filters (ADX, see below) or [Trend Following](trend-following) position-sizing.

## Risk Management

- **Whipsaw control** — require a close-beyond confirmation, or add a regime filter (only trade crossovers when ADX > 25, i.e., a trend exists).
- **Trailing exits** — exit on opposite cross OR a faster MA cross (hybrid).
- **Volatility sizing** — size by ATR so chop periods risk less per whipsaw.
- **Timeframe alignment** — trade the LTF crossover only in the direction of the HTF MA regime.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| bideeen/Building-A-Trading-Strategy-With-Python | 64 | MA crossover strategy build in Python | https://github.com/bideeen/Building-A-Trading-Strategy-With-Python |
| pratiknabriya/Moving-Average-Crossover-Trading-Strategy-with-Python | 34 | Buy/sell signals via SMA crossover | https://github.com/pratiknabriya/Moving-Average-Crossover-Trading-Strategy-with-Python |
| cinar/indicator | 1199 | Go TA indicators incl. MA/crossover | https://github.com/cinar/indicator |
| bukosabino/ta | 5106 | TA library with MA indicators | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- Perry Kaufman — *Trading Systems and Methods* (the systematic-trading encyclopedia)
- John Murphy — *Technical Analysis of the Financial Markets*

## Relationships

Simplest [Trend Following](trend-following); shares lag/whipsaw with [MACD](macd); filtered by [ADX](adx); trend-filter for [Price Action](price-action) and [Ichimoku Cloud](ichimoku) (Tenkan/Kijun are MA-like midpoints).
