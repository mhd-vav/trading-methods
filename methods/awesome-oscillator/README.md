---
title: Awesome Oscillator (AO)
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: low-moderate
inventor: Bill Williams
markets: all
timeframe: any
github_repo: mhd-vav/trading-methods
branch: awesome-oscillator
---

# Awesome Oscillator (AO)

The Awesome Oscillator (AO), created by Bill Williams, is an unbounded momentum histogram comparing a 5-period simple moving average to a 34-period SMA, both of the median price (high+low)/2. AO = SMA5(median) − SMA34(median). It visualizes momentum: bars above zero = bullish momentum, below = bearish; rising green bars = strengthening bullish, falling red = weakening. Unlike bounded oscillators ([RSI](rsi), [Stochastic](stochastic-oscillator)), AO is open-ended and centered on zero, making it a momentum-velocity gauge akin to a smoothed [MACD](macd) histogram but using medians and fixed 5/34 periods.

## Signals

- **Zero-line cross** — AO crossing above zero = bullish momentum building; below = bearish. The baseline trigger.
- **Saucer / Twin Peaks** — Bill Williams' named setups: a "saucer" is three bars where the middle is lower (above zero, buy) or higher (below zero, sell); "twin peaks" = two peaks with a trough between them, both above zero (buy) or below (sell). These are AO-specific continuation signals.
- **Histogram color/momentum** — consecutive same-color bars signal momentum persistence; color flip signals momentum waning.

## Uses & Cautions

AO is a momentum confirmation tool, not a standalone system. Its strength is visualizing momentum acceleration/deceleration clearly and generating Bill Williams' "alligator" ecosystem signals alongside fractals and the Accelerator Oscillator. Its weakness: the fixed 5/34 periods are arbitrary and lag, and the unbounded scale makes "overbought/oversold" meaningless — you must read momentum direction, not levels. Best as a confirmation filter for [Price Action](price-action) entries or a momentum-confirmation layer on [Trend Following](trend-following) systems, overlapping in spirit with the [MACD](macd) histogram. Many traders prefer MACD for its configurability; AO's fixed periods appeal to Bill Williams' alligator/fractal adherents specifically.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| samgozman/AO-MACD-cross-tradingview | 31 | TradingView oscillator combining AO + MACD | https://github.com/samgozman/AO-MACD-cross-tradingview |
| Nikhil-Adithyan/Algorithmic-Trading-with-Awesome-Oscillator-in-Python | 2 | AO strategy backtest in Python | https://github.com/Nikhil-Adithyan/Algorithmic-Trading-with-Awesome-Oscillator-in-Python |
| bukosabino/ta | 5106 | Python TA library incl. AO | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- Bill Williams — *Trading Chaos* and *New Trading Dimensions* (origin of AO, Alligator, fractals)
- Justine Williams-Longo — *Trading Chaos, 2nd ed.* (updated AO applications)

## Relationships

Momentum-histogram kinship with [MACD](macd); confirmation layer for [Price Action](price-action) and [Trend Following](trend-following); part of Bill Williams' Alligator/fractal ecosystem; contrast with bounded oscillators [RSI](rsi) and [Stochastic Oscillator](stochastic-oscillator).
