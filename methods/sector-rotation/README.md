---
title: Sector Rotation
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 3
importance: moderate
markets: equity sectors/ETFs
timeframe: weeks–months (business cycle)
github_repo: mhd-vav/trading-methods
branch: sector-rotation
---

# Sector Rotation

Sector rotation rotates portfolio exposure across equity sectors based on the **phase of the business cycle**, premised on the idea that different sectors outperform at different cycle stages (e.g., technology/growth lead in early expansion; energy/materials lead in late-cycle inflation; consumer staples/utilities defend in recession). The classic Sam Stovall / S&P framework maps sectors to four cycle phases (early-cycle, mid-cycle, late-cycle, recession) and rotates accordingly. Systematic variants use relative-strength ([Cross-sectional Momentum](cross-sectional-momentum)) or macro leading indicators to time the rotation. It is a top-down, macro-aware equity strategy bridging [Global Macro](global-macro) and factor investing.

## Mechanics

- **Cycle-phase mapping** — early expansion: discretionary, financials, industrials; mid: tech, comm services; late: energy, materials, industrials; recession: staples, utilities, healthcare (defensive).
- **Signal options** — (1) discretionary macro call on cycle phase, (2) systematic relative-strength ranking of sector ETFs (go long the top-ranked, fade the bottom), (3) leading-indicator composite (ISM, yield curve, employment) to infer phase.
- **Implementation** — sector ETFs (XLK, XLE, XLF...) or sector index futures; long-only rotation or long-short sector pairs.

## Uses & Cautions

Sector rotation is intuitive and macro-grounded, but its execution is hard: identifying the cycle phase in real-time is notoriously unreliable, and sector leadership can diverge from the textbook cycle map (e.g., tech dominating across phases in the 2010s). The systematic relative-strength variant is more robust and overlaps [Cross-sectional Momentum](cross-sectional-momentum) — it's essentially momentum applied at the sector level. Risks: mistiming the cycle (rotating into late-cycle sectors just as recession hits), transaction costs from frequent rotation, and concentration risk if the model tilts heavily to one or two sectors. It connects to [Global Macro](global-macro) (the cycle view), [Cross-sectional Momentum](cross-sectional-momentum) (the systematic expression), [Value Investing](value-investing) (sector valuation spreads), and the broader factor-investing framework.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| hanadate/stock_analysis | 0 | Sector rotation strategy | https://github.com/hanadate/stock_analysis |
| HaripreethCJ/Sector_rotation_strategy | 0 | Sector rotation strategy (Indian market) | https://github.com/HaripreethCJ/Sector_rotation_strategy |
| landon-io/stocks-ai-agent | 0 | Cross-sector ETF rotation w/ backtesting | https://github.com/landon-io/stocks-ai-agent |
| Oil2Alpha/Accurate_sector_rotation-timing_strategy_for_smallcap_stocks | 0 | Sector rotation & timing for small-caps | https://github.com/Oil2Alpha/Accurate_sector_rotation-timing_strategy_for_smallcap_stocks |
| QuantConnect/Lean | 20334 | Algorithmic engine for sector-rotation strategies | https://github.com/QuantConnect/Lean |

## Books & Foundational Reading

- Sam Stovall — *Sector Investing* & *The Seven Rules of Wall Street* (cycle-phase sector map)
- Jeffrey Hirsch — *Stock Trader's Almanac* (seasonal/cycle sector tendencies)
- S&P / Fidelity sector-rotation research notes

## Relationships

Top-down kinship with [Global Macro](global-macro); systematic expression via [Cross-sectional Momentum](cross-sectional-momentum); valuation overlay from [Value Investing](value-investing); factor-investing framework shared with [Statistical Arbitrage](statistical-arbitrage); defensive-rotation logic contrasts with [Trend Following](trend-following) persistence.
