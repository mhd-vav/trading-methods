---
title: Trend Following
type: method
domain: trading
category: Quantitative & Statistical / Algorithmic
tier: 1
importance: critical
markets: futures (classic), forex, equities, crypto, commodities
timeframe: weeks to months (multi-week holds)
github_repo: mhd-vav/trading-methods
branch: trend-following
---

# Trend Following

Trend following is the strategy of identifying an established directional move in price and joining it — buying assets that are rising, selling short those that are falling — with the thesis that trends, once underway, tend to persist longer than random walks predict. It is the oldest and most robustly documented systematic approach, the backbone of the CTA (Commodity Trading Advisor) / managed-futures industry, and the philosophical counterweight to [mean reversion](mean-reversion). Where mean reversion bets deviations contract, trend following bets they *expand*.

Its defining trait is not the entry signal (any breakout/momentum trigger works) but the **risk-management architecture**: trend followers cut losers fast, let winners run, and size positions by volatility so no single trade can end the game. The edge is not a high win rate — trend systems typically win only 35–45% of trades — but a large average winner-to-loser ratio (cutting at -1R, riding to +5R or more). The asymmetry, repeated across many markets, produces the returns.

## Core Philosophy — "The Trend Is Your Friend"

Three beliefs underpin trend following:

1. **Markets trend.** Supply/demand imbalances, macro shifts, and behavioral herding cause prices to move directionally over weeks/months — not just oscillate. Capitalizing requires only that *some* markets trend *some* of the time; a diversified trend book rides whichever ones do.
2. **You cannot predict the start.** No one consistently calls tops and bottoms. So trend followers don't try — they wait for a move to *confirm*, then enter. They accept missing the first part of the move in exchange for confirmation it's real.
3. **The edge is in the exit, not the entry.** The entry is a mechanical trigger; the profit comes from disciplined trailing stops that let winners run and cut losers immediately. "Let profits run, cut losses short" is the entire strategy in six words.

## Why Trends Persist (the logic)

- **Behavioral:** herding, anchoring, and disposition effect (retail sells winners early, holds losers — fueling trends).
- **Macro/structural:** central-bank cycles, supply shocks, and secular shifts produce multi-month directional moves.
- **Information diffusion:** news and fundamentals are absorbed gradually, not instantly, producing trends rather than jumps.
- **Stop runs and option hedging:** gamma and delta hedging by option desks, plus stop clusters, extend moves.

A trend follower doesn't need to know *why* a trend exists — only that they do, statistically, and that a rules-based system can harvest them.

## Entry Signals

Trend entries are breakout/momentum triggers — any rule that detects "a move has begun":

- **Donchian channel breakout (Turtle rule):** enter long when price breaks the N-day high (classic: 20-day); short on the N-day low. The original Turtle Traders system used 20-day entries with 10-day exits. Simple, robust, the canonical trend signal.
- **Moving-average crossover:** golden cross (fast MA crosses above slow MA) → long; death cross → short. Common but laggier; prone to whipsaws in ranges.
- **Moving-average slope / price vs. MA:** price trading above a rising long MA = uptrend confirmed.
- **Momentum / rate of change:** price up X% over N days → long.
- **Moving-average ribbon:** multiple MAs stacking in order (fastest on top in an uptrend) confirms trend strength.
- **ATR / volatility expansion:** trends often begin with a volatility expansion; volatility breakouts can precede or confirm.

The specific trigger matters less than consistency and the exit logic. Most trend systems use a combination (e.g., Donchian breakout + MA filter to confirm direction).

## The Exit — Where the Money Is Made

- **Initial stop (cut losers):** placed at entry − (k × ATR) for longs, symmetric for shorts. ATR (average true range) scales the stop to current volatility so it's neither too tight (whipsawed out) nor too loose (large loss). Typical k = 1.5–3. The stop is *non-negotiable* — the moment it's hit, exit, no debate.
- **Trailing stop (let winners run):** as the trend progresses, the stop is ratcheted in the trend direction (e.g., trail by 2 ATR, or exit on a 10-day Donchian low for longs). This never moves against the trade. It allows the trend runner to capture most of the directional move while locking in profit as it extends.
- **Exit on opposite signal / trend break:** some systems exit when a counter-signal fires (e.g., MA cross back) or structure breaks.

