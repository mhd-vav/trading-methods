---
title: Candlestick Patterns
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 2
importance: high
era: 1700s Japan (Munehisa Homma) → Westernized 1990s (Steve Nison)
markets: all (stocks, futures, FX, crypto)
timeframe: any (most used intraday–daily)
github_repo: mhd-vav/trading-methods
branch: candlestick-patterns
---

# Candlestick Patterns

Candlestick analysis is the reading of single and multi-bar price formations — the *shape* of each candle's open, high, low, close (OHLC) and body/wick relationships — to infer the balance of buying and selling pressure. Originated in 18th-century Japanese rice markets and brought West by Steve Nison in the 1990s, candlesticks give price action a *vocabulary of sentiment shifts*: when control transfers from buyers to sellers within a bar, the candle's shape records it. A long-bodied bullish candle screams buyer dominance; a doji whispers indecision; an engulfing pattern shouts a reversal of power.

Candlesticks are the granular building block of all chart-based technical analysis — the single-bar input that [Chart Patterns](chart-patterns) are built from and that [Price Action](price-action) traders read directly. Used alone they are a *timing tool* (when to act), not a directional system; their power comes from combination with structure, trend, and levels.

## Core Philosophy — The Bar Is a Battle

Each candle is one period's battle between bulls and bears, recorded as four prices. The body (open→close) shows who won and by how much; the wicks/shadows (high/low excursions) show where each side pushed and was rejected. The method's premise: shifts in the body/wick relationship precede shifts in trend, because they record the moment control transfers. A candlestick pattern is a *micro-structure* signal — the smallest unit at which sentiment reversal is visible.

The crucial caveat, confirmed by decades of academic backtesting: **most single-candle patterns have weak standalone predictive power.** Their value is conditional — a hammer at a major support level after a downtrend is meaningful; the same hammer mid-range in a chop is noise. Context is everything.

## Candle Anatomy

- **Body** — open-to-close range; color shows direction (bullish = close above open).
- **Upper shadow (wick)** — high minus max(open,close); rejection of higher prices.
- **Lower shadow** — min(open,close) minus low; rejection of lower prices.
- **Marubozu** — no wicks (or tiny); one side dominated the entire period. A bullish marubozu opens at low, closes at high — total buyer control.
- **Doji** — open ≈ close; indecision; the body is a thin line. Forms at the *end* of moves, not in isolation.
- **Long-legged doji (rickshaw)** — doji with long both wicks; violent two-way battle, no resolution — high reversal potential.

The relative size of body vs wicks is the first read: long body + short wicks = conviction; short body + long wicks = indecision/rejection.

## Single-Candle Patterns

- **Hammer** — small body at top, long lower wick (≥2× body). Bullish reversal after a downtrend; the lower wick shows sellers pushed down and were overrun. Inverted (hanging man) at the top of an uptrend is bearish.
- **Shooting star** — small body at bottom, long upper wick. Bearish reversal after an uptrend; buyers pushed up and were rejected. The mirror of the hammer.
- **Doji** — indecision; meaningful only at extremes or after a run.
- **Marubozu** — conviction; continuation when with the trend, exhaustion when against it at an extreme.
- **Spinning top** — small body, long both wicks; indecision like doji but with a small body.

## Two-Candle Patterns

- **Bullish/bearish engulfing** — second candle's body completely engulfs the first's. The strongest reversal candlestick signal: control transfers decisively in one bar. Bullish engulfing at support after a decline is a textbook long.
- **Harami (pregnant)** — small body *inside* the prior large body. Reversal/consolidation signal; the second candle's loss of momentum. Weaker than engulfing.
- **Piercing line** — bearish candle, then bullish candle opening below the prior low but closing above its midpoint. Bullish reversal.
- **Dark cloud cover** — bullish candle, then bearish candle opening above prior high but closing below its midpoint. Bearish reversal — the piercing line's mirror.
- **Tweezer tops/bottoms** — two candles with matching highs (tops) or lows (bottoms). Shows a level was tested twice and held/rejected; reversal at that level.

## Three-Candle Patterns

- **Morning star / evening star** — three-candle reversal. Morning star: big bearish → small body (gap down, indecision) → big bullish (gap up, close well into first candle). A high-reliability bottom. Evening star is the bearish mirror (top).
- **Three white soldiers / three black crows** — three consecutive long-bodied same-direction candles, each opening within the prior body and closing higher/lower. Strong continuation at a *start* of a move; exhaustion if they appear after an extended run (climax).
- **Three inside up/down** — harami + confirmation candle; the confirmed harami.
- **Abandoned baby** — rare doji-star with gaps on both sides; strong reversal (top or bottom).

## The Context Rule (Critical)

A pattern's meaning is defined by *where it forms*, not its shape:
- **At a level** (support/resistance, supply/demand zone, Fibonacci retracement) → reversal signal. See [Supply & Demand](supply-demand), [Fibonacci Trading](fibonacci-trading).
- **In a trend, with the trend** → continuation signal (e.g., marubozu in an uptrend).
- **After an extended move** → exhaustion signal (climax candles, long-legged doji).
- **Mid-range, no level** → noise; ignore.

The professional use: candlesticks are *triggers* — they confirm that a level you already identified is holding/reversing, providing the entry. They are not the level itself. A hammer at a random price is worthless; a hammer at a daily demand zone is an entry.

