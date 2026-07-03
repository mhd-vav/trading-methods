---
title: Term-structure Trading
type: method
domain: trading
category: Futures & Spread Trading
tier: 3
importance: moderate
markets: commodities, rates, FX futures, crypto perps
timeframe: days–weeks
github_repo: mhd-vav/trading-methods
branch: term-structure-trading
---

# Term-structure Trading

Term-structure trading exploits the **shape and dynamics of the futures curve** — the relationship between prices at different expirations. The curve can be in **contango** (near < far, normal for storable commodities with carry costs) or **backwardation** (near > far, signaling scarcity or positive roll yield). Term-structure traders express views on curve shape: flatten/steepen trades, roll-yield harvesting, and curve-arbitrage. The key insight: in backwardation, rolling a long futures position forward captures a positive "roll yield" (sell expiring high, buy next-month lower) — a structural return source independent of spot direction, central to [CTA / Managed Futures](cta-managed-futures) and commodity investors. In crypto, the perp-vs-spot basis and funding rate are the curve-analog.

## Mechanics

- **Curve shape** — plot futures prices by expiry; classify contango vs backwardation. Scarcity, storage cost, interest, and convenience yield determine the shape.
- **Roll yield** — backwardation = positive roll yield for longs (structural carry); contango = negative roll yield (a drag on longs). The "roll yield" is a major component of commodity-index returns.
- **Calendar/curve spreads** — [Calendar Spreads](calendar-spreads) between specific months express views on localized curve segments; butterfly spreads (long-short-long across three expiries) bet on curvature.
- **Flatten/steepen** — express a view that the near-far differential will compress (flatten) or widen (steepen).

## Uses & Cautions

Term-structure trading is the systematic core of commodity trend/carry strategies and a rich source of carry ([Carry Trade](carry-trade) cousin). The edge: understanding the fundamental drivers of curve shape (scarcity, storage, seasonality, interest) and trading the curve's mean-reversion or trend. Risks: curve shape can shift abruptly on supply shocks (a prompt-month scarcity spike flips contango to steep backwardation overnight), roll yield can be overwhelmed by spot moves, and curve trades carry execution/roll-cost drag. Term-structure trading is built on [Calendar Spreads](calendar-spreads), overlaps [Basis Trading](basis-trading) (cash-futures as a curve anchor), feeds [CTA / Managed Futures](cta-managed-futures) roll-yield harvest, and connects to [Volatility Arbitrage](volatility-arbitrage) via the vol term structure.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| QuantConnect/Lean | 20334 | Algorithmic engine for futures curve/term-structure strategies | https://github.com/QuantConnect/Lean |
| je-suis-tm/quant-trading | 10241 | Python quant strategies incl. curve/roll-yield | https://github.com/je-suis-tm/quant-trading |
| joshualutkemuller/vix_hedging_states | 0 | VIX term-structure states for hedging timing | https://github.com/joshualutkemuller/vix_hedging_states |

## Books & Foundational Reading

- Helyette Geman — *Commodities and Commodity Derivatives* (term-structure theory)
- Hilary Till & Joseph Eagleeye — *Intelligent Commodity Investing* (roll yield, curve dynamics)
- Robert Greer — *The Nature of Commodity Index Returns* (roll yield decomposition)

## Relationships

Built on [Calendar Spreads](calendar-spreads); overlaps [Basis Trading](basis-trading); feeds [CTA / Managed Futures](cta-managed-futures) roll-yield; carry kinship with [Carry Trade](carry-trade); vol-term-structure link to [Volatility Arbitrage](volatility-arbitrage); curve-arbitrage logic shared with [Statistical Arbitrage](statistical-arbitrage).
