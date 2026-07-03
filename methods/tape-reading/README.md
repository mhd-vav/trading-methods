---
title: Tape Reading / Order Book
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: 1860s–1920s (ticker tape) → electronic Level 2 (1990s+)
markets: equities (historical), futures, crypto
timeframe: real-time (tick)
github_repo: mhd-vav/trading-methods
branch: tape-reading
---

# Tape Reading / Order Book

Tape reading is the original art of trading from the *time and sales* (the "tape") and the *order book* (Level 2 depth) — watching every print and every resting order to infer who is buying, who is selling, and at what urgency. Pioneered by Jesse Livermore and Richard Wyckoff on the paper ticker tape of the 1890s–1920s, it is the ancestor of all [Order Flow Trading](order-flow). In the electronic era, "tape reading" means watching the time-and-sales feed and the depth-of-market (DOM) in real time, reading absorption, urgency, and large-participant footprints tick by tick.

## The Two Feeds

- **Time & Sales (the tape)** — every executed trade: price, size, time, and aggressor side (buy/sell initiated). The read: pace (lots of prints = urgency), size (large blocks = institutional), and the direction of aggression.
- **Level 2 / DOM (the book)** — resting limit orders at multiple price levels. The read: stacked size (defense), pulling/adding (intent shifts), spoofing (fake size).

## Classic Reads

- **Absorption** — heavy selling on the tape fails to drop price; a large buyer is absorbing into resting bids. Reversal long when sellers exhaust.
- **Urgency / climax** — a burst of large same-direction prints accelerating; often marks a climax near a level.
- **Iceberg detection** — prints far exceeding visible size at a level; a hidden order is filling.
- **Pulling liquidity** — a large bid vanishing as price approaches; the defender is retreating, signaling weakness.

Tape reading is the discretionary, real-time core of [Order Flow Trading](order-flow); modern equivalents ([Footprint Charts](footprint-charts), [Order Flow](order-flow) metrics) systematize what a tape reader does by eye. It demands deep liquidity (futures, large caps, crypto majors) and fast reaction; thin instruments are untradeable by tape.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| DegenSugarBoo/OpenBook | 169 | Real-time crypto depth heatmap + trade tape (Rust) | https://github.com/DegenSugarBoo/OpenBook |
| murtazayusuf/OrderflowChart | 244 | Orderflow/footprint charts (the modern tape) | https://github.com/murtazayusuf/OrderflowChart |
| srlcarlg/srl-ctrader-indicators | 68 | Order Flow Ticks, Weis & Wyckoff for cTrader | https://github.com/srlcarlg/srl-ctrader-indicators |

## Books & Foundational Reading

- Jesse Livermore (Edwin Lefèvre) — *Reminiscences of a Stock Operator* (the tape-reading classic)
- Richard Wyckoff — *Studies in Tape Reading* (1908)
- Tom DeMark — *The New Science of Technical Analysis* (modern tape/price reads)

## Relationships

Ancestor of [Order Flow Trading](order-flow) and [Footprint Charts](footprint-charts); shares absorption/urgency logic with [Wyckoff Method](wyckoff-method) and [Volume Spread Analysis](volume-spread-analysis).
