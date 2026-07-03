---
title: CTA / Managed Futures
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 3
importance: moderate
markets: futures (equities, bonds, commodities, FX, metals)
timeframe: days–months
github_repo: mhd-vav/trading-methods
branch: cta-managed-futures
---

# CTA / Managed Futures

Commodity Trading Advisors (CTAs) and Managed Futures funds are systematic, trend-following (and increasingly multi-strategy) funds trading liquid futures markets across asset classes. The archetype: a diversified portfolio of [Time-series Momentum](time-series-momentum) signals across 50–150 futures contracts — equities indices, rates, currencies, energies, metals, grains, softs — each volatility-scaled and combined. CTAs are the institutional face of [Trend Following](trend-following); the SG CTA Index and BTOP50 benchmark the category. Their value proposition: low correlation to traditional 60/40 equity-bond portfolios and positive "crisis alpha" (they tend to profit in sustained trending downturns by going short as trends break).

## Core Mechanics

- **Multi-market trend signals** — long/short each futures market based on its own trend (moving-average crossover, breakout, or TSMOM sign), applied across a diversified global basket.
- **Volatility targeting & risk parity** — each market sized to contribute equal risk (inverse-volatility weighting), so a calm bond market and a wild crude market contribute comparably; the whole portfolio vol-targeted (e.g., 10–15% annualized).
- **Signal diversification** — mix multiple lookbacks (fast/slow trends, [Breakout](breakout-trading), [Moving Average Crossover](moving-average-crossover)) and regime filters ([ADX](adx)) to smooth returns.
- **Systematic, rules-based** — discretionary CTAs exist but the category is overwhelmingly systematic, with disciplined execution via [Execution Algorithms](execution-algorithms).

## Uses & Cautions

CTAs are prized as portfolio diversifiers: historically near-zero correlation to equities and a tendency to shine in crisis trends (2008, 2022). The cautions: CTAs underperform in range-bound, choppy markets (the "trend-following whipsaw") — 2015–2017 and 2018 were difficult. They also face capacity constraints in smaller markets and high transaction/roll costs. Modern CTAs have diversified beyond pure trend into [Mean Reversion](mean-reversion), [Statistical Arbitrage](statistical-arbitrage), carry, and [ML/AI](ml-ai-trading) signal overlays. The category overlaps heavily with [Time-series Momentum](time-series-momentum) (its academic formalization) and [Trend Following](trend-following) (its philosophy).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| QuantConnect/Lean | 20334 | Algorithmic engine for multi-asset futures CTA strategies | https://github.com/QuantConnect/Lean |
| je-suis-tm/quant-trading | 10241 | Python quant strategies incl. trend/momentum | https://github.com/je-suis-tm/quant-trading |
| evelynpurse/CTA_cross_sectional | 6 | Cross-sectional momentum for futures (CTA) | https://github.com/evelynpurse/CTA_cross_sectional |
| LuoMeng09/CTA-Strategy_Price-Volume-Factors | 2 | CTA price-volume factor strategy (China futures) | https://github.com/LuoMeng09/CTA-Strategy_Price-Volume-Factors |

## Books & Foundational Reading

- Michael Stonberg — *The CTA Trend Following Encyclopedia*
- Kathryn Kaminski — *Trend Following with Managed Futures* (crisis alpha, academic-CTA bridge)
- Andreas Clenow — *Following the Trend* (how CTAs actually operate)
- AQR — *A Century of Evidence on Trend-Following Investing* (white paper)

## Relationships

Institutional form of [Trend Following](trend-following); academic core is [Time-series Momentum](time-series-momentum); signal diversification with [Moving Average Crossover](moving-average-crossover), [Breakout Trading](breakout-trading), [ADX](adx); modern overlays in [Mean Reversion](mean-reversion), [Statistical Arbitrage](statistical-arbitrage), [ML/AI Trading](ml-ai-trading); execution via [Execution Algorithms](execution-algorithms).