The asymmetry: losers are capped at ~1–2 ATR (small), winners can run 5–20 ATR (large) in a big trend. The rare huge winner ("fat right tail") pays for all the small losers and then some.

## Position Sizing — Volatility-Targeted

This is what makes trend following survivable and is arguably its real innovation. Position size is set so each trade risks a *fixed fraction* of equity and each market contributes *equal volatility*:

1. **Determine risk per trade:** e.g., risk 0.5%–2% of equity on the stop distance (the Turtle rule used ~2% but modern systems use less for diversification).
2. **Volatility-normalize:** size = (risk $) / (ATR × point value). A volatile market gets a smaller position; a calm market a larger one, so each contributes similar risk.
3. **Equalize across markets:** each market in the portfolio gets roughly equal risk weight, so no single market dominates. Diversification across 30–60 markets smooths the equity curve.

This makes the system robust to *which* market trends — it doesn't matter, because it's equally positioned to catch whichever one moves. Position sizing is the difference between a trend system that survives and one that blows up on a string of whipsaws.

## The Turtle Traders (Canonical Case)

In 1983–84, Richard Dennis and William Eckhardt ran an experiment: could trend following be taught? They recruited novices ("Turtles"), taught them a rules-based Donchian-breakout system with ATR-based stops and sizing, and gave them capital. The Turtles reportedly made >$100M over several years, demonstrating that disciplined rules — not innate talent — drove the results.

Core Turtle rules:
- **Entry:** 20-day high breakout (long) / 20-day low (short). (A 55-day system for longer-term.)
- **Exit:** 10-day low (long) / 10-day high (short).
- **Stop:** 2 × ATR(20) from entry.
- **Sizing:** risk 2% of account per unit, adjusted by ATR; units added (pyramiding) as the trend confirmed.
- **Markets:** diversified across commodities, currencies, metals, bonds, equities.

The Turtle system remains the reference implementation for teaching trend following because every component is explicit and the logic is transparent.

## Strengths and Weaknesses

**Strengths:**
- Robust across decades and markets — the same rules work on 1980s commodities and 2020s crypto.
- Captures the rare large moves ("fat tails") that define asset returns.
- Low correlation to traditional buy-and-hold (does well in extended bull or bear regimes, including 2008).
- Rules-based and emotionless; scales across many markets simultaneously.
- Asymmetric payoff (small losses, large wins) means a low win rate is fine.

**Weaknesses:**
- **Whipsaws in ranging markets.** Sideways action produces a string of small losses (false breakouts) — "death by a thousand cuts." This is the cost of being positioned for every trend.
- **Low win rate (35–45%).** Psychologically hard; requires discipline to keep taking signals after a losing streak.
- **Lagging entries/exits.** Confirmation-based entry gives back the first part of the move; trailing stops give back the last part. You capture the middle.
- **Drawdowns in chop.** Extended non-trending periods can produce 15–30% drawdowns before the next trend arrives.
- **Sensitive to parameter choice in a limited way** — but robust systems are deliberately *under*-optimized to avoid overfitting.

## Regime Awareness

Trend following thrives in trending regimes and bleeds in ranging ones. While the strategy's design (cut losers, diversify) is meant to *survive* the ranges without predicting them, many practitioners add filters:
- **Volatility regime:** trend systems often do better in expanding vol; some reduce exposure in collapsing vol.
- **Correlation regime:** when all markets trend together (e.g., risk-on/risk-off), diversification benefit drops.
- The honest stance: trend followers generally *don't* try to time regime switches (it undermines the systematic nature); they rely on diversification and sizing to endure the bad periods.

## Risk Management — The System

