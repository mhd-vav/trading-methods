---
title: Supply & Demand Trading
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 2
importance: high
era: 2000s–present (formalized by Sam Seiden / Online Trading Academy)
markets: forex, futures, stocks, crypto, indices
timeframe: any (HTF bias + LTF entry)
github_repo: mhd-vav/trading-methods
branch: supply-demand
---

# Supply & Demand Trading

Supply & Demand (S&D) trading is a price-action methodology that reduces all market movement to a single premise: price moves from one *level of imbalance* to the next. Wherever buyers overwhelm sellers, price gaps away leaving an unfilled "demand zone"; wherever sellers overwhelm buyers, it leaves a "supply zone." The trader's entire job is to map these zones on higher timeframes, wait for price to return, and enter when the zone is respected — mirroring how institutional orders are thought to rest at those levels.

Unlike pure [Wyckoff Method](wyckoff-method), which narrates the full accumulation/distribution cycle, S&D narrows focus to **the origin leg of an explosive move** and the **imbalances** it leaves behind. It is the most systematized retail framework for trading "order blocks" and "liquidity" concepts, and it overlaps heavily with [Smart Money Concepts / ICT](smc-ict), which re-labeled many of the same zones (order blocks, fair value gaps).

## Core Philosophy — Imbalance Is the Edge

Seiden's central claim: markets spend most of their time in *balance* (two-way trade, sideways) and only briefly in *imbalance* (one-sided, fast moves). The fast imbalanced moves are where institutions transact aggressively and leave footprints. Those footprints — the base candles before the impulse — are the zones. Because institutions cannot fill their entire order in one print, price tends to return to those zones to complete the fill, then continue. The retail edge is to wait at the zone rather than chase the impulse.

This is fundamentally an **inventory-restocking** model: large buyers need repeated visits to a price to accumulate size; each visit is a demand zone.

## The Two Zones

### Demand Zone

A price area where buyers were in control, evidenced by a strong bullish impulse *leaving* the area. Two classic patterns:

- **Rally-Base-Rally (RBR)** — a small base (1–3 candles) consolidating after a rally, then another explosive rally up. The base is the demand zone.
- **Drop-Base-Rally (DBR)** — a drop into a base, then a sharp rally up. The base marks where demand overcame supply.

### Supply Zone

The mirror image: a price area where sellers dominated, with a strong bearish impulse leaving it.

- **Drop-Base-Drop (DBD)** — base followed by a sharp drop.
- **Rally-Base-Drop (RBD)** — rally into a base, then a sharp drop.

The zone is drawn from the *base* candles (the consolidation), not the impulse. The impulse proves the imbalance; the base marks where orders rested.

## Zone Classification by Strength

Not all zones are equal. S&D traders rank zones by the quality of the move that left them:

1. **Fresh (untested) zones** — highest probability. Price has not returned since creation. Each retest weakens the zone as resting orders get filled.
2. **Strong imbalance** — the departure candle was very large relative to recent ATR, ideally leaving a gap (imbalance/FVG) on the way out. Gaps = no two-way trade = pure institutional aggression.
3. **Zone with a "profit margin"** — the distance from the zone to the next opposing zone is large enough to offer a favorable risk:reward (minimum 3:1, often 1:4 or better). If the next supply is only 10 pips above a demand entry, the trade is rejected.
4. **HTF zones** — daily/weekly zones carry more weight than 5-minute zones because they represent larger institutional orders and longer-dated interest.

## The Four-Step Trade Plan

The canonical Seiden/OTA process:

1. **Determine trend on the HTF** — is the market making higher highs/lows (demand in control) or lower (supply in control)? Trade only with the HTF bias.
2. **Identify the nearest fresh demand (in uptrend) or supply (in downtrend) zone** on that timeframe.
3. **Drop to a lower timeframe** and wait for price to enter the zone.
4. **Enter on confirmation** — typically a reversal candle (pin bar, engulfing) at the zone, or a smaller-timeframe structure break. Place the stop just beyond the zone; target the next opposing zone.

Confirmation is the most-debated step. Pure S&D enters on a touch with no confirmation (limit orders at the zone); others demand a 5-minute change of structure (BOS) before committing, accepting a slightly worse entry for higher win-rate.

## Relationship to Liquidity

