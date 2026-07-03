---
title: Supertrend Indicator
type: method
domain: trading
category: Indicator & Oscillator-Based Strategies
tier: 3
importance: moderate
inventor: Olivier Seban (used widely from ~2010s)
markets: all; especially futures, forex, crypto
timeframe: trending markets, any TF
github_repo: mhd-vav/trading-methods
branch: supertrend
---

# Supertrend Indicator

Supertrend is a trend-following overlay built on [ATR](vwap-trading) (Average True Range) and a median price. It plots a single line that flips color/position above or below price to signal trend direction. Upper band = (median + multiplier × ATR), lower band = (median − multiplier × ATR); the indicator trails price, switching to the opposing band when price closes through it. Default multiplier 3, ATR period 10. Its appeal: one clean visual trend signal with a built-in trailing stop, less noisy than dual-MA crossovers.

## Mechanics

- **Trend flip** — when price closes above the upper band, Supertrend flips bullish (line moves to lower band = support); close below the lower band flips bearish (line = resistance). The flip itself is the signal.
- **Trailing stop** — the Supertrend line acts as a dynamic trailing stop, tightening as ATR shrinks and loosening as volatility expands. Exit when price closes back across the line.
- **Multiplier tuning** — lower multiplier (e.g., 2) = more responsive, more flips, more whipsaw; higher (e.g., 4) = fewer flips, larger stops, better in strong trends. This is the [Bollinger Bands](bollinger-bands)-style volatility-scaling tradeoff.

## Uses & Cautions

Supertrend excels in trending markets as a mechanical trend-following system — enter on flip, trail the stop, exit on reverse flip. Its weakness is identical to all trend overlays: choppy/ranging markets produce rapid consecutive flips (whipsaw losses), since ATR-based bands are crossed repeatedly. Best combined with a trend-strength filter like [ADX](adx) (only take flips when ADX > 20–25) or [Ichimoku Cloud](ichimoku) alignment, and with [Price Action](price-action) structure to avoid flips inside consolidation. The trailing-stop nature makes it a natural companion to [Breakout Trading](breakout-trading) and [Trend Following](trend-following).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| techietrader/Trading-indicators-and-Chart-patterns | 173 | ATR, SuperTrend, Heiken Ashi, Renko | https://github.com/techietrader/Trading-indicators-and-Chart-patterns |
| mr-easy/streaming_indicators | 152 | TA indicators for streaming data incl. SuperTrend | https://github.com/mr-easy/streaming_indicators |
| DaScient/SuperTrendTradingBot | 27 | Autonomous SuperTrend trading bot | https://github.com/DaScient/SuperTrendTradingBot |
| bukosabino/ta | 5106 | Python TA library (ATR-based indicators) | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- Olivier Seban — *Ulcer Index & SuperTrend* articles (French origin, popularized via MetaTrader/TradingView)
- John Murphy — *Technical Analysis of the Financial Markets* (ATR & volatility-based stops)

## Relationships

Volatility-trailing kinship with [Parabolic SAR](parabolic-sar) and [Bollinger Bands](bollinger-bands); trend-following logic shared with [Trend Following](trend-following) and [Moving Average Crossover](moving-average-crossover); trend confirmation via [ADX](adx) and [Ichimoku Cloud](ichimoku); structure context from [Price Action](price-action).
