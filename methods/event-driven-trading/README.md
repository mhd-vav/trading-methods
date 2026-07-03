---
title: Event-driven Trading
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 3
importance: moderate
markets: equities, credit, options
timeframe: days–months (to event resolution)
github_repo: mhd-vav/trading-methods
branch: event-driven-trading
---

# Event-driven Trading

Event-driven trading takes positions around **specific corporate or macro events** — mergers & acquisitions (merger/risk arbitrage), earnings releases, spin-offs, restructurings, FDA approvals, index rebalances, and macro releases (CPI, FOMC, NFP). The thesis: events create discrete, identifiable price catalysts whose outcomes can be probabilistically assessed, and the market often misprices the outcome or the timing. Merger arbitrage is the canonical sub-strategy: after a deal is announced, the target trades at a discount to the offer price (the "deal spread"); the arb buys the target (and shorts the acquirer if stock-funded), earning the spread if the deal closes, losing if it breaks. Other event styles trade the earnings/revenue surprise drift or the binary outcome of regulatory/catalyst events via options.

## Mechanics

- **Merger/risk arbitrage** — post-announcement, target price < offer price (spread reflects break risk + time value + financing uncertainty). Buy target, short acquirer (if stock deal); profit = spread if deal closes, loss = (entry − pre-deal price) if it breaks. Annualized returns depend on deal velocity.
- **Earnings/announcement drift** — trade the post-earnings-announcement drift (PEAD): stocks underreact to earnings surprises, drifting for weeks; or trade the immediate reaction via options (straddle/strangle on implied-vol crush).
- **Catalyst/binary events** — FDA approvals, court rulings, regulatory decisions: use options to express asymmetric views on binary outcomes; IV typically elevated pre-event, crushes post.
- **Index rebalancing / supply** — trade the predictable demand from index adds/removes, share lockup expirations, secondary offerings.

## Uses & Cautions

Event-driven is the domain of specialized hedge funds (merger arb desks, catalyst funds). Its appeal: catalysts provide defined exit and timing, and the edge is in superior assessment of deal-break probability, regulatory outcome, or earnings quality. Risks: deal-break risk (the central merger-arb risk — a blocked deal can gap the target far below entry), deal-timing/financing risk, and binary-event outcomes are genuinely uncertain. Merger arb has a negatively-skewed return profile (many small wins, occasional large loss on a break). The style overlaps [Options Strategies](options-strategies) (binary events), [Sentiment & News Trading](sentiment-news-trading) (news catalysts), and [Global Macro](global-macro) (macro releases), and shares portfolio-mechanics with [Statistical Arbitrage](statistical-arbitrage) in its long-short construction.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| frankljbe/merger-arbitrage-system | 0 | Event-driven merger-arb system (LLM + Kafka) | https://github.com/frankljbe/merger-arbitrage-system |
| SiqiWang11/HK-Merger-Arbitrage-Analysis | 0 | HK M&A event-driven arb (CAR methodology) | https://github.com/SiqiWang11/HK-Merger-Arbitrage-Analysis |
| irudrakshgupta/Merger-Arbitrage-Tracker | 0 | Real-time merger-arb spread tracker | https://github.com/irudrakshgupta/Merger-Arbitrage-Tracker |
| QuantConnect/Lean | 20334 | Algorithmic engine for event-driven strategies | https://github.com/QuantConnect/Lean |

## Books & Foundational Reading

- Thomas Connolly — *Mergers, Acquisitions, and Restructuring* (deal mechanics for arb)
- Keith Moore — *Risk Arbitrage* (the merger-arb practitioner's text)
- Marti Subrahmanyam — research on PEAD and event-study methodology

## Relationships

Catalyst-driven kinship with [Sentiment & News Trading](sentiment-news-trading); binary events via [Options Strategies](options-strategies); macro-release variant under [Global Macro](global-macro); long-short mechanics shared with [Statistical Arbitrage](statistical-arbitrage); defined-exit logic contrasted with open-ended [Trend Following](trend-following).
