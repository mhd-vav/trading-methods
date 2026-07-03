---
title: Statistical Arbitrage / Pairs Trading
type: method
domain: trading
category: Quantitative & Statistical
tier: 1
importance: critical
markets: equities (classic), ETFs, futures, crypto
timeframe: minutes to days (intraday/multi-day)
github_repo: mhd-vav/trading-methods
branch: statistical-arbitrage
---

# Statistical Arbitrage / Pairs Trading

Statistical arbitrage ("stat arb") is a family of quantitative, market-neutral strategies that exploit temporary mispricings between statistically related instruments. The canonical and most accessible form is **pairs trading**: identify two assets whose prices move together in a long-run equilibrium (cointegrated), and trade the spread between them — long the underperformer, short the outperformer — when the spread diverges, profiting when it reverts to the mean.

Stat arb generalizes pairs to large portfolios (index arbitrage, cross-sectional mean reversion across hundreds of stocks), but the core mechanic is identical: **find a stable long-run relationship, measure deviations, and bet on reversion.** It is one of the foundational quantitative strategies, famously run by hedge funds like Renaissance, Citadel, and D.E. Shaw, and it remains the entry point for most aspiring quants because its mathematics (cointegration) is clean and well-understood.

## Core Intuition

Two stocks in the same sector — say Pepsi (PEP) and Coca-Cola (KO) — face the same macro forces and tend to move together. Their prices are not identical, but their *spread* (the difference, or a weighted combination) is stable over time: it fluctuates around a constant mean. When the spread widens abnormally — PEP rallies while KO lags — the assumption is that the divergence is temporary. The pairs trader sells the rich one (PEP) and buys the cheap one (KO). If the relationship holds, the spread reverts, and both legs together profit regardless of the overall market direction.

The "arbitrage" is statistical, not riskless: there is no guarantee the spread reverts within the trader's horizon. The edge is the *probability* of reversion, established by testing the historical relationship rigorously.

## Why It Works (Economic Logic)

- **Common risk factors:** Cointegrated pairs share economic drivers (sector, factor exposure, supply chain). Temporary divergence is noise; the shared drivers pull them back.
- **Mean-reverting mispricing:** Transient order-flow imbalance or news-driven overreaction pushes one leg away from fair value; liquidity providers (stat arb traders) supply the other side and capture the reversion.
- **Market neutrality:** Because the trade is long/short, it hedges out broad market beta — returns come from the relative spread, not market direction. This produces low correlation to indices and (historically) smooth equity curves.

## The Statistical Foundation — Cointegration

This is the mathematical heart of pairs trading. Two non-stationary price series (each individually a random walk) can be **cointegrated**: a linear combination of them *is* stationary (mean-reverting). This is exactly the property needed — the spread must be stable enough to revert.

### Stationarity (the prerequisite)

A series is **stationary** if its statistical properties (mean, variance) are constant over time — it doesn't wander off. Price series are typically *non-stationary* (they trend), but *returns* are often stationary. For pairs trading we need the **spread** to be stationary, even though each price is not.

- **ADF (Augmented Dickey-Fuller) test:** the standard test for stationarity. Null hypothesis = unit root (non-stationary); rejecting it (low p-value, typically <0.05) means the series is stationary.
- A spread that passes ADF is mean-reverting → tradeable.

### Cointegration (the relationship)

Two series X and Y are cointegrated if a linear combination `Spread = Y − β·X` is stationary, for some hedge ratio β. The classic test:

- **Engle-Granger two-step method:**
  1. Regress Y on X: `Y = α + β·X + ε` (ordinary least squares). β is the hedge ratio.
  2. Test the residuals ε for stationarity with ADF. If residuals are stationary → X and Y are cointegrated. β tells you how many units of X to hold per unit of Y to keep the spread flat.
- **Johansen test:** a more general multivariate test that handles >2 series and doesn't require pre-specifying which is dependent. Used for portfolio stat arb.

The hedge ratio β is dynamic — it drifts as the relationship evolves — so it is usually re-estimated on a rolling window rather than fixed forever.

### The Spread and Its Z-Score

Given β, the spread `S = Y − β·X`. To make it comparable across pairs, normalize to a **z-score**:

```
z = (S − mean(S)) / std(S)
```

