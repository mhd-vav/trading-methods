// include/mp/analytics/statistics.hpp
// Weighted descriptive statistics over the discrete price profile (A5).
//
// All moments are computed in TICK units against integer tick coordinates
// (x = (price - reference)/tick_size) so they are translation-invariant and
// free of floating-point price drift. Skewness is the third standardized
// central moment; kurtosis is EXCESS kurtosis (fourth moment minus 3).
// These are the mathematical objects defined in the A1-A10 spec and must not
// be conflated with POC or the Value Area.
#pragma once

#include "mp/data_structures/price_ladder.hpp"
#include "mp/foundation/types.hpp"
#include <cmath>

namespace mp {

struct MomentResult {
    bool defined{false};
    double mean_tick{0.0};
    double variance_tick2{0.0};
    double skewness{0.0};
    double excess_kurtosis{0.0};
    double bimodality{0.0};
};

class Statistics {
public:
    // Weighted mean in tick units. reference is subtracted from every price
    // before dividing by tick_size; the result is independent of reference.
    [[nodiscard]] static MomentResult compute(const PriceLadder& ladder,
                                              Price reference,
                                              std::int64_t tick_size) noexcept {
        MomentResult out;
        if (ladder.empty() || tick_size <= 0) {
            return out;
        }
        long double sum_w = 0.0L;
        long double sum_wx = 0.0L;
        for (std::size_t i = 0; i < ladder.size(); ++i) {
            const long double w = static_cast<long double>(ladder.volume_at(i));
            const long double x = static_cast<long double>(ladder.price_at(i) - reference)
                                  / static_cast<long double>(tick_size);
            sum_w += w;
            sum_wx += w * x;
        }
        if (sum_w <= 0.0L) {
            return out;
        }
        const long double mean = sum_wx / sum_w;

        long double m2 = 0.0L;
        long double m3 = 0.0L;
        long double m4 = 0.0L;
        for (std::size_t i = 0; i < ladder.size(); ++i) {
            const long double w = static_cast<long double>(ladder.volume_at(i));
            const long double x = static_cast<long double>(ladder.price_at(i) - reference)
                                  / static_cast<long double>(tick_size);
            const long double d = x - mean;
            m2 += w * d * d;
            m3 += w * d * d * d;
            m4 += w * d * d * d * d;
        }
        m2 /= sum_w;
        m3 /= sum_w;
        m4 /= sum_w;

        out.defined = true;
        out.mean_tick = static_cast<double>(mean);
        out.variance_tick2 = static_cast<double>(m2);

        if (m2 > 1e-15L) {
            const long double s = std::sqrt(m2);
            out.skewness = static_cast<double>(m3 / (s * s * s));
            out.excess_kurtosis = static_cast<double>(m4 / (m2 * m2) - 3.0L);
            out.bimodality = bimodality_coefficient(out.skewness, out.excess_kurtosis,
                                                    static_cast<double>(ladder.size()));
        } else {
            out.skewness = 0.0;
            out.excess_kurtosis = 0.0;
            out.bimodality = 0.0;
        }
        return out;
    }

    // BC = (skew^2 + 1) / (kurt + 3*(n-1)^2/((n-2)(n-3))).
    // BC > 0.555 is the conventional bimodality hint (A9 shape descriptor).
    [[nodiscard]] static double bimodality_coefficient(double skewness,
                                                       double excess_kurtosis,
                                                       double n) noexcept {
        if (n <= 3.0) {
            return 0.0;
        }
        const double numerator = skewness * skewness + 1.0;
        const double denom = excess_kurtosis + 3.0 + (3.0 * (n - 1.0) * (n - 1.0))
                             / ((n - 2.0) * (n - 3.0));
        if (denom <= 1e-15) {
            return 0.0;
        }
        return numerator / denom;
    }
};

} // namespace mp
