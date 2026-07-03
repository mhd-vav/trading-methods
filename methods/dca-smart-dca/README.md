---
title: DCA & Smart DCA (Dollar-Cost Averaging)
type: method
domain: trading
category: Algorithmic & Systematic Strategies
tier: 3
importance: moderate
markets: equities, crypto, ETFs
timeframe: weeks–years (accumulation)
github_repo: mhd-vav/trading-methods
branch: dca-smart-dca
---

# DCA & Smart DCA (Dollar-Cost Averaging)

Dollar-Cost Averaging (DCA) is the systematic purchase of a fixed dollar amount of an asset at regular intervals (e.g., $100 of BTC every week), regardless of price. Its logic: buying more units when price is low and fewer when high naturally averages the entry price below the time-weighted average, and removes timing/emotion from accumulation. "Smart DCA" extends the idea with conditional sizing — buy more when price is below a moving average, oversold ([RSI](rsi)), or at a drawdown threshold; buy less or skip when extended — to tilt the average further. DCA is the default accumulation strategy for retail index/ETF and crypto investors, and a natural fit for assets with positive expected drift ([Buy-and-Hold](buy-and-hold)).

## Mechanics

- **Plain DCA** — fixed $ amount at fixed interval. Mechanically simple, emotion-free, captures the volatility discount (average price < average-of-prices when variance > 0).
- **Smart / conditional DCA** — scale the amount by a signal: increase allocation when price is below an MA, in [Bollinger Bands](bollinger-bands) lower band, or [RSI](rsi) oversold; reduce when extended. "Value-averaging" targets a growing portfolio value and adjusts purchases to hit it.
- **Threshold DCA** — only buy when price falls X% below the last buy or a reference (a mild [Mean Reversion](mean-reversion) tilt).

## Uses & Cautions

DCA's strength is behavioral and structural: it enforces discipline during accumulation, avoids the (statistically poor) attempt to time lump-sum entries, and for high-drift assets like equities it captures the volatility discount. Its weakness: in strong uptrends, lump-sum investing historically beats DCA (money in the market longer earns the drift); DCA "wins" mainly by reducing regret/variance, not by maximizing expected return. Smart DCA improves the average entry but adds complexity and can under-buy during long steady rallies. The "DCA bots" in crypto are often [Grid Trading](grid-trading) or [Martingale](martingale-anti-martingale) averaging-down in disguise — beware the distinction. DCA is the accumulation cousin of [Buy-and-Hold](buy-and-hold) and a milder version of [Mean Reversion](mean-reversion) scaling.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| lukeliasi/binance-dca-bot | 178 | Auto DCA buy bot for Binance | https://github.com/lukeliasi/binance-dca-bot |
| dcapal/dcapal | 82 | Free online DCA portfolio-balancing tool | https://github.com/dcapal/dcapal |
| kdmukai/gdax_bot | 59 | Micro DCA bot for crypto | https://github.com/kdmukai/gdax_bot |
| DCAStack/DCAStackCefi | 59 | Automated DCA bot for CEX crypto | https://github.com/DCAStack/DCAStackCefi |
| adocquin/kraken-dca | 43 | DCA bot for Kraken pairs | https://github.com/adocquin/kraken-dca |

## Books & Foundational Reading

- Vanguard research — *Cost Averaging: Invest Now or Temporarily Hold Your Cash* (lump-sum vs DCA study)
- John Bogle — *The Little Book of Common Sense Investing* (DCA as the index-investor discipline)
- Michael Edleson — *Value Averaging* (the "smart DCA" value-targeting variant)

## Relationships

Accumulation cousin of [Buy-and-Hold](buy-and-hold); mild [Mean Reversion](mean-reversion) tilt in smart/threshold variants; sizing signals via [RSI](rsi), [Bollinger Bands](bollinger-bands); distinct from [Martingale](martingale-anti-martingale) averaging-down (DCA is fixed/conditional, not loss-doubling); execution-discipline shared with [Execution Algorithms](execution-algorithms).
