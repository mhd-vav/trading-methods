---
title: Time-Series Momentum
type: method
domain: trading
category: Quantitative & Statistical Strategies
tier: 3
importance: moderate
markets: futures, FX, commodities, equities
timeframe: weeks–months (lookback 1–12m)
github_repo: mhd-vav/trading-methods
branch: time-series-momentum
---

# Time-Series Momentum

Time-series momentum (TSMOM, formalized by Moskowitz, Ooi & Pedersen 2012) takes a directional position in **each asset** based on its own past return: go long an asset if its lookback return is positive, short if negative. This contrasts with [Cross-sectional Momentum](cross-sectional-momentum), which only bets on the ranking between assets and is market-neutral. TSMOM is the academic formalization of [Trend Following](trend-following) / CTA strategies: a diversified portfolio of long/short signals across dozens of futures markets, each trend-following on its own past, volatility-scaled. The 2012 paper showed TSMOM was positive and significant across 58 instruments over 25 years — validating the CTA industry's bread-and-butter.

## Mechanics

- **Per-asset signal** — sign of the past K-month return (K typically 1, 3, or 12 months). Long if positive, short if negative, flat or inverse-vol-sized otherwise.
- **Volatility scaling** — each position sized inversely to its own volatility so each market contributes equal risk (the "risk parity" ingredient that makes TSMOM robust across asset classes).
- **Diversified portfolio** — applied across a broad basket (equities, bonds, commodities, FX, metals) so uncorrelated trend signals diversify; the portfolio Sharpe is far higher than any single market's trend signal.
- **Rebalance** — monthly, re-evaluating each asset's lookback sign.

## Uses & Cautions

TSMOM is the engine of the managed-futures / [CTA](cta-managed-futures) industry and a premier crisis-alpha strategy: it tends to profit in sustained trending crashes (2008, 2022) by going short as trends turn down. Its weakness: choppy, range-bound, or rapidly-reversing markets produce "trend-following whipsaw" — consecutive false breakouts that bleed the portfolio. The performance is also regime-dependent: strong in the 2000s–2010s, weaker in low-volatility range periods. It overlaps with [Trend Following](trend-following) (essentially the systematic, diversified expression) and is the directional counterpart to [Cross-sectional Momentum](cross-sectional-momentum). Managed via volatility targeting, lookback diversification (mixing 1/3/12-month signals), and trend-strength filters like [ADX](adx).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| bideeen/Building-A-Trading-Strategy-With-Python | 64 | TSMOM strategy build & backtest in Python | https://github.com/bideeen/Building-A-Trading-Strategy-With-Python |
| harshitcodes/momentum_trading_testing | 33 | Time-series momentum implementation & backtest | https://github.com/harshitcodes/momentum_trading_testing |
| benjaminchodroff/oandamomentum | 23 | TSMOM strategy for Oanda | https://github.com/benjaminchodroff/oandamomentum |
| anthonymakarewicz/bitcoin-momentum-trading | 14 | Intraday TSMOM on 5-min Bitcoin | https://github.com/anthonymakarewicz/bitcoin-momentum-trading |
| QuantConnect/Lean | 20334 | Algorithmic engine for TSMOM futures portfolios | https://github.com/QuantConnect/Lean |

## Books & Foundational Reading

- Moskowitz, Ooi & Pedersen (2012) — *Time Series Momentum* (Journal of Financial Economics; the founding study)
- Hurst, Ooi, Pedersen — *A Century of Evidence on Trend-Following Investing* (AQR, 2017)
- Gary Antonacci — *Dual Momentum Investing* (TSMOM + cross-sectional combined)
- Andrew Lo — *Adaptive Markets* (behavioral basis of momentum)

## Relationships

Directional expression of [Trend Following](trend-following); counterpart to [Cross-sectional Momentum](cross-sectional-momentum); engine of [CTA / Managed Futures](cta-managed-futures); trend-strength gated by [ADX](adx); diversification logic shared with [Statistical Arbitrage](statistical-arbitrage) portfolios; whipsaw risk same as [Breakout Trading](breakout-trading).
