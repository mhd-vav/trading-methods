---
title: Sentiment & News Trading
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 3
importance: moderate
markets: equities, crypto, FX
timeframe: minutes–days (news); days–weeks (sentiment)
github_repo: mhd-vav/trading-methods
branch: sentiment-news-trading
---

# Sentiment & News Trading

Sentiment & news trading generates signals from textual data — news articles, earnings releases, social media, and structured sentiment indices — rather than price/volume. The modern form applies NLP/LLMs to classify news tone (positive/negative/neutral), extract events (M&A, FDA approvals, earnings beats), and aggregate sentiment into tradeable signals. Classic sentiment proxies include the VIX (fear gauge), put/call ratios, AAII retail sentiment surveys, and CFTC commitment-of-traders positioning; modern crypto sentiment draws on X/Twitter, Reddit fear-greed indices, and on-chain flows. The thesis: sentiment extremes and news catalysts precede or accelerate price moves, and NLP can extract that signal faster/more comprehensively than a human reader.

## Mechanics

- **News NLP** — FinBERT / LLMs classify headline tone; event extraction tags catalysts; signals fed into a factor model or direct trigger. The edge is speed and breadth (read thousands of items/sec).
- **Sentiment aggregation** — rolling sentiment scores per ticker/asset; trade extremes (contrarian: fade euphoria/buy panic) or momentum (trade the direction of shifting sentiment).
- **Sentiment proxies** — VIX, put/call ratio, AAII survey, funding rates (crypto), CoT positioning. These are lagging crowd-positioning gauges, often used contrarianly.
- **Event-driven news** — machine-readable economic releases (NFP, CPI, FOMC) traded in milliseconds by [HFT](high-frequency-trading); earnings/revenue surprises traded over hours-days.

## Uses & Cautions

Sentiment/news is a rising area thanks to LLMs, but the signal is noisy, non-stationary (sentiment-word drift, media bias), and often already priced by the time retail sees it. The durable edges: (1) speed on machine-readable news ([HFT](high-frequency-trading)), (2) breadth (NLP scans thousands of sources a human cannot), (3) contrarian extremes (crowd sentiment is a known mean-reverting signal). Pitfalls: overfitting NLP models to historical sentiment, ignoring that markets react to the *surprise* vs expectations not the absolute news, and survivorship/selection bias in news corpora. Sentiment blends with [Event-driven Trading](event-driven-trading) (catalysts), [Global Macro](global-macro) (policy/news), [Contrarian](contrarian) (extremes), and increasingly [ML/AI Trading](ml-ai-trading).

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| silvernine209/nlp_bitcoin_trading | 16 | NLP topic modeling + sentiment for BTC features | https://github.com/silvernine209/nlp_bitcoin_trading |
| rohinishimpatwar/The-NLP-News-Sentiment-Trading-Strategy | 12 | NLP news-sentiment factor strategy for S&P 500 | https://github.com/rohinishimpatwar/The-NLP-News-Sentiment-Trading-Strategy |
| Abood991B/insightbull | 5 | Stock sentiment platform: real-time news + FinBERT | https://github.com/Abood991B/insightbull |
| galactic-me/Stock-Sentiment-Analysis | 4 | News sentiment shaping investor behavior | https://github.com/galactic-me/Stock-Sentiment-Analysis |

## Books & Foundational Reading

- Sanjiv Das & Mike Chen — *Yahoo! for Amazon: Sentiment Extraction using Small Training Sets* (early finance-NLP)
- Lo, Mamaysky & Wang — foundational textual-sentiment alpha research
- Pete L. Brandt — *Diary of a Professional Commodity Trader* (discretionary news/sentiment)
- benchmark: FinBERT (ProsusAI) — finance-tuned BERT for sentiment

## Relationships

Overlaps [Event-driven Trading](event-driven-trading) and [Global Macro](global-macro); contrarian extremes link to [Contrarian](contrarian); speed variant is [HFT](high-frequency-trading); modern NLP implementation is [ML/AI Trading](ml-ai-trading); positioning proxies complement [On-chain Analysis](on-chain-analysis) in crypto.
