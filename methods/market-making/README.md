---
title: Market Making
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 2
importance: high
era: 1980s–present (formalized by Avellaneda-Stoikov 2008)
markets: equities, options, futures, crypto, FX
timeframe: tick / millisecond
github_repo: mhd-vav/trading-methods
branch: market-making
---

# Market Making

Market making is the business of providing liquidity — simultaneously quoting a bid (buy) and an ask (sell) around a fair value, earning the spread when both sides transact, while managing the *inventory* risk of holding an unwanted position. Unlike directional traders who profit from price moves, a market maker profits from *flow*: the repeated capture of the bid-ask spread, agnostic (in the ideal case) to direction. It is the dominant strategy of designated liquidity providers, options market makers, and crypto exchange makers, and it is the strategy most bound to market microstructure.

The market maker's central tension: **spread income vs inventory risk.** Every fill pushes the maker's inventory away from flat; the maker must attract an offsetting fill (to realize the spread) before adverse price movement turns the inventory into a loss. The art is skewing quotes to attract the *offsetting* flow and discourage the *aggravating* flow — without giving away so much spread that the income disappears.

## Core Philosophy — Sell Liquidity, Manage Inventory

A pure market maker has no view on where price is going. The thesis is that, over many quotes, the spread captured exceeds the losses from adverse selection (being filled by someone who knows more than you — the toxic/informed flow). The maker is effectively selling a service (immediacy) and being paid the spread for it. The business works when the ratio of *informed* to *uninformed* flow is low and when the maker can recycle inventory quickly.

Two failure modes define the strategy's risk:
1. **Adverse selection** — informed traders hit your quotes just before price moves against you; you're always the dumb money in those fills.
2. **Inventory blow-up** — one-sided flow accumulates a large position; a price move then wipes out days of spread income.

Every market-making algorithm is an engineering response to these two risks.

## The Classic Model — Avellaneda-Stoikov (2008)

The reference framework. The maker quotes a reservation price `r` and a spread `δ` around it:

- **Reservation price** — the fair value *adjusted for current inventory*. If you're long, you lower your quotes (willing to sell cheaper to offload, reluctant to buy more); if short, you raise them. The skew is proportional to inventory size and the asset's volatility, and inversely proportional to time remaining (urgency grows as the session ends).
- **Optimal spread** — derived to maximize expected utility; it widens with volatility and risk aversion.

The reservation price `r(s,q,t) = s - q·γ·σ²·(T-t)` where `s` is mid, `q` is inventory, `γ` risk-aversion, `σ` volatility, `T-t` time left. The quote skew (`q·γ·σ²·(T-t)`) is the inventory penalty — it's what makes a long maker sell aggressively and buy reluctantly. The Avellaneda-Stoikov insight is that the *optimal* spread and skew are coupled, not free parameters.

Modern makers extend this: stochastic volatility, transient impact, and learning the order-arrival intensities from data rather than assuming them.

## Quote Management — The Mechanics

- **Top-of-book vs deep quotes** — makers compete for queue priority. Being at the front of the bid queue maximizes fill probability when a sell order arrives. Co-location and low latency matter because queue position is first-come.
- **Pegging** — re-quote as the mid moves, keeping a fixed offset. Fast pegging captures more spread but pays more in cancel/replace fees and risk of being picked off.
- **Skew** — asymmetric offsets: wider on the side you don't want filled, tighter on the side you do. A long maker tightens the ask (eager to sell) and widens the bid (reluctant to buy).
- **Layering** — multiple price levels (e.g., bid at best, +1 tick, +2 ticks) to capture fills across a range and average into inventory gradually.
- **Stale-quote avoidance** — cancel instantly when the mid jumps, before getting picked off at a stale price (the "flickering quotes" behavior).

## Inventory Management

The dominant operational concern. Approaches:

- **Hard inventory limits** — stop quoting on the accumulating side once a position cap is reached; force the maker to wait for natural offsetting flow or cross the spread to liquidate.
- **Inventory-skew targets** — continuous skew (Avellaneda-Stoikov) rather than hard limits; the maker gently pushes inventory toward a target (often zero) by skewing quotes.
- **Hedging** — options market makers especially: delta-hedge the accumulated inventory via underlying or other options, leaving only the spread/vega to manage. See [Options Strategies](options-strategies).
- **Inventory risk limits by volatility regime** — tighten limits when realized vol spikes (adverse selection risk rises).

## Adverse Selection Defense

Toxic flow — orders from informed traders — is the maker's enemy. Defenses:

- **VPIN / order-flow toxicity** — estimate the probability that the current flow is informed; widen quotes or pause when toxicity spikes. See [Order Flow Trading](order-flow).
- **Trade-size awareness** — large aggressive orders are more likely informed; quote tighter for smalls, wider (or pull) for larges.
- **Latency arbitrage awareness** — if a faster venue's price just moved, your quote is stale and about to be picked off; sub-millisecond reaction or "speed bumps" (intentional delays to level the field) help.
- **Toxic flow profiling** — identify counterparties (where possible) with consistently profitable fills against you and avoid quoting them.