A modern refinement (heavily ICT-influenced): zones are only tradable once *liquidity* has been taken. Price often spikes *past* a demand zone to sweep a prior low (stop run / liquidity grab), then reverses sharply into the zone. This "stop-hunt then zone hold" is the highest-probability S&D setup and is why S&D traders are taught to mark liquidity pools (equal highs/lows, prior session extremes) alongside zones. See [Smart Money Concepts / ICT](smc-ict) for the full liquidity framework.

## Risk Management

- **Stop placement**: beyond the zone's base, not at an arbitrary pip distance. If the zone is wider than your risk allows, the trade is skipped or sized down — never widen the stop.
- **Position sizing**: fixed fractional (0.5–1% per trade). Because zones are wide, entry precision matters for R:R.
- **Targets**: the next opposing zone, or a measured-move from the impulse leg. Scale out at the first target, trail the remainder.
- **Time stop**: if price enters a zone and stalls without reversal within a defined number of bars, exit — the imbalance is being consumed, not respected.

## Common Pitfalls

- **Drawing every base as a zone** — clutter. Only mark zones with a genuine imbalance (large departure, ideally a gap). 3–5 zones per chart is plenty.
- **Trading middle zones** — zones in the middle of a range, far from current price, are low-probability. Focus on the freshest zones nearest price.
- **Ignoring HTF context** — a pristine 15-minute demand zone means nothing if the daily trend is bearish and price is breaking structure down. HTF overrides LTF.
- **Forgetting zones get consumed** — a zone tested 3 times is largely spent. Demand held twice already has absorbed most resting buy orders.
- **Chasing the impulse** — the move *away* from a zone is the confirmation that the zone mattered, but entering on the impulse is late. Wait for the *return*.
- **No liquidity awareness** — entering a demand zone before the equal lows below are swept exposes you to the stop-hunt that invalidates the zone.

## Relationships to Other Methods

- **Wyckoff** — S&D's "demand zone" ≈ Wyckoff's spring/last point of support; the impulse away ≈ the sign of strength. S&D is a zoomed-in, rule-bound slice of the Wyckoff cycle.
- **SMC/ICT** — order blocks are functionally supply/demand bases; fair value gaps (FVG) are the imbalance S&D traders require. S&D predates and overlaps the ICT vocabulary.
- **Price Action** — S&D is a structured subset of price action; the entry confirmation candles are pure price-action patterns.
- **Market Profile** — high-volume nodes often coincide with consumed demand/supply (accepted price); low-volume nodes are the imbalances S&D targets. See [Market Profile / Volume Profile](market-profile).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| passiontrader/SMC-Quantitative-Suite | 5 | High-fidelity Python: SMC market structure, order blocks, zones, backtesting | https://github.com/passiontrader/SMC-Quantitative-Suite |
| samiath17/smc-tradingview-indicator | 28 | Pine v5 SMC pack: order blocks, zones, liquidity, BOS/CHoCH | https://github.com/samiath17/smc-tradingview-indicator |
| GeneralTradingSarl/Smart-Money-Concepts | 9 | MT5 SMC indicator: order blocks, supply/demand, liquidity | https://github.com/GeneralTradingSarl/Smart-Money-Concepts |
| trisjohn/ForexZoneBot | 5 | Bot building supply & demand zones from user input, trades retests | https://github.com/trisjohn/ForexZoneBot |
| idliwada/nse-sd-scanner | 0 | NSE S&D scanner: DBR/RBR/RBD/DBD zones, backtesting, Fibonacci | https://github.com/idliwada/nse-sd-scanner |
| nelsonchaves/trading-strategy-automation | 0 | Systematic automation of discretionary S/D strategy, multi-TF | https://github.com/nelsonchaves/trading-strategy-automation |

## Books & Education

- Sam Seiden — OTA core curriculum (supply/demand origin leg, odds enhancers)
- *Trading in the Zone* — Mark Douglas (psychology, not S&D mechanics, but the title is apt)
- LTC/ICT mentorship (2020–2022) — modernized the order-block/FVG/liquidity vocabulary that overlaps S&D

## Further Study

- Compare zone-hold entries across instruments: FX majors, indices (NQ/ES), gold. Zones tend to be cleaner on instruments with strong institutional participation.
- Build a zone-freshness tracker: log each zone's number of tests; retire after 2–3.
- Cross-reference with [Volume Spread Analysis](volume-spread-analysis): a demand zone holding on declining volume (no supply) is a stronger long.
