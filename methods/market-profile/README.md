---
title: Market Profile / Volume Profile
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 1
importance: high
originator: J. Peter Steidlmayer (Market Profile); late additions for Volume Profile
era: 1980s (CBOT) – present
markets: futures (classic), equities, forex, crypto
timeframe: intraday to daily
github_repo: mhd-vav/trading-methods
branch: market-profile
---

# Market Profile / Volume Profile

Market Profile is a charting and analytical method developed by J. Peter Steidlmayer at the Chicago Board of Trade in the 1980s. It reorganizes price data not as a time-based candlestick chart but as a **distribution** of where the market actually traded — a profile that reveals how price was accepted or rejected over a session. The central idea is that markets auction back and forth searching for value: price spends time where two-sided trade is comfortable (value) and moves quickly through prices where it is not. The profile makes that acceptance/rejection structure visible.

**Volume Profile** is the closely related modern variant that plots traded *volume* at each price rather than the time-based TPO (Time Price Opportunity) counts of classic Market Profile. Both answer the same question — *where did the market do business, and where did it refuse to?* — and share the same vocabulary (POC, value area, nodes). The terms are often used interchangeably in software.

## Core Philosophy — The Market as an Auction

Steidlmayer's insight: markets are continuous two-way auctions. Price advertises opportunity; time regulates all opportunities. The market probes up to find sellers and down to find buyers; where it finds both, it lingers (value), and where it doesn't, it moves on. Market Profile renders this auction process statistically:

- **Price advertises** — the market offers a price to attract the other side.
- **Time regulates** — prices that attract two-sided trade are sustained (high TPO/volume); prices that don't are quickly abandoned (low TPO/volume).
- **Volume facilitates** — heavy volume at a price confirms acceptance; thin volume means rejection.

The result is a bell-curve-like distribution for each session, whose *shape* tells the trader whether the market is balanced (ranging, two-sided) or imbalanced (trending, one-sided).

## The Profile Structure

Classic Market Profile divides the session into half-hour periods (e.g., the 8:30–3:15 futures session = ~13 periods) and records each price touched in each period as a letter (A, B, C...). Stacking these letters by price produces the profile shape. Each letter = one TPO (Time Price Opportunity). Volume Profile substitutes actual traded volume for the letter counts, but the resulting shape and analysis are the same.

### The Bell Curve and Its Anatomy

A balanced session produces a roughly normal (bell-shaped) distribution:

- **POC (Point of Control):** the price level with the most TPOs/volume — the "fairest" price of the session, where the most trade occurred. The POC is the gravitational center; price tends to revisit it.
- **Value Area (VA):** the price range containing 70% of the session's TPOs/volume (one standard deviation). This is where the market found fair value — the "comfort zone." The **Value Area High (VAH)** and **Value Area Low (VAL)** bound it.
- **High Volume Nodes (HVN):** price levels with heavy TPO/volume — acceptance zones, magnets, future support/resistance.
- **Low Volume Nodes (LVN):** price levels with little TPO/volume — rejection zones; price tends to move *through* them quickly when revisited (they're "voids" the market didn't accept).

The shape — bell (balanced) vs. elongated/tailed (imbalanced) — is the first read: balanced profiles favor range trades (fade edges back to POC); imbalanced profiles favor trend continuation (trade with the extension).

### Key Reference Points

- **Initial Balance (IB):** the range of the first hour (first two periods, A and B). The IB often frames the day's framework — many days stay within or reference the IB. An IB extension (move beyond IB) signals conviction; a narrow IB often leads to a range day.
- **Open Range:** the opening period's range; related to IB.
- **Range Extension:** price beyond the IB; the direction of extension biases the session.
- **Buying/Selling Tails:** single-print extremes at the session low (buying tail — sellers rejected) or high (selling tail — buyers rejected). Long tails = strong rejection = the extreme is significant; a single-period low print that holds = acceptance of higher prices.
- **Profile Range:** the full high-to-low of the session.

## Day Types (Steidlmayer / Dalton)

The profile's shape classifies the day, which dictates strategy:

- **Normal Day:** wide IB (~80% of range), balanced profile. Fade the edges toward the POC.
- **Normal Variation:** smaller IB (~50% of range) with extension. Range trade with a directional lean.
- **Trend Day:** strong one-sided move; profile elongated, few single prints except in the trend direction, POC near one extreme. Trade *with* the trend; do not fade.
- **Double Distribution Trend Day:** initial balance forms, then a pause, then a second distribution extends the trend. Two value areas.
- **Neutral Day:** balanced, narrow range, POC in the middle. Range trade; low conviction.
- **Non-Trend Day:** very narrow, listless; often before a news event. Stand aside.

Recognizing the day type early (by the IB and first few periods) sets the correct tactics: fade on balanced days, follow on trend days.

## Trading With the Profile

- **Value-area trades (balanced day):** fade moves outside the value area back toward the POC — long at/under VAL, short at/over VAH — when the profile is balanced and the move lacks follow-through. Exit at POC.
- **Value-area break (initiative trade):** if price breaks VAH and *accepts* above it (sustains, builds volume), the value area is shifting up — go long targeting the next HVN/extension. Symmetric at VAL.
- **Trend-day trade:** on an elongated profile, buy pullbacks to the developing POC / prior HVN; don't fade. Trail with the developing value area.
- **Node reaction:** expect reactions at prior-session HVNs (support/resistance) and quick moves through LVNs (voids). Plan entries just beyond LVNs on the side of value; expect momentum through the void.
- **POC migration:** a rising POC across sessions = uptrend; falling POC = downtrend. A POC that fails to migrate = range.
- **Balanced target:** the projection `2 × POC − VAL` (or symmetric from VAH) gives a measured-move target for balanced-range breakouts (the library exposes this as `balanced_target`).

