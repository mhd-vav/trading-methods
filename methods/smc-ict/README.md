---
title: Smart Money Concepts (SMC) / ICT
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 1
importance: critical
originator: Michael J. Huddleston (The Inner Circle Trader, ICT)
era: 2000s–present
markets: forex, indices, crypto, metals, stocks
timeframe: any (HTF bias + LTF execution)
github_repo: mhd-vav/trading-methods
branch: smc-ict
---

# Smart Money Concepts (SMC) / ICT

Smart Money Concepts (SMC) is a contemporary technical framework popularized by Michael J. Huddleston, known as "The Inner Circle Trader" (ICT). It reframes price action around the premise that markets are engineered by institutional "smart money" — algorithms and large interests that seek **liquidity** (clusters of resting stop-losses and pending orders) and leave **imbalances** in their wake. SMC provides a vocabulary — Order Blocks, Fair Value Gaps, Break of Structure, Change of Character, Liquidity Sweeps — to read where smart money has acted and to trade in alignment with it.

Though the terminology is modern, the underlying mechanics are deeply connected to [Wyckoff](wyckoff-method): the Spring ≈ a liquidity sweep, accumulation/distribution ≈ order-block engineering. SMC's distinctive contribution is its emphasis on *time and session structure* (killzones, opening range, time-based pivots) and a precise micro-structure vocabulary.

## Core Philosophy — Liquidity & Imbalance

Two ideas run through all of SMC:

1. **Liquidity is the target.** Retail traders cluster stop-losses above old highs and below old lows (equal highs/lows, trendline taps, round numbers, session opens). Smart money drives price into these zones to fill its large orders — taking the other side of the triggered stops — then reverses. A move that looks like a "breakout" to retail is often a **liquidity sweep** by smart money.
2. **Imbalance reveals intent.** When smart money acts with urgency, it leaves **Fair Value Gaps** (price regions where buyers/sellers failed to find a counterpart — a 3-candle imbalance). Price tends to return to rebalance these gaps (mitigation), and the candle preceding an imbalance is the **Order Block** — the institutional origin of the move.

The SMC trader's job: identify the HTF (higher-timeframe) bias, wait for liquidity to be swept, confirm a structural shift (CHoCH) on a lower timeframe, and enter at an Order Block or FVG in the direction of the HTF bias.

## Key Concepts & Vocabulary

### Market Structure — BOS and CHoCH

Market structure is the backbone. Price makes **higher highs / higher lows** (uptrend) or **lower highs / lower lows** (downtrend). Structure breaks are classified:

- **BOS (Break of Structure):** a continuation signal. Price breaks a prior swing high (in an uptrend) or low (in a downtrend), confirming the trend continues. The break is judged by close or by wick depending on ruleset.
- **CHoCH (Change of Character):** a reversal signal. Price breaks the *last* counter-trend swing — e.g., breaks a lower high *before* making a new low — indicating the character of the move has shifted. CHoCH is the SMC equivalent of a Wyckoff effort-vs-result reversal warning: the first sign smart money has changed posture.

Detection (from the `smartmoneyconcepts` package): a swing high is a high that is the highest of N candles before and after; a swing low symmetrically. BOS/CHoCH fire when price closes (or wicks, per setting) beyond the most recent relevant swing.

### Order Blocks (OB)

An **Order Block** is the last opposing candle before a strong, impulsive directional move. In a bullish impulse, the last down-candle before the rally is the bullish OB; in a bearish impulse, the last up-candle is the bearish OB. The assumption: this candle is where institutional buy/sell orders were filled before the impulsive move, leaving residual unfilled interest that price tends to revisit (mitigate).

Properties tracked in code:
- **Top/Bottom** — the OB's price range.
- **OBVolume** — volume of the OB candle plus prior two (a measure of its institutional weight).
- **Percentage (strength)** — `min(highVol,lowVol)/max(highVol,lowVol)`; closer to 1.0 = more balanced/stronger.
- **Mitigation** — when price returns to the OB; the OB is then "used up."

Traders enter on the OB after a higher-timeframe bias is confirmed: price pulls back into a bullish OB and shows rejection.

### Fair Value Gaps (FVG)

A **Fair Value Gap** is a 3-candle imbalance:
- **Bullish FVG:** candle[i-1].high < candle[i+1].low — the middle candle's rally left a gap no seller filled.
- **Bearish FVG:** candle[i-1].low > candle[i+1].high.

FVGs represent inefficiency — price moved too fast for two-sided trade. The market tends to **mitigate** (return to) FVGs to restore efficiency, making them high-probability reaction zones and entry areas. Consecutive FVGs may be merged (highest top, lowest bottom) into a single zone.

FVGs and Order Blocks usually coincide: the OB candle sits at the origin of the move that created the FVG. A reaction zone where an OB *and* an FVG align is considered a high-quality SMC entry.

### Liquidity

