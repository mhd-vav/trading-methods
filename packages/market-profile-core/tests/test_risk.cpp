// tests/test_risk.cpp
#include "test_harness.hpp"

#include "mp/risk/position_sizer.hpp"
#include "mp/risk/risk_limits.hpp"
#include "mp/foundation/types.hpp"

using namespace mp;

TEST_CASE("Kelly fraction is zero for negative edge") {
    CHECK(PositionSizer::kelly_fraction(0.4, 1.0) == 0.0);
}

TEST_CASE("Kelly fraction positive for real edge, capped at quarter-Kelly") {
    // f* = (0.6*3 - 1)/2 = 0.4; quarter-Kelly cap = 0.25 -> 0.25
    CHECK(PositionSizer::kelly_fraction(0.6, 2.0) == 0.25);
}

TEST_CASE("Position size respects fixed-fractional risk") {
    PositionSizer::SizingInput input;
    input.equity = 100'000.0;
    input.entry_price = double_to_price(100.0);
    input.stop_loss = double_to_price(98.0); // $2 risk per unit
    input.win_probability = 0.55;
    input.reward_risk_ratio = 2.0;
    const auto out = PositionSizer::compute_size(input);
    CHECK(out.error == ErrorCode::SUCCESS);
    CHECK(out.quantity > 0);
    // 2% of 100k = $2000 / $2 = 1000 units (before Kelly cap)
    CHECK(out.quantity <= 1000);
}

TEST_CASE("Drawdown limit halts trading") {
    RiskLimits risk(100'000.0);
    CHECK(risk.check_can_trade() == ErrorCode::SUCCESS);
    risk.record_trade_result(-16'000.0); // 16% drawdown exceeds 15% cap
    CHECK(risk.is_halted());
    CHECK(risk.check_can_trade() == ErrorCode::RISK_LIMIT_EXCEEDED);
}

TEST_CASE("Zero risk-per-unit rejected") {
    PositionSizer::SizingInput input;
    input.equity = 100'000.0;
    input.entry_price = double_to_price(100.0);
    input.stop_loss = double_to_price(100.0); // no distance
    input.win_probability = 0.55;
    input.reward_risk_ratio = 2.0;
    const auto out = PositionSizer::compute_size(input);
    CHECK(out.error != ErrorCode::SUCCESS);
   CHECK(out.error == ErrorCode::INVALID_PRICE);
}

int main() {
    return ::test_harness::run_all();
}
