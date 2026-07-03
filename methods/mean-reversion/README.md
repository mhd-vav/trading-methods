---
title: Mean Reversion
type: method
domain: trading
category: Quantitative & Statistical
tier: 1
importance: high
markets: equities, futures, forex, crypto, ETFs
timeframe: intraday to multi-day
github_repo: mhd-vav/trading-methods
branch: mean-reversion
---

# Mean Reversion

Mean reversion is the trading premise that prices — or derived quantities like spreads, ratios, and indicators — tend to return to their historical average after deviating. A mean-reversion trader sells strength (price well above its mean) and buys weakness (price well below its mean), profiting when the snap-back occurs. It is the conceptual opposite of trend following: where the trend follower bets that deviations *persist*, the mean-reverter bets that they *revert*.

The strategy rests on a statistical claim: the series being traded is **stationary** (or at least boundable) — it oscillates around a central value rather than wandering freely. When that is true, extreme deviations are finite and a return to the mean is more likely than continued drift. When it is *not* true (the asset is trending/non-stationary), mean reversion fails badly — which is why regime detection is central to the method.

## Core Intuition

Markets overreact. News, order-flow imbalance, and sentiment push prices past fair value; then calm returns and price gravitates back toward a baseline. A rubber band stretched too far snaps back. The mean-reverter measures how far the band is stretched (the deviation from a moving average or a normalized z-score) and trades the snap.

The single-asset version trades price against its own moving average. The market-neutral version trades a spread between related assets (this is [pairs/stat arb](statistical-arbitrage)). The principles overlap; the difference is whether you hedge the market out.

## The Statistical Basis

- **Mean (the anchor):** typically a moving average (simple, exponential, or weighted) of price over a lookback window. The window choice defines what "mean" you're reverting to — a 20-day MA vs. a 200-day MA define very different trades.
- **Deviation (the signal):** how far price is from the mean. Measured as:
  - **Z-score:** `(price − MA) / std(price)` over the window — standardized distance in standard deviations.
  - **Bollinger Band position:** Bollinger Bands plot MA ± k·std; price touching the lower band = −2σ-ish deviation.
  - **RSI / oscillator extremes:** RSI < 30 = oversold (price extended down relative to recent closes); RSI > 70 = overbought.
- **Reversion:** the bet that deviation → 0 (price returns to the MA).

Critical: the method requires the series to be **mean-reverting (stationary)**. Equities in the very long run are not (they trend upward with growth), so mean reversion is typically applied on shorter horizons, on spreads/ratios, or on instruments known to range (range-bound FX, volatility products, commodities near production cost).

## Common Implementations

### Bollinger Band Mean Reversion

The classic. Bands at MA ± 2σ. Rules:
- **Entry long:** price closes below the lower band (oversold) → buy. Exit when price returns to the MA (middle band).
- **Entry short:** price closes above the upper band (overbought) → sell. Exit at the MA.
- **Stop:** price closes beyond a wider band (e.g., ±3σ) — the move may be a genuine breakout/trend, not an overreaction.
- Parameter: window length (20 common), k (2 common). Tighter bands = more trades but weaker deviation; wider = fewer, stronger.

Bollinger Bands encode mean reversion directly: the bands widen in volatile regimes and contract in calm ones, adapting the entry threshold to current volatility.

### RSI / Oscillator Reversion

Use RSI (or stochastics, %R) to gauge extension:
- **Long:** RSI dips below 30 (oversold) then turns up → buy.
- **Short:** RSI exceeds 70 (overbought) then turns down → sell.
- Exit on return toward the 50 midline, or on opposite extreme.
RSI reversion works best in ranging markets; in trends, RSI can stay extreme for long stretches ("RSI pegging") and naive reversion gets run over.

### Z-Score Reversion (Single Asset)

Generalize Bollinger: compute a rolling z-score of price vs. its MA. Enter long when z < −threshold (e.g., −2), short when z > +threshold; exit at z ≈ 0; stop beyond a catastrophic z. Identical math to pairs trading, applied to one asset's deviation from its own mean rather than a spread's.

### RSI + Bollinger Confluence

Combine signals: only take the long when price is at the lower band *and* RSI is oversold — the confluence filters out weak signals and raises the probability of reversion.

### Intraday / Opening Range Reversion

Price stretches away from the session VWAP or opening range; fade the extreme expecting a return to VWAP by close. Common among equities day traders and prop shops. See [VWAP trading](vwap-trading).

## Regime Detection — Survival Skill

Mean reversion's nemesis is the trending regime. A market in trend keeps deviating — the "rubber band" doesn't snap, it breaks. The single greatest determinant of a mean-reverter's survival is knowing when *not* to trade. Regime filters:

- **ADX (trend strength):** ADX > 25–30 = trending regime → disable mean reversion. ADX < 20 = ranging → enable.
- **Hurst exponent:** H < 0.5 indicates mean-reverting behavior; H > 0.5 trending; H ≈ 0.5 random walk. A regime-aware reverter trades only when H < 0.5.
- **MA slope / cross:** a flat or sideways MA (no clear slope) favors reversion; a steeply sloped MA favors trend.
- **Volatility regime:** reversion often works in calm, low-vol regimes and breaks in vol explosions (where deviations persist).