- **Cut losers fast, no exceptions.** The stop is the system's immune system. Discretionary stop-widening destroys the edge.
- **Let winners run.** Premature profit-taking truncates the right tail that pays for everything.
- **Volatility sizing** so risk per trade and per market is controlled.
- **Diversify** across many uncorrelated markets to smooth returns (a trend in one market offsets whipsaws in another).
- **Limit total portfolio risk** (sum of individual risks) to avoid ruin in correlated drawdowns.
- **Pyramiding** (adding to winners) increases exposure to confirmed trends — but must be done with risk discipline, not greed.

## Common Pitfalls

- **Moving stops to avoid a loss.** The cardinal sin. The moment you widen a stop, the asymmetric payoff is gone.
- **Taking profits early.** Truncates the winners that fund the strategy.
- **Too few markets.** A 3-market trend book is just gambling on those 3; the law of large numbers needs 20+ markets.
- **Over-optimizing parameters.** Tweaking the Donchian length or ATR multiplier to maximize backtest returns overfits to history. Robust systems use round, under-tuned parameters.
- **Skipping signals after a losing streak.** Recency bias; the next signal may be the big winner.
- **Ignoring costs.** Futures roll costs and slippage erode returns; trade liquid markets.

## Relationship to Other Methods

- **Mean Reversion:** The opposite pillar. A complete systematic book often runs both to cover trending and ranging regimes. See [Mean Reversion](mean-reversion).
- **Breakout Strategies:** Trend following is essentially disciplined breakout trading with superior risk management. See the Donchian/breakout entries in [Algorithmic & Systematic Strategies](cluster-algo).
- **Momentum (cross-sectional):** A relative form — buy the strongest, sell the weakest within a universe. Cross-sectional momentum is a cousin of time-series trend following. See [cluster-quant](cluster-quant).
- **CTA / Managed Futures:** The institutional industry built on trend following. See [Macro & Fundamental Methods](cluster-macro).

## Why It's a Pillar

Trend following is arguably the most validated systematic strategy in existence — profitable across a century of data, every major asset class, and through every crisis. Its power is not cleverness but discipline: a simple, robust rule set, relentless risk management, and diversification. Learning it teaches the most important trading lesson — that the exit and the sizing, not the entry, determine outcomes — and provides a strategy whose logic generalizes to any trending market, forever. For a systematic trader, trend following and mean reversion together, filtered by regime, form the backbone of a robust book.

## Open-Source References

- **chrism2671/PyTrendFollow** (★465) — systematic futures trading using trend following; production-style trend system. https://github.com/chrism2671/PyTrendFollow
- **rolling-panda-san/notebooks** (★729) — systematic strategy analysis incl. trend-following, carry, mean-reversion. https://github.com/rolling-panda-san/notebooks
- **Harvey-Sun/TurtleTrading** (★50) — Turtle trading strategy implementation (stock daily). https://github.com/Harvey-Sun/TurtleTrading
- **bideeen/Building-A-Trading-Strategy-With-Python** (★64) — trend & MA strategy construction in Python. https://github.com/bideeen/Building-A-Trading-Strategy-With-Python
- **pratiknabriya/Moving-Average-Crossover-Trading-Strategy-with-Python** (★34) — SMA/EMA crossover signal generation. https://github.com/pratiknabriya/Moving-Average-Crossover-Trading-Strategy-with-Python
- **igormoondev/forex-meta-trader-trading-bot** (★24) — trend-following bot using MA crossover (MT). https://github.com/igormoondev/forex-meta-trader-trading-bot
- **EigenEngineer/Donchian-Channel-Trading** (★8) — near-universal rule set based on Donchian channels. https://github.com/EigenEngineer/Donchian-Channel-Trading
- **QuantConnect/Lean** (★20334) — algorithmic engine with trend-following templates (Donchian, MA) in Python/C#. https://github.com/QuantConnect/Lean

## Further Study

- Michael Covel — *Trend Following* and *The Complete TurtleTrader* (the definitive popular + historical treatment).
- Curtis Faith — *Way of the Turtle* (by a Turtle; the system in detail).
- Robert Carver — *Systematic Trading* and *Advances in Financial Machine Learning*-adjacent practical sizing.
- Andreas Clenow — *Following the Trend* (CTA/managed-futures mechanics).
- Original Turtle rules PDF (widely circulated) — the reference implementation.