## Confirmation and Filtering

Because standalone candle reliability is modest, practitioners filter:
- **Volume confirmation** — a bullish engulfing on rising volume is far stronger than on falling volume. Volume validates the conviction the candle implies. See [Volume Spread Analysis](volume-spread-analysis).
- **Next-bar confirmation** — wait for the bar after the pattern to confirm direction (e.g., enter on the break of the engulfing candle's high). Reduces false signals at the cost of worse entry.
- **Trend filter** — only trade bullish patterns in uptrends (or at uptrend support), bearish in downtrends. Counter-trend candle patterns fail more often.
- **Higher-timeframe alignment** — a 1h bullish engulfing aligned with a daily uptrend is high-probability; against the daily trend is a scalp at best.

## Risk Management

- **Stop placement** — beyond the pattern's extreme (below the hammer's low, below the engulfing candle's low). The pattern's invalidation level is structural, not arbitrary.
- **Target** — the next structure level or a measured move; candlesticks give entry, not target. Combine with structure for exits.
- **Position sizing** — fixed fractional; candle entries tend to be tight (small stop beyond the pattern), allowing larger size for the same risk — but the small stop is more easily stopped out by noise, so size for the *real* risk, not the pattern's theoretical stop.

## Common Pitfalls

- **Trading every pattern** — the screen has dozens of candles; most are meaningless. Only act at levels/context.
- **Ignoring the trend** — bullish patterns in downtrends, bearish in uptrends = fighting the flow.
- **Over-reliance on one pattern** — no single candlestick is a system; it's a tool within a larger method.
- **Ignoring volume** — a low-volume engulfing is a weak signal; the shape alone doesn't measure conviction.
- **Forgetting gaps matter** — many patterns (morning star, abandoned baby) require gaps to be valid; in 24/7 crypto or with no overnight gaps, the classical patterns morph.
- **Backtesting naively** — patterns detected mechanically without context show poor results; the academic literature's "candlesticks don't work" finding usually omits the context filter that practitioners apply.

## Relationships to Other Methods

- **Price Action** — candlesticks are the vocabulary of price action; PA is the broader grammar. See [Price Action Trading](price-action).
- **Chart Patterns** — multi-bar chart patterns are built from candles; the candle is the atom. See [Chart Patterns](chart-patterns).
- **Volume Spread Analysis** — VSA reads the same bars with volume as the first-class citizen; candlesticks + volume ≈ VSA. See [Volume Spread Analysis](volume-spread-analysis).
- **Supply & Demand** — candlesticks provide the entry trigger at S/D zones. See [Supply & Demand Trading](supply-demand).
- **Heikin-Ashi** — a candle modification that smooths trends; a direct relative. See [Heikin-Ashi](heikin-ashi).
- **Fibonacci Trading** — candle confirmation at Fib levels. See [Fibonacci Trading](fibonacci-trading).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| hackingthemarkets/candlestick-screener | 656 | Web-based candlestick pattern screener (Python/Flask) | https://github.com/hackingthemarkets/candlestick-screener |
| femtotrader/pandas_talib | 781 | Pandas technical-analysis indicators incl. candlestick patterns | https://github.com/femtotrader/pandas_talib |
| xgboosted/pandas-ta-classic | 383 | Pandas TA Classic: 70+ indicators incl. candlestick patterns | https://github.com/xgboosted/pandas-ta-classic |
| GaneshJainarain/Candlestick-Pattern-Recognition-with-Python-and-TA-Lib | 36 | Candlestick recognition with Python + TA-Lib | https://github.com/GaneshJainarain/Candlestick-Pattern-Recognition-with-Python-and-TA-Lib |
| edgetrader/candlestick-pattern | 32 | Candlestick pattern detection in Python | https://github.com/edgetrader/candlestick-pattern |
| RauchenwaldC/motivewave-candlestick-pattern-study | 8 | 33+ patterns, dual-MA trend filter, MotiveWave study | https://github.com/RauchenauldC/motivewave-candlestick-pattern-study |
| johnmuchow/Python-Candlestick-Pattern-Matching | 13 | Streamlit screener for 60+ candlestick patterns (Nasdaq100/SP500) | https://github.com/johnmuchow/Python-Candlestick-Pattern-Matching |
| rishav-singh-0/candlestick-patterns | 6 | Dash dashboard to visualize & backtest candlestick patterns | https://github.com/rishav-singh-0/candlestick-patterns |

## Books & Foundational Reading

- Steve Nison — *Japanese Candlestick Charting Techniques* (the Western-canonical text)
- Steve Nison — *Beyond Candlesticks* (newer Japanese techniques: Renko, Kagi, Three-Line Break)
- Gregory Morris — *Candlestick Charting Explained*
- Thomas Bulkowski — *Encyclopedia of Candlestick Charts* (statistical win-rates per pattern)

## Further Study

- Backtest the 5 highest-rated patterns (engulfing, hammer, morning star, three soldiers, doji) at S/R levels vs random entry; measure the context premium.
- Compare candle reliability on gapped instruments (equities) vs 24/7 (crypto) — quantify the gap-dependence.
- Build a screener that only fires when a reversal candle forms at a pre-marked HTF level (demand/supply or Fib) — the conditional system most practitioners actually run.
