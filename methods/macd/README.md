---
title: MACD (Moving Average Convergence Divergence)
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: Gerald Appel (1979)
markets: all
timeframe: any
github_repo: mhd-vav/trading-methods
branch: macd
---

# MACD

MACD is a momentum/trend indicator built from the difference between two EMAs (typically 12 and 26), plotted with a 9-period EMA "signal line" and a histogram of their difference. It captures *convergence/divergence* of moving averages: when the fast EMA pulls away from the slow (divergence), momentum is accelerating; when they converge, momentum is fading. MACD is one of the most-used indicators because it fuses trend (the MACD line's sign/slope) and momentum (the histogram) in one tool, and because its divergences with price are a classic reversal warning.

## Components

- **MACD line** = EMA(12) − EMA(26).
- **Signal line** = EMA(9) of the MACD line.
- **Histogram** = MACD line − signal line (visualizes momentum of momentum).

## Signals

- **Signal-line crossover** — MACD crosses above signal = bullish; below = bearish. The primary trigger (analogous to an MA crossover of the MAs themselves).
- **Zero-line crossover** — MACD crossing above zero (fast EMA above slow) = bullish regime; below = bearish.
- **Divergence** — price makes a new high but MACD does not (bearish divergence) = momentum exhausted; the opposite for bullish. The highest-regarded MACD signal.
- **Histogram momentum** — shrinking histogram = momentum fading ahead of a turn.

## Uses & Cautions

MACD is a trend/momentum *confirmation* tool, best used with structure ([Price Action](price-action), [Support & Demand](supply-demand)). It lags (EMA-based) so signals are late in fast moves; it whipsaws in chop. Divergences are powerful but can run extended (price keeps rising while MACD diverges for many bars). Like all oscillators, it fails in strong trends (sustained overbought/oversold). Pair with [ADX](adx) for regime and never trade MACD alone.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| losingloonies/Best-MACD-Trading-Validation | 127 | Validating the "Best MACD" trading strategy | https://github.com/losingloonies/Best-MACD-Trading-Validation |
| cinar/indicator | 1199 | Go TA indicators incl. MACD | https://github.com/cinar/indicator |
| je-suis-tm/quant-trading | 10241 | Quant strategies incl. MACD | https://github.com/je-suis-tm/quant-trading |
| bukosabino/ta | 5106 | TA library with MACD | https://github.com/bukosabino/ta |

## Relationships

EMA-crossover cousin of [Moving Average Crossover](moving-average-crossover); momentum/divergence shared with [RSI](rsi); trend-confirm for [Trend Following](trend-following).
