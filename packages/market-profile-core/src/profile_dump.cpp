// src/profile_dump.cpp
// Headless JSON dumper for the Market Profile engine. Reads a price ladder
// from stdin (one "price,volume" pair per line), runs the full ProfileResult
// computation, and writes a single JSON object to stdout. This is the bridge
// that feeds the C++ math (POC / Value Area / shape / moments / HVN/LVN) to
// the Python debate agents: agents argue over THESE numbers, never free text.
//
// Usage:
//   echo -e "100.00,4\n100.25,10\n100.50,6" | ./build/mp_profile
//   ./build/mp_profile --tick 0.25 --ref 100.00 < ladder.csv
#include "mp/analytics/profile_engine.hpp"
#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"
#include "mp/strategy/signal_generator.hpp"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using namespace mp;

static const char* shape_name(ProfileShape shape) {
    switch (shape) {
        case ProfileShape::D_SHAPE: return "D";
        case ProfileShape::P_SHAPE: return "P";
        case ProfileShape::B_SHAPE: return "B";
        case ProfileShape::DOUBLE_DISTRIBUTION: return "double";
        default: return "undefined";
    }
}

static const char* shape_label(ProfileShape shape) {
    switch (shape) {
        case ProfileShape::D_SHAPE: return "balanced";
        case ProfileShape::P_SHAPE: return "negative_skew";
        case ProfileShape::B_SHAPE: return "positive_skew";
        case ProfileShape::DOUBLE_DISTRIBUTION: return "bimodal";
        default: return "undefined";
    }
}

static const char* signal_type_name(SignalType type) {
    switch (type) {
        case SignalType::LONG: return "LONG";
        case SignalType::SHORT: return "SHORT";
        case SignalType::CLOSE_LONG: return "CLOSE_LONG";
        case SignalType::CLOSE_SHORT: return "CLOSE_SHORT";
        default: return "NONE";
    }
}

static void emit_price_array(const std::vector<Price>& xs) {
    std::printf("[");
    for (std::size_t i = 0; i < xs.size(); ++i) {
        if (i) std::printf(", ");
        std::printf("%.4f", price_to_double(xs[i]));
    }
    std::printf("]");
}

int main(int argc, char** argv) {
    double tick_double = 0.01;
    double ref_double = 0.0;

    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if ((arg == "--tick" || arg == "-t") && i + 1 < argc) {
            tick_double = std::strtod(argv[++i], nullptr);
        } else if ((arg == "--ref" || arg == "-r") && i + 1 < argc) {
            ref_double = std::strtod(argv[++i], nullptr);
        } else if (arg == "--help" || arg == "-h") {
            std::printf("usage: mp_profile [--tick T] [--ref R] < ladder.csv\n");
            return 0;
        }
    }

    if (tick_double <= 0.0) {
        std::fprintf(stderr, "error: --tick must be positive\n");
        return 2;
    }

    PriceLadder ladder;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        const auto comma = line.find(',');
        if (comma == std::string::npos) continue;
        const std::string pstr = line.substr(0, comma);
        const std::string vstr = line.substr(comma + 1);
        const double price = std::strtod(pstr.c_str(), nullptr);
        const double volume = std::strtod(vstr.c_str(), nullptr);
        if (price <= 0.0 || volume <= 0.0) continue;
        ladder.add_tick(double_to_price(price), static_cast<Volume>(volume + 0.5));
    }

    if (ladder.empty()) {
        std::printf("{\"valid\": false, \"error\": \"empty ladder\"}\n");
        return 1;
    }

    if (ref_double <= 0.0) {
        ref_double = price_to_double(ladder.min_price());
    }

    const std::int64_t tick_size = double_to_price(tick_double);
    const Price reference = double_to_price(ref_double);

    ProfileEngine engine;
    const ProfileResult result = engine.compute(ladder, reference, tick_size);

    const auto& va = result.value_area;
    const auto& m = result.moments;

    const Price last_price = ladder.price_at(ladder.size() - 1);
    const Position position{};
    SignalGenerator generator;
    const Signal signal = generator.generate(last_price, result, position);

    std::printf("{");
    std::printf("\"valid\": %s", result.valid ? "true" : "false");
    std::printf(", \"levels\": %zu", ladder.size());
    std::printf(", \"total_volume\": %llu",
                static_cast<unsigned long long>(ladder.total_volume()));
    std::printf(", \"reference\": %.4f", ref_double);
    std::printf(", \"tick_size\": %.4f", tick_double);
    std::printf(", \"poc\": %.4f", price_to_double(va.poc));
    std::printf(", \"val\": %.4f", price_to_double(va.val));
    std::printf(", \"vah\": %.4f", price_to_double(va.vah));
    std::printf(", \"va_volume\": %llu",
                static_cast<unsigned long long>(va.volume));
    std::printf(", \"va_pct\": %.4f",
                 ladder.total_volume() > 0
                     ? static_cast<double>(va.volume) /
                           static_cast<double>(ladder.total_volume())
                     : 0.0);
    std::printf(", \"last_price\": %.4f", price_to_double(last_price));
    std::printf(", \"shape\": \"%s\"", shape_name(result.shape));
    std::printf(", \"shape_label\": \"%s\"", shape_label(result.shape));
    std::printf(", \"mean_tick\": %.6f", m.mean_tick);
    std::printf(", \"variance_tick2\": %.6f", m.variance_tick2);
    std::printf(", \"stddev_tick\": %.6f",
                 m.variance_tick2 > 0.0 ? std::sqrt(m.variance_tick2) : 0.0);
    std::printf(", \"skewness\": %.6f", m.skewness);
    std::printf(", \"excess_kurtosis\": %.6f", m.excess_kurtosis);
    std::printf(", \"bimodality\": %.6f", m.bimodality);
    std::printf(", \"hvn_count\": %zu", result.hvn.size());
    std::printf(", \"lvn_count\": %zu", result.lvn.size());
    std::printf(", \"hvn\": ");
    emit_price_array(result.hvn);
    std::printf(", \"lvn\": ");
    emit_price_array(result.lvn);
    std::printf(", \"engine_signal\": \"%s\"", signal_type_name(signal.type));
    std::printf(", \"engine_confidence\": %.4f", signal.confidence);
    std::printf(", \"engine_entry\": %.4f", price_to_double(signal.entry_price));
    std::printf(", \"engine_stop\": %.4f", price_to_double(signal.stop_loss));
    std::printf(", \"engine_target\": %.4f", price_to_double(signal.take_profit));
    std::printf("}\n");
    return 0;
}
