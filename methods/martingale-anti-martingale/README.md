---
title: Martingale & Anti-Martingale
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 3
importance: moderate
markets: forex, crypto, options (any)
timeframe: any (per-trade)
github_repo: mhd-vav/trading-methods
branch: martingale-anti-martingale
---

# Martingale & Anti-Martingale

Martingale and Anti-Martingale are **position-sizing / money-management** schemes layered on any entry strategy, not entry signals themselves. **Martingale**: double the position size after each loss, so a single win recovers all prior losses plus one unit of profit (origin: 18th-century betting). **Anti-Martingale** (let-it-ride / pyramiding): increase position size after wins, decrease after losses, betting that streaks persist. In trading, Martingale is widely used in forex/crypto "DCA bots" and reverse-grid systems (disguised as "averaging down"), while Anti-Martingale aligns with [Trend Following](trend-following) pyramiding. The mathematics of Martingale are unforgiving: it produces many small wins punctuated by catastrophic drawdowns, with a negative expected value once table limits, margin, and the probability of ruin are accounted for.

## Mechanics

- **Martingale** — after a losing trade, double the next size; a win resets to the base unit. Geometric progression: 1, 2, 4, 8, 16... A single win nets +1 unit, but a long losing streak requires exponentially growing capital and hits margin/size limits.
- **Anti-Martingale / pyramiding** — after a win, add to the position (often at +1 unit or a fraction); after a loss, reduce. Catches trends but gives back profits when the streak ends.
- **Modified / "smart" Martingale** — cap the doubling at N levels, use fractional multipliers (e.g., 1.5×), or reset after a target — all attempts to bound the tail risk that pure Martingale ignores.

## Uses & Cautions

Martingale is seductive in backtest: high win rate, smooth equity curve — until the inevitable losing streak triggers a margin call or account blowup. It is structurally a **negative-expectancy amplifier**: it does not create edge, it redistributes outcomes toward frequent small wins and rare ruin. The "martingale crypto bots" popular in retail are essentially [Grid Trading](grid-trading) or [Mean Reversion](mean-reversion) "averaging down" with martingale sizing — profitable in ranges, catastrophic in trends. Anti-Martingale is the more rational companion to [Trend Following](trend-following): trend systems have positive expectancy and fat right tails (big winners), so adding to winners is mathematically sound. The sensible lesson: size up on proven edge/streaks (anti-martingale), never martingale into losses. Martingale's only defensible use is bounded, with hard stops and a pre-committed max-level — and even then, the risk-adjusted return is poor.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| DogsTailFarmer/martin-binance | 227 | Adaptive reverse-grid martingale for Binance Spot | https://github.com/DogsTailFarmer/martin-binance |
| eugeneglova/binance-trading-bot | 70 | Binance Futures auto bot (martingale) | https://github.com/eugeneglova/binance-trading-bot |
| ehabyahia/MT4-Martingale-Bot-With-Reinforcement-Learning | 13 | Martingale forex bot + deep Q-learning | https://github.com/ehabyahia/MT4-Martingale-Bot-With-Reinforcement-Learning |
| akilibots/akili-martingale | 7 | Martingale/DCA mean-reversion crypto bot | https://github.com/akilibots/akili-martingale |

## Books & Foundational Reading

- Ralph Vince — *The Mathematics of Money Management* (position sizing math, martingale critique)
- Van K. Tharp — *Trade Your Way to Financial Freedom* (anti-martingale / position sizing on expectancy)
- Nassim Taleb — *Fooled by Randomness* (the ruin math of martingale-style strategies)

## Relationships

Sizing scheme often paired with [Grid Trading](grid-trading) and [Mean Reversion](mean-reversion); anti-martingale aligns with [Trend Following](trend-following) pyramiding; risk-ruin math shared with [DCA & Smart DCA](dca-smart-dca); contrast with volatility-targeted [Statistical Arbitrage](statistical-arbitrage) sizing.
