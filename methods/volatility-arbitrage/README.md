---
title: Volatility Arbitrage
type: method
domain: trading
category: Options-Specific Strategies
tier: 2
importance: high
markets: options, volatility derivatives (VIX futures/var swaps)
timeframe: days–weeks (delta-hedged)
github_repo: mhd-vav/trading-methods
branch: volatility-arbitrage
---

# Volatility Arbitrage

Volatility Arbitrage is a delta-neutral strategy that trades the difference between **implied volatility** (the market's forward expectation, embedded in option prices) and **realized volatility** (what the underlying actually does). The core trade: if implied > realized expected, sell options (or the implied-vol-rich leg) and delta-hedge the underlying continuously; if implied < realized expected, buy options and delta-hedge. Profit accrues as the gap closes — either vol mean-reverts or the delta hedge captures the realized-vs-implied differential. It is the institutional backbone of options market-making and vol funds, fundamentally different from directional betting because edge lives in the volatility dimension, not price direction.

## Core Mechanics

- **Implied vs realized** — implied vol (IV) is solved from the option price via Black-Scholes; realized vol (RV) is the annualized standard deviation of underlying returns over the hold. The trade bets on IV − RV convergence.
- **Delta hedging** — to isolate the vol bet from directional risk, the option position is hedged with the underlying so net delta ≈ 0. Hedging is done discretely (daily, or on delta bands), which itself introduces "hedging slippage" — the frequency/coverage tradeoff (Gamma scalping).
- **Vega** — the position's sensitivity to IV. Long vega profits if IV rises; short vega if IV falls. Vol arb sizes vega against a forecast of realized vol.
- **Vol-of-vol and skew** — advanced variants trade the vol smile/skew (e.g., risk reversal), the term structure (calendar vol arb), or vol-of-vol itself via var swaps and VIX derivatives.

## Strategy Variants

1. **Short vol / overpriced implied** — the historical bias: implied vol trades at a premium to realized (the "variance risk premium"). Systematically selling vol (short straddle/strangle, delta-hedged) harvests this premium but carries tail risk (vol spikes).
2. **Long vol / underpriced implied** — buy when IV is depressed relative to a vol forecast or event catalyst; profit on a vol spike.
3. **Relative value vol** — trade one maturity/strike vs another (calendar vol arb, [Calendar Spreads](calendar-spreads)); or one asset's vol vs another's.
4. **Dispersion trading** — short index vol, long component single-stock vol (or vice versa), betting on the index-vs-components correlation regime.

## Risk Management

- **Tail / gap risk** — the defining risk of short vol: a sudden jump (flash crash, geopolitical shock) blows through the delta hedge and produces outsized losses. Position sizing and explicit tail hedges (far OTM puts) are mandatory.
- **Delta-hedging slippage** — discrete hedging vs continuous Black-Scholes assumption introduces path-dependency; gamma scalping frequency is a tuned tradeoff between slippage cost and hedge accuracy.
- **Vega/skew risk** — being right on vol level but wrong on skew/term-structure moves can erode edge.
- **Margin/capital efficiency** — short option positions are margin-intensive; VAR swap and VIX futures offer more capital-efficient vol exposure.

## Common Pitfalls

- **Picking up pennies in front of a steamroller** — short-vol variance-premium harvesting looks like steady income until a tail event; many funds blew up in 2008, Feb 2018 ("Volmageddon"), and March 2020.
- **Model risk** — vol forecasts (GARCH, Heston, vol-of-vol models) can be wrong; over-reliance on a single vol model is dangerous.
- **Ignoring skew/term structure** — trading ATM vol alone ignores that the smile often holds the real mispricing.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| junsu489/volatility_arbitrage | 72 | Volatility arbitrage in Heston model | https://github.com/junsu489/volatility_arbitrage |
| coleschaffer/Gabagool | 47 | Automated vol-arb bot for Polymarket, delta-neutral | https://github.com/coleschaffer/Gabagool |
| ThewindMom/151-trading-strategies | 9 | 151 Trading Strategies incl. vol arb (FastAPI) | https://github.com/ThewindMom/151-trading-strategies |
| stefan-jansen/machine-learning-for-trading | 19491 | ML for vol forecasting & trading (ch. on vol) | https://github.com/stefan-jansen/machine-learning-for-trading |

## Books & Foundational Reading

- Emanuel Derman — *The Volatility Smile* (practitioner's guide to vol, skew, surface)
- Sheldon Natenberg — *Option Volatility and Pricing* (the standard vol-trading primer)
- Tim Kletzke — *Volatility Trading* (Antony Kletzke; variance risk premium, vol forecasting)
- Jim Gatheral — *The Volatility Surface* (academic, local/stochastic vol models)

## Relationships

Options-dimension sibling of [Options Strategies](options-strategies); relies on [Statistical Arbitrage](statistical-arbitrage) thinking (mean reversion of vol); execution via [Market Making](market-making) in options; relative-value kinship with [Calendar Spreads](calendar-spreads); tail-risk contrast with [Trend Following](trend-following); uses [Mean Reversion](mean-reversion) of the vol regime.
