---
title: Point & Figure
type: method
domain: trading
category: Discretionary Technical / Chart-Based
tier: 3
importance: moderate
era: 1890s (Charles Dow era); refined by DeVilliers, Cohen, Blumenthal
markets: stocks, futures, FX
timeframe: price-based (time-independent)
github_repo: mhd-vav/trading-methods
branch: point-and-figure
---

# Point & Figure (P&F)

Point & Figure is the oldest price-based charting method, predating candlesticks in the West. It plots columns of Xs (rising prices) and Os (falling prices), printing only when price moves a defined *box size*, and reversing the column only on a multi-box counter-move (the *reversal amount*). Like [Renko](renko-trading), it discards time and noise, but P&F adds structured support/resistance and a unique **horizontal counting** technique for price targets. It is the charting method most directly tied to [Wyckoff's](wyckoff-method) "cause and effect" — the horizontal width of a P&F base *is* the cause that projects the effect.

## Mechanics

- **Box size** — the minimum price move to print a symbol (fixed or ATR-based).
- **Reversal amount** — typically 3 boxes: a column reverses only on a 3× box-size move against it.
- Columns of Xs (uptrend) and Os (downtrend); no time axis. Only meaningful moves print.

## Reading P&F

- **Support/resistance** — horizontal levels where columns repeatedly reverse are clean S/R (no noise to obscure them).
- **Breakouts** — a new X above a prior X-column's high (double-top break) or new O below a prior low (double-bottom break) are high-conviction signals; P&F breakouts are famous for reliability because they require sustained movement.
- **Targets (horizontal count)** — count the number of boxes in the widest row of a base; multiply by box size × reversal; project from the breakout. This is the P&F "cause→effect" projection, shared conceptually with Wyckoff point-and-figure counting.
- **Bullish/bearish patterns** — double-top/bottom, triple-top/bottom, bullish-catapul/bearish-catapult, poles.

## Uses

P&F shines for objective trend/S/R analysis and target projection, and for filtering noise on instruments where time-based charts whipsaw. Its weakness: parameter sensitivity (box/reversal choice) and the loss of timing/volume info. Used by [Wyckoff](wyckoff-method) practitioners for cause-counting and by systematic [Breakout Trading](breakout-trading) for clean signals.

## Open-Source References

| Source | Stars | Description | URL |
|---|---|---|---|
| dannasman/point_and_figure | 11 | Python script for creating P&F charts | https://github.com/dannasman/point_and_figure |
| EarnForex/Point-and-Figure | 7 | P&F indicator to plot charts in MetaTrader | https://github.com/EarnForex/Point-and-Figure |
| cjknox/PyPnF | 7 | Point and Figure charting in Python | https://github.com/cjknox/PyPnF |

## Books & Foundational Reading

- Thomas Dorsey — *Point and Figure Charting* (the modern standard)
- Victor DeVilliers — *The Point and Figure Method of Anticipating Stock Price Movements* (1933, original)
- A.W. Cohen — *How to Use the Three-Point Reversal Method of Point and Figure Stock Market Trading*

## Relationships

Cause-counting tool of [Wyckoff Method](wyckoff-method); price-based cousin of [Renko Trading](renko-trading); S/R & breakout method for [Breakout Trading](breakout-trading), [Chart Patterns](chart-patterns).
