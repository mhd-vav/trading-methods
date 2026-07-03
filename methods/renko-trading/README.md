---
title: Renko Trading
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: Japan (砖 "brick"); popularized West 2010s
markets: all
timeframe: price-based (time-independent)
github_repo: mhd-vav/trading-methods
branch: renko-trading
---

# Renko Trading

Renko (from Japanese *renga*, "brick") is a price-based charting method that filters out time and small moves, drawing a new "brick" only when price moves a fixed amount. This strips time and noise: a quiet day prints nothing; a volatile day prints many bricks. The result is a chart of pure *trend* — clean sequences of bricks where reversals require a full brick-size move against the trend, reducing whipsaws. Renko excels at trend identification and breakout timing where time-based charts drown in noise.

## Mechanics

- **Brick size** — fixed (e.g., $1) or ATR-derived (adaptive to volatility). The choice controls sensitivity.
- A new brick prints only when price closes beyond the last brick by one brick size. Bricks are drawn at 45° angles; color flips on reversal.
- Time is absent: the x-axis is brick count, not calendar time.

## Trading Renko

- **Trend** — a run of same-color bricks; the simplest trend read.
- **Reversal** — a brick of opposite color (requires a full brick-size counter-move); used as the trend-change trigger.
- **Support/resistance** — brick consolidation zones act as levels.
- **Breakout** — exiting a flat brick zone in the trend direction.

Renko's strength (noise reduction) is also its risk: brick size choice is critical — too small = whipsaws; too large = late signals. And because Renko ignores time, it must be paired with time-based charts for session/context awareness. Popular with [Trend Following](trend-following) and [Breakout Trading](breakout-trading) traders in noisy instruments.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| GerardBCN/RenkoTrading | 50 | Renko-chart algorithm applied to crypto trading | https://github.com/GerardBCN/RenkoTrading |
| filipemarques87/fx-charts | 29 | Build Renko bricks in Python | https://github.com/filipemarques87/fx-charts |
| aticio/renko | 26 | Renko chart creator | https://github.com/aticio/renko |
| techietrader/Trading-indicators-and-Chart-patterns | 173 | ATR, SuperTrend, Heiken Ashi, Renko | https://github.com/techietrader/Trading-indicators-and-Chart-patterns |

## Books & Foundational Reading

- Steve Nison — *Beyond Candlesticks* (Renko, Kagi, Three-Line Break)
- Nison — *Japanese Candlestick Charting Techniques* (Renko section)

## Relationships

Noise-filter cousin of [Heikin-Ashi](heikin-ashi) and [Point & Figure](point-and-figure); trend tool for [Trend Following](trend-following), [Breakout Trading](breakout-trading).
