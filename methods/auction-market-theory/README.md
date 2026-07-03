---
title: Auction Market Theory
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
inventor: J. Peter Steidlmayer
era: 1980s–present
markets: futures (most), equities, crypto
timeframe: intraday (session-based)
github_repo: mhd-vav/trading-methods
branch: auction-market-theory
---

# Auction Market Theory (AMT)

Auction Market Theory is the theoretical framework underlying [Market Profile](market-profile) and much of [Order Flow Trading](order-flow), developed by J. Peter Steidlmayer at the CBT. AMT models the market as a continuous two-way auction: price *advertises* opportunity up and down, *time* regulates (price that spends time at a level is accepted; price that passes through is rejected), and *volume* validates acceptance. The market seeks a balance where buyers and sellers transact; imbalance drives price to new levels until balance is found. AMT is less a signal-set than a *mental model* for reading where value is and how price is searching for it.

## The Three Variables

1. **Price advertises** — price probes up and down to attract buyers/sellers. Every price is an advertisement.
2. **Time regulates** — the time price spends at a level measures acceptance. Long time = accepted (fair value); brief touch = rejected (unfair).
3. **Volume validates** — high volume at a level confirms acceptance; low volume confirms rejection.

## Key Concepts

- **Value** — the price area where the most volume transacts over time (the value area). Price above value = overpriced (sell), below = underpriced (buy); price inside value = fair (no edge).
- **Balance/imbalance** — balanced markets range around value; imbalanced markets trend as price searches for new value.
- **Initiative vs responsive** — initiative moves break to new value (trend); responsive moves return toward value (mean-revert). Identifying which type of move is occurring frames every trade.
- **Day types** — normal day, trend day, double-distribution trend day, etc. — classifying the session's structure to anticipate how it develops.

AMT operationalizes via [Market Profile](market-profile) (the TPO/volume-profile visualization) and [Order Flow](order-flow) (the tick-level auction read). The trader's edge: identify where value is and whether price is accepting or rejecting relative to it.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| bfolkens/py-market-profile | 397 | Market Profile / Volume Profile in Python (AMT visualization) | https://github.com/bfolkens/py-market-profile |
| beinghorizontal/market_profile_github_repo | 1 | Nifty TPO Market Profile analyzer using AMT (RAG-powered) | https://github.com/beinghorizontal/market_profile_github_repo |

## Books & Foundational Reading

- J. Peter Steidlmayer & Steven Hawkins — *Markets and Market Logic* (the AMT origin)
- Jim Dalton — *Mind Over Markets* (the practitioner's AMT/Profile bible)
- Jim Dalton — *Markets in Profile*

## Relationships

Theoretical basis of [Market Profile / Volume Profile](market-profile) and [Order Flow Trading](order-flow); shares POC/value-area concepts with [Footprint Charts](footprint-charts) and [VWAP Trading](vwap-trading).
