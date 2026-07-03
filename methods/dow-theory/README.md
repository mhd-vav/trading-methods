---
title: Dow Theory
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
inventor: Charles Dow (1851–1902); refined by Hamilton & Rhea
era: 1890s–1930s
markets: equities (indices), all markets by extension
timeframe: daily/weekly (primary trend focus)
github_repo: mhd-vav/trading-methods
branch: dow-theory
---

# Dow Theory

Dow Theory is the oldest formal framework of technical analysis, formulated by Charles Dow (co-founder of Dow Jones & Co. and the Wall Street Journal) in a series of editorials around 1900, then codified by William Hamilton and Robert Rhea in the 1920s–30s. It is the conceptual root of all modern trend-following technical analysis: Dow defined *trend* (higher highs/lows), distinguished primary/secondary/minor trends, and asserted that averages must confirm each other and that volume confirms trend. Nearly every later method — [Wyckoff](wyckoff-method), [Price Action](price-action), [Trend Following](trend-following), [Chart Patterns](chart-patterns) — descends from Dow's principles.

Dow Theory is less a tradable system than a *theory of market behavior*: a lens for classifying what the market is doing. Its value today is foundational — it teaches the vocabulary and logic every technician uses.

## The Six Tenets

1. **The averages discount everything** — prices reflect all known information (sentiment, fundamentals, expectations). This is the original statement of the efficient-market idea, ~70 years before Fama. All news is already in price.
2. **Three trends** — primary (1+ years, the main tide), secondary (weeks–months, reactions within the primary), and minor (days–weeks, noise). Trade the primary; the secondary offers entries.
3. **Primary trend has three phases** — accumulation (smart money buys the bad news), public participation (trend recognized, crowd enters), distribution (smart money sells the good news to the late public). This is the direct ancestor of [Wyckoff's](wyckoff-method) accumulation/markup/distribution/markdown cycle.
4. **Averages must confirm each other** — Dow watched the Industrials and Rails (now Transports): no industrial bull signal was valid unless transports confirmed. The logic: if factories produce (industrials up) but goods aren't shipped (transports flat/down), the signal is suspect. Modern analog: confirm across related markets/sectors.
5. **Volume confirms trend** — volume should expand in the direction of the primary trend and contract on counter-trend moves. Rising prices on rising volume = genuine demand; rising prices on falling volume = suspect. The conceptual root of [Volume Spread Analysis](volume-spread-analysis).
6. **Trends persist until clear reversal signals** — a trend is assumed in force until definitively broken (e.g., a secondary reaction fails to make a new high and breaks the prior low). Avoid calling tops/bottoms prematurely; the burden of proof is on the reversal.

## Trend Definition (Dow's Lasting Contribution)

Dow defined trends by the sequence of highs and lows — the structure still used everywhere:
- **Uptrend** — higher highs (HH) and higher lows (HL).
- **Downtrend** — lower highs (LH) and lower lows (LL).
- **Range** — mixed; no clear progression.

Reversal = the structure breaking: an uptrend reverses when a prior higher low is broken (lower low printed). This is the genesis of modern market-structure analysis (BOS/CHoCH in [Smart Money Concepts](smc-ict)) and of breakout logic in [Trend Following](trend-following) and [Breakout Trading](breakout-trading).

## Practical Use Today

Dow Theory's value is mostly *framework*, not signal: use it to (1) classify the trend regime before applying any method, (2) confirm signals across related instruments, (3) validate with volume, (4) avoid premature reversal calls. It's the philosophical bedrock, not a standalone edge.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| techietrader/Trading-indicators-and-Chart-patterns | 173 | ATR, SuperTrend, Heiken Ashi, Renko — trend-classic tooling | https://github.com/techietrader/Trading-indicators-and-Chart-patterns |
| bukosabino/ta | 5106 | TA library (Pandas/Numpy) for trend/momentum indicators | https://github.com/bukosabino/ta |

## Books & Foundational Reading

- Robert Rhea — *The Dow Theory* (1932, the definitive codification)
- William Hamilton — *The Stock Market Barometer* (1922)
- Richard Russell — *The Dow Theory Today* (modern interpretation)
- Charles Dow — original WSJ editorials (1900–1902)

## Relationships

Foundational to [Wyckoff Method](wyckoff-method), [Trend Following](trend-following), [Price Action](price-action), [Chart Patterns](chart-patterns), [Volume Spread Analysis](volume-spread-analysis), and the market-structure logic in [Smart Money Concepts](smc-ict).
