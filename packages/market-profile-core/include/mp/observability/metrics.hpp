// include/mp/observability/metrics.hpp
// Lock-free latency histogram and aggregate trading counters.
#pragma once

#include "mp/foundation/types.hpp"
#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>

namespace mp {

class LatencyHistogram {
    static constexpr std::size_t NUM_BUCKETS = 64;
    std::array<std::atomic<std::uint64_t>, NUM_BUCKETS> buckets_{};
    std::atomic<std::uint64_t> count_{0};
    std::atomic<std::uint64_t> sum_ns_{0};
    std::atomic<std::uint64_t> max_ns_{0};

public:
    void record(std::uint64_t ns) noexcept {
        const std::size_t bucket = (ns == 0) ? 0
            : static_cast<std::size_t>(63 - __builtin_clzll(ns));
        const std::size_t idx = std::min(bucket, NUM_BUCKETS - 1);
        buckets_[idx].fetch_add(1, std::memory_order_relaxed);
        count_.fetch_add(1, std::memory_order_relaxed);
        sum_ns_.fetch_add(ns, std::memory_order_relaxed);
        std::uint64_t prev = max_ns_.load(std::memory_order_relaxed);
        while (ns > prev && !max_ns_.compare_exchange_weak(
            prev, ns, std::memory_order_relaxed, std::memory_order_relaxed)) {
        }
    }

    // Lower bound of the bucket holding the p-th percentile.
    [[nodiscard]] std::uint64_t percentile(double percentile) const noexcept {
        const std::uint64_t total = count_.load(std::memory_order_relaxed);
        if (total == 0) {
            return 0;
        }
        const std::uint64_t target = static_cast<std::uint64_t>(static_cast<double>(total) * percentile);
        std::uint64_t cumulative = 0;
        for (std::size_t i = 0; i < NUM_BUCKETS; ++i) {
            cumulative += buckets_[i].load(std::memory_order_relaxed);
            if (cumulative >= target) {
                return std::uint64_t{1} << i; // lower bound of bucket i
            }
        }
        return max_ns_.load(std::memory_order_relaxed);
    }

    [[nodiscard]] std::uint64_t mean() const noexcept {
        const std::uint64_t counted = count_.load(std::memory_order_relaxed);
        return (counted > 0) ? sum_ns_.load(std::memory_order_relaxed) / counted : 0;
    }
    [[nodiscard]] std::uint64_t max() const noexcept { return max_ns_.load(std::memory_order_relaxed); }
    [[nodiscard]] std::uint64_t count() const noexcept { return count_.load(std::memory_order_relaxed); }
};

struct alignas(CACHE_LINE_SIZE) TradingMetrics {
    std::atomic<std::uint64_t> ticks_processed{0};
    std::atomic<std::uint64_t> signals_generated{0};
    std::atomic<std::uint64_t> orders_sent{0};
    std::atomic<std::uint64_t> orders_filled{0};
    std::atomic<std::uint64_t> orders_rejected{0};
    LatencyHistogram tick_to_signal;
    LatencyHistogram signal_to_order;
};

} // namespace mp
