---
title: Price Action Trading
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 1
importance: high
markets: forex, futures, stocks, crypto, indices
timeframe: any
github_repo: mhd-vav/trading-methods
branch: price-action
---

# Price Action Trading

Price action trading is the practice of making trading decisions from the raw movement of price on a chart — the sequence of highs, lows, opens, and closes — without relying primarily on lagging indicators. It is the parent discipline from which more specialized chart-reading methods (Wyckoff, SMC, supply/demand, candlestick analysis) descend. A price-action trader reads the *structure* the market has built (swings, levels, ranges, trends) and the *behavior* of price at those structures (rejection, acceptance, momentum) to infer supply/demand balance and probable direction.

Its central tenet: **price discounts everything, and the chart is the most direct evidence available.** Indicators are derivatives of price; reading price directly is reading the source.

## Core Philosophy

Price action rests on the belief that all known information — fundamentals, news, sentiment, institutional intent — is already reflected in price. Therefore the chart contains the information needed to trade, encoded in:

- **Structure:** the sequence of swing highs and lows that defines trend or range.
- **Levels:** prior significant highs and lows that act as future support/resistance.
- **Bars/candles:** the footprint of the battle between buyers and sellers in each period — body size, wicks, position relative to prior bars.
- **Context:** how price behaves *at* a level matters more than the level itself. The same candle means different things at range support vs. mid-range.

The discipline is contextual, not pattern-matching. A pin bar is not a signal in isolation; a pin bar *at a key level after a liquidity sweep in a trending market* is a signal.

## Market Structure — The Backbone

The foundation of price-action reading is market structure — the progression of swing points:

- **Uptrend:** higher highs (HH) and higher lows (HL). Each pullback holds above the prior low; each push exceeds the prior high.
- **Downtrend:** lower highs (LH) and lower lows (LL).
- **Range:** price oscillates between a defined support and resistance without a sequence of HH/HL or LH/LL — equal highs/lows.

**Structure break = bias change.** A break of the last higher low (in an uptrend) is the first warning of reversal; a break of the last lower high (in a downtrend) warns of a bottom. This is the same concept SMC labels CHoCH. Identifying the current structure tells the trader whether to look for longs, shorts, or to stand aside in a range.

