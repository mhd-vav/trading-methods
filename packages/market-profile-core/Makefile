# Build for the Market Profile engine. No CMake dependency.
CXX      ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Wpedantic -Iinclude
LDFLAGS  ?=

SRC_DIR := src
TST_DIR := tests
INC_DIR := include

BIN := build
TARGETS := $(BIN)/mp_demo $(BIN)/mp_profile $(BIN)/test_profile $(BIN)/test_risk

.PHONY: all test clean run

all: $(TARGETS)

$(BIN)/mp_demo: $(SRC_DIR)/main.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)

$(BIN)/mp_profile: $(SRC_DIR)/profile_dump.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)

$(BIN)/test_profile: $(TST_DIR)/test_profile_engine.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)

$(BIN)/test_risk: $(TST_DIR)/test_risk.cpp | $(BIN)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)

$(BIN):
	mkdir -p $(BIN)

test: $(BIN)/test_profile $(BIN)/test_risk
	@echo "--- profile engine tests ---"
	./$(BIN)/test_profile
	@echo "--- risk tests ---"
	./$(BIN)/test_risk

run: $(BIN)/mp_demo
	./$(BIN)/mp_demo

profile: $(BIN)/mp_profile
	./$(BIN)/mp_profile

clean:
	rm -rf $(BIN)
