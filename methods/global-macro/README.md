---
title: Global Macro
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 2
importance: high
markets: FX, rates, equities, commodities, credit (cross-asset)
timeframe: weeks–months (discretionary); systematic variants
github_repo: mhd-vav/trading-methods
branch: global-macro
---

# Global Macro

Global Macro is a top-down, cross-asset trading style that takes positions based on **macroeconomic themes and relative-value opportunities** across currencies, interest rates, equities, commodities, and credit — rather than bottom-up stock picking or chart patterns. The macro manager forms a view on the global economic cycle, central-bank policy differentials, inflation regimes, and geopolitical shifts, then expresses it via the most liquid instruments (FX, bond futures, index futures, commodities). It is the archetype of the discretionary "macro hedge fund" (Bridgewater's Pure Alpha, Brevan Howard, Tudor), though systematic variants exist. Global Macro is defined by its top-down thesis-driven nature and cross-asset flexibility — it goes where the macro edge is, not where a single mandate confines it.

## Core Mechanics

- **Top-down thesis** — build a view on growth, inflation, and policy across regions (e.g., "US growth surprised positive, Fed stays hawkish vs dovish ECB → long USD, short EUR rates"). The thesis drives the trade selection and instrument choice.
- **Cross-asset expression** — translate the macro view into the cleanest instruments: FX for relative-policy views, bond futures for rate/duration views, index futures for growth/risk views, commodities for supply/demand/inflation views.
- **Relative value** — often expressed as relative-value (long X / short Y) rather than outright direction, to isolate the macro factor and reduce directional market beta.
- **Discretionary vs systematic** — discretionary macro (human judgment on thesis and sizing) vs systematic macro (rules-based, often overlapping [Trend Following](trend-following) and [Carry Trade](carry-trade) signals, e.g., Bridgewater's All-Weather).

## Risk Management

- **Thesis-risk / being wrong** — the central risk: a macro thesis can be fundamentally wrong or right-but-timing-wrong. Macro trades can take weeks-months to play out and draw down materially meanwhile.
- **Cross-asset correlation risk** — in risk-off episodes, correlations converge to 1 (everything sells off together), breaking the diversification macro relies on.
- **Policy/tail risk** — central-bank surprises and geopolitical shocks are both the alpha source and the risk source.
- **Position sizing** — vol-targeting and thesis-conviction weighting; macro funds typically run modest gross with high conviction tilts.

## Common Pitfalls

- **Narrative over edge** — a compelling macro story is not a tradeable edge; many macro theses are consensus and already priced.
- **Timing** — being early is indistinguishable from being wrong; macro regimes persist longer than expected.
- **Over-reliance on a single theme** — concentration in one macro bet (e.g., short JPY for years) can produce prolonged drawdowns.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| wellbeing18/pgm-oil | 13 | Bayesian/HMM macro model for oil (global macro signals) | https://github.com/wellbeing18/pgm-oil |
| pthanay/Macro_Strategies | 0 | Blog repo of macro indicators & analysis | https://github.com/pthanay/Macro_Strategies |
| QuantConnect/Lean | 20334 | Algorithmic engine for systematic macro strategies | https://github.com/QuantConnect/Lean |

## Books & Foundamental Reading

- Steven Drobny — *Inside the House of Money* & *The Invisible Hands* (macro hedge-fund manager interviews)
- Ray Dalio — *Principles for Navigating Big Debt Crises* (macro cycle framework)
- Paul Tudor Jones — publicly available macro research notes
- Mark Spitznagel — *The Dao of Capital* (Austrian-influenced macro/tail hedging)

## Relationships

Cross-asset framework hosting [Carry Trade](carry-trade), [Event-driven Trading](event-driven-trading), [Sentiment & News Trading](sentiment-news-trading); systematic cousin of [Trend Following](trend-following) and [CTA / Managed Futures](cta-managed-futures); uses [Term-structure Trading](term-structure-trading) and [Inter-commodity Spreads](inter-commodity-spreads); contrasted with bottom-up [Value Investing](value-investing).
