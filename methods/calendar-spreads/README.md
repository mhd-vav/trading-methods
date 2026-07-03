---
title: Calendar Spreads (Time Spreads)
type: method
domain: trading
category: Futures & Spread Trading
tier: 3
importance: moderate
markets: futures, options
timeframe: days–weeks (to expiry)
github_repo: mhd-vav/trading-methods
branch: calendar-spreads
---

# Calendar Spreads (Time Spreads)

A calendar spread (time spread) is the simultaneous long-short of the same underlying at **different expirations** — in futures, long one delivery month and short another of the same contract; in options, same strike, different expiry. The futures version bets on the **shape of the term structure**: in a contango curve (near < far), buying the spread (long far, short near) profits if contango flattens; in backwardation (near > far), the inverse. Calendar spreads are inherently lower-risk than outright positions because the two legs are highly correlated — the bet is on the relative value between expirations, not direction. They are the building block of curve and roll-yield strategies in commodities and rates.

## Mechanics

- **Futures calendar spread** — long month A / short month B of the same contract (e.g., long Dec WTI / short Jan WTI). P&L = change in (A − B). Driven by storage costs, interest, convenience yield, and supply/demand by delivery window.
- **Roll yield** — in backwardated markets, rolling long futures forward (selling expiring high, buying next-month lower) captures a positive roll yield; the calendar spread is the direct expression of this. Trend/CTA funds harvest roll yield implicitly.
- **Options calendar** — long longer-dated option, short shorter-dated same strike. Profits from time decay differential (the short decays faster) and changes in the vol term structure ([Volatility Arbitrage](volatility-arbitrage) variant).

## Uses & Cautions

Calendar spreads are favored for their low margin (exchanges margin spreads far below outrights) and defined relative-value risk. The edge: understanding supply/demand by delivery window (e.g., grain crop timing, crude storage tightness, gas winter demand) and the term-structure implications. Risks: the spread can diverge sharply on delivery-specific shocks (a localized shortage of the prompt month can blow the spread far beyond historical norms), liquidity in deferred months can be thin, and the "low risk" framing tempts over-leverage. Calendar spreads are the atomic unit of [Term-structure Trading](term-structure-trading), overlap with [Basis Trading](basis-trading) (cash-futures is a special calendar-like spread), and their options form feeds [Volatility Arbitrage](volatility-arbitrage).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| quantrocket-codeload/calspread | 15 | Intraday futures calendar-spread strategy (crude, 1-min) | https://github.com/quantrocket-codeload/calspread |
| QuantConnect/Lean | 20334 | Algorithmic engine for futures spread strategies | https://github.com/QuantConnect/Lean |
| adamelgbouri/commodity-options-and-derivatives-analytics-platform | 1 | Commodity derivatives pricer across 65+ markets | https://github.com/adamelgbouri/commodity-options-and-derivatives-analytics-platform |

## Books & Foundational Reading

- Helyette Geman — *Commodities and Commodity Derivatives* (term structure, calendar spreads)
- Colin Bennett — *Trading and Hedging with Agricultural Futures* (calendar/inter-crop spreads)
- Robert Carver — *Systematic Trading* (spread/trend system design)

## Relationships

Building block of [Term-structure Trading](term-structure-trading); options variant feeds [Volatility Arbitrage](volatility-arbitrage); cash-futures cousin is [Basis Trading](basis-trading); roll-yield logic shared with [CTA / Managed Futures](cta-managed-futures); relative-value kinship with [Statistical Arbitrage](statistical-arbitrage).
