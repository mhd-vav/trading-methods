---
title: ADX (Average Directional Index)
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: J. Welles Wilder Jr. (1978)
markets: all
timeframe: any
github_repo: mhd-vav/trading-methods
branch: adx
---

# ADX (Average Directional Index)

ADX measures the **strength** of a trend (not its direction). Built by J. Welles Wilder alongside [RSI](rsi) and [Parabolic SAR](parabolic-sar), it derives two directional indicators (+DI and −DI) from directional movement, then computes ADX as a smoothed average of their difference. ADX ranges 0–100: readings >25 indicate a strong trend (worth trading trend-followingly), <20 indicate a weak/range-bound market (where trend systems fail and [Mean Reversion](mean-reversion) works). Crucially, ADX does not tell you direction — rising ADX says "a trend is strengthening," whether up or down; +DI vs −DI crossover gives the directional signal.

## Mechanics

- **+DI / −DI** — +DI rises when up-movement dominates; −DI rises when down-movement dominates. +DI crossing above −DI = bullish; below = bearish. These are the directional triggers.
- **ADX line** — the strength gauge. ADX > 25 = trending; < 20 = ranging. A rising ADX (even if direction-neutral) is a green light for trend strategies; a falling ADX warns that [Trend Following](trend-following) systems are about to whipsaw.
- **The DI/ADX combination** — take +DI/−DI crossovers only when ADX is rising and >20–25; ignore them when ADX is low (the signals are noise in a range).

## Uses & Cautions

ADX's primary value is as a **regime filter**: it tells you whether to deploy a trend-following or a mean-reverting playbook. Pair it with [Supertrend](supertrend) or [Parabolic SAR](parabolic-sar) (only trade their flips when ADX > 25), with [Moving Average Crossover](moving-average-crossover) (skip crossovers when ADX < 20), or with [Bollinger Bands](bollinger-bands) (trade band touches mean-revertingly when ADX < 20, band breakouts when ADX > 25). Its weakness: ADX is a lagging smoothed indicator — by the time it confirms a strong trend, a chunk of the move is gone, and it lags at turning points. It is a filter, not a standalone entry. Born from the same Wilder 1978 book as [RSI](rsi).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| estebanvz/crypto_trading_lr_adx | 8 | Crypto long/short via linear regression + ADX | https://github.com/estebanvz/crypto_trading_lr_adx |
| Lipishree/WQU-Capstone | 17 | Short-term strategy w/ RSI-MACD-ADX-BB | https://github.com/Lipishree/WQU-Capstone |
| JustinGuese/python_tradingbot_framework | 34 | Algo bot framework incl. ADX filtering | https://github.com/JustinGuese/python_tradingbot_framework |
| cinar/indicator | 1199 | Go TA library incl. ADX/+DI/−DI | https://github.com/cinar/indicator |
| bukosabino/ta | 5106 | Python TA library incl. ADX | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- J. Welles Wilder Jr. — *New Concepts in Technical Trading Systems* (1978; origin of ADX/DMS)
- Perry Kaufman — *Trading Systems and Methods* (DMS as a regime filter)

## Relationships

Regime filter for [Trend Following](trend-following), [Supertrend](supertrend), [Parabolic SAR](parabolic-sar), [Moving Average Crossover](moving-average-crossover); same Wilder origin as [RSI](rsi); gates [Mean Reversion](mean-reversion) (low ADX) vs trend (high ADX); combined with [Bollinger Bands](bollinger-bands) for regime-specific execution.
