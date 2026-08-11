# Market Profile Engine (v2)

A C++20 Market Profile / Volume Profile trading engine built strictly on the
formal math specification `../Market_Profile/formal mathematical specification
A1-A10.md`. Pure, deterministic, replay-testable math core, ready for a Sierra
Chart data feed.

## Why this exists

The original files in `Trading_Project/` contain a correct math spec and good
architectural ideas (cache-aligned SoA ladder, lock-free SPSC, compile-time risk
policy, golden-fixture testing) but the C++ did not compile: filename/content
mismatches, missing `#include` extensions, `[[nodiscard]` typos, `lader`/`ladder`
mix-ups, and referenced-but-undefined symbols (`PositionSizer`, `Position`,
`price_to_double`). This `v2/` tree keeps the spec and architecture, rewrites
the code clean, and ships passing golden-fixture tests.

## Math core (per A1-A10)

- **A1** discrete tick domain; prices are fixed-point `int64_t` (×1e8).
- **A2** histogram construction over integer ticks; volume/trade/TPO weights.
- **A3** total weight, support, session range.
- **A4** POC = the MODE (argmax weight), deterministic lowest-index tie-break.
- **A5** weighted mean/variance/skewness/excess-kurtosis in TICK units (long
  double accumulation), translation-invariant.
- **A6** Value Area = contiguous coverage interval grown greedily from POC to
  the target fraction (default 70%). NOT a variance band.
- **A7** VAH/VAL = upper/lower bounds of that interval.
- **A8** HVN/LVN = smoothed local maxima/minima with a prominence filter.
- **A9** shape from skewness sign + bimodality coefficient (D/P/B/double).
- **A10** invariants enforced by tests (empty/translation/symmetry).

## Layout

```
v2/include/mp/
  foundation/        types.hpp (fixed-point Price), error.hpp (Result<T>)
  data_structures/   price_ladder.hpp (SoA, sorted, binary-search insert)
  analytics/         statistics.hpp, profile_engine.hpp
  risk/              risk_limits.hpp (drawdown/equity), position_sizer.hpp (Kelly)
  strategy/          signal_generator.hpp (mean-reversion at VA edges)
  observability/     metrics.hpp (lock-free latency histogram)
v2/src/main.cpp      demo driver
v2/tests/            golden-fixture suite (no external deps)
v2/Makefile          build / test / run
```

## Build

```
make        # build demo + tests
make test   # run the suite
make run    # run the demo
```

Requires g++ 13+ (C++20). No CMake, no external libraries.

## Test status

13 tests, all passing, including the F1 golden fixture verified to the spec's
exact numbers (variance 1.0769230769, excess kurtosis -0.4795918367). Builds
clean under `-Wall -Wextra -Wpedantic` and under ASan+UBSan.

## Next: backtest + Sierra Chart feed

The math core and signal generator are feed-agnostic. Next steps:
1. Sierra Chart data adapter: stream OHLC/tick prints into `PriceLadder`.
2. Backtest harness: feed historical sessions, replay signals, track P&L
   through `RiskLimits`/`PositionSizer`, and emit an equity curve + stats.