## Crypto Market Making

Crypto markets are 24/7, fragmented across exchanges, retail-heavy (more uninformed flow), and have funding rates on perps. This makes them attractive for makers but introduces:
- **Cross-exchange arbitrage** of the same asset — a maker on one venue can be picked off by latency arb from another. See [Arbitrage Strategies](cluster-arbitrage).
- **Funding-rate management** — a maker holding perpetual inventory pays/receives funding; the funding cost must be factored into the quote skew.
- **Withdrawal/deposit risk and exchange counterparty risk** — capital is held on the exchange being made.
- **AMMs (Uniswap-style)** — a different paradigm: automated liquidity pools with a deterministic curve rather than discrete quotes. The "impermanent loss" is the AMM maker's inventory risk. See [Crypto-Native / DeFi Methods](cluster-crypto).

## Risk Management

- **Position limits** — absolute caps per asset, per venue, per session.
- **Loss limits / kill switches** — halt trading if cumulative loss exceeds a threshold; the maker should never blow up from a single event.
- **Volatility scaling** — widen spreads and reduce size as vol rises; the spread must always exceed the expected adverse move over the inventory-holding horizon.
- **Latency budget** — know your reaction time vs the fastest participant; if you can't cancel before being picked off, you're the liquidity, not the maker.
- **Capital efficiency** — margin/posting across venues; a maker's capital is mostly tied in inventory and posted margin.

## Common Pitfalls

- **Underestimating adverse selection** — backtests that ignore informed flow show rosy spreads; live, the toxic fills dominate.
- **Ignoring market impact of own cancels** — massive cancel rates (10–100× fills) can trigger exchange throttles or fees.
- **Static spreads in a dynamic vol regime** — a fixed spread that worked at 10% vol loses money at 40% vol.
- **No inventory plan** — quoting symmetrically regardless of position leads to runaway inventory in one-sided markets.
- **Treating it as a spread-capture game only** — the spread is the income; inventory is the risk. Beginners optimize spread, professionals optimize inventory.
- **Forgetting the maker's edge is tiny per fill** — a single bad inventory event can erase a week of spread income; tail risk dominates the distribution.

## Relationships to Other Methods

- **Grid Trading** — a grid is a static, simplified market maker; real MM quotes dynamically and manages inventory continuously. See [Grid Trading](grid-trading).
- **Order Flow Trading** — adverse selection detection (VPIN) and flow toxicity are shared tools. See [Order Flow Trading](order-flow).
- **High-Frequency Trading** — market making is the dominant HFT strategy; latency is the edge. See [High-Frequency Trading](high-frequency-trading).
- **Statistical Arbitration** — makers sometimes run stat-arb overlays to hedge inventory with correlated instruments. See [Statistical Arbitration](statistical-arbitrage).
- **Options Strategies** — options market making requires delta/gamma/vega hedging on top of spread capture. See [Options Strategies](options-strategies).
- **Latency Arbitrage** — the strategy that preys on slow makers. See [Latency Arbitrage](latency-arbitrage).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| hummingbot/hummingbot | 19059 | Open-source high-frequency crypto trading/market-making bot platform | https://github.com/hummingbot/hummingbot |
| nkaz001/hftbacktest | 4244 | HFT & market-making backtesting/trading bot (Rust core, Python) | https://github.com/nkaz001/hftbacktest |
| ctubio/Krypto-trading-bot | 3703 | Self-hosted crypto HFT market-making bot in C++ | https://github.com/ctubio/Krypto-trading-bot |
| warproxxx/poly-maker | 1373 | Automated market-making bot for Polymarket liquidity | https://github.com/warproxxx/poly-maker |
| purefinance/mmb | 607 | Market-making bot in Rust with strategy automation | https://github.com/purefinance/mmb |
| ondra-novak/mmbot | 254 | Market-making bot for crypto markets | https://github.com/ondra-novak/mmbot |
| algotrading-lab/coinbase-market-making-bot | 92 | Coinbase liquidity-providing market-making bot | https://github.com/algotrading-lab/coinbase-market-making-bot |

## Books & Foundational Reading

- Avellaneda & Stoikov — *High-frequency trading in a limit order book* (2008, the foundational paper)
- Lehalle & Laruelle — *Market Microstructure in Practice* (2nd ed.)
- Foucault, Pagano & Röell — *Market Liquidity: Theory, Evidence, and Policy*
- Maureen O'Hara — *High Frequency Market Microstructure*

## Further Study

- Implement Avellaneda-Stoikov reservation pricing in hftbacktest; compare PnL vs a fixed-spread pegged maker.
- Measure the adverse-selection cost: track the mid move in the seconds *after* each of your fills; the average post-fill adverse move is your toxicity tax.
- Compare maker spreads that survive vs fail across vol regimes — derive the minimum spread as a function of realized vol and inventory-horizon.
