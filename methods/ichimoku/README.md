---
title: Ichimoku Cloud (Ichimoku Kinko Hyo)
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 2
importance: high
inventor: Goichi Hosoda (Ichimoku Sanjin)
era: 1930s–1960s Japan (published 1968)
markets: all (FX most popular; indices, stocks, crypto)
timeframe: any (daily most classic)
github_repo: mhd-vav/trading-methods
branch: ichimoku
---

# Ichimoku Cloud (Ichimoku Kinko Hyo)

Ichimoku Kinko Hyo — "equilibrium chart at a glance" — is a complete, self-contained technical system invented by Japanese journalist Goichi Hosoda ("Ichimoku Sanjin") and refined over three decades before publication in 1968. Unlike most indicators that bolt onto price, Ichimoku is a *holistic overlay*: five components computed from the midpoints of lookback highs/lows that together render trend direction, momentum, support/resistance, and forward projection on one chart. Its defining feature is the **Kumo (cloud)** — a shaded band projected 26 periods *into the future*, giving the trader a visual forecast of support/resistance before it arrives.

The method's name captures its philosophy: *at a glance*, a trader should read trend, strength, and key levels without a second indicator. Where [Price Action](price-action) is minimalist and [Smart Money Concepts](smc-ict) is structural-narrative, Ichimoku is *rule-dense and self-sufficient* — a single system engineered to answer "where is price going and is it safe to be long?"

## Core Philosophy — Equilibrium at a Glance

Hosoda's premise: markets oscillate around equilibrium, and that equilibrium — and its shifts — can be computed and displayed from price's own high/low midpoints over specific lookbacks. The five components each measure a different timeframe of equilibrium (9, 26, 52 periods) and present them together so the eye integrates them instantly. The cloud visualizes the *balance of power*: thick and green (bullish) when short-term equilibrium is above long-term; thin and red (bearish) when below. Price above the cloud is a bull regime; below, a bear regime; inside, undecided.

The 26-period forward shift of the cloud and the Chikou (lagging) span is the genius touch: the trader sees *future* support/resistance and *past* price's relationship to *current* price simultaneously, enabling a time-as-well-as-price read most indicators cannot offer.

## The Five Components

All use the midpoint `(high + low) / 2` over their lookback, not closes:

1. **Tenkan-sen (Conversion Line)** — 9-period midpoint. The fastest line; short-term equilibrium. Its slope is the first momentum read; flat = consolidation.
2. **Kijun-sen (Base Line)** — 26-period midpoint. The medium-term equilibrium and the system's *anchor* — the "default" support/resistance and the line all signals reference. Price's relationship to Kijun defines near-term bias. A flat Kijun = strong equilibrium, a magnet.
3. **Senkou Span A (Leading Span A)** — `(Tenkan + Kijun) / 2`, plotted **26 periods forward**. The fast edge of the cloud.
4. **Senkou Span B (Leading Span B)** — 52-period midpoint, plotted **26 periods forward**. The slow edge of the cloud; the long-term equilibrium.
5. **Chikou Span (Lagging Span)** — current close plotted **26 periods back**. A momentum/confirmation read: if current price (seen 26 back) is above the price of 26 periods ago, momentum is bullish.

## The Kumo (Cloud)

The shaded region between Senkou Span A and B (projected forward). It is the heart of Ichimoku:
- **Color** — green (bullish) when Span A > Span B; red (bearish) when Span A < Span B.
- **Thickness** — the gap between A and B reflects the strength of the equilibrium divergence; a thick cloud = strong, well-separated equilibria = strong trend regime; a thin cloud = weak/indecisive.
- **Twist (Kumo flip)** — when A crosses B, the cloud flips color; a regime-change signal. A twist *after* a long trend is a reversal warning.
- **Forward support/resistance** — because the cloud is 26 periods ahead, the trader sees tomorrow's/next week's support/resistance today. Price returning to a future cloud often finds reaction there.

## Trend Determination (The At-a-Glance Read)

The canonical three-condition trend filter:
- **Strong bullish** — price *above* the cloud, cloud is *green*, Tenkan > Kijun.
- **Strong bearish** — price *below* the cloud, cloud is *red*, Tenkan < Kijun.
- **Neutral/uncertain** — price *inside* the cloud; no trade (the cloud is "noise").

This three-condition filter is Ichimoku's core edge: it keeps you out of chop (inside cloud) and aligns you only when all three confirm. Most losses come from trading inside or against the cloud.

## Key Signals & Setups

- **TK Cross (Tenkan/Kijun crossover)** — the primary entry signal. Tenkan crossing above Kijun = bullish; below = bearish. Strongest when in the direction of the cloud and price-cloud relationship. A TK cross *above* the cloud in a green cloud is high-confirmation long.
- **Price–Kijun relationship** — price holding above Kijun = bullish health; breaking below Kijun = momentum weakening. Kijun acts as dynamic support/resistance and trailing reference.
- **Cloud breakout** — price breaking *out of* the cloud (up or down) is a regime change; a cleaner, slower signal than the TK cross. Often used by trend-followers as the primary trigger.
- **Kumo twist** — the cloud flipping color; a medium-term reversal signal, especially after extended trends.
- **Chikou confirmation** — Chikou (lagging span) must be in open space (not blocked by prior price) for a clean trend. Chikou above prior price = bullish confirmation; below = bearish. A Chikou "free and clear" (no prior candles in its path) is a strong trend signal.
- **Kijun bounce** — in a trend, price pulling back to Kijun and bouncing is a continuation entry (Kijun as dynamic support).

