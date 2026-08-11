// include/mp/risk/risk_limits.hpp
// Compile-time risk policy + runtime equity/drawdown tracker.
#pragma once

#include "mp/foundation/error.hpp"
#include "mp/foundation/types.hpp"
#include <algorithm>

namespace mp {

template <typename RiskRatio, typename DrawdownRatio, typename LeverageRatio>
struct RiskPolicy {
    static constexpr double risk_per_trade =
        static_cast<double>(RiskRatio::num) / static_cast<double>(RiskRatio::den);
    static constexpr double max_drawdown =
        static_cast<double>(DrawdownRatio::num) / static_cast<double>(DrawdownRatio::den);
    static constexpr double max_leverage =
        static_cast<double>(LeverageRatio::num) / static_cast<double>(LeverageRatio::den);

    static_assert(risk_per_trade > 0.0 && risk_per_trade <= 0.05,
                  "Risk per trade must be in (0%, 5%]");
    static_assert(max_drawdown > 0.0 && max_drawdown <= 0.50,
                  "Max drawdown must be in (0%, 50%]");
    static_assert(max_leverage >= 1.0 && max_leverage <= 10.0,
                  "Leverage must be in [1x, 10x]");
};

using DefaultRiskPolicy = RiskPolicy<RiskPerTrade, MaxDrawdown, MaxLeverage>;

class RiskLimits {
    double initial_capital_{0.0};
    double current_equity_{0.0};
    double peak_equity_{0.0};
    double daily_loss_limit_{0.0};
    double daily_pnl_{0.0};
    std::uint32_t consecutive_losses_{0};
    std::uint32_t max_consecutive_losses_{5};
    bool trading_halted_{false};

public:
    explicit RiskLimits(double initial_capital) noexcept
        : initial_capital_{initial_capital},
          current_equity_{initial_capital},
          peak_equity_{initial_capital},
          daily_loss_limit_{initial_capital * DefaultRiskPolicy::risk_per_trade * 3.0} {}

    [[nodiscard]] ErrorCode check_can_trade() const noexcept {
        if (trading_halted_) {
            return ErrorCode::RISK_LIMIT_EXCEEDED;
        }
        if (peak_equity_ > 0.0) {
            const double drawdown = (peak_equity_ - current_equity_) / peak_equity_;
            if (drawdown >= DefaultRiskPolicy::max_drawdown) {
                return ErrorCode::RISK_LIMIT_EXCEEDED;
            }
        }
        if (daily_pnl_ <= -daily_loss_limit_) {
            return ErrorCode::RISK_LIMIT_EXCEEDED;
        }
        if (consecutive_losses_ >= max_consecutive_losses_) {
            return ErrorCode::RISK_LIMIT_EXCEEDED;
        }
        return ErrorCode::SUCCESS;
    }

    void record_trade_result(double pnl) noexcept {
        current_equity_ += pnl;
        daily_pnl_ += pnl;
        peak_equity_ = std::max(peak_equity_, current_equity_);
        if (pnl < 0.0) {
            ++consecutive_losses_;
        } else {
            consecutive_losses_ = 0;
        }
        if (check_can_trade() != ErrorCode::SUCCESS) {
            trading_halted_ = true;
        }
    }

    void reset_daily() noexcept { daily_pnl_ = 0.0; }
    void resume_trading() noexcept { trading_halted_ = false; }

    [[nodiscard]] double current_equity() const noexcept { return current_equity_; }
    [[nodiscard]] double peak_equity() const noexcept { return peak_equity_; }
    [[nodiscard]] double drawdown() const noexcept {
        return (peak_equity_ > 0.0) ? (peak_equity_ - current_equity_) / peak_equity_ : 0.0;
    }
    [[nodiscard]] bool is_halted() const noexcept { return trading_halted_; }
};

} // namespace mp
