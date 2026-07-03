---
title: RSI (Relative Strength Index)
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: J. Welles Wilder Jr. (1978)
markets: all
timeframe: any
github_repo: mhd-vav/trading-methods
branch: rsi
---

# RSI (Relative Strength Index)

RSI is a bounded (0–100) momentum oscillator measuring the speed and magnitude of recent gains vs losses over a lookback (default 14). It answers: is the recent move more up than down, and by how much? Readings above 70 are conventionally "overbought" (extended, vulnerable to pullback), below 30 "oversold" (extended down, vulnerable to bounce). RSI's enduring popularity comes from its divergence signal — when price makes a new extreme but RSI does not, momentum is diverging and a reversal is near — and from its use as a regime/timing filter in systematic strategies.

## The Formula

RS = average gain / average loss over N periods (Wilder's smoothing).
RSI = 100 − (100 / (1 + RS)).

## Signals

- **Overbought/oversold** — >70 / <30. *Caution*: in strong trends RSI stays overbought/oversold for long stretches; treating 70/30 as automatic reversals loses in trends. Better: use 80/20 in trends, or trade the *exit* from OB/OS (RSI crossing back below 70 / above 30) rather than the touch.
- **Centerline (50)** — RSI > 50 = bullish momentum regime; < 50 = bearish. Used as a trend filter.
- **Divergence** — price new high + RSI lower high = bearish divergence (momentum exhaustion); the reverse for bullish. The strongest RSI signal.
- **Failure swings** — RSI making its own higher low / lower high independent of price; a self-contained reversal signal Wilder emphasized.

## Uses & Cautions

RSI is a momentum/timing tool, not a standalone system. Its weakness: OB/OS levels are not reversals in trends (the "RSI stays overbought" trap), and divergences can run extended. Best as a confirmation filter (e.g., buy [Supply & Demand](supply-demand) zones only when RSI is oversold and turning up) or divergence trigger combined with structure. The "RSI + mean reversion" use (buy oversold in ranges) overlaps [Mean Reversion](mean-reversion); the "RSI > 50 trend filter" use overlaps [Trend Following](trend-following).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| SharmaVidhiHaresh/Backtesting-Trading-Strategies-with-Python | 45 | Crossover strategy backtest incl. RSI | https://github.com/SharmaVidhiHaresh/Backtesting-Trading-Strategies-with-Python |
| chemicoPy/MACD-RSI-STOCHASTIC-strategy | 12 | Combined MACD/RSI/Stochastic strategy | https://github.com/chemicoPy/MACD-RSI-STOCHASTIC-strategy |
| cinar/indicator | 1199 | Go TA indicators incl. RSI | https://github.com/cinar/indicator |
| bukosabino/ta | 5106 | TA library with RSI | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- J. Welles Wilder — *New Concepts in Technical Trading Systems* (1978, the origin of RSI, ATR, ADX)
- Constance Brown — *Technical Analysis for the Trading Professional* (advanced RSI: rethinking OB/OS per trend)

## Relationships

Momentum/divergence shared with [MACD](macd); OB/OS mean-reversion use overlaps [Mean Reversion](mean-reversion); trend-filter (50-line) for [Trend Following](trend-following); confirmation at [Supply & Demand](supply-demand) zones.
