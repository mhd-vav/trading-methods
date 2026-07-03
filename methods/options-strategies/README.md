---
title: Options Strategies
type: method
domain: trading
category: Options-Specific Strategies
tier: 2
importance: high
era: 1973–present (post-Black-Scholes-Merton)
markets: equity options, index options, futures options, crypto options
timeframe: days to months (expiration-bound)
github_repo: mhd-vav/trading-methods
branch: options-strategies
---

# Options Strategies

Options strategies trade the *derivative* contracts that convey the right (not obligation) to buy (call) or sell (put) an underlying at a strike by an expiration. Unlike linear instruments, options have *non-linear* payoffs defined by multiple risk dimensions — the Greeks (delta, gamma, vega, theta, vanna, etc.). This richness lets a trader express views not just on *direction* but on *volatility*, *time*, and the *shape of the implied vol surface* — views impossible to take with stock or futures alone.

The field splits into two families: **directional** strategies (use options to lever or finance a directional view) and **volatility** strategies (trade the spread between implied and realized vol, or the shape of the surface, often delta-neutral). Mastery requires fluency in the Greeks, because every options position is simultaneously a bet on several variables and decays (theta) by the day.

## Core Philosophy — You Trade the Greeks, Not the Stock

A stock position has one risk: price. An options position has at least four primary risks:
- **Delta (Δ)** — sensitivity to underlying price (~directional exposure, ~hedge ratio).
- **Gamma (Γ)** — sensitivity of delta to price (convexity; how fast delta changes).
- **Vega (ν)** — sensitivity to implied volatility (±1% IV move).
- **Theta (Θ)** — time decay per day (the cost of optionality).

A long call is long delta, long gamma, long vega, short theta. A short straddle is short delta-neutral, short gamma, short vega, long theta. The trader doesn't "buy a call" — they buy a *package of Greek exposures* and must manage each. The defining insight of options trading: **you can be right on direction and still lose** because vol collapsed or theta bled you; you can be wrong on direction and still profit if vol spiked. Managing the Greeks, not predicting the stock, is the discipline.

## The Greeks in Practice

- **Delta hedging** — offset directional risk by trading the underlying (or other options). A delta-hedged option is a pure vol/time bet. Market makers run continuous delta hedges; see [Market Making](market-making).
- **Gamma** — the option seller's enemy and buyer's friend. Long gamma means you get longer as price rises (buy high) and shorter as it falls (sell low) when delta-hedging — a cost (negative gamma PnL for the long) unless realized vol exceeds implied. Gamma is highest for at-the-money, short-dated options.
- **Vega** — long vega profits when IV rises; the dominant driver of long-dated options. Vega scales with sqrt(time).
- **Theta** — the silent tax on long options; the seller's income. Theta accelerates exponentially in the last weeks for ATM options (the "decay cliff").

The equilibrium condition: **gamma PnL (from realized vol) ≈ theta cost + vega PnL (from IV change).** This is why "long vol" profits when realized vol exceeds implied, and "short vol" profits when implied exceeds realized.

## Family 1 — Directional Strategies

Use options to express a directional view, usually to lever capital or define risk.

- **Long call / long put** — max loss = premium; unlimited/defined upside. Pure directional, long vega, short theta. The leverage and defined-risk properties are the appeal; the theta/vega drag is the cost.
- **Bull/bear call spread (vertical)** — buy lower-strike call, sell higher-strike call. Caps both loss and gain; cheaper than naked call; lower breakeven. Pays off direction with reduced vega/theta exposure.
- **Bull/bear put spread** — the put-side mirror. Same risk shape, different capital posting.
- **Ratio spreads / backspreads** — unequal legs (e.g., buy 1 call, sell 2 higher calls). Adds a vol/directionality tilt; backspreads are long vol (profit on big moves).
- **Calendar / diagonal spreads** — trade different expirations (calendar = same strike, diagonal = different strike+expiry). Profit from time decay and term-structure differences.

The directional trader's edge: pick strikes/expirations where the *implied* move (IV) misprices the *realized* move they expect, so the Greeks work in their favor rather than against.

## Family 2 — Volatility Strategies (Delta-Neutral)

Trade vol, not direction. These are the heart of options trading and the source of most professional options PnL.

