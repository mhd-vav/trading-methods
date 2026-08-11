// include/mp/data_structures/price_ladder.hpp
// Cache-optimized price ladder. Struct-of-Arrays layout so that the profile
// engine scans contiguous volume memory. Prices are kept sorted ascending so
// index == price-rank, which makes Value-Area expansion and HVN/LVN detection
// straightforward array walks (A2 histogram construction, A3 support/range).
#pragma once

#include "mp/foundation/types.hpp"
#include <algorithm>
#include <array>
#include <cstring>

namespace mp {

class PriceLadder {
    alignas(CACHE_LINE_SIZE) std::array<Price, MAX_PRICE_LEVELS> prices_{};
    alignas(CACHE_LINE_SIZE) std::array<Volume, MAX_PRICE_LEVELS> volumes_{};
    alignas(CACHE_LINE_SIZE) std::array<std::uint32_t, MAX_PRICE_LEVELS> tpo_counts_{};

    std::size_t size_{0};
    Price min_price_{};
    Price max_price_{};
    Volume total_volume_{0};
    std::uint32_t total_ticks_{0};

public:
    PriceLadder() noexcept = default;

    void reset() noexcept {
        size_ = 0;
        min_price_ = 0;
        max_price_ = 0;
        total_volume_ = 0;
        total_ticks_ = 0;
        std::memset(volumes_.data(), 0, MAX_PRICE_LEVELS * sizeof(Volume));
        std::memset(tpo_counts_.data(), 0, MAX_PRICE_LEVELS * sizeof(std::uint32_t));
    }

    // Add one print at (price, volume). Existing levels accumulate (A2).
    // Returns false if the ladder is full.
    bool add_tick(Price price, Volume volume) noexcept {
        if (size_ >= MAX_PRICE_LEVELS) {
            return false;
        }
        auto* begin = prices_.begin();
        auto it = std::lower_bound(begin, begin + static_cast<std::ptrdiff_t>(size_), price);
        const std::size_t idx = static_cast<std::size_t>(it - begin);

        if (idx < size_ && prices_[idx] == price) {
            volumes_[idx] += volume;
            tpo_counts_[idx] += 1;
        } else {
            if (idx < size_) {
                std::memmove(&prices_[idx + 1], &prices_[idx],
                             (size_ - idx) * sizeof(Price));
                std::memmove(&volumes_[idx + 1], &volumes_[idx],
                             (size_ - idx) * sizeof(Volume));
                std::memmove(&tpo_counts_[idx + 1], &tpo_counts_[idx],
                             (size_ - idx) * sizeof(std::uint32_t));
            }
            prices_[idx] = price;
            volumes_[idx] = volume;
            tpo_counts_[idx] = 1;
            ++size_;
        }

        if (size_ == 1) {
            min_price_ = price;
            max_price_ = price;
        } else {
            min_price_ = std::min(min_price_, price);
            max_price_ = std::max(max_price_, price);
        }
        total_volume_ += volume;
        total_ticks_ += 1;
        return true;
    }

    // Bulk load from an already-sorted (price, volume) series. Faster than
    // repeated add_tick when replaying a session snapshot.
    void load_sorted(const Price* prices, const Volume* volumes, std::size_t count) noexcept {
        reset();
        count = std::min(count, MAX_PRICE_LEVELS);
        for (std::size_t i = 0; i < count; ++i) {
            prices_[i] = prices[i];
            volumes_[i] = volumes[i];
            tpo_counts_[i] = 1;
            total_volume_ += volumes[i];
        }
        size_ = count;
        total_ticks_ = static_cast<std::uint32_t>(count);
        if (count > 0) {
            min_price_ = prices_[0];
            max_price_ = prices_[count - 1];
        }
    }

    [[nodiscard]] bool empty() const noexcept { return size_ == 0; }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] Price price_at(std::size_t i) const noexcept { return prices_[i]; }
    [[nodiscard]] Volume volume_at(std::size_t i) const noexcept { return volumes_[i]; }
    [[nodiscard]] std::uint32_t tpo_at(std::size_t i) const noexcept { return tpo_counts_[i]; }
    [[nodiscard]] Price min_price() const noexcept { return min_price_; }
    [[nodiscard]] Price max_price() const noexcept { return max_price_; }
    [[nodiscard]] Volume total_volume() const noexcept { return total_volume_; }
    [[nodiscard]] std::uint32_t total_ticks() const noexcept { return total_ticks_; }

    // Binary search the index of a price, or size() if absent.
    [[nodiscard]] std::size_t index_of(Price price) const noexcept {
        auto* begin = prices_.begin();
        auto it = std::lower_bound(begin, begin + static_cast<std::ptrdiff_t>(size_), price);
        const std::size_t idx = static_cast<std::size_t>(it - begin);
        return (idx < size_ && prices_[idx] == price) ? idx : size_;
    }
};

} // namespace mp
