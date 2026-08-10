"""Test risk governor logic."""
import pytest
from app.risk_governor import risk_check


class TestRiskCheck:
    def test_low_conviction_passes(self):
        result = risk_check(0.0, 0.05, 'EUR/USD', 'forex', 'trending')
        assert result['verdict'] == 'pass'
        assert result['scale'] == 1.0

    def test_high_vol_low_conviction_scale_down(self):
        result = risk_check(0.2, 0.2, 'EUR/USD', 'forex', 'high_volatility')
        assert result['verdict'] == 'scale_down'
        assert result['scale'] == 0.5

    def test_risk_off_with_bullish_signal_scale_down(self):
        result = risk_check(0.5, 0.5, 'EUR/USD', 'forex', 'risk_off')
        assert result['verdict'] == 'scale_down'
        assert result['scale'] == 0.3

    def test_normal_conditions_pass(self):
        result = risk_check(0.2, 0.4, 'EUR/USD', 'forex', 'trending')
        assert result['verdict'] == 'pass'

    def test_risk_on_pass(self):
        result = risk_check(0.3, 0.5, 'EUR/USD', 'forex', 'risk_on')
        assert result['verdict'] == 'pass'

    def test_ranging_pass(self):
        result = risk_check(0.1, 0.3, 'EUR/USD', 'forex', 'ranging')
        assert result['verdict'] == 'pass'
