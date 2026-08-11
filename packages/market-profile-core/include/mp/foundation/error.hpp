// include/mp/foundation/error.hpp
// Status codes and a thin Result<T> for the engine. Pure math functions stay
// noexcept and return a status-bearing result rather than throwing.
#pragma once

#include <cstdint>
#include <variant>

namespace mp {

enum class ErrorCode : std::uint8_t {
    SUCCESS = 0,
    EMPTY_PROFILE = 1,
    INVALID_PRICE = 2,
    INVALID_VOLUME = 3,
    QUEUE_FULL = 4,
    RISK_LIMIT_EXCEEDED = 5,
    UNDEFINED_STATISTIC = 6
};

template <typename T>
class Result {
public:
    Result(T value) : storage_{std::move(value)} {}
    Result(ErrorCode error) : storage_{error} {}

    [[nodiscard]] bool ok() const noexcept { return std::holds_alternative<T>(storage_); }
    [[nodiscard]] bool has_error() const noexcept { return !ok(); }
    [[nodiscard]] ErrorCode error() const noexcept { return std::get<ErrorCode>(storage_); }
    [[nodiscard]] const T& value() const noexcept { return std::get<T>(storage_); }

private:
    std::variant<T, ErrorCode> storage_;
};

} // namespace mp
