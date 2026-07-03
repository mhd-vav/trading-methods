---
title: Wyckoff Method
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 1
importance: critical
inventor: Richard D. Wyckoff
era: 1900s–1930s
markets: stocks, futures, forex, crypto
timeframe: any (daily most classic)
github_repo: mhd-vav/trading-methods
branch: wyckoff-method
---

# Wyckoff Method

The Wyckoff Method is a price-and-volume analysis framework developed by Richard D. Wyckoff in the early 1900s. It treats the market as a story told by a "Composite Operator" (smart money) through the interaction of price bars and volume. The method identifies four recurring market phases — Accumulation, Markup, Distribution, and Markdown — and provides a structured vocabulary of *events* within each phase so a trader can locate where in the cycle an instrument sits and act on the highest-probability setups.

Its central insight is deceptively simple: **price and volume must always be read together, never in isolation.** Volume is the effort; the price spread is the result. When they agree, the trend is confirmed. When they diverge, a change is near.

## Core Philosophy — The Composite Operator

Wyckoff proposed that the market behaves as if a single large operator — the "Composite Operator" (CO) — were accumulating, marking up, distributing, and marking down a stock. The CO represents the aggregate of large interests (institutions, syndicates, smart money). The retail trader's job is to read the CO's footprints in price/volume and align with them, buying alongside accumulation and selling alongside distribution.

This is not literal: there is no single operator. But the *model* is powerful because institutional order flow does leave detectable signatures — absorption on declines, distribution on rallies, tested supply drying up. Wyckoff gives a vocabulary for those signatures.

## The Three Laws (Foundation)

Every Wyckoff analysis applies these three laws first. They are the first principles from which all event detection follows.

### 1. Law of Supply and Demand

Price rises when demand exceeds supply; falls when supply exceeds demand; moves sideways when they are in balance. **Volume reveals which force is dominant.** On rallies, strong volume = genuine demand; weak volume = lack of demand. On declines, strong volume = genuine supply; weak volume = lack of supply. The trader always checks whether volume confirms the direction of price.

### 2. Law of Cause and Effect

A horizontal trading range (the "cause") determines the magnitude of the subsequent trend (the "effect"). Long accumulation → large markup. Long distribution → deep markdown. The trader measures the *duration* and *width* of a trading range to estimate a price target. This is the basis of Wyckoff's point-and-figure counting technique: each horizontal column of Xs/Os in a point-and-figure chart represents a unit of "cause," and the count projects the "effect."

### 3. Law of Effort vs. Result

Volume is the effort; the price spread (range of the bar) is the result. They should agree. Divergences are warnings:
- **Heavy volume + small price spread** — effort produced little result. Supply is absorbing demand (or vice versa). Potential reversal.
- **Large price move + thin volume** — result without effort. Unsustainable, likely to be retraced.

Effort/Result divergence is the single most actionable of the three laws and is the conceptual ancestor of modern Volume Spread Analysis (VSA).

## The Four Market Phases

Every instrument cycles through these phases. The primary analytical task is to identify which phase the instrument is in and where within that phase it currently sits.

### Phase 1 — Accumulation

Smart money quietly buys after a prolonged decline. Price ranges sideways. Volume shows supply being absorbed: decreasing volume on dips, increasing volume on rallies. This is where the "cause" is built for the next advance. The range appears boring and directionless to the public, which is exactly the point — the CO wants to accumulate without pushing price up.

### Phase 2 — Markup

Demand clearly exceeds supply. Higher highs and higher lows. Pullbacks are shallow and on low volume. This is the trending phase — the "effect" of the accumulation cause. The public begins to notice and chase; late buyers fuel the move.

### Phase 3 — Distribution

Smart money sells to the public near the top. Price ranges sideways again. Volume shows supply entering: increasing volume on drops, decreasing volume on rallies. The CO unloads into the demand created by bullish news and euphoria. This builds the cause for the next decline.

### Phase 4 — Markdown

Supply overwhelms demand. Lower highs and lower lows. Rallies are weak and on low volume. The effect of the distribution cause. Panic eventually accelerates the decline into the next accumulation.

## The Accumulation Schematic — Events & Sub-Phases

