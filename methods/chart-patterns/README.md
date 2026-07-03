---
title: Chart Patterns
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 2
importance: high
era: 1900s–present (Dow, Schabacker, Edwards-Magee, Bulkowski)
markets: all (stocks, futures, FX, crypto)
timeframe: any (daily/weekly most studied)
github_repo: mhd-vav/trading-methods
branch: chart-patterns
---

# Chart Patterns

Chart-pattern analysis identifies geometric formations in price structure — the shapes price draws over many bars — that encode the psychology of the prior trend and forecast its continuation or reversal. Where a [Candlestick Pattern](candlestick-patterns) reads one to three bars, a chart pattern reads tens to hundreds: the slow arc of a rounding bottom, the converging lines of a triangle, the three peaks of a head and shoulders. These are the *macro-structures* of price action, and they are the oldest formal layer of technical analysis, codified by Schabacker and Edwards-Magee and statistically catalogued by Bulkowski.

The method's premise: price movements are not random walks but leave recurring footprints of crowd psychology — accumulation, distribution, indecision, conviction, climax. These footprints, drawn as support/resistance trendlines, form recognizable shapes whose breakouts have measurable forward expectations. The academic verdict is mixed (efficient-market purists reject them; practitioners and Bulkowski's large-sample stats find real but modest edges), but chart patterns remain the lingua franca of discretionary technical trading and the geometric backbone of [Price Action](price-action).

## Core Philosophy — Geometry of Crowd Psychology

A chart pattern is a *consolidation or transition* between trends. Trends move in impulses and corrections; the corrections draw shapes. The pattern's geometry reveals whether buyers or sellers are gaining ground during the pause:
- **Contracting patterns** (triangles, flags, pennants, VCP) — volatility is diminishing; one side is being exhausted; the next move, when it breaks out, tends to be explosive (volatility expansion follows contraction).
- **Reversal patterns** (head & shoulders, double tops/bottoms, rounding) — the prior trend's momentum is dying; control is transferring.
- **Continuation patterns** (flags, pennants, rectangles) — a brief pause in a trend that resumes.

The shared mechanic: a pattern builds "cause" (Wyckoff's term — see [Wyckoff Method](wyckoff-method)) and the breakout is the "effect." The taller/wider the pattern, the larger the expected move (measured-move rule).

## The Major Patterns

### Reversal Patterns

- **Head and Shoulders** — three peaks, middle (head) highest, with a neckline connecting the two intervening troughs. Forms after an uptrend. The right shoulder failing to exceed the head shows buyers exhausted; breaking the neckline confirms the reversal. Target = head height projected below neckline. The inverse H&S is the bottom equivalent. The most famous reversal pattern; Bulkowski ranks it among the more reliable.
- **Double Top / Double Bottom** — price tests a high (low) twice at roughly the same level and fails, forming an "M" (or "W"). The second test shows the level is defended; the break of the intervening trough (peak) confirms. Targets measured from the breakout. "Tweezer" extreme variant.
- **Triple Top / Bottom** — three tests; rarer, more reliable than double. The level held three times = strong defense.
- **Rounding Top/Bottom (saucer)** — slow semicircular transition; the gradual shape reflects a slow, deliberate transfer of control (often accumulation/distribution). Long-term pattern, days to months.
- **V-Top/Bottom (spike reversal)** — sharp reversal with no consolidation; a climax spike immediately reversing. Hard to trade (no entry zone), common at exhaustion.

### Continuation Patterns

- **Flags** — a sharp impulse (the "pole") followed by a small counter-trend rectangle channel (the "flag") sloping against the trend. Brief (1–3 weeks); breakout resumes the trend. One of the highest-reliability patterns.
- **Pennants** — like flags but the consolidation is a small symmetrical triangle (converging lines), not a rectangle. Same pole-and-pause structure.
- **Rectangles (trading ranges)** — price bounces between parallel horizontal support/resistance. Continuation if it breaks in the trend's direction; can reverse. A pause where supply and demand are roughly balanced.

### Contracting / Triangle Patterns

- **Symmetrical triangle** — converging trendlines (lower highs, higher lows); indecision. Breakout direction is not predetermined; trade the breakout, not the anticipation. Volatility contracts → expansion on breakout.
- **Ascending triangle** — flat top (resistance), rising bottom (higher lows). Buyers increasingly eager; bullish bias. Breakout up is the expected resolution.
- **Descending triangle** — flat bottom (support), falling tops. Bearish bias. Mirror of ascending.
- **Wedge (rising/falling)** — converging lines both sloping the same direction. A rising wedge (both lines up, but converging) is bearish (momentum fading); falling wedge bullish. Reversal pattern despite trending direction.

### The Volatility Contraction Pattern (VCP)

Mark Minervini's modern refinement, central to his SEPA momentum method: a series of nested contractions — each successive pullback tighter (lower volatility) and shallower than the last — ending in a tight squeeze and breakout. VCP encodes the idea that *as supply dries up during a base, volatility must contract*; the breakout from the final tight contraction is the highest-probability entry. VCP is essentially a structured, multi-contraction flag/pennant tuned for momentum-stock breakouts.

## The Measured-Move Rule

Most patterns project a target by measuring the pattern's height and extending it from the breakout point:
- H&S: head-to-neckline distance, projected below neckline break.
- Triangle: widest part of triangle projected from breakout.
- Flag: pole height projected from the flag breakout.

This isn't magic — it's a volatility-scaling heuristic: bigger cause → bigger effect. Use as a *first target*, not a guarantee.

## The Context Rule (Again, Critical)

Like candlesticks, patterns are context-dependent:
- **With the prevailing trend** — continuation patterns (flags, pennants) in trends are high-probability; reversal patterns against a strong trend often fail.
- **After extended moves** — reversal patterns at the end of long trends are more meaningful.
- **At major levels** — patterns completing at HTF support/resistance, Fib levels, or round numbers carry more weight. See [Fibonacci Trading](fibonacci-trading), [Supply & Demand](supply-demand).
- **Volume** — breakouts on rising volume are genuine; breakouts on falling volume are suspect (no conviction). Volume should decline *into* a triangle/flag (contraction) and *expand* on the breakout.

## Confirmation and Entry

- **Breakout entry** — enter on the close beyond the pattern boundary (neckline, trendline, resistance). Risk: false breakouts.
- **Pullback entry (throwback/pullback)** — wait for the breakout, then enter on the retest of the broken boundary from the new side. Higher win-rate, worse entry. The boundary that was resistance becomes support.
- **Stop placement** — beyond the pattern's opposite extreme (below the flag's low, below the H&S right shoulder) or just inside the broken boundary. Structural invalidation.
- **Time stop** — if a breakout doesn't follow through within a reasonable window, the pattern is failing; exit.

