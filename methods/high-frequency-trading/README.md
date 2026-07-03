---
title: High-Frequency Trading (HFT)
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 2
importance: high
markets: equities, futures, crypto
timeframe: microseconds–seconds
github_repo: mhd-vav/trading-methods
branch: high-frequency-trading
---

# High-Frequency Trading (HFT)

High-Frequency Trading is a class of fully automated strategies that exploit tiny, fleeting price inefficiencies by submitting and cancelling thousands of orders per second, holding positions for microseconds to minutes, and ending the day flat. HFT is defined not by a single alpha source but by **speed**: colocation, direct market access, FPGA/network-engineered data paths, and microsecond-latency order management. Alpha sources include [Market Making](market-making) (capturing the spread), [Latency Arbitrage](latency-arbitrage), [Statistical Arbitrage](statistical-arbitrage) at tick level, event arbitrage (reacting to news in microseconds), and [Momentum Ignition](momentum-ignition). The economics: tiny per-trade edge × enormous trade count − infrastructure/colocation/data costs.

## Core Characteristics

- **Speed as edge** — HFT firms colocate servers in exchange data centers, use kernel-bypass NICs and FPGAs, and optimize the full network path to be faster than competitors. Being first to act on a quote change or news tick is the moat.
- **Flat at close** — HFT carries no overnight risk; inventory is liquidated intraday, often within seconds. Capital turnover is extreme (daily turnover can dwarf the firm's capital many times over).
- **Order book micromechanics** — HFT reads full L2/L3 order book depth, queue position, and order-flow imbalance ([Order Flow](order-flow)) to predict sub-second price drift. It postulates liquidity, cancels, and revises continuously.
- **Market making bent** — much HFT is automated market making: posting passive limit orders on both sides to capture the bid-ask spread, managing inventory with skew, and unwinding before adverse selection hits.

## Strategy Families Within HFT

1. **Passive market making** — capture spread, manage inventory skew, race to cancel on toxic flow. The largest HFT revenue source. See [Market Making](market-making).
2. **Latency arbitrage** — exploit stale quotes on a slow venue vs a fast one. See [Latency Arbitrage](latency-arbitrage).
3. **Statistical / pairs at tick level** — cointegration or lead-lag between correlated instruments executed at high frequency. See [Statistical Arbitrage](statistical-arbitrage).
4. **Event arbitrage** — machine-readable news (e.g., economic releases) parsed and traded in microseconds.
5. **Momentum ignition / order anticipation** — detecting a large institutional order and front-running the resulting momentum. Ethically and legally fraught (often = spoofing). See [Momentum Ignition](momentum-ignition).

## Risk Management

- **Latency risk** — the dominant risk: if your quotes are stale when the market moves, you get adversely selected ("run over"). Mitigated by aggressive cancel logic and queue-position awareness.
- **Inventory/overnight risk** — avoided by mandatory flat-close and tight inventory caps with auto-liquidation skew.
- **Technology/operational risk** — software bugs at HFT speed can lose millions in seconds ("kill switches," hard position limits, pre-trade risk checks are mandatory).
- **Regulatory risk** — spoofing, layering, and momentum-ignition practices are illegal in most jurisdictions (Dodd-Frank, MAR). HFT firms invest heavily in compliance/surveillance.

## Common Pitfalls

- **Backtest mirage** — tick data survivorship and microstructure effects make naive backtests wildly optimistic; real fills are worse than assumed due to queue position and cancellation.
- **Infrastructure arms race** —edge decays as competitors match your speed; constant reinvestment in hardware is required.
- **Adverse selection** — the fundamental market-making trap: your resting orders get filled exactly when informed flow is about to move price against you.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| nkaz001/hftbacktest | 4245 | HFT & market-making backtesting/trading framework (Rust/Python) | https://github.com/nkaz001/hftbacktest |
| hummingbot/hummingbot | 19059 | High-frequency crypto market-making/grid bot platform | https://github.com/hummingbot/hummingbot |
| michaelgrosner/tribeca | 4114 | HFT crypto market-making platform in Node.js | https://github.com/michaelgrosner/tribeca |
| ctubio/Krypto-trading-bot | 3703 | Self-hosted HFT crypto market-making bot in C++ | https://github.com/ctubio/Krypto-trading-bot |
| jamesmawm/High-Frequency-Trading-Model-with-IB | 2889 | HFT model w/ pairs & mean-reversion on IB | https://github.com/jamesmawm/High-Frequency-Trading-Model-with-IB |
| rorysroes/SGX-Full-OrderBook-Tick-Data-Trading-Strategy | 2300 | HFT strategies via data science on full order book | https://github.com/rorysroes/SGX-Full-OrderBook-Tick-Data-Trading-Strategy |

## Books & Foundational Reading

- Irene Aldridge — *Real-Time Risk* and *High-Frequency Trading*
- Rolf Bovy — *Proposals for a HFT Tick-by-Tick Dataset*; Ph.D. thesis work
- Michael Lewis — *Flash Boys* (popular, journalistic; the spoofing/front-running debate)
- Thierry Foucault, Marco Pagano, Ailsa Röell — *Market Liquidity* (academic microstructure theory)

## Relationships

Shares market-making core with [Market Making](market-making); uses [Statistical Arbitrage](statistical-arbitrage) at tick level; overlaps [Latency Arbitrage](latency-arbitrage); reads the same microstructure as [Order Flow](order-flow), [Tape Reading](tape-reading), and [Footprint Charts](footprint-charts); the dark side overlaps [Momentum Ignition](momentum-ignition); execution discipline relevant to [Execution Algorithms](execution-algorithms).