### Long Volatility (Long Gamma/Vega)
- **Long straddle** — buy ATM call + ATM put. Profits from a large move in *either* direction or an IV spike; loses to theta if the market sits. The breakeven is ±(move needed to cover premium). Long gamma means delta-hedging harvests realized vol.
- **Long strangle** — buy OTM call + OTM put. Cheaper than straddle, but needs a bigger move. Long-vol-on-a-budget.
- **Risk reversal / collar** — buy call, sell put (or vice versa). Financed long/short delta exposure; the vol tilt depends on skew.

### Short Volatility (Short Gamma/Vega) — Income
- **Short straddle / strangle** — sell ATM/OTM call + put. Profit if price stays in a range and IV falls; theta is the income. Catastrophic tail risk (naked short gamma); historically the strategy that blows up funds (Volmageddon 2018, short-vol ETNs). Always risk-defined in practice (iron condor) or strictly size/stop-managed.
- **Iron condor** — sell an OTM put spread + sell an OTM call spread. Defined-risk short vol: max loss capped, income from theta/IV crush. The workhorse retail income strategy. Profit zone is the range between the short strikes.
- **Iron butterfly** — sell ATM straddle, buy OTM wings. Higher income than condor, narrower profit zone. Peak theta at the money.
- **Credit spreads** — single-sided defined-risk short vol (bull put spread / bear call spread). Income with capped loss.

### Delta-Neutral Vol Arbitrage
- **Implied vs realized vol** — sell IV when it exceeds expected realized (short straddle/iron condor), buy when below. The core vol-trading edge. See [Volatility Arbitrage](volatility-arbitrage).
- **Vol surface / skew trades** — trade the *shape*: risk reversals (skew), calendar (term structure), butterflies (curvature). E.g., if put skew is historically extreme, sell the skew via a risk reversal.
- **Dispersion trading** — short index vol, long constituent vol (or vice versa), exploiting index/constituent implied correlation. A classic stat-arb-flavored vol trade.

## Family 3 — Income / Carry Strategies

- **The Wheel** — systematic cash-secured put assignment → covered call cycle. Sell puts on a stock you're willing to own; if assigned, sell covered calls against it until called away; repeat. Income from theta; the "risk" is owning the stock at the put strike (which you wanted). Popular with retail for its simplicity and defined behavior. See the Alpaca wheel template.
- **Covered call** — own stock, sell calls against it. Income + capped upside; effectively lowers cost basis. The most common options income strategy.
- **Cash-secured put** — sell a put, hold cash to cover assignment. Income + obligation to buy at strike. The entry half of the Wheel.
- **Buy-write / covered combo** — simultaneous covered call + cash-secured put; a financed stock position with income.

## Family 4 — Gamma Scalping

A delta-hedged long-gamma position (long straddle, dynamically hedged) profits from *realized* volatility: each delta-hedge rebalance buys low and sells high (the long-gamma rebalancing edge). The trade profits when realized vol > implied vol (the theta paid). Gamma scalping is the explicit harvesting of this: the trader delta-hedges frequently to capture the oscillation, paying theta, and wins if oscillation exceeds the theta cost. It is the operational form of "long vol" and the conceptual inverse of the short-straddle theta collector.

Gamma scalping requires frequent hedging (cost: spread + commissions) and is most viable on liquid underlyings with low transaction costs. It is also the lens through which market makers understand their long-gamma inventory: they *want* realized vol, and they pay theta for it.

## Risk Management

- **Defined-risk bias** — for non-professionals, prefer defined-risk structures (spreads, iron condors) over naked short gamma. Naked short vol has unbounded loss and has ruined many accounts.
- **Position sizing by Greek exposure, not premium** — size by vega/delta dollars, not by number of contracts or premium collected. Two iron condors can have wildly different risk.
- **Tail-risk hedging** — for short-vol books, allocate a small % to long out-of-the-money puts (convex tail hedges) to cap the Volmageddon scenario. The cost is a drag; the value is survival.
- **Assignment/early-exercise awareness** — short American options on dividend-paying stocks can be assigned early; pin risk near expiration on ITM options.
- **IV crush** — selling options into earnings/events captures elevated IV that collapses post-event; buying options into events pays elevated IV that crushes. Event IV is a major PnL driver to model.
- **Liquidity / wide bid-ask** — options markets are wider than stock; crossing the spread repeatedly destroys edge. Trade liquid underlyings and use limit orders.

