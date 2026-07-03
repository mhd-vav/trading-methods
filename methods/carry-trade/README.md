---
title: Carry Trade
type: method
domain: trading
category: Macro & Fundamental Methods
tier: 3
importance: moderate
markets: FX (G10, EM), commodities (roll yield), rates
timeframe: weeks–months
github_repo: mhd-vav/trading-methods
branch: carry-trade
---

# Carry Trade

The carry trade borrows (or shorts) a low-yield/low-cost asset to buy a high-yield/high-carry asset, profiting from the **interest-rate / yield differential** ("carry") as long as the exchange rate (or price) doesn't move against the position. The classic FX carry trade: borrow in a low-rate funding currency (JPY, CHF), invest in a high-rate target (AUD, NZD, EM currencies), collecting the rate differential daily. The strategy is profitable in calm, risk-on regimes (carry is "paid for risk") but suffers sharp crashes when funding currencies spike (the "carry unwind") — a positively-skewed-fee / negatively-skewed-crash profile. The carry concept generalizes beyond FX: commodity roll yield (backwardation carry, see [Term-structure Trading](term-structure-trading)), bond yield-curve carry, and crypto funding-rate carry ([Funding-rate Arbitrage](funding-rate-arbitrage)).

## Mechanics

- **FX carry** — long high-rate currency / short low-rate currency; daily rollover (swap) credits the interest differential. Carry = funding-rate differential; profit = carry + spot change.
- **Volatility weighting** — modern carry portfolios vol-weight each pair so a wild EM currency doesn't dominate; diversification across many carry pairs smooths returns.
- **Commodity/rates carry** — backwardated commodity futures (positive roll yield), steepener bond positions (curve carry), and the crypto spot-perp funding carry are all "carry" expressions.
- **Signal** — rank currencies/assets by yield; long the top, short the bottom (a cross-sectional carry factor, parallel to [Cross-sectional Momentum](cross-sectional-momentum)).

## Uses & Cautions

Carry is one of the most documented FX factors — historically positive long-run returns, but with fat-tailed crash risk. The 1998 JPY spike, 2008 crisis, and 2022 EM stress all produced sharp carry-unwind losses. The structural lesson: carry is compensation for crash risk (it "picks up pennies in front of a steamroller," like short [Volatility Arbitrage](volatility-arbitrage)). Risk management centers on vol targeting, stop-loss/tail hedging, and regime awareness (carry works in risk-on, fails in risk-off). Carry blends with [Global Macro](global-macro) (policy-differential view), overlaps [Term-structure Trading](term-structure-trading) (roll-yield carry) and [Funding-rate Arbitrage](funding-rate-arbitrage) (crypto carry), and is a sibling factor to [Cross-sectional Momentum](cross-sectional-momentum) in factor-investing portfolios.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| spantaleoni/CarryTradeStrategy | 3 | FX carry-trade strategy | https://github.com/spantaleoni/CarryTradeStrategy |
| KutayMendi/FX-Carry | 0 | FX carry-trade strategy on a currency pair | https://github.com/KutayMendi/FX-Carry |
| kushagrapandey2852/FX-Carry-Trade-Currency-Risk-Model | 0 | G10 FX carry platform w/ IR differentials | https://github.com/kushagrapandey2852/FX-Carry-Trade-Currency-Risk-Model |
| NavyBlueCheese/carry-trade-monitor | 1 | React app to monitor G10 carry trades | https://github.com/NavyBlueCheese/carry-trade-monitor |

## Books & Foundational Reading

- Craig Burnside — *Carry Trade Strategies* (academic survey of the carry factor)
- Jessica James — *FX Option Performance* (carry & vol risk premia)
- Ralph Koijen et al. — *Carry* (generalized carry across asset classes, Fama-Miller working paper)

## Relationships

Factor-investing sibling of [Cross-sectional Momentum](cross-sectional-momentum); commodity-roll variant is [Term-structure Trading](term-structure-trading); crypto variant is [Funding-rate Arbitrage](funding-rate-arbitrage); crash-risk kinship with short [Volatility Arbitrage](volatility-arbitrage); policy-differential view under [Global Macro](global-macro); long-short mechanics shared with [Statistical Arbitrage](statistical-arbitrage).
