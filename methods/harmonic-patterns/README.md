---
title: Harmonic Patterns
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 2
importance: medium-high
originator: H.M. Gartley (1935); Scott Carney, Larry Pesavento (refined)
markets: forex, stocks, futures, crypto
timeframe: any
github_repo: mhd-vav/trading-methods
branch: harmonic-patterns
---

# Harmonic Patterns

Harmonic trading is a geometric, Fibonacci-based methodology that identifies specific price structures ("harmonic patterns") where the relationships between swing legs conform to precise Fibonacci ratios. Originating with H.M. Gartley's 1935 *Profits in the Stock Market* and systematized by Scott Carney (*Harmonic Trading*) and Larry Pesavento, it posits that markets form recurring geometric shapes — XABCD structures — whose internal retracements and extensions, when aligned to Fibonacci ratios, define high-probability reversal zones (the "Potential Reversal Zone," PRZ).

The method's edge is its **specificity**: unlike loose chart patterns, harmonic patterns demand exact Fibonacci ratios between four pivot points (X, A, B, C, D). A structure that almost fits is not the pattern. This precision yields defined entry zones, tight invalidation (stops just beyond the PRZ), and measured targets.

## Core Philosophy — Geometry + Fibonacci Reversal

Harmonic trading assumes that price swings relate to each other by Fibonacci ratios because those ratios reflect natural retracement and extension levels where supply/demand rebalances. When a four-leg structure (X→A→B→C→D) completes with the correct ratios, point D is a "Potential Reversal Zone" — a confluence of Fibonacci support/resistance where a reversal is probable. The trader enters at D with a tight stop beyond it, targeting the prior swing structure.

The key concept is the **AB=CD** idea: in many patterns, the CD leg equals (or is a Fibonacci extension of) the AB leg, so the D completion is both geometrically and mathematically defined.

## The XABCD Structure

All harmonic patterns are built on four pivots labeled X, A, B, C, D:

- **XA** — the initial impulse leg (the move the pattern retraces/extends from).
- **AB** — the first retracement of XA.
- **BC** — a retracement of AB.
- **CD** — an extension (or retracement) that completes at D, the PRZ.

The pattern is defined by the Fibonacci relationships among these legs. D is where the trade is taken (a reversal is expected). X is the extreme that defines the stop (just beyond X).

## The Core Patterns

### ABCD (the simplest, the foundation)

Three pivots A, B, C, D (no X leg): AB defines a move, BC retraces AB, CD extends to complete.
- **AB = CD** in both price and time (the classic). Or CD = 1.272×AB or 1.618×AB (Fibonacci extension).
- BC typically retraces AB by 61.8% or 78.6%.
- **D is the PRZ** — enter for a reversal toward B/C. Stop beyond D.
- Bullish ABCD: D is a low (buy). Bearish ABCD: D is a high (sell).

ABCD is the building block; every other pattern embeds an ABCD relationship.

### Gartley (the original, 1935)

- **AB retraces XA by 61.8%.**
- **BC retraces AB by 38.2%–88.6%** (often 61.8%).
- **CD = 1.272×AB** (or 1.618×) — the ABCD completion.
- **AD retraces XA by 78.6%** — D is the 78.6% retracement of XA.
- Bullish Gartley: forms at a pullback in an uptrend; D is a buy. Bearish Gartley: mirror.

