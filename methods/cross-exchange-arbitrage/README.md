---
title: Cross-exchange Arbitrage
type: method
domain: trading
category: Arbitrage Strategies
tier: 3
importance: moderate
markets: crypto (multi-CEX/DEX)
timeframe: seconds–minutes
github_repo: mhd-vav/trading-methods
branch: cross-exchange-arbitrage
---

# Cross-exchange Arbitrage

Cross-exchange arbitrage exploits the same asset trading at different prices on **different exchanges**: buy on the cheaper venue, sell on the richer, capturing the spread. In crypto, BTC/USDT may differ across Binance, Kraken, and a DEX by a few basis points at any moment, due to fragmented liquidity and asynchronous price discovery. The arbitrageur detects the gap (net of fees, transfer, and slippage), executes both legs, and optionally rebalances inventory across venues. Unlike [Triangular Arbitrage](triangular-arbitrage) (same exchange, three pairs), cross-exchange is two venues, one pair. The trade is "riskless" only if both legs fill at the detected prices — the central operational challenge.

## Mechanics

- **Spread detection** — monitor order books across venues; compute the executable spread (best bid on venue A vs best ask on venue B, net of fees and estimated slippage).
- **Execution** — buy the ask on the cheap venue, sell the bid on the rich venue, ideally simultaneously. Pre-funded inventory on both venues (or a credit/borrow facility) removes transfer latency; otherwise you must transfer the asset, during which the spread may close.
- **Inventory rebalancing** — after repeated one-directional arbs, inventory accumulates on one venue; periodic rebalancing (transfer or reverse-arb) is required, incurring fees/time.
- **Cost threshold** — the spread must exceed fees (both legs) + slippage + transfer/network costs; below that, the arb is uneconomic.

## Uses & Cautions

Cross-exchange arb is the bread-and-butter of crypto market efficiency — it keeps venue prices aligned and provides much of crypto's price discovery. Profitable operation requires low-latency monitoring, pre-funded inventory across venues (capital-intensive), and favorable fee tiers. Key risks: leg risk (one side fills, the other doesn't, leaving a directional position), transfer latency (the cheap->rich transfer takes minutes; spread closes), withdrawal freezes/outages, exchange/counterparty risk, and the arms-race decay as more bots compete the spreads down. It overlaps [Triangular Arbitrage](triangular-arbitrage) (combine for "cross-triangular" cycles), [Latency Arbitrage](latency-arbitrage) (speed-driven), [DEX Arbitrage](dex-arbitrage) (CEX↔DEX legs), and [Basis Trading](basis-trading)/[Funding-rate Arbitrage](funding-rate-arbitrage) (spot-vs-perp cross-venue). Hummingbot is the leading open-source framework.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| your-quantguy/cross-exchange-arbitrage | 117 | Framework for cross-exchange spread arb in crypto futures | https://github.com/your-quantguy/cross-exchange-arbitrage |
| bigmacman1129/crypto-arbitrage | 87 | Triangular + cross-exchange arb bot | https://github.com/bigmacman1129/crypto-arbitrage |
| notlelouch/ArbiBot | 32 | Go cross-exchange arb bot via WebSocket | https://github.com/notlelouch/ArbiBot |
| hummingbot/hummingbot | 19059 | Leading open-source crypto arb/MM framework | https://github.com/hummingbot/hummingbot |
| kelvinau/crypto-arbitrage | 844 | Triangular & cross-exchange crypto arb | https://github.com/kelvinau/crypto-arbitrage |

## Books & Foundational Reading

- Paolo Tasca et al. — *Blockchain and Crypto Assets* (cross-venue microstructure)
- Hummingbot docs — *Cross-Exchange Market Making & Arbitrage* guides
- Andreas Park — research on crypto exchange fragmentation and arbitrage

## Relationships

Two-venue cousin of [Triangular Arbitrage](triangular-arbitrage); speed-driven variant is [Latency Arbitrage](latency-arbitrage); CEX↔DEX legs link to [DEX Arbitrage](dex-arbitrage); spot-vs-perp link to [Basis Trading](basis-trading) and [Funding-rate Arbitrage](funding-rate-arbitrage); infrastructure shared with [HFT](high-frequency-trading) and [Market Making](market-making).
