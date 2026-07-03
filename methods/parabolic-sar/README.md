---
title: Parabolic SAR (Stop and Reverse)
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: J. Welles Wilder Jr. (1978)
markets: all; trending markets
timeframe: any
github_repo: mhd-vav/trading-methods
branch: parabolic-sar
---

# Parabolic SAR (Stop and Reverse)

The Parabolic SAR (Stop and Reverse), invented by J. Welles Wilder, is a trend-following overlay that places dots above (downtrend) or below (uptrend) price, trailing closer as the trend extends. It computes a time/price-based stop that accelerates (parabolically) toward the market price each bar — the "acceleration factor" (AF, default 0.02, max 0.20) increments each new extreme until the stop is hit and the position reverses. Designed for "stop and reverse" systems: you are always in the market, long or short, flipping at each SAR hit.

## Mechanics

- **Dot position** — dots below price = uptrend (bullish); dots above = downtrend. The dot itself is the stop for that bar.
- **Acceleration factor** — each time a new extreme is made (new high in uptrend), AF increments by the step (0.02) up to the cap (0.20), tightening the stop parabolically. This lets profits run early but exits fast once momentum stalls.
- **Reversal** — when price touches the SAR, the system reverses position and resets AF; the new SAR starts at the prior extreme of the just-finished trend.

## Uses & Cautions

Parabolic SAR is excellent as a trailing-stop mechanism in trending markets and as a mechanical "always-in" reversal system. Its defining weakness: in choppy or sideways markets the accelerating stop triggers constant false reversals, producing a string of small losses (the classic "whipsaw death"). It should only be applied when a trend is confirmed — pair with [ADX](adx) (Wilder's own trend-strength gauge; SAR works best when ADX > 25) or a moving-average slope. As a trailing stop it complements [Trend Following](trend-following) and [Breakout Trading](breakout-trading); as an exit it pairs with [Supply & Demand](supply-demand) entries. Conceptually sibling to [Supertrend](supertrend) (both are volatility-trailing overlays) and born from the same 1978 Wilder book as [RSI](rsi) and ADX.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| je-suis-tm/quant-trading | 10241 | Python quant strategies incl. pattern/SAR | https://github.com/je-suis-tm/quant-trading |
| pacificbay/sar | 22 | Pine Script Parabolic SAR indicator | https://github.com/pacificbay/sar |
| EarnForex/PSAR-Trailing-Stop | 16 | MT Parabolic SAR trailing-stop EA | https://github.com/EarnForex/PSAR-Trailing-Stop |
| cinar/indicator | 1199 | Go TA library incl. Parabolic SAR | https://github.com/cinar/indicator |

## Books & Foundational Reading

- J. Welles Wilder Jr. — *New Concepts in Technical Trading Systems* (1978; origin of SAR, RSI, ATR, ADX)
- Perry Kaufman — *Trading Systems and Methods* (SAR in systematic reversal systems)

## Relationships

Volatility-trailing sibling of [Supertrend](supertrend); trend-strength gating via [ADX](adx); same Wilder origin as [RSI](rsi); trailing-stop role in [Trend Following](trend-following) and [Breakout Trading](breakout-trading); exit logic for [Supply & Demand](supply-demand) entries.
