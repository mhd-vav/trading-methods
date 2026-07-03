---
title: Basis Trading (Cash-Futures Basis)
type: method
domain: trading
category: Futures & Spread Trading
tier: 3
importance: moderate
markets: commodities, Treasuries, crypto (spot-perp)
timeframe: days–weeks (to convergence)
github_repo: mhd-vav/trading-methods
branch: basis-trading
---

# Basis Trading (Cash-Futures Basis)

Basis trading exploits the difference between the **cash (spot) price** and the **futures price** of the same underlying — the "basis." The basis = cash − futures (or futures − cash, convention-dependent). It converges to zero at futures expiry (futures settles to spot), so a trader who buys the basis (long cash, short futures) when the basis is wide profits as it narrows. In commodities, basis reflects local supply/demand, transport, quality, and storage; in Treasuries, the "cash-futures basis" is a major relative-value market (cheapest-to-deliver dynamics); in crypto, the spot-vs-perp basis (and funding rate) is the analogous trade. Basis trading is a convergence/relative-value strategy, structurally a cousin of [Statistical Arbitrage](statistical-arbitrage).

## Mechanics

- **The basis** — cash − futures. At expiry, basis → 0. A wide basis (futures rich vs cash) → sell futures, buy cash ("sell the basis"); a narrow/negative basis → buy futures, sell cash ("buy the basis").
- **Convergence** — profit accrues as the basis narrows toward expiry. The trade is largely directional-neutral; the bet is on basis mean-reversion/convergence, not spot direction.
- **Drivers** — interest/carry, storage, transport, local supply/demand (commodities), cheapest-to-deliver (Treasuries), funding rate and basis-band arbitrage (crypto).
- **Crypto spot-perp basis** — perpetual futures trade at a basis to spot, kept in line by the funding-rate mechanism; [Funding-rate Arbitrage](funding-rate-arbitrage) is the crypto-native basis trade.

## Uses & Cautions

Basis trading is a staple of commodity merchants, Treasury desks, and crypto basis funds — a convergence trade with defined exit (expiry). The edge: understanding the fundamental drivers of the basis and trading dislocations. Risks: the basis can diverge sharply before converging ("basis risk" — the spread moves against you intraday), convergence can be imperfect (delivery-grade mismatch, delivery logistics), and the trade ties up capital in the cash leg. In crypto, exchange/counterparty risk and funding-rate flips add complexity. Basis trading is a special case of [Calendar Spreads](calendar-spreads)-style relative value, overlaps [Term-structure Trading](term-structure-trading), connects to [Index Arbitrage](index-arbitrage) (basket-futures basis), and its crypto form is [Funding-rate Arbitrage](funding-rate-arbitrage).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| domrushton/masters-dissertation | 0 | Treasury cash-futures basis trade (Masters thesis) | https://github.com/domrushton/masters-dissertation |
| QuantConnect/Lean | 20334 | Algorithmic engine for cash-futures basis strategies | https://github.com/QuantConnect/Lean |
| yousra-aoudi/Spot-Futures-Arbitrage-Strategy | 7 | Python spot-futures arbitrage (basis) strategy | https://github.com/yousra-aoudi/Spot-Futures-Arbitrage-Strategy |

## Books & Foundamental Reading

- CME Group — *Understanding Basis* (commodity basis fundamentals)
- Burghardt, Belton, Lane, Luce — *The Treasury Bond Basis* (the CTD basis bible)
- Helyette Geman — *Commodities and Commodity Derivatives* (basis in commodity markets)

## Relationships

Relative-value cousin of [Statistical Arbitrage](statistical-arbitrage); overlaps [Calendar Spreads](calendar-spreads) and [Term-structure Trading](term-structure-trading); basket-futures link to [Index Arbitrage](index-arbitrage); crypto form is [Funding-rate Arbitrage](funding-rate-arbitrage); convergence logic shared with [Cross-exchange Arbitrage](cross-exchange-arbitrage).
