// src/main.cpp
// Demo driver: build a sample session profile, compute the market profile,
// print POC / Value Area / shape / nodes, and emit a signal for a probe price.
// Feed wiring (Sierra Chart) lands in a later step; this proves the math core.
#include "mp/analytics/profile_engine.hpp"
#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"
#include "mp/strategy/signal_generator.hpp"
#include <cstdio>

using namespace mp;

static const char* shape_name(ProfileShape shape) {
    switch (shape) {
        case ProfileShape::D_SHAPE: return "D (balanced)";
        case ProfileShape::P_SHAPE: return "P (neg skew)";
        case ProfileShape::B_SHAPE: return "B (pos skew)";
        case ProfileShape::DOUBLE_DISTRIBUTION: return "bimodal";
        default: return "undefined";
    }
}

static const char* signal_name(SignalType type) {
    switch (type) {
        case SignalType::LONG: return "LONG";
        case SignalType::SHORT: return "SHORT";
        case SignalType::CLOSE_LONG: return "CLOSE_LONG";
        case SignalType::CLOSE_SHORT: return "CLOSE_SHORT";
        default: return "NONE";
    }
}

int main() {
    constexpr std::int64_t tick_size = PRICE_SCALE / 4; // $0.25 per tick
    constexpr Price reference = 100LL * PRICE_SCALE;    // 100.00 fixed-point

    PriceLadder ladder;
    for (int tick = -4; tick <= 6; ++tick) {
        const Price price = reference + static_cast<Price>(tick) * tick_size;
        const int raw_weight = 10 - (tick - 1) * (tick - 1);
        const unsigned weight = static_cast<unsigned>(raw_weight > 0 ? raw_weight : 1);
        ladder.add_tick(price, weight);
    }

    ProfileEngine engine;
    const auto result = engine.compute(ladder, reference, tick_size);

    std::printf("=== Market Profile / Volume Profile ===\n");
    std::printf("levels           : %zu\n", ladder.size());
    std::printf("total volume     : %llu\n",
                static_cast<unsigned long long>(ladder.total_volume()));
    std::printf("POC              : %.4f\n", price_to_double(result.value_area.poc));
    std::printf("Value Area Low   : %.4f\n", price_to_double(result.value_area.val));
    std::printf("Value Area High  : %.4f\n", price_to_double(result.value_area.vah));
    std::printf("VA volume        : %llu\n",
                static_cast<unsigned long long>(result.value_area.volume));
    std::printf("shape            : %s\n", shape_name(result.shape));
    std::printf("mean (ticks)     : %.4f\n", result.moments.mean_tick);
    std::printf("variance (ticks) : %.4f\n", result.moments.variance_tick2);
    std::printf("skewness         : %.4f\n", result.moments.skewness);
    std::printf("excess kurtosis  : %.4f\n", result.moments.excess_kurtosis);
    std::printf("HVN count        : %zu\n", result.hvn.size());
    std::printf("LVN count        : %zu\n", result.lvn.size());

    SignalGenerator generator;
    const Price probe = double_to_price(99.00); // below VAL, expect fade-long
    const Position position{};
    const Signal signal = generator.generate(probe, result, position);
    std::printf("\n=== Signal @ %.4f ===\n", price_to_double(probe));
    std::printf("type             : %s\n", signal_name(signal.type));
    std::printf("confidence       : %.2f\n", signal.confidence);
    std::printf("entry            : %.4f\n", price_to_double(signal.entry_price));
    std::printf("stop             : %.4f\n", price_to_double(signal.stop_loss));
    std::printf("target           : %.4f\n", price_to_double(signal.take_profit));
    return 0;
}
