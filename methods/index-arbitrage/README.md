---
title: Index Arbitrage
type: method
domain: trading
category: Arbitrage Strategies
tier: 3
importance: moderate
markets: equity index futures vs constituent stocks
timeframe: seconds–minutes
github_repo: mhd-vav/trading-methods
branch: index-arbitrage
---

# Index Arbitrage

Index Arbitrage exploits the price discrepancy between an equity index futures contract and the basket of its constituent stocks (or the ETF tracking the index). The futures price is tied to the spot index by cost-of-carry: Fair Futures = Spot × (1 + (r − q) × t), where r = risk-free rate, q = dividend yield, t = time to expiry. When the actual futures price deviates from this fair value beyond transaction costs, the arbitrageur buys the cheaper leg and sells the richer: if futures are rich (above fair value), sell futures + buy the stock basket; if cheap, buy futures + sell the basket. The trade closes as the two converge at expiry (or when the gap mean-reverts).

## Mechanics

- **Fair value** — continuously computed from spot index, risk-free rate, dividends, and time. The deviation (futures − fair value) is the signal.
- **Basket execution** — the arbitrageur must trade the full constituent basket (or a tracking ETF/representative subset) in the correct index weights, incurring slippage and commissions across potentially hundreds of names.
- **Convergence** — at futures expiry the futures price converges to the spot settlement, locking the arbitrage. Before expiry, the trader can also unwind when the spread reverts to fair value.
- **Program trading** — historically executed via "program trading" baskets; now dominated by [HFT](high-frequency-trading)-style automated systems reacting to fair-value gaps in real time.

## Uses & Cautions

Index arbitrage is a classic near-riskless convergence trade, but the edge is thin and competed away by fast automated players — profitability now requires speed ([Latency Arbitrage](latency-arbitrage) infrastructure) and extremely low execution costs. Residual risks: dividend announcement changes (shifts fair value), execution slippage on the basket, and "leg risk" if one side fills but the other doesn't. It is structurally related to [Statistical Arbitrage](statistical-arbitrage) (both are convergence trades on a relationship) and to [Basis Trading](basis-trading) (cash-futures basis), and its automated execution shares DNA with [Market Making](market-making).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| SergioIommi/Quant-Trading-Dashboards | 24 | Pair/stat arb & multi-variable index regression | https://github.com/SergioIommi/Quant-Trading-Dashboards |
| yousra-aoudi/Spot-Futures-Arbitrage-Strategy | 7 | Python spot-futures arbitrage strategy classes | https://github.com/yousra-aoudi/Spot-Futures-Arbitrage-Strategy |
| QuantConnect/Lean | 20334 | Algorithmic engine supporting index/futures arb | https://github.com/QuantConnect/Lean |

## Books & Foundational Reading

- Robert Schwartz, Liuren Wu — research on index-fair-value and program trading
- Perry Kaufman — *Trading Systems and Methods* (index arbitrage chapter)
- Thierry Foucault et al. — *Market Liquidity* (microstructure of index arbitrage)

## Relationships

Convergence-logic sibling of [Statistical Arbitrage](statistical-arbitrage) and [Basis Trading](basis-trading); automated execution via [HFT](high-frequency-trading) and [Latency Arbitrage](latency-arbitrage); cash-futures link shared with [Calendar Spreads](calendar-spreads); relative-value kinship with [Market Making](market-making).
