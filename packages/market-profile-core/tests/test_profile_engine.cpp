// tests/test_profile_engine.cpp
// Golden-fixture tests for the profile engine (A1-A10). The F1 symmetric case
// is verified against the exact numbers published in the formal spec.
#include "test_harness.hpp"

#include "mp/analytics/profile_engine.hpp"
#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"

using namespace mp;

// Build a ladder from (tick_index, weight) pairs with a tick size and reference.
static PriceLadder make_ladder(const std::vector<std::pair<int, unsigned>>& ticks,
                               std::int64_t tick_size, Price reference) {
    PriceLadder ladder;
    for (const auto& [tick, weight] : ticks) {
        const Price price = reference + static_cast<Price>(tick) * tick_size;
        ladder.add_tick(price, weight);
    }
    return ladder;
}

// F1: symmetric unimodal weights {1,3,5,3,1} at ticks {-2..+2}.
// Expected: total=13, POC=tick 0, mean=0, variance=1.0769230769,
// skew=0, excess kurtosis=-0.4795918367, VAH=+1, VAL=-1 (70% VA).
TEST_CASE("F1 symmetric profile matches golden values") {
    constexpr std::int64_t tick = 1;
    constexpr Price reference = 0;
    auto ladder = make_ladder({{-2, 1}, {-1, 3}, {0, 5}, {1, 3}, {2, 1}}, tick, reference);

    ProfileEngine engine;
    const auto result = engine.compute(ladder, reference, tick);

    CHECK(result.valid);
    CHECK(ladder.total_volume() == 13);
    CHECK(result.value_area.poc == reference);          // POC = tick 0
    CHECK(result.value_area.vah == reference + tick);   // VAH = tick +1
    CHECK(result.value_area.val == reference - tick);   // VAL = tick -1

    const auto& moments = result.moments;
    CHECK(moments.defined);
    CHECK_APPROX(moments.mean_tick, 0.0);
    CHECK_APPROX(moments.variance_tick2, 1.0769230769230769);
    CHECK_APPROX(moments.skewness, 0.0);
    CHECK_APPROX(moments.excess_kurtosis, -0.4795918367);
}

TEST_CASE("A4 POC is the mode, not the mean") {
    auto ladder = make_ladder({{0, 10}, {1, 50}, {2, 20}}, PRICE_SCALE, double_to_price(100.0));
    ProfileEngine engine;
    CHECK(engine.poc_index(ladder) == 1);
    const auto result = engine.compute(ladder, double_to_price(100.0), PRICE_SCALE);
    CHECK(result.value_area.poc == double_to_price(101.0));
}

TEST_CASE("A6 Value Area captures at least 70 percent of volume") {
    auto ladder = make_ladder({{0, 10}, {1, 20}, {2, 50}, {3, 20}, {4, 10}}, 1, 0);
    ProfileEngine engine;
    const auto result = engine.compute(ladder, 0, 1);
    const double captured = static_cast<double>(result.value_area.volume);
    const double total = static_cast<double>(ladder.total_volume());
    CHECK(captured >= 0.70 * total - 1e-6);
    CHECK(result.value_area.val <= result.value_area.poc);
    CHECK(result.value_area.vah >= result.value_area.poc);
}

TEST_CASE("A9 symmetric profile is D-shape") {
    auto ladder = make_ladder(
        {{0, 2}, {1, 4}, {2, 8}, {3, 4}, {4, 2}, {5, 4}, {6, 8}, {7, 4}, {8, 2}},
        1, 0);
    ProfileEngine engine;
    const auto result = engine.compute(ladder, 0, 1);
    CHECK(result.shape == ProfileShape::D_SHAPE);
}

TEST_CASE("A9 positive skew yields B-shape") {
    // Volume concentrated low, long tail up => positive skew.
    auto ladder = make_ladder(
        {{0, 50}, {1, 20}, {2, 8}, {3, 4}, {4, 2}, {5, 1}, {6, 1}}, 1, 0);
    ProfileEngine engine;
    const auto result = engine.compute(ladder, 0, 1);
    CHECK(result.moments.skewness > 0.5);
    CHECK(result.shape == ProfileShape::B_SHAPE);
}

TEST_CASE("A8 HVN/LVN detect local extrema") {
    // Bimodal: two peaks at ticks 2 and 8, valley at tick 5.
    auto ladder = make_ladder(
        {{0, 1}, {1, 4}, {2, 9}, {3, 4}, {4, 2}, {5, 1},
         {6, 2}, {7, 4}, {8, 9}, {9, 4}, {10, 1}}, 1, 0);
    ProfileEngine engine;
    std::vector<Price> hvn;
    std::vector<Price> lvn;
    engine.detect_nodes(ladder, hvn, lvn);
    CHECK(hvn.size() == 2);
    CHECK(lvn.size() == 1);
    CHECK(lvn[0] == 5);
}

TEST_CASE("Empty ladder yields safe defaults") {
    PriceLadder ladder;
    ProfileEngine engine;
    const auto result = engine.compute(ladder, 0, 1);
    CHECK(!result.valid);
    CHECK(result.shape == ProfileShape::UNDEFINED);
}

TEST_CASE("Translation invariance: shifting prices does not change moments") {
    constexpr std::int64_t tick = 1;
    auto base = make_ladder({{-2, 1}, {-1, 3}, {0, 5}, {1, 3}, {2, 1}}, tick, 0);
    auto shifted = make_ladder({{-2, 1}, {-1, 3}, {0, 5}, {1, 3}, {2, 1}}, tick, double_to_price(500.0));
    ProfileEngine engine;
    const auto a = engine.compute(base, 0, tick);
    const auto b = engine.compute(shifted, double_to_price(500.0), tick);
    CHECK_APPROX(a.moments.skewness, b.moments.skewness);
    CHECK_APPROX(a.moments.excess_kurtosis, b.moments.excess_kurtosis);
    CHECK_APPROX(a.moments.variance_tick2, b.moments.variance_tick2);
}

int main() {
    return ::test_harness::run_all();
}
