---
title: Breakout Trading (Donchian / Turtle)
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 2
importance: high
markets: all liquid markets
timeframe: days–months
github_repo: mhd-vav/trading-methods
branch: breakout-trading
---

# Breakout Trading (Donchian / Turtle)

Breakout trading enters when price breaks beyond a defined range boundary — historically the high/low of the past N periods (a Donchian channel), or a chart consolidation ([Chart Patterns](chart-patterns)). The premise: ranges and consolidations represent equilibrium; a breakout signals a shift in supply/demand balance and the start of a new trend. The most famous codification is the **Turtle Trading** system (Richard Dennis & William Eckhardt, 1983): a rules-based [Trend Following](trend-following) system built on 20-day (entry) and 10-day (exit) Donchian-channel breakouts, ATR-based position sizing, and pyramiding. The Turtles proved that a mechanical breakout/trend system, executed with discipline, could generate outsized returns — launching the systematic trend-following industry.

## Core Mechanics

- **Donchian channel** — the highest high and lowest low of the past N periods. A close above the N-day high = bullish breakout (buy); below the N-day low = bearish (sell/short).
- **Turtle system specifics** — System 1: 20-day breakout entry, 10-day breakout exit; System 2: 55-day entry, 20-day exit. Position sized as 1 unit of risk = 2% account / (N × dollar-per-point), where N = 20-day ATR (volatility-normalized sizing). Pyramiding: add units every 0.5N favorable.
- **Filter / confirmation** — many variants require a close beyond the level (not just an intraday poke), volume confirmation ([VSA](volume-spread-analysis)), or a pullback retest of the broken level ("breakout-and-retest").
- **Stop / exit** — exit on the opposite breakout channel (e.g., 10-day low for longs) or a trailing [Parabolic SAR](parabolic-sar)/[Supertrend](supertrend). The exit is what makes trend systems work: cut losers fast, let winners run.

## Risk Management

- **Volatility-normalized sizing (ATR/ "N")** — the Turtle insight: size each position so 1 unit of risk ≈ constant % of equity, accounting for each market's volatility. This is the bridge between breakout entries and modern volatility-targeted [Trend Following](trend-following).
- **Cut losers fast** — breakouts have a low win rate (~30–45%); the system survives because winners are many multiples of losers. A tight invalidation stop (just inside the broken level, or ATR-based) is mandatory.
- **Let winners run / pyramid** — add to winning trends (anti-martingale, see [Martingale & Anti-Martingale](martingale-anti-martingale)); the fat right tail of trend payoffs funds the many small losses.
- **Diversification** — apply across many markets so uncorrelated breakout signals diversify (the [CTA / Managed Futures](cta-managed-futures) model).

## Common Pitfalls

- **False breakouts / whipsaw** — the defining risk: in choppy markets, price pokes beyond the level then reverses. Many breakouts fail; the system depends on the few that run. Mitigate with [ADX](adx) trend-strength filtering, wait-for-close confirmation, or [Bollinger Bands](bollinger-bands) squeeze-then-expand logic.
- **Over-optimizing the channel length** — the original 20/55-day parameters worked across decades and markets; curve-fitting to recent data degrades robustness.
- **Poor exits** — the entry is only half the system; tight exits on winners (taking profit too early) or loose exits on losers destroys the payoff ratio.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| je-suis-tm/quant-trading | 10241 | Python quant strategies incl. Donchian/Turtle | https://github.com/je-suis-tm/quant-trading |
| timchepeleff/turtles | 18 | Turtle trend-following for algo frameworks | https://github.com/timchepeleff/turtles |
| nerdyckc/turtle_soup_bitmex | 14 | "Turtle Soup" false-breakout strategy | https://github.com/nerdyckc/turtle_soup_bitmex |
| odonnell31/Turtle-Trading-Simulator | 5 | Turtle Trading strategy simulator | https://github.com/odonnell31/Turtle-Trading-Simulator |
| QuantConnect/Lean | 20334 | Algorithmic engine for breakout/trend systems | https://github.com/QuantConnect/Lean |

## Books & Foundational Reading

- Curtis Faith — *Way of the Turtle* (firsthand account of the Turtle experiment)
- Richard Dennis / William Eckhardt — original Turtle rules (circulated documents, widely reproduced)
- Michael Covel — *Trend Following* (breakout/trend system philosophy and practitioners)
- Linda Raschke — *Street Smarts* ("Turtle Soup" false-breakout counter-strategy)

## Relationships

The systematic entry of [Trend Following](trend-following) and [CTA / Managed Futures](cta-managed-futures); academic core is [Time-series Momentum](time-series-momentum); consolidation context from [Chart Patterns](chart-patterns) and [Price Action](price-action); false-breakout detection via [VSA](volume-spread-analysis) and [ADX](adx); volatility exit via [Supertrend](supertrend)/[Parabolic SAR](parabolic-sar); pyramiding logic from [Martingale & Anti-Martingale](martingale-anti-martingale).