computed over a rolling window (e.g., 60 days). The z-score measures how many standard deviations the spread is from its mean. This is the signal: z far from zero = divergence; z returning toward zero = the trade.

## The Trading Logic

1. **Pair selection:** Screen a universe (e.g., S&P 500 stocks) for cointegrated pairs — run Engle-Granger or Johansen on candidate pairs, keep those with strong cointegration (low ADF p-value) and economic logic (same sector/ETF). Re-test periodically because relationships break.
2. **Hedge ratio:** Estimate β (rolling OLS or Kalman filter for adaptive β).
3. **Signal:** Compute the rolling z-score of the spread.
   - **Entry (long the spread):** when z drops below −threshold (e.g., −2.0): spread is too cheap → buy Y, sell β·X. (Y is the underperformer.)
   - **Entry (short the spread):** when z rises above +threshold (e.g., +2.0): spread is too rich → sell Y, buy β·X.
   - **Exit:** when z reverts to 0 (or a small band like ±0.5). Take profit on the reversion.
   - **Stop:** if z exceeds a catastrophic level (e.g., ±3.5–4.0) the relationship may have broken — cut to limit a blow-up.
4. **Sizing:** dollar-neutral (equal dollar long/short) or beta-neutral (equal beta) so the book carries no market beta.
5. **Rebalance:** as prices move, the hedge ratio drifts; periodically re-hedge to keep the book neutral.

## Variants

- **Distance method:** the simplest pairs approach — trade pairs whose normalized price distance exceeds a threshold, no cointegration test. Easier but less rigorous; prone to trading non-stationary (trending) spreads.
- **Cointegration method (classic):** the Engle-Granger approach above. The academic standard.
- **Kalman-filter / dynamic β:** let the hedge ratio evolve continuously via a state-space model, adapting to a slowly shifting relationship. More robust to regime change than fixed OLS β.
- **Copula methods:** model the dependence structure non-linearly; useful when the relationship isn't well-captured by linear cointegration.
- **Machine learning / RL:** learn the entry/exit policy or enhance pair selection with features. (See `wywongbd/pairstrade-fyp-2019` for an RL comparison.)
- **Index/stat arb (portfolio):** generalize from 2-name pairs to a basket that mean-reverts to an index or factor model — the equity market-neutral book at scale.
- **Triangular arbitrage (FX/crypto):** a related but distinct arb exploiting pricing inconsistencies across three currencies; near-instantaneous, not mean-reverting. See [Arbitrage Strategies](cluster-arbitrage).

## Risk Management

- **Stationarity break risk:** the biggest danger. A cointegrated relationship can *stop* cointegrating (structural break — merger, delisting, sector shock). The spread trends instead of reverting → unbounded loss. Mitigate with rolling re-tests, hard z-stop, and not over-concentrating in one pair.
- **Beta drift:** β changes; a stale hedge ratio leaves residual market exposure. Re-estimate frequently.
- **Crowding:** popular pairs (KO/PEP, GLD/GDX) are crowded → thinner edge and worse fills. Edge decays as more capital chases the same signal.
- **Costs:** two legs = double transaction costs + borrow costs on the short + slippage. The reversion must exceed these. High-frequency stat arb requires very low costs.
- **Tail risk:** mean-reverting strategies harvest small gains but occasionally take large hits when spreads blow out (the "picking up pennies in front of a steamroller" profile). Position sizing and stops are non-negotiable.
- **Capital efficiency:** market-neutral books use leverage to scale small per-trade edge; leverage amplifies break risk.

## Practical Pipeline (Code)

