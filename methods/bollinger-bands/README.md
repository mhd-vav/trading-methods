---
title: Bollinger Bands
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: John Bollinger (1980s)
markets: all
timeframe: any
github_repo: mhd-vav/trading-methods
branch: bollinger-bands
---

# Bollinger Bands

Bollinger Bands are a volatility envelope: a moving average (middle band, default 20 SMA) bracketed by upper/lower bands set at ±N standard deviations (default 2) of price. The bands widen when volatility rises and contract when it falls — visually encoding volatility regime. The two core trading uses are **mean reversion** (fade touches of the outer bands back toward the mean, in ranges) and **volatility breakout** (trade the expansion when bands contract to a squeeze then expand). The bands' adaptiveness to volatility is the key advantage over fixed envelopes.

## Components

- **Middle band** = SMA(20).
- **Upper/lower bands** = middle ± 2σ (σ = standard deviation over 20 periods).
- **Bandwidth** = (upper − lower) / middle; measures volatility (the "squeeze").
- **%B** = (price − lower) / (upper − lower); where price is within the bands (0–1, >1 above upper, <0 below lower).

## Strategies

- **Mean reversion** — in a range, price touching the upper band is overextended (short toward middle), lower band overextended (long). Works in ranging regimes; fails in trends (price "walks the band").
- **Bollinger squeeze / volatility breakout** — when bandwidth contracts to a multi-period low (squeeze = low volatility = compression), an expansion is imminent; trade the break in the direction of the breakout. The volatility-contraction→expansion principle shared with [Chart Patterns](chart-patterns) (triangles, VCP).
- **Band walk** — in strong trends, price riding the upper/lower band is trend-continuation, not reversal. Don't fade a band walk in a trend.
- **W-bottom / M-top** — Bollinger-assisted reversal patterns where the second touch is outside the band but on lower RSI (divergence).

## Uses & Cautions

Bollinger Bands are a volatility/timing tool. The critical skill is *regime*: mean-revert the bands in ranges, trade the squeeze-breakout in compression, don't fade in trends. Bandwidth and %B are as important as the bands themselves. Pair with [RSI](rsi)/[MACD](macd) for momentum confirmation and [ADX](adx) for regime. The bands are not standalone signals — a tag of the upper band is context-dependent, not automatic.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| je-suis-tm/quant-trading | 10241 | Quant strategies incl. Bollinger Bands | https://github.com/je-suis-tm/quant-trading |
| gawd-coder/Backtest-Indicator-Strategies | 23 | Backtested indicator strategies incl. Bollinger | https://github.com/gawd-coder/Backtest-Indicator-Strategies |
| cinar/indicator | 1199 | Go TA indicators incl. Bollinger Bands | https://github.com/cinar/indicator |
| bukosabino/ta | 5106 | TA library with Bollinger Bands | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- John Bollinger — *Bollinger on Bollinger Bands* (the authoritative text)

## Relationships

Mean-reversion use overlaps [Mean Reversion](mean-reversion); squeeze-breakout overlaps [Breakout Trading](breakout-trading) and VCP/[Chart Patterns](chart-patterns); volatility-regime shared with [ADX](adx) and [Supertrend](supertrend).