Swing highs/lows are defined objectively: a swing high is a bar whose high is the highest of N bars on either side (N is the trader's sensitivity). Most price-action traders use a mix of major (higher N) and minor (lower N) swings to read both the macro structure and the micro shifts.

## Support and Resistance

Support = a price level where buying interest has repeatedly overcome selling, halting declines. Resistance = where selling has repeatedly overcome buying. These are not lines but **zones** — areas where prior reactions clustered. Strength of a level increases with:

- **Number of tests** (more touches = more participants committed there).
- **Touch freshness** (recent tests matter more than ancient ones).
- **Timeframe** (a daily level outweighs a 5-minute level).
- **Volume at the level** (high-volume reactions = real interest).
- **Round numbers / psychological levels** (00, 50 handles often align).

Key behavior at a level:
- **Reaction (rejection):** wicks/bodies closing away from the level = buyers/sellers defended it. A long lower wick at support = demand appeared.
- **Acceptance (break):** bars closing beyond the level = the defenders lost. A close beyond resistance often flips it to support (and vice versa) — the **role reversal**.
- **False break (stop run):** a wick beyond the level that fails to hold = liquidity sweep. This is among the highest-probability price-action setups: the level was defended *after* taking stops.

## Candlestick Reading

A single candle encodes the period's four prices (OHLC) and, via body/wick proportions, the conviction of the move. Core reads (context-dependent):

- **Body size** = conviction. Large bodies = decisive move; small bodies = indecision.
- **Wicks (shadows)** = rejection. A long upper wick = buyers pushed price up but sellers rejected it back down. Long lower wick = sellers pushed down but buyers rejected it.
- **Position** relative to prior candles: a strong close beyond the prior bar's range = expansion/breakout; a doji at a level after a trend = potential exhaustion.

Key candles (as setups only at structure, not standalone):
- **Pin bar (hammer / shooting star):** small body, long opposing wick. At support = bullish rejection; at resistance = bearish rejection.
- **Engulfing:** a candle whose body fully engulfs the prior body. Bullish engulfing at support = demand takeover.
- **Inside bar:** a bar fully within the prior bar's range = consolidation/contraction. Breakouts of inside-bar ranges often fuel expansion; the mother bar's high/low frames the trade.
- **Doji:** open ≈ close, indecision. Meaningful at range extremes after a trend; noise mid-range.
- **Outside bar (master candle):** engulfs both prior high and low; can signal a volatility expansion and short-term reversal.

Programmatic pattern detection libraries (e.g., `cm45t3r/candlestick`, `TA-Lib`) codify dozens of these; price-action traders use them as filters, not signals.

## Bar-by-Bar Reading

The deeper skill is reading the *sequence* — asking after each bar:

1. Did price do what it should have done given the context? (e.g., at support, did buyers hold, or did sellers break through?)
2. Was the move on rising or falling volume? (price action + light volume confirmation — see [Volume Spread Analysis](volume-spread-analysis))
3. Where did the bar close relative to its range and the prior bar? Close near the high = buyers in control into the close.
4. Is the range expanding (trend) or contracting (consolidation building energy for a breakout)?

This is the "tape reading on a chart" discipline — the descendant of Jesse Livermore's and Wyckoff's reading of the ticker tape.

## Core Price-Action Setups

- **Pullback to a level (trend continuation):** In an uptrend, wait for a pullback to prior swing-low support (or a moving average / trendline). Watch for a rejection candle (pin/engulfing) → enter long, stop below the rejection, target the prior high / next resistance.
- **Breakout and retest (role reversal):** Price breaks resistance decisively (strong close, expansion) → wait for the pullback to retest the broken level (now support) → enter on rejection → target measured-move or next resistance.
- **Range reversal:** In a range, fade the edges: at resistance, short on rejection (pin/engulfing), stop above the range high, target range support. Symmetric at support.
- **False break (stop run) reversal:** Price wicks beyond a key level (sweeping stops), then closes back inside the range/prior structure → enter against the false-break direction, stop beyond the wick. High reward because the swept liquidity often fuels the reversal.
- **Inside-bar breakout:** After contraction (inside bars), trade the breakout of the mother bar in the trend direction; stop at the opposite end of the mother bar.

## Trendlines and Channels

A trendline connects successive swing lows (uptrend) or highs (downtrend). It is a visual proxy for the trend's slope. Valid trendlines need ≥3 touches; the more touches, the more meaningful — and the more liquidity rests beyond them when broken. **A trendline break = structure shift** (a weaker version of a swing break). Channels (parallel trendlines) frame the trading range within a trend; channel traders fade the edges and trade breakouts of the channel in the trend direction.

A common pitfall: forcing trendlines onto choppy structure. A trendline is only valid if the swings it connects are genuine and the trend is orderly.

## Confluence — The Price-Action Edge

No single price-action signal has a robust edge in isolation. The edge comes from **confluence** — stacking independent reasons:

- Trend direction (structure) agrees with the level.
- The level is strong (multiple touches, HTF, volume).
- A trigger candle confirms rejection.
- A liquidity pool sits nearby to fuel the move / define the target.
- (Optional) a higher timeframe bias aligns.

A trade with 4–5 confluences at a key level has materially higher probability than a pin bar in a vacuum. The discipline is to *wait* for confluence and pass when it's absent.

## Higher-Timeframe Context

Price-action traders typically use a higher timeframe (HTF) for bias and a lower timeframe (LTF) for entry:
- HTF (e.g., daily) determines the trend and the key levels.
- LTF (e.g., 1h/15m) is used to pinpoint entries at those levels with trigger candles and structure shifts.

Trading only the LTF without HTF context leads to being on the wrong side of the prevailing move. The HTF→LTF routine is shared with SMC and is a general best practice.

## Risk Management

- **Stops:** beyond the structure that invalidates the thesis — below the rejection candle's low (long), above its high (short). Not at arbitrary pip distances.
- **Position sizing:** fixed-fractional (risk a fixed % of equity per trade).
- **Targets:** the next opposing structure level (prior high/low, range edge), or a measured move (range height projected from breakout). Book partial at first target, trail the rest.
- **R:R:** seek ≥2R; price-action setups at confluent levels often offer 3R+ because targets are structural.

## Common Pitfalls

- **Pattern-matching without context.** A pin bar in the middle of a range is noise. Context (level, trend, sweep) is what makes a candle a signal.
- **Drawing too many levels.** Every tick is not support/resistance. Keep to the most significant HTF levels; clutter destroys clarity.
- **Chasing breakouts without retest.** Entering on the breakout candle often means buying the high. The retest entry is higher-probability and lower-risk.
- **Ignoring the higher timeframe.** LTF price action against the HTF trend is a low-probability fade.
- **Overtrading.** Price action requires patience for confluence; forcing trades in low-context conditions erodes capital.

## Relationship to Other Methods

- **Wyckoff:** Price action is the umbrella; Wyckoff adds the accumulation/distribution phase model and volume-confirmation discipline. See [Wyckoff Method](wyckoff-method).
- **SMC/ICT:** SMC is a specialized price-action dialect adding the liquidity/order-block/FVG vocabulary and session structure. See [Smart Money Concepts / ICT](smc-ict).
- **Supply & Demand:** A simplified price-action variant focused on order clusters (zones). See [Supply & Demand Trading](supply-demand).
- **Candlestick Patterns:** The single-candle/multi-candle pattern sub-discipline of price action. See [Candlestick Patterns](candlestick-patterns).
- **Volume Spread Analysis:** Adds volume to each price-action bar to read effort vs. result. See [Volume Spread Analysis](volume-spread-analysis).

## Why It's Foundational

Price action is the lingua franca of technical trading. Every specialized chart method (Wyckoff, SMC, harmonic, supply/demand) is a dialect of it, applying extra structure or vocabulary to the same raw price data. A trader fluent in structure, levels, candle behavior, and confluence can read any chart in any market without indicators — and can layer other methods on top with understanding rather than confusion. It is the base skill that makes every other method legible.

## Open-Source References

- **TA-Lib/ta-lib-python** (★12090) — the standard technical-analysis library (Python wrapper); includes candlestick pattern recognition (CDLPATTERN functions) used to codify price-action triggers. https://github.com/TA-Lib/ta-lib-python
- **bukosabino/ta** (★5106) — Technical Analysis library using Pandas/Numpy; candlestick patterns included. https://github.com/bukosabino/ta
- **cm45t3r/candlestick** (★492) — focused candlestick-pattern detection library (61+ patterns). The cleanest programmatic reference for candle signals. https://github.com/cm45t3r/candlestick
- **stockalgo/stolgo** (★336) — Price Action Trading APIs; algorithmic candlestick/structure detection for securities. https://github.com/stockalgo/stolgo
- **akurgat/automating-technical-analysis** (★438) — data analytics + popular trading strategies/indicators to identify best trades; price-action-aware. https://github.com/akurgat/automating-technical-analysis
- **yulz008/GOLD_ORB** (★247) — Open Range Breakout EA for XAUUSD; a concrete price-action breakout implementation. https://github.com/yulz008/GOLD_ORB
- **przemyslawbak/OHLC_Candlestick_Patterns** (★37) — detection for 37 bullish + 37 bearish patterns. https://github.com/przemyslawbak/OHLC_Candlestick_Patterns

## Further Study

- Al Brooks — *Reading Price Charts Bar by Bar* (the exhaustive modern price-action text).
- Lance Beggs (YourTradingCoach) — price-action course focused on context and bar-by-bar reading.
- Steve Nison — *Japanese Candlestick Charting Techniques* (the canonical Western introduction to candlesticks).
- Adam Grimes — free course and stats-driven analysis of price-action edge.

