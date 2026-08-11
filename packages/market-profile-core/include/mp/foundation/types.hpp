// include/mp/foundation/types.hpp
// Core domain types for the Market Profile / Volume Profile engine.
// All prices are fixed-point integers (actual_price * PRICE_SCALE) to avoid
// floating-point drift, per the A1 discrete-price-domain rule.
#pragma once

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <ratio>
#include <string_view>

namespace mp {

inline constexpr std::size_t CACHE_LINE_SIZE = 64;
inline constexpr std::size_t MAX_PRICE_LEVELS = 10'000;

// Fixed-point scale: 8 decimal places. A price of 100.25 -> 10'025'000'000.
inline constexpr std::int64_t PRICE_SCALE = 100'000'000LL;

// Risk configuration (compile-time fractions): 2% per trade, 15% max DD, 3x.
using RiskPerTrade = std::ratio<2, 100>;
using MaxDrawdown  = std::ratio<15, 100>;
using MaxLeverage  = std::ratio<3, 1>;
using KellyFraction = std::ratio<1, 4>; // quarter-Kelly cap

// Fixed-point price. Always an integer multiple of PRICE_SCALE.
using Price = std::int64_t;
using Volume = std::uint64_t;
using Quantity = std::uint32_t;
using OrderId = std::uint64_t;
using Timestamp = std::chrono::nanoseconds;
using Symbol = std::string_view;

enum class Side : std::uint8_t {
    BID = 0,
    ASK = 1,
    UNKNOWN = 255
};

enum class OrderType : std::uint8_t {
    MARKET = 0, LIMIT = 1, STOP = 2, STOP_LIMIT = 3
};

enum class OrderStatus : std::uint8_t {
    PENDING = 0, OPEN = 1, PARTIAL_FILL = 2, FILLED = 3, CANCELLED = 4, REJECTED = 5
};

enum class TimeInForce : std::uint8_t {
    GTC = 0, IOC = 1, FOK = 2, DAY = 3
};

enum class SignalType : std::uint8_t {
    NONE = 0, LONG = 1, SHORT = 2, CLOSE_LONG = 3, CLOSE_SHORT = 4
};

// Auction profile shape (Steidlmayer conventions), driven by skewness sign.
enum class ProfileShape : std::uint8_t {
    D_SHAPE = 0,              // balanced / normal
    P_SHAPE = 1,              // negative skew: volume high, tail left
    B_SHAPE = 2,              // positive skew: volume low, tail right
    DOUBLE_DISTRIBUTION = 3,  // bimodal
    UNDEFINED = 255
};

// Convert a decimal price to fixed-point. Rounds half away from zero.
// Implemented in the header because it is used widely across translation units.
inline Price double_to_price(double value) noexcept {
    if (value >= 0.0) {
        return static_cast<Price>(value * static_cast<double>(PRICE_SCALE) + 0.5);
    }
    return static_cast<Price>(value * static_cast<double>(PRICE_SCALE) - 0.5);
}

// Convert a fixed-point price back to decimal.
inline double price_to_double(Price price) noexcept {
    return static_cast<double>(price) / static_cast<double>(PRICE_SCALE);
}

} // namespace mp
