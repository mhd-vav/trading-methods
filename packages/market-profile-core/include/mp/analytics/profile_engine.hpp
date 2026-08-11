// include/mp/analytics/profile_engine.hpp
// The Market Profile / Volume Profile math core (A4 POC, A6 Value Area,
// A7 VAH/VAL, A8 HVN/LVN, A9 shape).
//
// All routines are pure and deterministic: identical inputs yield identical
// outputs, so the engine can be replay-tested against golden fixtures
// independently of any feed handler. The Value Area is a CONTIGUOUS coverage
// interval grown greedily outward from the POC until the target fraction of
// total weight is captured (A6); it is NOT a variance band.
#pragma once

#include "mp/analytics/statistics.hpp"
#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"
#include <algorithm>
#include <vector>

namespace mp {

struct ValueArea {
    Price poc{0};
    Price vah{0};
    Price val{0};
    Volume volume{0};
    std::size_t poc_index{0};
    std::size_t val_index{0};
    std::size_t vah_index{0};
};

struct ProfileResult {
    bool valid{false};
    ValueArea value_area{};
    ProfileShape shape{ProfileShape::UNDEFINED};
    MomentResult moments{};
    std::vector<Price> hvn{}; // high-volume nodes (local maxima)
    std::vector<Price> lvn{}; // low-volume nodes (local minima)
};

class ProfileEngine {
public:
    struct Config {
        double value_area_fraction = 0.70; // A6 target coverage
        double skewness_threshold = 0.5;   // A9 shape gate
        double bimodality_cutoff = 0.555;  // A9 double-distribution gate
        std::size_t hvn_lvn_window = 1;    // half-window for smoothing (A8)
        double hvn_min_prominence = 0.0;   // reject tiny nodes (fraction of POC)

        Config() noexcept = default;
    };

    explicit ProfileEngine() noexcept = default;
    explicit ProfileEngine(Config config) noexcept : config_{config} {}

    // A4: Point of Control = the price bin with maximum weight (the MODE).
    // Tie-break: lowest index (i.e. lowest price) wins, deterministic.
    [[nodiscard]] std::size_t poc_index(const PriceLadder& ladder) const noexcept {
        if (ladder.empty()) {
            return 0;
        }
        std::size_t best = 0;
        Volume best_vol = 0;
        for (std::size_t i = 0; i < ladder.size(); ++i) {
            if (ladder.volume_at(i) > best_vol) {
                best_vol = ladder.volume_at(i);
                best = i;
            }
        }
        return best;
    }

    // A6/A7: Value Area. Greedy expansion from the POC; at each step move the
    // boundary (up or down) that adds the larger weight, until the target
    // fraction of total weight is captured or both boundaries are pinned.
    [[nodiscard]] ValueArea compute_value_area(const PriceLadder& ladder) const noexcept {
        ValueArea va{};
        if (ladder.empty()) {
            return va;
        }
        const std::size_t poc = poc_index(ladder);
        const Volume total = ladder.total_volume();
        if (total == 0) {
            va.poc_index = poc;
            va.poc = ladder.price_at(poc);
            return va;
        }
        const double target = static_cast<double>(total) * config_.value_area_fraction;

        Volume accumulated = ladder.volume_at(poc);
        std::size_t lo = poc;
        std::size_t hi = poc;

        while (static_cast<double>(accumulated) < target) {
            const bool can_up = (hi + 1) < ladder.size();
            const bool can_down = lo > 0;
            if (!can_up && !can_down) {
                break;
            }
            const Volume vol_up = can_up ? ladder.volume_at(hi + 1) : 0;
            const Volume vol_down = can_down ? ladder.volume_at(lo - 1) : 0;

            if (can_up && (!can_down || vol_up >= vol_down)) {
                accumulated += vol_up;
                ++hi;
            } else {
                accumulated += vol_down;
                --lo;
            }
        }

        va.poc_index = poc;
        va.val_index = lo;
        va.vah_index = hi;
        va.poc = ladder.price_at(poc);
        va.val = ladder.price_at(lo);
        va.vah = ladder.price_at(hi);
        va.volume = accumulated;
        return va;
    }

    // A8: high/low volume nodes. Local maxima/minima of a lightly smoothed
    // weight series (smoothing window = 2*window+1). Prominence filter rejects
    // nodes smaller than hvn_min_prominence * poc_volume.
    void detect_nodes(const PriceLadder& ladder,
                      std::vector<Price>& hvn,
                      std::vector<Price>& lvn) const {
        hvn.clear();
        lvn.clear();
        if (ladder.size() < 3) {
            return;
        }
        const std::size_t w = config_.hvn_lvn_window;
        const Volume poc_vol = ladder.volume_at(poc_index(ladder));
        const double prominence = config_.hvn_min_prominence * static_cast<double>(poc_vol);

        auto smoothed = [&](std::size_t i) -> double {
            double sum = 0.0;
            int cnt = 0;
            for (std::ptrdiff_t off = -static_cast<std::ptrdiff_t>(w);
                 off <= static_cast<std::ptrdiff_t>(w); ++off) {
                const std::ptrdiff_t j = static_cast<std::ptrdiff_t>(i) + off;
                if (j >= 0 && j < static_cast<std::ptrdiff_t>(ladder.size())) {
                    sum += static_cast<double>(ladder.volume_at(static_cast<std::size_t>(j)));
                    ++cnt;
                }
            }
            return cnt ? sum / cnt : 0.0;
        };

        for (std::size_t i = 1; i + 1 < ladder.size(); ++i) {
            const double cur = smoothed(i);
            const double left = smoothed(i - 1);
            const double right = smoothed(i + 1);
            if (cur > left && cur > right) {
                if (cur - std::min(left, right) >= prominence) {
                    hvn.push_back(ladder.price_at(i));
                }
            } else if (cur < left && cur < right) {
                lvn.push_back(ladder.price_at(i));
            }
        }
    }

    // A9: shape from skewness sign + bimodality gate.
    [[nodiscard]] ProfileShape classify_shape(const MomentResult& moments,
                                              std::size_t support) const noexcept {
        if (!moments.defined || support < 4) {
            return ProfileShape::UNDEFINED;
        }
        if (moments.bimodality > config_.bimodality_cutoff) {
            return ProfileShape::DOUBLE_DISTRIBUTION;
        }
        if (moments.skewness > config_.skewness_threshold) {
            return ProfileShape::B_SHAPE; // tail right, volume low
        }
        if (moments.skewness < -config_.skewness_threshold) {
            return ProfileShape::P_SHAPE; // tail left, volume high
        }
        return ProfileShape::D_SHAPE;
    }

    // Full bundle over a session profile. reference/tick_size drive the
    // moment computation (use 0 and the instrument tick size).
    [[nodiscard]] ProfileResult compute(const PriceLadder& ladder,
                                        Price reference,
                                        std::int64_t tick_size) const {
        ProfileResult result{};
        if (ladder.empty()) {
            return result;
        }
        result.valid = true;
        result.value_area = compute_value_area(ladder);
        result.moments = Statistics::compute(ladder, reference, tick_size);
        result.shape = classify_shape(result.moments, ladder.size());
        detect_nodes(ladder, result.hvn, result.lvn);
        return result;
    }

private:
    Config config_;
};

} // namespace mp