The Gartley is a *retracement* pattern — D stays inside the XA range (doesn't exceed X).

### Bat

- **AB retraces XA by < 61.8%** (often 38.2%–50%).
- **BC retraces AB by 38.2%–88.6%.**
- **CD = 1.618×BC** (extension).
- **AD retraces XA by 88.6%** — D is deeper than Gartley but still inside XA.
- High-precision pattern; the 88.6% retracement is the defining ratio.

### Alternate Bat (Alt-Bat)

- AB retraces XA by 38.2%.
- BC retraces AB by 38.2%–88.6%.
- CD = 2.0×BC (extension).
- AD retraces XA by 113% (D exceeds X slightly).

### Butterfly

- **AB retraces XA by 78.6%.**
- BC retraces AB by 38.2%–88.6%.
- **CD = 1.618×AB** (extension).
- **AD extends XA by 127%–161.8%** — D *exceeds* X (an extension pattern, unlike Gartley/Bat).
- The 127.2% extension is the classic Butterfly completion.

### Crab

- AB retraces XA by 38.2%–61.8%.
- BC retraces AB by 38.2%–88.6%.
- **CD = 2.24×–3.618×AB** (large extension).
- **AD extends XA by 161.8%** — D far beyond X. The most extended pattern; tightest PRZ relative to the move.

### Deep Crab

- AB retraces XA by 88.6%.
- Otherwise like Crab: CD extension 2.24×–3.618×AB, AD = 161.8% extension of XA. D beyond X.

### Shark

- A three-leg structure (O, X, A, B) — distinct from the XABCD family. Based on the 88.6% retracement and 113% extension.
- BC retraces OX by 88.6%; CD extends by 113% of OX. D (the "5-0" completion) is the PRZ.

### Cypher

- XC retraces XA by 38.2%–61.8%.
- BC extends beyond A: **BC = 113%–141.4% of XA** (extension, not retracement).
- CD = 78.6% retracement of XC.
- D is the PRZ. The Cypher's defining feature is the BC extension beyond A.

### Three Drives

Three successive ABCD-like drives, each extending by 1.272 then 1.618, with each retracement at 61.8%. A clean three-wave exhaustion pattern marking a top/bottom.

## Trading the Patterns

1. **Detect the structure:** Use a ZigZag indicator (filters noise into pivots) to identify X, A, B, C, then project where D *should* complete based on the ratios. Libraries like `djoffrey/HarmonicPatterns` automate this (completed + predicting patterns).
2. **Wait for D to form:** Don't enter on projection alone. Wait for price to reach the PRZ and show a reversal trigger (candle rejection, momentum turn) — this confirms the pattern is completing.
3. **Enter at the PRZ:** with the reversal trigger, in the direction of the expected reversal (long at a bullish D, short at a bearish D).
4. **Stop:** just beyond X (for retracement patterns) or beyond D (for extension patterns where D exceeds X). The tight invalidation is harmonic's R:R advantage.
5. **Targets:** the first target is the 38.2% retracement of CD, the second the 61.8% retracement — i.e., retrace the CD leg. Some traders target the pattern's prior swing highs/lows.
6. **Scale out:** book partial at the first target, trail the rest.

## Risk Management

- **Tight stops:** the defined PRZ and X-based invalidation give harmonic trades inherently good R:R (often 2R–5R) *if* the pattern holds.
- **Pattern invalidation:** if price blows through D beyond the ratio tolerance, the pattern failed — exit. Don't hope.
- **Confluence:** the best harmonic setups have PRZs that align with other structure (prior support/resistance, an order block, a Fibonacci cluster from a higher timeframe).
- **Position sizing:** standard fixed-fractional; because stops are tight, sizing must account for slippage at D (volatility can spike into the PRZ).

## Common Pitfalls

- **Forcing patterns.** Not every swing is a harmonic pattern. The Fibonacci ratios must fit within tolerance (typically ±1–2%); a sloppy fit is not the pattern.
- **Entering on the projection.** The "predicting" D is a *zone to watch*, not an entry. Price must reach it and show reversal. Many projected patterns never complete.
- **Ignoring the bigger trend.** A bullish harmonic in a strong downtrend is a counter-trend fade — lower probability. Align patterns with the higher-timeframe trend when possible.
- **Over-reliance on a single ratio.** The PRZ is a confluence; the more ratios that align at D (AB=CD + AD retracement + BC extension), the higher quality the setup.
- **Holding through invalidation.** The tight stop is the method's strength; widening it defeats the R:R and turns a defined trade into a gamble.

## Relationship to Other Methods

- **Fibonacci Trading:** Harmonic is Fibonacci trading applied to geometric structures. The ratios are the engine. See [Fibonacci Trading](fibonacci-trading).
- **Price Action / Patterns:** Harmonic is a precise sub-discipline of chart-pattern trading. See [Chart Patterns](chart-patterns).
- **Wyckoff / SMC:** D completions often coincide with Wyckoff Spring/UTAD zones or SMC order blocks — confluence raises conviction. See [Wyckoff Method](wyckoff-method).
- **Elliott Wave:** The XABCD legs relate to Elliott's impulse/correction waves; harmonic offers precise Fibonacci completion points within wave structure. See [Elliott Wave Theory](elliott-wave).

## Why It's Useful

Harmonic trading's appeal is **defined risk with measured reward**. Because every pattern demands exact Fibonacci ratios and offers a clear invalidation point (beyond D/X), a harmonic trade has its R:R known *before* entry — a rarity in discretionary technicals. The method rewards the patient pattern-fisher and punishes the force-fitter. Its precision makes it complementary to looser methods: when a harmonic PRZ lands on a structural level from another method, the confluence is among the highest-conviction setups in technical trading.

## Open-Source References

- **djoffrey/HarmonicPatterns** (★135) — modern high-performance Python library detecting 9 patterns (ABCD, Gartley, Bat, Alt-Bat, Butterfly, Crab, Deep Crab, Shark, Cypher); completed + predicting scans, mplfinance visualization. The canonical automated reference. https://github.com/djoffrey/HarmonicPatterns
- **sandybradley/HarmonicTrader** (★10) — backtest and trade harmonic patterns on Deribit. https://github.com/sandybradley/HarmonicTrader
- **rajatjpatel/Hamonics** (★6) — harmonic pattern reference/implementations (Gartley origin documented). https://github.com/rajatjpatel/Hamonics
- **ignaciocorball/loretzian-bot** (★5) — trading bot combining TA, ML, and harmonic patterns. https://github.com/ignaciocorball/loretzian-bot
- **lazybigcat0624/harmonic-patterns-s** (★1) — professional MQL5 automated harmonic detection for MT. https://github.com/lazybigcat0624/harmonic-patterns-s
- **BenWilliams2109/Forex-Harmonic-Pattern-Scanner** (★4) — bullish Gartley locator using Fibonacci. https://github.com/BenWilliams2109/Forex-Harmonic-Pattern-Scanner
- **TA-Lib** — ZigZag + Fibonacci computation underlying pattern detection.

## Further Study

- Scott Carney — *Harmonic Trading, Vols. 1 & 2* (the definitive modern system; all pattern ratios).
- Larry Pesavento — *Fibonacci Ratios with Pattern Recognition*.
- H.M. Gartley — *Profits in the Stock Market* (the 1935 origin; the Gartley pattern).
- Pesavento's "HarmonicTrader" site — pattern library and education.

