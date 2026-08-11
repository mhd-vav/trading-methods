// include/mp/strategy/signal_generator.hpp
// Turns a profile result + current price + position into a discrete signal.
//
// Core logic: Market Profile mean-reversion. Fade price that rejects beyond the
// Value Area back toward the POC. Shape (D/P/B/double) gates confidence because
// a balanced profile is more reliable for fading than a one-sided or bimodal one.
#pragma once

#include "mp/analytics/profile_engine.hpp"
#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"
#include <algorithm>

namespace mp {

struct Position {
    Quantity long_qty{0};
    Quantity short_qty{0};
    [[nodiscard]] int net_position() const noexcept {
        return static_cast<int>(long_qty) - static_cast<int>(short_qty);
    }
};

struct Signal {
    SignalType type{SignalType::NONE};
    Price entry_price{0};
    Price stop_loss{0};
    Price take_profit{0};
    Quantity quantity{0};
    double confidence{0.0};
    ProfileShape shape{ProfileShape::UNDEFINED};
};

class SignalGenerator {
public:
    struct Config {
        double va_penetration_threshold = 0.0002; // 2 bps beyond VA before fading
        double stop_distance_multiple = 1.5;      // stop = multiple of (poc-edge)
        double min_confidence = 0.55;

        Config() noexcept = default;
    };

    explicit SignalGenerator() noexcept = default;
    explicit SignalGenerator(Config config) noexcept : config_{config} {}

    [[nodiscard]] Signal generate(Price current_price,
                                  const ProfileResult& profile,
                                  const Position& position) const noexcept {
        Signal sig;
        sig.shape = profile.shape;
        if (!profile.valid) {
            return sig;
        }
        const auto& va = profile.value_area;
        if (va.vah == 0 || va.val == 0 || va.poc == 0) {
            return sig;
        }

        const double px = price_to_double(current_price);
        const double vah = price_to_double(va.vah);
        const double val = price_to_double(va.val);
        const double poc = price_to_double(va.poc);
        const double band = px * config_.va_penetration_threshold;

        if (px <= val - band && position.net_position() <= 0) {
            sig.type = SignalType::LONG;
            sig.entry_price = current_price;
            const double stop_dist = std::max((poc - val), 0.0) * config_.stop_distance_multiple;
            sig.stop_loss = double_to_price(px - stop_dist);
            sig.take_profit = va.poc;
            sig.confidence = confidence_for_long(profile);
        } else if (px >= vah + band && position.net_position() >= 0) {
            sig.type = SignalType::SHORT;
            sig.entry_price = current_price;
            const double stop_dist = std::max((vah - poc), 0.0) * config_.stop_distance_multiple;
            sig.stop_loss = double_to_price(px + stop_dist);
            sig.take_profit = va.poc;
            sig.confidence = confidence_for_short(profile);
        } else if (position.net_position() > 0 && px >= poc) {
            sig.type = SignalType::CLOSE_LONG;
            sig.confidence = 1.0;
        } else if (position.net_position() < 0 && px <= poc) {
            sig.type = SignalType::CLOSE_SHORT;
            sig.confidence = 1.0;
        }

        if ((sig.type == SignalType::LONG || sig.type == SignalType::SHORT)
            && sig.confidence < config_.min_confidence) {
            sig.type = SignalType::NONE;
        }
        return sig;
    }

private:
    [[nodiscard]] double confidence_for_long(const ProfileResult& profile) const noexcept {
        double confidence = 0.55;
        if (profile.shape == ProfileShape::B_SHAPE) confidence += 0.15;
        else if (profile.shape == ProfileShape::D_SHAPE) confidence += 0.05;
        else if (profile.shape == ProfileShape::DOUBLE_DISTRIBUTION) confidence -= 0.10;
        return std::clamp(confidence, 0.0, 1.0);
    }

    [[nodiscard]] double confidence_for_short(const ProfileResult& profile) const noexcept {
        double confidence = 0.55;
        if (profile.shape == ProfileShape::P_SHAPE) confidence += 0.15;
        else if (profile.shape == ProfileShape::D_SHAPE) confidence += 0.05;
        else if (profile.shape == ProfileShape::DOUBLE_DISTRIBUTION) confidence -= 0.10;
        return std::clamp(confidence, 0.0, 1.0);
    }

    Config config_;
};

} // namespace mp
