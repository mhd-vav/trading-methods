---
title: Inter-commodity Spreads
type: method
domain: trading
category: Futures & Spread Trading
tier: 3
importance: moderate
markets: commodities (energy, grains, metals, livestock)
timeframe: days–weeks
github_repo: mhd-vav/trading-methods
branch: inter-commodity-spreads
---

# Inter-commodity Spreads

Inter-commodity spreads are long-short positions in **two different but economically related futures contracts** — betting on the relative value between them rather than outright direction. Classic examples: crude oil vs heating oil/gasoline (the "crack" family), soybeans vs soybean meal/oil (the "crush"), gold vs silver, wheat vs corn, live cattle vs feeder cattle, Brent vs WTI crude. The economic logic: the spread represents a processing margin, a substitution relationship, or a quality differential that reverts to a fundamental equilibrium driven by supply, demand, and processing economics. Spread traders express a view on that margin/differential while neutralizing broad market direction.

## Mechanics

- **Processing-margin spreads** — the [Crack/Crush](crack-crush-spreads) family: buy raw input, sell processed output (or vice versa), expressing a view on the processor's margin. The most economically grounded spreads.
- **Substitution spreads** — wheat vs corn (both feed grain; switch based on protein value), gold vs silver (both precious; ratio mean-reverts), heating oil vs natural gas (heating substitutes). Bet on the relative value reverting as substitution economics assert.
- **Quality/location spreads** — Brent vs WTI (different crude grades/basins), No.2 vs No.1 fuel oil. Reflect logistics, quality, and regional supply.
- **Weighting** — spreads are often weighted by the conversion ratio of the process (e.g., 3:2:1 crack = 3 crude : 2 gasoline : 1 heating oil) to represent one refining "unit."

## Uses & Cautions

Inter-commodity spreads are favored for their directional neutrality and fundamental grounding — the spread reverts because real-world processing/substitution economics enforce it. They have lower margin and volatility than outrights. Risks: spread relationships can shift structurally (new processing capacity, regulation, substitution tech), localized supply shocks can blow the spread far beyond history, and the "reversion to equilibrium" assumption breaks in dislocations. They are tightly linked to [Crack/Crush Spreads](crack-crush-spreads) (the processing-margin subset), [Term-structure Trading](term-structure-trading) (curve context), and [Basis Trading](basis-trading) (location/quality spreads). Spread execution benefits from [Execution Algorithms](execution-algorithms) to manage the two-leg footprint.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| QuantConnect/Lean | 20334 | Algorithmic engine for multi-leg commodity spreads | https://github.com/QuantConnect/Lean |
| je-suis-tm/quant-trading | 10241 | Python quant strategies incl. spread/pairs | https://github.com/je-suis-tm/quant-trading |
| adamelgbouri/commodity-options-and-derivatives-analytics-platform | 1 | Commodity derivatives analytics across 65+ markets | https://github.com/adamelgbouri/commodity-options-and-derivatives-analytics-platform |

## Books & Foundational Reading

- Helyette Geman — *Commodities and Commodity Derivatives* (inter-commodity spread fundamentals)
- Richard Weissman — *Trading Commodities and Financial Futures* (spread trading practice)
- CME Group — *Self-Study Guide to Hedging with Grain and Oilseed Futures* (crush spread mechanics)

## Relationships

Processing-margin subset is [Crack/Crush Spreads](crack-crush-spreads); curve context from [Term-structure Trading](term-structure-trading); location/quality cousin is [Basis Trading](basis-trading); relative-value logic shared with [Calendar Spreads](calendar-spreads) and [Statistical Arbitrage](statistical-arbitrage); execution via [Execution Algorithms](execution-algorithms).