## Volume Profile vs. TPO (Market Profile)

- **TPO (classic Market Profile):** counts *time* spent at each price (one letter per period). Emphasizes *where price lingered* regardless of volume. Better for pure auction structure and day-type reading.
- **Volume Profile:** plots *traded volume* at each price. Emphasizes *where actual business was done*. Better for locating genuine institutional interest (heavy-volume levels).
- In practice they correlate but diverge: a price can have many TPOs (lingered) but low volume (no real trade), or few TPOs but high volume (a spike). Many traders use both — TPO for structure, volume for confirmation of acceptance.

## Multi-Day and Composite Profiles

- **Composite profile:** combine several sessions' profiles to find larger-scale POCs, value areas, and nodes. A multi-day HVN is far stronger support/resistance than a single-day one.
- **Naked POC:** a POC from a prior session that price has not returned to. Price often revisits naked POCs (unfilled value), making them targets/magnets.
- **Trend via composite value:** successive sessions' value areas shifting direction define the higher-timeframe trend.

## Risk Management

- **Stops:** beyond the rejected extreme — below a buying tail (long), above a selling tail (short). A tail's rejection defines invalidation.
- **Targets:** the opposite value-area edge, the POC, or the next HVN/LVN. On trend days, trail with the developing value area.
- **Day-type discipline:** the biggest risk is fading a trend day (treating a one-sided profile as balanced). Read the shape first; tactics follow.
- **Avoid the middle of a value area** as an entry — low edge, price can wander to either side. Enter at the edges with rejection or on confirmed VA breaks.

## Common Pitfalls

- **Forcing a balanced read on a trend day.** The classic loss. The profile shape tells you the day type; respect it.
- **Trading the POC in isolation.** The POC is a reference, not a signal. Context (day type, location vs. value, rejection) determines the trade.
- **Ignoring the higher-timeframe profile.** A daily HVN overrides an intraday pattern. Stack timeframes.
- **Confusing TPO and volume nodes.** They often differ; know which you're reading and why.
- **Over-reading a single session.** Profiles are statistical; a single day's shape is noisy. Look for patterns across sessions and composites.

## Relationship to Other Methods

- **Wyckoff:** Market Profile shows *where* the Composite Operator did business (the high-volume nodes = accumulation/distribution zones). Highly complementary — profile locates the range, Wyckoff reads the phase within it. See [Wyckoff Method](wyckoff-method).
- **Volume Spread Analysis:** VSA reads bar-by-bar volume; Market/Volume Profile aggregates volume by *price*. Together they cover time-by-bar and price-level views. See [Volume Spread Analysis](volume-spread-analysis).
- **VWAP:** VWAP is the volume-weighted average price (a single value); the profile is the full distribution. VWAP ≈ a summary statistic of the profile. See [VWAP Trading](vwap-trading).
- **Order Flow / Footprint:** Profile shows where volume traded by price; footprint shows it by bar. See [Footprint Charts](footprint-charts) and [Tape Reading](tape-reading).
- **Auction Market Theory:** The theoretical framework Market Profile operationalizes. See [Auction Market Theory](auction-market-theory).

## Why It's Powerful

Market Profile is one of the few methods that reveals the *structure of market acceptance* — not just where price went, but where the market was comfortable and where it was rejected. This makes it exceptional at identifying genuine support/resistance (the volume-confirmed levels) and at reading day-type/trend vs. range early in a session. It scales from intraday scalping (reacting to nodes) to swing trading (composite POCs) to trend detection (value-area migration). Traders who internalize "price advertises, time/volume regulate" develop a structural view of the market that no oscillator provides.

## Open-Source References

- **bfolkens/py-market-profile** (★397) — the canonical Python library: POC, value area, initial balance, high/low value nodes, balanced target from a Pandas OHLCV DataFrame. `pip install marketprofile`. https://github.com/bfolkens/py-market-profile
- **EarnForex/MarketProfile** (★193) — Market Profile indicator for MT4, MT5, and cTrader. https://github.com/EarnForex/MarketProfile
- **srlcarlg/srl-python-indicators** (★43) & **srl-ctrader-indicators** (★68) — Volume/TPO Profile, order flow ticks, Weis & Wyckoff system for Python and cTrader. https://github.com/srlcarlg/srl-python-indicators
- **lawrencezcl/DAX-Trading-System** — DAX system combining Market Profile with Wyckoff and options/futures analysis. https://github.com/lawrencezcl/DAX-Trading-System
- **chacterchen/trading_charts_pyqtgraph** — TPO + candlestick + Renko + P&F charting. https://github.com/chacterchen/trading_charts_pyqtgraph
- **mplfinance** ecosystem — used to render volume profiles alongside candles in Python.

## Further Study

- James Dalton — *Mind Over Markets* (the definitive Market Profile text; day types, profile structure, auction logic).
- J. Peter Steidlmayer — *Steidlmayer on Markets* (the originator's theory).
- Eric Jones & Robert Dalton — *Markets in Profile*.
- CBOT Market Profile education materials (the historical source of the method).

