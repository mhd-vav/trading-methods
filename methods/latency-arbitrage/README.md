---
title: Latency Arbitrage
type: method
domain: trading
category: Arbitrage Strategies
tier: 3
importance: moderate
markets: equities, crypto (multi-venue)
timeframe: microseconds
github_repo: mhd-vav/trading-methods
branch: latency-arbitrage
---

# Latency Arbitrage

Latency Arbitrage exploits the fact that different trading venues update their quotes at different speeds. An arbitrageur with a faster data feed observes a price change on a "fast" venue (e.g., the primary exchange or a consolidated feed) and trades against a "slow" venue whose quoted prices are momentarily stale. Example: NBBO moves up on the fast feed; the slow venue still shows the old (lower) offer, so the arbitrageur buys the stale offer and immediately could sell at the new higher bid — locking a near-instant, near-riskless spread. The edge is purely informational speed, not a view on direction or value.

## Mechanics

- **Stale-quote detection** — monitor a fast/consolidated feed; when it moves beyond a threshold vs a slow venue's resting quote, immediately take the stale quote.
- **Speed infrastructure** — requires colocation, direct market data, kernel-bypass networking, often FPGAs — the same kit as [HFT](high-frequency-trading). Being microseconds faster than the slow venue's quote refresh is the entire edge.
- **Inventory management** — positions are typically unwound immediately at the now-correct price on another venue, so inventory is fleeting.

## Uses & Cautions

Latency arbitrage is controversial: critics (and many exchanges/regulators) view it as exploiting a structural latency gap rather than providing genuine liquidity or price discovery — some venues introduced "speed bumps" or periodic auctions specifically to neutralize it. Practically, the edge has decayed sharply as venues improved quote-update latency and as the arms race compressed margins. It is a sub-discipline of [HFT](high-frequency-trading) and shares infrastructure with [Market Making](market-making), but its pure-informational nature distinguishes it from [Statistical Arbitrage](statistical-arbitrage) (which bets on a statistical relationship, not a literal stale price). In crypto, cross-exchange latency arb overlaps [Cross-exchange Arbitrage](cross-exchange-arbitrage).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| jmakov/dragonflybot | 69 | Low-latency stream-processing trading framework | https://github.com/jmakov/dragonflybot |
| Raf3-Tech/arbitrage-bot | 2 | Low-latency crypto cross-exchange arb detection | https://github.com/Raf3-Tech/arbitrage-bot |
| ethanbabel/CryptoArbitrage | 1 | Low-latency circular arbitrage on Ethereum | https://github.com/ethanbabel/CryptoArbitrage |

## Books & Foundational Reading

- Thierry Foucault, Marco Pagano, Ailsa Röell — *Market Liquidity* (latency arb in microstructure theory)
- Irene Aldridge — *High-Frequency Trading* (latency-arb mechanics)
- Michael Lewis — *Flash Boys* (popular account of latency arb / dark pools)

## Relationships

Sub-discipline of [HFT](high-frequency-trading); shares infrastructure with [Market Making](market-making); contrasted with [Statistical Arbitrage](statistical-arbitrage) (statistical vs literal stale price); crypto variant overlaps [Cross-exchange Arbitrage](cross-exchange-arbitrage); informational-velocity kinship with [Index Arbitrage](index-arbitrage).
