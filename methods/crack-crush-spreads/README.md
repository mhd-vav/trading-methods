---
title: Crack & Crush Spreads
type: method
domain: trading
category: Futures & Spread Trading
tier: 3
importance: moderate
markets: energy (crack), grains (crush)
timeframe: days–weeks
github_repo: mhd-vav/trading-methods
branch: crack-crush-spreads
---

# Crack & Crush Spreads

Crack and crush spreads are the processing-margin subset of [Inter-commodity Spreads](inter-commodity-spreads), expressing the economics of converting a raw commodity into refined products. The **crack spread** models oil refining: buy crude, sell gasoline + heating oil (the classic 3:2:1 = 3 barrels crude → 2 gasoline + 1 distillate). The **crush spread** models soybean processing: buy soybeans, sell soybean meal + soybean oil (the 10:9:1 = 10 bushels beans → 9 meal + 1 oil). The spread value *is* the processor's gross margin per unit; trading it expresses a view on whether that margin will expand or compress, independent of whether crude or beans themselves rise or fall.

## Mechanics

- **3:2:1 crack** — long 3 crude / short 2 gasoline + short 1 heating oil. Represents one refining unit's margin. Buying the spread = long the refining margin (expect it to widen); selling = short the margin.
- **10:9:1 crush (board crush)** — long 10 soybean bushels / short 9 meal + 1 oil. Represents one crush unit's margin. Same long/short logic on the processing margin.
- **Drivers** — refining/crushing margins driven by product demand (driving season gasoline, winter heating oil), feedstock supply (crude/bean harvest), capacity/utilization outages, and regulatory blend requirements.
- **Weighting** — the ratios reflect actual yield: a refinery yields ~2 gasoline : 1 distillate from crude; a crusher yields ~80% meal : 20% oil by weight from beans.

## Uses & Cautions

Crack/crush spreads let refiners/crushers hedge their margin and let speculators bet on processing economics with directional neutrality. The edge is fundamental: understanding seasonal demand, capacity outages, and supply shocks. Risks: margins can spike violently on refinery outages or crop failures (the "margin blowout"), the exact ratio is an approximation of real yields, and the legs have different volatilities/liquidity. The spreads are the most economically concrete instance of [Inter-commodity Spreads](inter-commodity-spreads), share relative-value DNA with [Calendar Spreads](calendar-spreads) and [Statistical Arbitrage](statistical-arbitrage), and execution requires careful [Execution Algorithms](execution-algorithms) across the multi-leg structure.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| AnuragChaudhari7/gasoil-crack-spread-analysis | 0 | Statistical + ML forecasting of gas-oil crack spread | https://github.com/AnuragChaudhari7/gasoil-crack-spread-analysis |
| QuantConnect/Lean | 20334 | Algorithmic engine for multi-leg crack/crush spreads | https://github.com/QuantConnect/Lean |
| adamelgbouri/commodity-options-and-derivatives-analytics-platform | 1 | Commodity derivatives analytics (energy/grains) | https://github.com/adamelgbouri/commodity-options-and-derivatives-analytics-platform |

## Books & Foundational Reading

- CME Group — *Crack Spread Handbook* and *Soybean Crush Reference Guide* (official mechanics)
- Helyette Geman — *Commodities and Commodity Derivatives* (processing margin theory)
- Richard Weissman — *Trading Commodities and Financial Futures* (crack/crush in practice)

## Relationships

Subset of [Inter-commodity Spreads](inter-commodity-spreads); curve context via [Term-structure Trading](term-structure-trading); relative-value kinship with [Calendar Spreads](calendar-spreads) and [Statistical Arbitrage](statistical-arbitrage); multi-leg execution via [Execution Algorithms](execution-algorithms); fundamental-analysis kinship with [Global Macro](global-macro).