## Common Pitfalls

- **Picking the wrong strategy for the view** — buying a straddle when you have a directional view (you're paying for vol you don't need); using a credit spread when you want unlimited upside.
- **Ignoring theta** — holding long options through decay "hoping" the move comes; theta is relentless.
- **Selling naked vol unhedged** — the asymmetric disaster trade. Defined-risk equivalents exist for almost every short-vol thesis.
- **Chasing IV without realized basis** — high IV alone isn't a sell signal; high IV *vs expected realized* is.
- **Mis-sizing by premium** — a $2 credit on a wide iron condor is not "safer" than a $2 debit on a spread; size by max loss and Greek dollars.
- **Forgetting assignment risk** — short ITM options near expiry or ex-dividend get assigned; plan rolls/exits.
- **Over-trading the Greeks** — delta-hedging every tick incurs costs that swamp the gamma edge for non-HFT traders.

## Relationships to Other Methods

- **Market Making** — options MMs are the institutional short-vol/delta-hedging engine; their flow shapes the surface. See [Market Making](market-making).
- **Volatility Arbitrage** — the IV-vs-RV trade is the canonical vol-arb; options are the instrument. See [Volatility Arbitrage](volatility-arbitrage).
- **Statistical Arbitration** — dispersion trading is stat-arb applied to the vol surface. See [Statistical Arbitration](statistical-arbitrage).
- **Delta-Neutral / Gamma Scalping** — overlaps with market-making inventory management. See [Market Making](market-making).
- **Event-Driven / Sentiment** — earnings/event IV plays. See [Sentiment & News Trading](sentiment-news).
- **Holding-Period Styles** — options income (Wheel, covered calls) is typically a swing/position timeframe. See [Swing Trading](swing-trading), [Position Trading](position-trading).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| QuantConnect/Lean | 20334 | Algorithmic trading engine (Python/C#) with options support | https://github.com/QuantConnect/Lean |
| jasonstrimpel/volatility-trading | 1934 | Volatility estimators based on Euan Sinclair's *Volatility Trading* | https://github.com/jasonstrimpel/volatility-trading |
| Lumiwealth/lumibot | 1724 | Backtestable algo strategies for stocks, options, crypto | https://github.com/Lumiwealth/lumibot |
| goldspanlabs/optopsy | 1411 | Nimble options research & backtesting library (Python) | https://github.com/goldspanlabs/optopsy |
| OptionsnPython/Option-strategies-backtesting-in-Python | 171 | Backtesting book code: Greeks strategies in Python | https://github.com/OptionsnPython/Option-strategies-backtesting-in-Python |
| lambdaclass/options_portfolio_backtester | 240 | Backtester for options & equity portfolio strategies | https://github.com/lambdaclass/options_portfolio_backtester |
| alpacahq/options-wheel | 123 | Runnable algo template for the Options Wheel strategy | https://github.com/alpacahq/options-wheel |
| boyac/pyOptionPricing | 316 | Black-Scholes & Monte Carlo option pricing, Greeks | https://github.com/boyac/pyOptionPricing |
| XanderRobbins/Arbitrage-Free-Volatility-Surface | 9 | Arbitrage-free vol surface: SVI & Heston calibration | https://github.com/XanderRobbins/Arbitrage-Free-Volatility-Surface |
| v-buchkov/statistical_arbitrage_backtester | 7 | Vol stat-arb via delta-hedge option replication | https://github.com/v-buchkov/statistical_arbitrage_backtester |

## Books & Foundational Reading

- Sheldon Natenberg — *Option Volatility and Pricing* (the standard reference)
- Euan Sinclair — *Volatility Trading* (IV vs RV, the practitioner's bible)
- Espen Haug — *The Complete Guide to Option Pricing Formulas*
- Nassim Taleb — *Dynamic Hedging* (managing the Greeks, tail risk)
- Jim Bennett / Charles Cottle — *Options Trading: The Hidden Reality*

## Further Study

- Backtest a 30-DTE iron condor on SPX entered at 16-delta short strikes, managed at 50% profit or 21-DTE exit; compare to hold-to-expiration.
- Build an IV-RV term-structure monitor (VIX vs realized 30d) to time long/short vol.
- Implement a delta-hedged long straddle and measure gamma-scalping PnL vs theta cost across realized-vol regimes.
