---
title: Funding-rate Arbitrage
type: method
domain: trading
category: Arbitrage Strategies
tier: 3
importance: moderate
markets: crypto perpetual futures
timeframe: hours–days (funding intervals)
github_repo: mhd-vav/trading-methods
branch: funding-rate-arbitrage
---

# Funding-rate Arbitrage

Funding-rate arbitrage is the crypto-native cash-and-carry trade: hold a **delta-neutral** position — long spot (or a dated futures) and short an equal-size perpetual future (or vice versa) — to harvest the **funding rate**. Crypto perpetual futures have no expiry; instead, a periodic funding rate keeps the perp price tethered to spot: when the perp trades at a premium (longs pay shorts), funding is positive; when at a discount (shorts pay longs), negative. When funding is persistently positive (a leveraged-long market), the arbitrageur goes long spot + short perp, collecting the funding every interval while the delta-hedge neutralizes spot price moves. It is the crypto analogue of [Basis Trading](basis-trading) and a delta-neutral cousin of [Volatility Arbitrage](volatility-arbitrage).

## Mechanics

- **Delta-neutral construction** — long 1 unit spot + short 1 unit perp (when funding positive); the perp's delta approximates 1, so net delta ≈ 0. Spot price moves cancel out; only the funding stream matters.
- **Funding stream** — funding is paid/received every 8 hours (typically) based on the perp-spot premium. In a hot market, annualized funding can exceed 30–100%, a rich "carry" for the short-perp/long-spot holder.
- **Convergence/risk** — unlike dated-futures basis, the perp never converges to spot at an expiry; the funding mechanism continuously pulls it toward spot. The arb is "carry" not "convergence."
- **Inverse construction** — when funding is persistently negative (leveraged-short market), go short spot + long perp to collect the funding.

## Uses & Cautions

Funding-rate arb is one of crypto's most popular delta-neutral strategies — in bull markets, the short-perp/long-spot carry can be substantial and low-variance. It is structurally a [Basis Trading](basis-trading)/[Carry Trade](carry-trade) variant, monetizing the cost of leverage in the perp market. Risks: funding can flip sign (a market regime change turns positive carry negative), the spot leg incurs custody/borrow costs and exchange risk, the perp leg faces liquidation risk if the hedge drifts (requires rebalancing), and during violent moves the perp can trade at a large temporary discount ("negative funding shock") that pressures the position. Execution and inventory management overlap [Cross-exchange Arbitrage](cross-exchange-arbitrage) (spot on one venue, perp on another) and [Market Making](market-making) infrastructure. Godzilla and aoki-h-jp/funding-rate-arbitrage are leading open-source implementations.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| godzilla-foundation/godzilla-community | 354 | C++/Python infra for self-hosted crypto funding-rate arb | https://github.com/godzilla-foundation/godzilla-community |
| aoki-h-jp/funding-rate-arbitrage | 301 | Funding-rate arbitrage on cryptocurrency | https://github.com/aoki-h-jp/funding-rate-arbitrage |
| vooi-app/vooi-funding-bot-example | 11 | Delta-neutral funding-rate arb bot example | https://github.com/vooi-app/vooi-funding-bot-example |
| vvonha/crypto-trading-tools | 41 | Binance/Polymarket arb + funding-rate scanner | https://github.com/vvonha/crypto-trading-tools |

## Books & Foundational Reading

- BitMEX/Binance research — *Perpetual Futures & Funding Rate Mechanics* (official docs)
- Paolo Tasca et al. — *Blockchain and Crypto Assets* (perp microstructure)
- Hummingbot docs — *Spot-Perpetual Arbitrage* strategy guide

## Relationships

Crypto-native [Basis Trading](basis-trading); delta-neutral kinship with [Volatility Arbitrage](volatility-arbitrage); carry logic shared with [Carry Trade](carry-trade); cross-venue execution overlaps [Cross-exchange Arbitrage](cross-exchange-arbitrage); infrastructure shared with [Market Making](market-making) and [HFT](high-frequency-trading).