**Liquidity** in SMC = resting orders (stops and pending entries). It pools at predictable locations:
- **Equal highs / equal lows (EQH/EQL):** multiple highs/lows within a small range (`range_percent`). These are magnets — a pool of buy-stops above equal highs, sell-stops below equal lows.
- **Trendline liquidity:** stops resting beyond a trendline touch.
- **Session liquidity:** above/below the Asian session range, the London open, the previous day's high/low.
- **Round numbers / psychological levels.**

Smart money sweeps these pools: price spikes beyond the liquidity, triggers stops (its fuel), then reverses. The sweep + reversal is the SMC entry trigger. Identifying *where* liquidity rests *before* the move is the core planning skill.

### Liquidity Sweep (Judas Swing)

A **liquidity sweep** (ICT's "Judas Swing") is the false move that grabs liquidity before the true move. Typical pattern: price breaks an obvious level (equal highs, session high), triggers breakout traders and stop-losses, then sharply reverses in the opposite direction. The sweep often occurs early in a session (e.g., the London open fake-out) to engineer liquidity for the later session direction.

### Premium and Discount (PD Arrays)

SMC divides any range into **Premium** (upper half — expensive, sell zone) and **Discount** (lower half — cheap, buy zone) relative to a dealing range (swing high to swing low). Longs are sought in discount; shorts in premium. This enforces buying low / selling high relative to the current dealing range rather than chasing. Specific entry arrays ("PD Arrays") include OBs, FVGs, and liquidity voids located in the correct half.

### Imbalance / Liquidity Void

A **liquidity void** is a one-directional move with little two-way trade (a large FVG or a series of consecutive imbalance candles). Price tends to either continue through voids or snap back to fill them. They mark zones where smart money moved price urgently.

## Time & Session Structure (ICT)

ICT's distinctive layer is **time-based** structure — the idea that smart money operates on a schedule:

- **Killzones:** high-probability time windows — the **London Killzone** (~02:00–05:00 EST) and the **New York Killzone** (~07:00–10:00 EST). ICT teaches that the day's expansion move often initiates in or just after these windows.
- **Opening Range / Initial Balance:** the first hour's range often defines the day's framework; liquidity beyond it is a sweep target.
- **Power of 3 (AMD):** Accumulation, Manipulation, Distribution. The session tends to (1) range/build liquidity, (2) sweep it (Judas swing), then (3) run the true direction. Recognizing the manipulation leg is key — enter during/after it for the distribution leg.
- **Time-based pivots:** specific times (e.g., 09:50, 10:10, 13:30–14:00 EST) where reversals cluster.
- **Daily/weekly profiles:** the previous day's high/low and the weekly open are recurring liquidity pools.

## The SMC Entry Model (HTF → LTF)

A disciplined SMC trade is a multi-timeframe alignment:

1. **HTF Bias (4H/Daily):** Determine the prevailing trend and the next likely liquidity pool (e.g., an unfilled FVG or equal lows below price in an uptrend).
2. **Mark Liquidity:** Identify where stops rest relative to HTF structure (buy-side above equal highs, sell-side below equal lows).
3. **Wait for the Sweep:** Price takes the liquidity (e.g., sweeps equal lows in an uptrend). This is the manipulation leg.
4. **LTF Confirmation (5m/15m):** After the sweep, watch for a **CHoCH** on the LTF — the first structural break signaling reversal back into the HTF bias direction.
5. **Entry at OB/FVG:** Drawdown into a fresh LTF Order Block or Fair Value Gap in the HTF-bias direction, in the discount (for longs) or premium (for shorts). Enter on confirmation (engulfing, change of character).
6. **Targets:** the opposing liquidity pool (e.g., the buy-side liquidity above equal highs for a long) and/or an unfilled HTF FVG.

This is conceptually "buy the spring, confirmed by structure, at the institutional level" — the Wyckoff lineage made operational.

## Common Setups

- **FVG entry after sweep:** HTF uptrend → LTF sweeps sell-side liquidity → CHoCH up → price pulls into a bullish FVG → enter long, target buy-side liquidity above.
- **Order Block reversal:** Price sweeps a major HTF high (buy-side liquidity) and prints a bearish CHoCH → drawdown into the bearish OB → short toward discount-side liquidity.
- **Silver Bullet / Power of 3:** ICT-named setups in specific killzone windows exploiting the AMD session sequence.

## Risk Management

- **Stop placement:** beyond the sweep extreme (the low of a bullish sweep / high of a bearish sweep). If price closes beyond the OB it invalidated the thesis.
- **R:R:** SMC trades target opposing liquidity, often 3R+ because the target is a structural pool, not an arbitrary level.
- **Position sizing:** standard fixed-fractional; HTF bias trades carry higher conviction than LTF-only plays.
- **Time invalidation:** if the expected expansion does not develop within the killzone/session window, ICT traders often cut — time is part of the thesis.

## Common Pitfalls

- **Labeling everything an Order Block.** Not every opposing candle is institutional. The OB must precede a *strong, imbalanced* move (an FVG-creating displacement). Weak moves don't produce valid OBs.
- **Ignoring HTF bias.** Taking LTF CHoCH signals against the HTF trend is the most common SMC loss pattern. Bias first, micro-structure second.
- **Chasing sweeps without confirmation.** A sweep alone is not an entry — it needs the LTF CHoCH to confirm the reversal. Entering on the sweep anticipates rather than reacts.
- **Over-fitting killzones.** Time windows are statistical tendencies, not guarantees. They raise probability, they don't replace structure.
- **Confusing BOS with CHoCH.** BOS = continuation, CHoCH = reversal. Mislabeling leads to trading reversals as continuations.
- **Treating SMC as a system with a backtestable edge in isolation.** SMC is a *reading framework*; its edge depends on the trader's discretion in selecting HTF bias and valid levels. Pure mechanical SMC bots tend to degrade.

## Relationship to Other Methods

- **Wyckoff:** Direct lineage. SMC's liquidity sweep ≈ Wyckoff Spring/UTAD; OB accumulation ≈ Wyckoff absorption; CHoCH ≈ effort-vs-result reversal signal. SMC is, in large part, Wyckoff re-lexiconed with a time/session layer. See [Wyckoff Method](wyckoff-method).
- **Price Action:** SMC is a specialized price-action dialect. General price-action traders use the same swings, breakouts, and rejections without the "smart money" ontology. See [Price Action Trading](price-action).
- **Supply & Demand:** Zones are a simplified SMC/Wyckoff hybrid. See [Supply & Demand Trading](supply-demand).
- **Order Flow / Footprint:** SMC infers institutional action from price; order-flow tools observe it directly via the book and prints. Complementary. See [Footprint Charts](footprint-charts) and [Tape Reading / Order Book](tape-reading).

## Why It's Influential

SMC spread explosively in the 2020s because it gave retail traders a coherent narrative for *why* obvious levels fail (liquidity sweeps) and a precise micro-structure vocabulary for entries (OB, FVG, CHoCH). Whether one accepts the "smart money engineers the market" ontology literally or as a useful model, the concepts map onto real market-microstructure phenomena: stop-cluster runs, imbalance-driven rebalancing, and session-driven flow. Its practical value is the disciplined HTF→LTF routine and the focus on liquidity as the driver of movement.

## Open-Source References

- **joshyattridge/smart-money-concepts** (★1825) — the canonical Python package implementing ICT/SMC: FVG, Order Blocks, BOS/CHoCH, Liquidity, Swing Highs/Lows. `pip install smartmoneyconcepts`. The de facto programmatic reference for SMC concepts. https://github.com/joshyattridge/smart-money-concepts
- **MobiusQuant/OpenMobius-skill** (★415) — ICT/SMC trading-knowledge skill for AI coding agents (Claude Code / Codex / OpenClaw / Hermes). A packaged knowledge base of SMC concepts. https://github.com/MobiusQuant/OpenMobius-skill
- **KVignesh122/MT5-SMC-trading-bot** (★62) — MQL5 SMC bot trading Order Blocks, FVGs, BOS with adaptive ATR/session/regime filters and equity risk controls. https://github.com/KVignesh122/MT5-SMC-trading-bot
- **manuelinfosec/profittown-sniper-smc** (★60) — ICT Smart Money Concept Sniper Bot. https://github.com/manuelinfosec/profittown-sniper-smc
- **GifariKemal/xaubot-ai** (★52) — AI-powered XAUUSD bot with XGBoost ML + SMC + HMM regime detection. https://github.com/GifariKemal/xaubot-ai
- **haza79/MT5-Smart-Money-Concept-Indicator** (★42) — MT5 SMC + price-action indicator. https://github.com/haza79/MT5-Smart-Money-Concept-Indicator
- **samiath17/smc-tradingview-indicator** (★28) — Pine Script v5 SMC pack automating institutional concepts in TradingView. https://github.com/samiath17/smc-tradingview-indicator
- **carlosrod723/MQL5-Trading-Bot** (★72) — fractal-based liquidity sweeps + Fibonacci zones + order blocks. https://github.com/carlosrod723/MQL5-Trading-Bot
- **bigmacman1129/crypto-ai-trading-bot** (★121) — crypto liquidity detection & order-book analysis bot (SMC-adjacent microstructure). https://github.com/bigmacman1129/crypto-ai-trading-bot

## Further Study

- ICT's YouTube series — the original source of the terminology (voluminous; the killzone/AMD/time concepts originate here).
- *Smart Money Concepts* community documentation and the `smartmoneyconcepts` package README — the cleanest written reference for the core definitions.
- Compare with Wyckoff (Hank Pruden, *Three Skills for Top Trading*) to see the conceptual lineage.

