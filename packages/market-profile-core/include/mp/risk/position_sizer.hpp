// include/mp/risk/position_sizer.hpp
// Position sizing: risk-fractional capped by quarter-Kelly.
#pragma once

#include "mp/foundation/error.hpp"
#include "mp/foundation/types.hpp"
#include "mp/risk/risk_limits.hpp" // DefaultRiskPolicy
#include <algorithm>

namespace mp {

class PositionSizer {
public:
    struct SizingInput {
        double equity{0.0};          // account equity
        Price entry_price{0};        // fixed-point
        Price stop_loss{0};          // fixed-point
        double win_probability{0.0}; // p in [0,1]
        double reward_risk_ratio{0.0};
    };

    struct SizingOutput {
        ErrorCode error{ErrorCode::SUCCESS};
        Quantity quantity{0};
        double kelly_fraction{0.0};
        double risk_amount{0.0};
        double risk_per_unit{0.0};
    };

    // Kelly fraction f* = (p*(b+1) - 1) / b, where b = reward_risk_ratio.
    // Clamped to [0, quarter-Kelly]. Returns 0 for negative edge.
    [[nodiscard]] static double kelly_fraction(double win_probability,
                                               double reward_risk_ratio) noexcept {
        if (reward_risk_ratio <= 0.0) {
            return 0.0;
        }
        const double f = (win_probability * (reward_risk_ratio + 1.0) - 1.0)
                         / reward_risk_ratio;
        const double kelly = std::clamp(f, 0.0, 1.0);
        const double quarter_kelly =
            static_cast<double>(KellyFraction::num) / static_cast<double>(KellyFraction::den);
        return std::min(kelly, quarter_kelly);
    }

    [[nodiscard]] static SizingOutput compute_size(const SizingInput& in) noexcept {
        SizingOutput out;
        if (in.entry_price <= 0 || in.stop_loss <= 0) {
            out.error = ErrorCode::INVALID_PRICE;
            return out;
        }
        const double entry = price_to_double(in.entry_price);
        const double stop = price_to_double(in.stop_loss);
        const double risk_per_unit = std::abs(entry - stop);
        if (risk_per_unit <= 1e-12) {
            out.error = ErrorCode::INVALID_PRICE;
            return out;
        }
        out.risk_per_unit = risk_per_unit;
        out.risk_amount = in.equity * DefaultRiskPolicy::risk_per_trade;
        out.kelly_fraction = kelly_fraction(in.win_probability, in.reward_risk_ratio);

        const double kelly_risk = in.equity * out.kelly_fraction;
        const double effective_risk = std::min(out.risk_amount, kelly_risk);
        if (effective_risk <= 0.0 || risk_per_unit <= 0.0) {
            out.error = ErrorCode::INVALID_PRICE;
            return out;
        }
        const double qty = effective_risk / risk_per_unit;
        out.quantity = static_cast<Quantity>(qty);
        return out;
    }
};

} // namespace mp