This is the heart of practical Wyckoff trading. When a stock has been declining and begins to range, the trader looks for these events in sequence. The schematic below is the canonical model (Hutson/Pruden refinement of Wyckoff's originals).

### Phase A — Stopping the Downtrend

- **PS (Preliminary Support):** The first notable buying after a prolonged decline. Volume expands and the price spread widens, but the downtrend is not yet over. It signals that demand is beginning to appear.
- **SC (Selling Climax):** A wide-spread, high-volume plunge to a low. This is the climactic exhaustion of supply — panic selling meets expanding demand. It often marks the absolute low of the move. Volume is the highest of the decline.
- **AR (Automatic Rally):** A sharp bounce after the SC, driven by short covering and early demand. The top of this rally defines the **upper boundary (resistance)** of the emerging trading range.
- **ST (Secondary Test):** Price returns to the SC area on reduced volume and narrower spread. It confirms that selling pressure has diminished — supply is being absorbed.

### Phase B — Building the Cause

Institutions accumulate their full position. Price oscillates between support (SC area) and resistance (AR area) with multiple tests. Volume may spike on individual tests but the overall level is lower than Phase A. Phase B is where the "cause" is built — **its duration determines the magnitude of the subsequent markup.** This phase can take weeks to months. Traders mostly wait; premature entries here are punished by whipsaws.

### Phase C — The Spring (Highest-Probability Setup)

- **Spring / Shakeout:** Price briefly penetrates *below* the support of the trading range to trap remaining sellers (late bears and shaken-out longs) and test whether any supply remains.
  - A **low-volume Spring** is the single highest-probability Wyckoff buy signal. Thin volume below support means supply is exhausted — there is nothing left to sell. The CO has absorbed it all.
  - A **high-volume Spring** is more cautionary: it may indicate residual supply, requiring a stronger confirmation (an Upthrust-like test back through support) before entry.

The Spring is the moment of maximum public pessimism and maximum CO confidence. It is the classic "false breakdown."

### Phase D — Demand Dominates

- **SOS (Sign of Strength):** A rally on widening spread and increasing volume that pushes up through or toward resistance. Demand is now visibly in control.
- **LPS (Last Point of Support):** A shallow, low-volume pullback after a SOS. This is the *best entry for a trend trader* — a low-risk pullback buy after the spring has confirmed the phase. The LPS rests on higher support than the spring.
- **Backup / ST (backup to the edge of the creek):** A minor retest of the breakout area. Confirms the old resistance has become support.

### Phase E — Markup Begins

Price exits the trading range to the upside. The markup phase is underway. The CO's accumulation is complete and the instrument is now in a confirmed uptrend.

## The Distribution Schematic — Mirror Image

Distribution is the accumulation schematic inverted. The same logic applies with supply and demand reversed.

### Phase A — Stopping the Uptrend
- **PSY (Preliminary Supply):** First notable selling after a long advance. Volume expands, spread widens, but uptrend not over.
- **BC (Buying Climax):** Wide-spread, high-volume spike to a top. Demand exhausts; the CO begins distributing into the euphoria.
- **AR (Automatic Reaction):** Sharp drop after the BC. The bottom defines the **lower boundary (support)** of the range.
- **ST (Secondary Test):** Return to the BC area on reduced volume/spread. Confirms demand is fading.

### Phase B — Building the Cause
Institutions distribute. Multiple tests of resistance (BC) and support (AR). Duration sets the size of the coming markdown.

### Phase C — The Upthrust (UTAD)
- **UTAD (Upthrust After Distribution):** Price briefly penetrates *above* resistance to trap remaining buyers and test for residual demand. A **low-volume UTAD** is the highest-probability Wyckoff short signal — demand is exhausted. This is the mirror of the Spring.

### Phase D — Supply Dominates
- **SOW (Sign of Weakness):** A decline on widening spread and increasing volume through or toward support.
- **LPSY (Last Point of Supply):** A shallow, low-volume rally after a SOW — the best low-risk short entry.

### Phase E — Markdown Begins
Price exits the range downward. Markdown underway.

## The Five-Step Approach to a Trade

Wyckoff codified a disciplined five-step method for executing a trade from analysis to entry:

1. **Determine the present position and probable future trend of the market as a whole.** Use a broad index. Are we in accumulation, markup, distribution, or markdown? This sets the directional bias.
2. **Select stocks that move in harmony with the trend** and have the strongest relative strength (for longs) or weakness (for shorts). Relative strength vs. the index is key — Wyckoff was an early practitioner of RS ranking.
3. **Select stocks with a sufficient "cause"** (a large enough accumulation/distribution base) to justify a worthwhile move. Use point-and-figure counting to project a target.
4. **Determine the stock's readiness to move.** Is a Spring/UTAD forming? Is there an SOS/SOW? Wait for the phase-C test or phase-D confirmation before committing.
5. **Time the commitment** with a reversal in the stock that is confirmed by the broader market turning in the same direction. The market (tape) is the final arbiter.

## Entry, Stops, and Targets

- **Entry:** At the LPS (long) / LPSY (short) — the low-risk pullback after the spring/UTAD confirmation. Aggressive traders enter at the spring itself with a stop just below.
- **Stop-loss:** Just below the Spring low (long) or above the UTAD high (short). Because the spring defines the boundary of "supply is exhausted," a close back through it invalidates the thesis.
- **Target:** Projected from the point-and-figure count of the trading range (Cause & Effect), or measured from the range height added to the breakout.

## Reading Price & Volume — The Practical Skill

The events above are not stand-alone patterns; they are *confirmed by price/volume behavior*. Core reads:

- **Narrow spread up, high volume** at the top of a rally → supply meeting demand, potential distribution.
- **Wide spread down, low volume** → lack of demand, not necessarily strong supply.
- **Narrow spread down, low volume** at range support → supply drying up (potential spring setup).
- **Wide spread up, high volume** breaking resistance → genuine demand, SOS.
- **Long upper wick, high volume** after an advance → buying met aggressive selling (potential upthrust).

The discipline is to ask, after every bar: *Was the effort (volume) rewarded by the result (spread)? Whose side did this bar help — the accumulator or the distributor?*

## Common Pitfalls

- **Forcing a phase label on every range.** Not every consolidation is accumulation. Many are just pauses in a trend. Demand confirmation (a low-volume spring + SOS) before assuming accumulation.
- **Entering in Phase B.** Phase B whipsaws are brutal. Patience for Phase C/D is what separates profitable Wyckoff traders.
- **Ignoring the higher-timeframe context.** A "spring" on the 1-hour chart inside a daily markdown is noise, not a setup. Align phases across timeframes.
- **Treating the schematic as a template.** Real ranges are messy: springs can be marginal, UTADs absent, phases blend. The schematic is a model, not a checklist to force-fit.
- **Overlooking volume.** A spring without a volume read is just a breakdown. The low-volume confirmation is what makes it a Wyckoff event.

## Relationship to Other Methods

- **VSA (Volume Spread Analysis):** Tom Williams, a Wyckoff-era syndicate trader, distilled Wyckoff's effort-vs-result law into a focused bar-by-bar volume method. VSA is essentially modernized, simplified Wyckoff. See [Volume Spread Analysis (VSA)](volume-spread-analysis).
- **SMC / ICT:** Smart Money Concepts (order blocks, liquidity sweeps) are a contemporary reframing of Wyckoff's absorption/accumulation ideas using different vocabulary (liquidity, order blocks, BOS/CHoCH). The Spring ≈ a liquidity sweep. See [Smart Money Concepts / ICT](smc-ict).
- **Market Profile / Volume Profile:** Complementary — shows *where* volume traded within the range, helping locate the CO's accumulation zone (high-volume nodes). See [Market Profile / Volume Profile](market-profile).
- **Supply & Demand Zones:** A simplified descendant of Wyckoff accumulation/distribution ranges, focused on the residual order clusters. See [Supply & Demand Trading](supply-demand).

## Why It Endures

Wyckoff predates nearly every modern indicator, yet remains one of the most respected technical frameworks a century later. The reason: it is grounded in the mechanics of how markets actually clear — large interests must accumulate and distribute *through* the public, and that process leaves volume/price signatures that no oscillator can fully synthesize. Learning to read effort vs. result teaches a trader to think in terms of order flow and absorption, which generalizes to any market and any timeframe.

## Open-Source References

- **jq88kazze/wyckoff-method-agent** — complete agent-implementation guide: theory, detection logic, pseudocode, and Python source for phase detection, S/R, volume profile. The canonical open reference for coding Wyckoff. https://github.com/jq88kazze/wyckoff-method-agent
- **YoungCan-Wang/WyckoffTradingAgent** (★530) — open-source Wyckoff trading agent and AI stock screener for volume-price analysis; CLI, web app, MCP tools, multi-market. https://github.com/YoungCan-Wang/WyckoffTradingAgent
- **srlcarlg/srl-ctrader-indicators** & **srl-python-indicators** — Weis & Wyckoff system, order flow ticks, Volume/TPO Profile for cTrader and Python. https://github.com/srlcarlg/srl-python-indicators
- **ozymandias0123/Wyckoff-Trading-Method-** — complete Wyckoff implementation as an MT5 automated bot. https://github.com/ozymandias0123/Wyckoff-Trading-Method-
- **lawrencezcl/DAX-Trading-System** — DAX system combining Wyckoff, Market Profile, and options/futures analysis. https://github.com/lawrencezcl/DAX-Trading-System

## Further Study

- *The Richard D. Wyckoff Method of Trading and Investing* — original course material.
- *Three Skills for Top Trading* (Hank Pruden) — the modern standard text refining the schematics.
- StockCharts ChartSchool: "Wyckoff" articles — accessible phase/event reference.
- The Wyckoff Analytics educational site (historical source of the schematics in widespread use).

