---
title: Cross-Sectional Momentum
type: method
domain: trading
category: Quantitative & Statistical Strategies
tier: 3
importance: moderate
markets: equities, futures, crypto
timeframe: weeks–months (lookback 3–12m)
github_repo: mhd-vav/trading-methods
branch: cross-sectional-momentum
---

# Cross-Sectional Momentum

Cross-sectional momentum (the academic foundation of "relative strength" investing) ranks a universe of assets by their past returns over a lookback (typically 3–12 months) and goes **long the top decile / quintile and short the bottom**, dollar- or beta-neutral. Unlike [Time-series Momentum](time-series-momentum), which takes a directional view per asset, cross-sectional momentum is explicitly relative — it only cares that winners beat losers within the cross-section, regardless of whether the whole market rises or falls. The Jegadeesh-Titman (1993) study is the canonical evidence: a long-short decile portfolio earned ~12%/yr historically. It is a market-neutral expression of the [Trend Following](trend-following) anomaly, formalized for institutional long-short equity portfolios.

## Mechanics

- **Lookback** — rank assets by cumulative return over the past 3, 6, or 12 months (skip the most recent month to avoid short-term reversal contamination).
- **Long-short construction** — buy the top K%, sell the bottom K%, equal- or volatility-weighted, rebalanced monthly or quarterly. The portfolio is constructed to be beta-neutral (longs and shorts offset market exposure).
- **Hold/rebalance** — typical holding period 1–12 months; rebalance to maintain the relative-strength ranking.
- **Risk controls** — sector/industry neutralization (don't let the bet collapse to a sector bet), volatility targeting, and turnover control (to manage transaction costs).

## Uses & Cautions

Cross-sectional momentum is one of the most robust anomalies in finance — documented across decades, countries, and asset classes — but it suffers sharp crashes during momentum reversal (e.g., 2009, when beaten-down losers rallied and recent winners lagged). The "momentum crash" risk is the central caution: momentum's fat left tail. Mitigations include volatility scaling, dynamic lookbacks, and pairing with a [Mean Reversion](mean-reversion) short-term-reversal overlay. It overlaps conceptually with [Time-series Momentum](time-series-momentum) (same anomaly, different construction) and with [Trend Following](trend-following) (the directional cousin). The long-short construction makes it a cousin of [Statistical Arbitrage](statistical-arbitrage) in portfolio mechanics, though the signal is price-trend rather than cointegration.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| tanish35/Momentum-Investing | 9 | Long-only momentum strategy in Backtrader | https://github.com/tanish35/Momentum-Investing |
| ryaniamfs/Crypto-Stat-Arb | 8 | Cross-sectional/time-series momentum on crypto perps | https://github.com/ryaniamfs/Crypto-Stat-Arb |
| jackmin97/Cross-Sectional-Momentum-Strategy | 6 | Cross-sectional momentum long-short notebook | https://github.com/jackmin97/Cross-Sectional-Momentum-Strategy |
| BenjiKCF/Signal-frontier-analysis | 7 | Cross-sectional momentum portfolio + param grid | https://github.com/BenjiKCF/Signal-frontier-analysis-and-model-parameterizations |
| QuantConnect/Lean | 20334 | Algorithmic engine for momentum portfolios | https://github.com/QuantConnect/Lean |

## Books & Foundamental Reading

- Jegadeesh & Titman (1993) — *Returns to Buying Winners and Selling Losers* (the founding study)
- Gary Antonacci — *Dual Momentum Investing* (combines cross-sectional + absolute momentum)
- Andrew Ang — *Asset Management* (factor investing, momentum as a factor)

## Relationships

Relative-strength cousin of [Time-series Momentum](time-series-momentum); directional sibling [Trend Following](trend-following); long-short portfolio mechanics shared with [Statistical Arbitrage](statistical-arbitrage); crash risk mitigated by [Mean Reversion](mean-reversion) overlays; factor-investing kinship with [Sector Rotation](sector-rotation).