A mean-reversion strategy without a regime filter is a short-volatility strategy in disguise — it grinds small wins until a trend vaporizes them.

## Risk Management

- **Stops are mandatory.** Because reversion assumes deviation is bounded, a genuine trend makes the loss theoretically unbounded. Hard stops (beyond a wider band / extreme z) cap the damage.
- **"Death by a thousand cuts" vs. "one knockout":** mean reversion typically has a high win rate (many small wins) punctuated by occasional large losses. Position sizing must survive the tail losses; martingale-style adding to losers is dangerous.
- **Time stop:** if price doesn't revert within N bars, exit — a deviation that persists is becoming a trend.
- **Diversification:** spread risk across many uncorrelated mean-reverting instruments to smooth the equity curve and reduce single-instrument break risk.
- **Avoid earnings/news:** fundamentals can break the stationarity assumption overnight. Many reversioners flat before scheduled events.

## Strengths and Weaknesses

**Strengths:**
- High win rate (most deviations do revert).
- Works in the common ranging regime that frustrates trend followers — the two styles are complementary.
- Clear, testable mathematics (stationarity, z-scores).
- Scales across many instruments simultaneously.

**Weaknesses:**
- Asymmetric payoff: small wins, occasional large losses. Requires discipline to take stops.
- Fails in trends; needs regime filtering.
- Edges decay in calm markets (crowding) and the strategy is short volatility (bleeds in crises).
- Stationarity is an assumption that can break — the "reverting" series starts trending.

## Common Pitfalls

- **No regime filter.** Trading reversion into a trend is the #1 way to blow up a mean-reversion book.
- **Adding to losers (martingale).** Tempting because reversion "should" come back, but a trend makes it catastrophic. Avoid scaling into adverse excursions.
- **Wrong instrument.** Applying reversion to a strong secular uptrend (e.g., a growth stock) without detrending. Use spreads, ratios, or range-bound instruments.
- **Ignoring costs.** Frequent small trades accumulate commissions and slippage that can exceed the thin reversion edge.
- **Static parameters.** Volatility changes; fixed bands/z-thresholds stop fitting. Adaptive parameters (volatility-scaled) are more robust.
- **Overfitting the lookback.** Optimizing the MA window in-sample to maximize reversion is classic overfitting. Out-of-sample and walk-forward are essential.

## Relationship to Other Methods

- **Statistical Arbitrage / Pairs:** The market-neutral expression of mean reversion — reversion of a *spread* rather than a single price. See [Statistical Arbitrage / Pairs Trading](statistical-arbitrage).
- **Trend Following:** The philosophical opposite. A diversified book often holds both to cover both regimes. See [Trend Following](trend-following).
- **Bollinger Bands / RSI (Indicators):** The indicator tools most used to implement mean reversion. See [Indicator & Oscillator-Based Strategies](cluster-indicator).
- **Grid Trading:** A structured mean-reversion variant that places a ladder of orders around a mean. See [Grid Trading](grid-trading).
- **ML/AI:** Reinforcement learning often learns mean-reversion-like policies in ranging regimes. See [Machine Learning & AI-Based Trading](cluster-ml).

## Why It Matters

Mean reversion is one of the two pillars of systematic trading (with trend following). It captures a real behavioral phenomenon — overreaction and correction — and it works precisely in the ranging regimes where trend strategies idle. A trader who understands *both* mean reversion and trend following, and a regime filter to switch between them, has the core of a robust systematic approach. The discipline it teaches — stationarity, deviation measurement, the danger of trends, the necessity of stops — is foundational quant literacy.

## Open-Source References

- **je-suis-tm/quant-trading** (★10241) — Python strategies incl. RSI, Bollinger Bands, Pair Trading, Monte Carlo; clear mean-reversion implementations. https://github.com/je-suis-tm/quant-trading
- **jamesmawm/High-Frequency-Trading-Model-with-IB** (★2889) — HFT model with mean-reversion in Python (IB API). https://github.com/jamesmawm/High-Frequency-Trading-Model-with-IB
- **rolling-panda-san/notebooks** (★729) — systematic strategy analysis (trend-following, carry, mean-reversion). https://github.com/rolling-panda-san/notebooks
- **moss-site/moss-trade-bot-skills** (★324) — LLM trading agents; mean reversion as one of five pillars. https://github.com/moss-site/moss-trade-bot-skills
- **Logicmn/pyx** (★113) — real-time stock trading using a basic mean reversion algorithm. https://github.com/Logicmn/pyx
- **arendarski/Simple-Mean-Reversion-Strategy-in-Python** — comprehensive 7-test validation of a mean-reversion pair. https://github.com/arendarski/Simple-Mean-Reversion-Strategy-in-Python
- **ntx97/backtester-mean-reversion** — RSI mean-reversion backtester on US tech stocks. https://github.com/ntx97/backtester-mean-reversion

## Further Study

- Ernie Chan — *Algorithmic Trading* (mean-reversion chapters with code).
- Robert Carver — *Systematic Trading* (regime-aware combination of trend and reversion).
- Covel — *Trend Following* (for the contrast and why the two are paired).
- Bollinger — *Bollinger on Bollinger Bands*.

