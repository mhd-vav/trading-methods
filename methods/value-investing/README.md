---
title: Value Investing
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 3
importance: moderate
markets: equities
timeframe: months–years (long holding)
github_repo: mhd-vav/trading-methods
branch: value-investing
---

# Value Investing

Value investing buys securities trading below their **intrinsic value** — the discounted value of future cash flows — based on fundamental analysis. Originated by Benjamin Graham and David Dodd, codified in *Security Analysis* (1934), and famously practiced/extended by Warren Buffett (with Charlie Munger's quality overlay) toward "buying wonderful companies at a fair price." The practitioner values a business via discounted cash flow (DCF), earnings power, asset value, or comparables, and buys when market price offers a "margin of safety" below that estimate. It is the antithesis of momentum/chart-based methods: the edge is fundamental mispricing that reverts as the market recognizes the value, typically over months-years.

## Core Mechanics

- **Intrinsic valuation** — DCF: discount projected future free cash flows at the cost of capital; compare to market price. Margin of safety = (intrinsic − price) / intrinsic.
- **Relative valuation** — price multiples (P/E, P/B, EV/EBITDA, P/FCF) vs history, sector, and peers. The "value factor" (Fama-French HML) systematically longs low-P/B, shorts high-P/B.
- **Quality overlay (Buffett/Munger)** — require durable competitive advantage (moat), high ROIC, conservative balance sheet, able management — quality value, not cheap junk.
- **Catalyst / mean reversion** — the value thesis requires a catalyst (earnings recovery, re-rating, activism, dividend) to close the price-to-value gap; otherwise "value traps" persist.

## Uses & Cautions

Value is one of the most studied equity factors — positive long-run premium, but with long, painful underperformance periods (1998-99 growth bubble, 2017-2020 growth leadership). The central caution: the "value trap" — a cheap stock is often cheap for a reason (secular decline, impaired business). Quality-value and deep-value variants trade off safety vs upside. Value is the foundational long-horizon method, contrasted with [Trend Following](trend-following)/momentum (which buys what's rising, not cheap) — the two factors are historically negatively correlated, motivating combined value+momentum portfolios. It overlaps [Contrarian](contrarian) (buying unloved), [Global Macro](global-macro) (top-down value in macro), and the [Buy-and-Hold](buy-and-hold) long-horizon discipline. Modern quantitative value (AQR, Dimensional) systematizes the Graham/Buffett principles into factor portfolios.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| storieswithsiva/Stock-Market-Analysis | 92 | Fundamental buy/sell decision method | https://github.com/storieswithsiva/Stock-Market-Analysis |
| ketan1741/Benjamin-Graham-and-Warren-Buffett-Model-Stock-Exchange- | 43 | Graham/Buffett value-investing model | https://github.com/ketan1741/Benjamin-Graham-and-Warren-Buffett-Model-Stock-Exchange- |
| nicdun/value-investing-ai-agent | 17 | AI fundamental research stock-analysis tool | https://github.com/nicdun/value-investing-ai-agent |
| stefan-jansen/machine-learning-for-trading | 19491 | ML for value/factor strategies (chapters) | https://github.com/stefan-jansen/machine-learning-for-trading |

## Books & Foundational Reading

- Benjamin Graham — *The Intelligent Investor* & *Security Analysis* (the foundation)
- Warren Buffett — *Berkshire shareholder letters* (quality-value practice)
- Seth Klarman — *Margin of Safety* (deep-value discipline)
- Aswath Damodaran — *Investment Valuation* (the DCF practitioner's reference)
- Eugene Fama & Kenneth French — *The Cross-Section of Expected Stock Returns* (the value factor)

## Relationships

Long-horizon discipline with [Buy-and-Hold](buy-and-hold); negatively-correlated factor sibling to [Trend Following](trend-following)/[Cross-sectional Momentum](cross-sectional-momentum); kinship with [Contrarian](contrarian); top-down macro variant under [Global Macro](global-macro); long-short factor mechanics shared with [Statistical Arbitrage](statistical-arbitrage).