## The Full Ichimoku Entry Checklist

A high-probability Ichimoku long requires *all* aligned:
1. Price above the cloud (regime).
2. Cloud is green (regime confirmation).
3. Tenkan above Kijun (momentum).
4. TK cross or Kijun-bounce (trigger).
5. Chikou above prior price, in open space (confirmation).
6. (Optional) Forward cloud green and rising (future support).

Fewer confirmations = lower probability; the system's discipline is demanding alignment, not catching every wiggle.

## Risk Management

- **Stop placement** — below the cloud (strong stop) or below Kijun (tighter). The cloud's bottom is the structural invalidation for a long. Wider clouds = wider stops; size accordingly.
- **Trailing with Kijun/Cloud** — Kijun as a trailing stop in trends; the cloud's far edge as a macro trail. Lets winners run with the trend.
- **Avoid the cloud interior** — the highest-conviction rule: don't initiate inside the cloud. Wait for breakout or clear TK cross with cloud alignment.
- **Timeframe hierarchy** — daily cloud overrides hourly; trade the LTF only in the direction of the HTF cloud.

## Common Pitfalls

- **Trading every TK cross** — TK crosses in chop (inside cloud) whipsaw; filter by cloud/price relationship.
- **Ignoring the cloud color/shape** — a TK cross above a thin, flattening red cloud is weak; the cloud context determines signal quality.
- **Forgetting the forward shift** — the cloud on the right edge of the chart is *future* support/resistance; treat it as projected, not historical.
- **Using default 9/26/52 blindly on all timeframes** — Hosoda tuned for the Japanese trading week (6 days × ~4.5 = 26). On 24/7 crypto or different sessions, parameters may need adjustment; test before trusting.
- **Over-complicating** — Ichimoku's strength is its self-sufficiency; bolting on 5 more indicators defeats the "at a glance" design.
- **Chikou misreading** — Chikou blocked by prior price (no open space) is a warning, not a signal; don't force trades against a blocked Chikou.

## Relationships to Other Methods

- **Moving Average Crossover** — Tenkan/Kijun are smoothed midpoints, conceptually MA-like; the TK cross is a crossover signal. See [Moving Average Crossover](moving-average-crossover). But Ichimoku uses midpoints, not closes, and adds the cloud/Chikou dimensions.
- **Trend Following** — Ichimoku is a trend-following system; cloud-breakout entries parallel Donchian breakout. See [Trend Following](trend-following).
- **Price Action** — Ichimoku is a rule-overlay on price; many PA traders use the cloud as a trend filter. See [Price Action Trading](price-action).
- **Heikin-Ashi** — fellow Japanese method; HA smooths price for trend clarity, complementary to Ichimoku's trend filter. See [Heikin-Ashi](heikin-ashi).
- **Smart Money Concepts** — the cloud as a regime filter complements SMC structural entries. See [Smart Money Concepts / ICT](smc-ict).
- **Dow Theory** — both are trend-definition frameworks; Ichimoku operationalizes trend with computed lines. See [Dow Theory](dow-theory).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| kumotrader/ichimoku-crypto | 60 | Sample Python code to plot Ichimoku for crypto | https://github.com/kumotrader/ichimoku-crypto |
| reuniware/CryptoForex-Trader-Framework | 31 | Automated market-analysis systems incl. Ichimoku | https://github.com/reuniware/CryptoForex-Trader-Framework |
| harryguiacorn/Ichimoku-Cloud-Signal-Python | 12 | Full-stack scanner for Ichimoku signals on indices | https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python |
| fearless-spider/IKH-Quant-Connect | 10 | Ichimoku strategy powered by QuantConnect (Python) | https://github.com/fearless-spider/IKH-Quant-Connect |
| thachp/ichimoku | 6 | Ichimoku Expert Advisor for MetaTrader 5 | https://github.com/thachp/ichimoku |
| viorell91/ichimoku-cloud | 4 | Generic tool for plotting Ichimoku clouds (mplfinance) | https://github.com/viorell91/ichimoku-cloud |
| EA31337/Strategy-Ichimoku | 0 | Strategy based on the Ichimoku Kinko Hyo indicator | https://github.com/EA31337/Strategy-Ichimoku |
| ZifuPath/backtest_ichimoku_cloud_statergy | 1 | Backtest OHLC data with Ichimoku Cloud strategy | https://github.com/ZifuPath/backtest_ichimoku_cloud_statergy |

## Books & Foundational Reading

- Goichi Hosoda — original Japanese works (rare in translation)
- Hidenobu Sasaki — *Ichimoku Kinko Hyo* (the disciple's definitive text; English translations exist)
- Nicole Elliott — *Ichimoku Charts* (Western accessible introduction)
- Ken Muranaka — *Ichimoku Kinko Hyo* (Commodity, 2000 — the article that introduced Ichimoku to many Western traders)
- Gareth Borcherds — Ichimoku training curriculum (modern Western practitioner)

## Further Study

- Backtest the full 5-condition checklist vs a cloud-breakout-only entry on a daily FX pair; measure the confirmation premium.
- Test parameter robustness: run default 9/26/52 vs session-adjusted parameters on crypto 24/7 data.
- Use the daily cloud as a regime filter for an LTF price-action or SMC entry strategy; quantify the filter's drawdown reduction.
