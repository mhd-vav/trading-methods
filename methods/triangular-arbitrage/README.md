---
title: Triangular Arbitrage
type: method
domain: trading
category: Arbitrage Strategies
tier: 3
importance: moderate
markets: crypto (FX historically)
timeframe: milliseconds–seconds
github_repo: mhd-vav/trading-methods
branch: triangular-arbitrage
---

# Triangular Arbitrage

Triangular arbitrage exploits a pricing inconsistency among three currency/asset pairs on the **same exchange** that should be mathematically consistent. Classic FX example: USD→EUR→GBP→USD should return the starting amount (zero arbitrage); if the implied cross-rate differs from the quoted one, a round-trip through the three pairs locks a riskless profit. In crypto, the cycle is typically BTC→ETH→USDT→BTC (or any three-pair triangle) on a single exchange: if the product of the three exchange rates exceeds 1 (after fees), execute all three legs and capture the spread. The edge is pure mathematical mispricing, self-correcting as the trades themselves move the rates back into line.

## Mechanics

- **Cycle detection** — scan all tradable triangles (A→B→C→A) on an exchange; compute the implied round-trip rate; if it exceeds 1 + total fees, a profitable cycle exists.
- **Simultaneous execution** — the three legs must execute near-simultaneously; if one leg slips or fails, the "riskless" trade becomes a directional bet. This requires low latency and often aggressive (taker) orders, which incur fees.
- **Fee threshold** — the mispricing must exceed the sum of the three legs' trading fees (typically 0.1% × 3 on a taker) plus slippage; this threshold filters out most detected cycles.
- **Self-correction** — executing the cycle moves the rates, closing the gap; the opportunity is fleeting (milliseconds to seconds) and competed away by bots.

## Uses & Cautions

Triangular arbitrage is a textbook riskless trade in theory; in practice it is an arms race of latency, fee thresholds, and execution reliability. Profitable cycles are rare and fleeting after fees, and the strategy demands [HFT](high-frequency-trading)-grade infrastructure and exchange fee tiers (maker rebates help). Key risks: partial fills (one leg fails, leaving an unhedged position), slippage on illiquid pairs, withdrawal/trade latency, and the fact that the exchange's order book changes between detection and execution. It is a sub-discipline of [HFT](high-frequency-trading), distinct from [Cross-exchange Arbitrage](cross-exchange-arbitrage) (which spans venues) and from [Statistical Arbitrage](statistical-arbitrage) (which bets on statistical, not literal, mispricing). In crypto it overlaps the broader [DEX Arbitrage](dex-arbitrage) and [MEV](mev-sandwich) ecosystem when triangles span AMMs.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| kelvinau/crypto-arbitrage | 844 | Triangular & exchange arbitrage crypto bot | https://github.com/kelvinau/crypto-arbitrage |
| ericjang/cryptocurrency_arbitrage | 858 | Pairwise & triangular arb detector | https://github.com/ericjang/cryptocurrency_arbitrage |
| eugenioclrc/binance-crypto-triangular-arbitrage | 290 | Profitable triangular-arb cycle finder (Binance) | https://github.com/eugenioclrc/binance-crypto-triangular-arbitrage |
| Drakkar-Software/Triangular-Arbitrage | 128 | Triangular-arb detector (Binance, Hyperliquid) | https://github.com/Drakkar-Software/Triangular-Arbitrage |
| Roibal/Cryptocurrency-Trading-Bots-Python-Beginner-Advance | 1439 | Triangular arb bots + beginner/advanced course | https://github.com/Roibal/Cryptocurrency-Trading-Bots-Python-Beginner-Advance |

## Books & Foundational Reading

- Paolo Tasca et al. — *Blockchain and Crypto Assets* (crypto arb microstructure)
- Luc Bauwens et al. — research on FX triangular arbitrage and self-correction
- Avellaneda & Stoikov — high-frequency market-making/arb theory

## Relationships

Sub-discipline of [HFT](high-frequency-trading); single-venue cousin of [Cross-exchange Arbitrage](cross-exchange-arbitrage); literal-mispricing contrast with [Statistical Arbitrage](statistical-arbitrage); crypto-AMM overlap with [DEX Arbitrage](dex-arbitrage) and [MEV / Sandwich](mev-sandwich); fee/latency economics shared with [Latency Arbitrage](latency-arbitrage).