## Risk Management

- **Pattern failure is real** — Bulkowski's data shows even good patterns fail 20–40% of the time. Size for being wrong.
- **False breakouts (whipsaws)** — the dominant risk; mitigate with close-confirmation (wait for the candle to close beyond the line, not just pierce it) and volume.
- **Don't pre-empt** — entering before the breakout "because it looks like an ascending triangle" is gambling. The edge is in the confirmed break.
- **Targets scale** — take partials at the measured move, trail the rest; don't hold the whole position for a best-case.

## Common Pitfalls

- **Pattern-fitting (pareidolia)** — the human eye sees patterns in noise; not every wiggle is a triangle. Require clear, multiple-touch geometry.
- **Ignoring the trend** — trading a "bullish ascending triangle" in a downtrend is fighting the flow.
- **Premature entry** — acting before the breakout. The pattern is a setup, the break is the trigger.
- **Volume-blind breakouts** — low-volume breaks fail disproportionately; always confirm.
- **Over-trusting measured moves** — they're targets, not guarantees; manage the trade, don't hope.
- **Neglecting timeframe** — a daily H&S dominates a 15-minute flag; HTF patterns override LTF.

## Relationships to Other Methods

- **Candlestick Patterns** — the building blocks of chart patterns; candle triggers at pattern breakouts. See [Candlestick Patterns](candlestick-patterns).
- **Price Action** — chart patterns are the geometric layer of price action. See [Price Action Trading](price-action).
- **Wyckoff Method** — Wyckoff ranges/springs are pattern structures with a phase narrative. See [Wyckoff Method](wyckoff-method).
- **Breakout Trading** — chart-pattern breakouts are a primary breakout-trading source. See [Breakout Trading](breakout-trading).
- **Elliott Wave** — Elliott structures subdivide into recognizable chart patterns at each degree. See [Elliott Wave Theory](elliott-wave).
- **Fibonacci Trading** — Fib confluence at pattern boundaries strengthens them. See [Fibonacci Trading](fibonacci-trading).
- **VCP / Momentum** — VCP is a pattern tuned for momentum-stock breakouts (Minervini). See [Trend Following](trend-following).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| keithorange/PatternPy | 464 | High-speed pattern recognition Python package | https://github.com/keithorange/PatternPy |
| zeta-zetra/chart_patterns | 106 | Automated detection of chart patterns | https://github.com/zeta-zetra/chart_patterns |
| shiyu2011/cookstock | 96 | Minervini VCP detection + stage analysis daily screener | https://github.com/shiyu2011/cookstock |
| tysoncung/crypto-chart-patterns | 14 | ML for crypto chart-pattern detection & TA (Python) | https://github.com/tysoncung/crypto-chart-patterns |
| crankycandle/volatility-contraction-pattern | 16 | Screener for stocks in VCP | https://github.com/crankycandle/volatility-contraction-pattern |
| nimaabf/Forex-Pattern-Recognition-System | 0 | ML detection of H&S, double tops, classic FX patterns | https://github.com/nimaabf/Forex-Pattern-Recognition-System |
| ishfaqmalik441/stock-chart-pattern-recognition | 0 | Algorithms for popular chart patterns | https://github.com/ishfaqmalik441/stock-chart-pattern-recognition |

## Books & Foundational Reading

- Robert Edwards & John Magee — *Technical Analysis of Stock Trends* (the canonical text)
- Richard Schabacker — *Technical Analysis and Stock Market Profits* (the origin)
- Thomas Bulkowski — *Encyclopedia of Chart Patterns* (statistical win/fail rates, the evidence base)
- Mark Minervini — *Trade Like a Stock Market Wizard* (VCP, SEPA momentum)
- William O'Neil — *How to Make Money in Stocks* (cup-and-handle, CAN SLIM)

## Further Study

- Replicate Bulkowski's win-rate stats on a modern dataset: do H&S and double tops still hit their measured moves at the published rates?
- Build a VCP scanner (cookstock-style) and track breakout follow-through vs false-break rate over 100 instances.
- Quantify the volume-confirmation premium: measure breakout success rate with vs without volume expansion.
