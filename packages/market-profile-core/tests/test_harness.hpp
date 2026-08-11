// tests/test_harness.hpp
// Minimal self-contained test harness so the suite has no external dependency.
#pragma once

#include <cmath>
#include <cstdio>
#include <functional>
#include <string>
#include <vector>

namespace test_harness {

struct Failure {
    std::string expr;
    std::string file;
    int line;
};

inline std::vector<Failure>& failures() {
    static std::vector<Failure> instance;
    return instance;
}

struct TestCase {
    std::string name;
    std::function<void()> fn;
};

inline std::vector<TestCase>& cases() {
    static std::vector<TestCase> instance;
    return instance;
}

inline void register_case(const char* name, std::function<void()> fn) {
    cases().push_back({name, std::move(fn)});
}

inline int check_impl(bool condition, const char* expr, const char* file, int line) {
    if (!condition) {
        failures().push_back({expr, file, line});
        std::printf("  FAIL: %s (%s:%d)\n", expr, file, line);
    }
    return 0;
}

struct Approx {
    double value;
    double epsilon;
    explicit Approx(double value_, double eps = 1e-9) : value(value_), epsilon(eps) {}
    bool operator==(double other) const {
        return std::fabs(other - value) <= epsilon;
    }
};

inline int run_all() {
    int failed = 0;
    for (const auto& tc : cases()) {
        const std::size_t before = failures().size();
        std::printf("[ RUN ] %s\n", tc.name.c_str());
        tc.fn();
        if (failures().size() > before) {
            ++failed;
            std::printf("[FAIL ] %s\n\n", tc.name.c_str());
        } else {
            std::printf("[PASS ] %s\n\n", tc.name.c_str());
        }
    }
    std::printf("==== %zu test(s), %d failed ====\n", cases().size(), failed);
    return failed ? 1 : 0;
}

} // namespace test_harness

#define CHECK(cond) ::test_harness::check_impl((cond), #cond, __FILE__, __LINE__)
#define CHECK_APPROX(actual, expected) \
    ::test_harness::check_impl( \
        (::test_harness::Approx(expected) == static_cast<double>(actual)), \
        #actual " ~= " #expected, __FILE__, __LINE__)

// TEST_CASE("name") { body } expands to a uniquely-named static function plus a
// namespace-scope registrar whose constructor enrolls it. Uniqueness comes from
// __LINE__ (monotonic within a file), avoiding string-literal token pasting.
#define MP_PASTE(a, b) a##b
#define MP_XPASTE(a, b) MP_PASTE(a, b)
#define MP_UNIQUE(base) MP_XPASTE(base, __LINE__)
#define TEST_CASE(name)                                              \
    static void MP_UNIQUE(mp_test_fn_)();                           \
    namespace {                                                      \
    struct MP_UNIQUE(mp_test_reg_) {                                \
        MP_UNIQUE(mp_test_reg_)() {                                 \
            ::test_harness::register_case(name, MP_UNIQUE(mp_test_fn_)); \
        }                                                            \
    } MP_UNIQUE(mp_test_inst_);                                      \
    }                                                                \
    static void MP_UNIQUE(mp_test_fn_)()