A reproducible pairs-trading pipeline (mirroring KidQuant's notebook):

1. Fetch OHLCV (e.g., yfinance) for a candidate universe.
2. For each candidate pair, run rolling OLS → residuals → ADF test. Keep pairs with p-value < 0.05 and economic sense.
3. For selected pairs, compute rolling hedge ratio β (window 60–120 days) and spread `Y − β·X`.
4. Z-score the spread (rolling). Generate signals at ±2σ entry, 0 exit, ±4σ stop.
5. Backtest with realistic costs; report Sharpe, max drawdown, hit rate, exposure.
6. Walk-forward / out-of-sample test — never trust in-sample cointegration alone (overfitting is severe).
7. Live: re-estimate β daily, monitor z, manage stops.

Libraries: `statsmodels` (OLS, ADF, cointegration), `pandas`/`numpy`, `yfinance`, backtest frameworks (`backtrader`, `zipline`, or `vectorbt`).

## Common Pitfalls

- **Overfitting the selection.** Testing thousands of pairs and keeping the best in-sample cointegration guarantees spurious results. Use out-of-sample validation and economic priors (same sector) to constrain the search.
- **Ignoring structural breaks.** A pair cointegrated for 5 years can break in a day. Rolling re-tests and stops are survival.
- **Static hedge ratio.** Fixed β from one regression drifts out of neutrality; re-estimate.
- **Underestimating costs.** Two legs, the short borrow, and slippage can erase a thin reversion edge.
- **Confusing correlation with cointegration.** Two assets can be highly correlated (move together day-to-day) but not cointegrated (their spread trends). Correlation ≠ a tradeable mean-reverting spread. Always test cointegration, not just correlation.

## Relationship to Other Methods

- **Mean Reversion:** Pairs trading is the market-neutral application of mean reversion to a spread rather than a single asset. See [Mean Reversion](mean-reversion).
- **Arbitrage (general):** Stat arb is "arbitrage" in the statistical sense; true arbitrage (triangular, cross-exchange) is riskless and instantaneous. See [Arbitrage Strategies](cluster-arbitrage).
- **Index Arbitrage:** A portfolio generalization — trade baskets vs. index futures when they diverge. See [Arbitrage Strategies](cluster-arbitrage).
- **ML/AI Trading:** Modern stat arb blends heavily with ML for pair selection and signal generation. See [Machine Learning & AI-Based Trading](cluster-ml).

## Why It's a Cornerstone

Statistical arbitrage is where quant finance becomes concrete for most practitioners: it has clean math (cointegration), a clear economic story (shared risk factors, mean reversion), and a market-neutral return profile that institutions value. Even as simple pairs edges have decayed with crowding, the framework — find stable relationships, trade deviations, manage the break risk — underpins a vast swath of market-neutral and relative-value strategies. Learning it teaches the core quant skills: stationarity, hypothesis testing, hedge ratios, market neutrality, and the discipline of out-of-sample validation.

## Open-Source References

- **je-suis-tm/quant-trading** (★10241) — Python quant strategies including Pair Trading, RSI, Bollinger, Monte Carlo; excellent pedagogical implementations. https://github.com/je-suis-tm/quant-trading
- **jamesmawm/High-Frequency-Trading-Model-with-IB** (★2889) — HFT model using IB API with pairs and mean-reversion in Python. https://github.com/jamesmawm/High-Frequency-Trading-Model-with-IB
- **KidQuant/Pairs-Trading-With-Python** (★764) — end-to-end tutorial: stationarity → cointegration → pair selection → signals. The cleanest learning pipeline. https://github.com/KidQuant/Pairs-Trading-With-Python
- **JerBouma/AlgorithmicTrading** (★1098) — three arbitrage approaches including Statistical Arbitrage, with runnable code. https://github.com/JerBouma/AlgorithmicTrading
- **lukstei/trading-backtest** (★350) — Java backtest engine with a cointegration pairs strategy. https://github.com/lukstei/trading-backtest
- **bradleyboyuyang/Statistical-Arbitrage** (★270) — high-frequency statistical arbitrage implementation. https://github.com/bradleyboyuyang/Statistical-Arbitrage
- **gregzanotti/dlsa-public** (★264) — Deep Learning Statistical Arbitrage (ML-enhanced stat arb). https://github.com/gregzanotti/dlsa-public
- **wywongbd/pairstrade-fyp-2019** (★272) — compares distance, cointegration, and RL approaches to pair trading. https://github.com/wywongbd/pairstrade-fyp-2019
- **tibkiss/huba-v1** (★200) — real live-traded pairs strategy (2012–2016) following Ernie Chan's methodology; candid post-mortem. https://github.com/tibkiss/huba-v1

## Further Study

- Ernie Chan — *Quantitative Trading* and *Algorithmic Trading* (the foundational practitioner texts; the huba-v1 repo follows them).
- Vidyamurthy — *Pairs Trading: Quantitative Methods and Analysis* (the academic monograph).
- Avellaneda & Lee — "Statistical Arbitrage in the US Equities Market" (the canonical paper).
- statsmodels documentation — `coint`, `adfuller`, OLS — for the implementation side.

