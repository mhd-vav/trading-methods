"""Test aggregation math — no LLM calls, pure logic."""
import pytest
from app.aggregation import aggregate_bundle, aggregate_orchestrator, get_decision, get_regime_weights


class TestAggregateBundle:
    def test_empty_agents(self):
        result = aggregate_bundle([])
        assert result['stance'] == 0.0
        assert result['confidence'] == 0.0
        assert result['dispersion'] == 0.0

    def test_single_agent_bullish(self):
        agents = [{'name': 'a', 'weight': 1.0, 'confidence': 0.9, 'stance': 0.8}]
        result = aggregate_bundle(agents)
        assert result['stance'] > 0.7
        assert result['confidence'] == 0.9
        assert result['dispersion'] == 0.0

    def test_two_agents_disagree(self):
        agents = [
            {'name': 'bull', 'weight': 1.0, 'confidence': 0.8, 'stance': 0.6},
            {'name': 'bear', 'weight': 1.0, 'confidence': 0.8, 'stance': -0.4},
        ]
        result = aggregate_bundle(agents)
        assert 0.0 < result['stance'] < 0.3
        assert result['dispersion'] > 0.0

    def test_low_confidence_dilutes_weight(self):
        agents = [
            {'name': 'confident', 'weight': 1.0, 'confidence': 1.0, 'stance': 1.0},
            {'name': 'unsure', 'weight': 1.0, 'confidence': 0.1, 'stance': -1.0},
        ]
        result = aggregate_bundle(agents)
        assert result['stance'] > 0.5  # confident agent dominates


class TestRegimeWeights:
    def test_all_regimes_sum_to_1(self):
        from app.aggregation import REGIME_WEIGHTS
        for regime, weights in REGIME_WEIGHTS.items():
            total = sum(weights.values())
            assert abs(total - 1.0) < 0.01, f'{regime} weights sum to {total}'

    def test_forex_removes_onchain(self):
        weights = get_regime_weights('trending', 'forex')
        assert weights.get('onchain', 0) == 0.0
        assert abs(sum(weights.values()) - 1.0) < 0.01

    def test_crypto_keeps_onchain(self):
        weights = get_regime_weights('trending', 'crypto')
        assert weights.get('onchain', 0) > 0.0


class TestAggregateOrchestrator:
    def test_unanimous_bullish(self):
        bundles = {
            'technical': {'stance': 0.8, 'dispersion': 0.0},
            'orderflow': {'stance': 0.7, 'dispersion': 0.0},
            'macro': {'stance': 0.6, 'dispersion': 0.0},
            'sentiment': {'stance': 0.5, 'dispersion': 0.0},
            'quant': {'stance': 0.9, 'dispersion': 0.0},
        }
        result = aggregate_orchestrator(bundles, 'trending', 'crypto')
        assert result['orchestrator_score'] > 0.5
        assert result['conviction'] > 0.4
        assert result['cross_divergence'] < 0.3

    def test_mixed_signals(self):
        bundles = {
            'technical': {'stance': 0.8, 'dispersion': 0.1},
            'orderflow': {'stance': -0.6, 'dispersion': 0.2},
            'macro': {'stance': 0.1, 'dispersion': 0.1},
            'sentiment': {'stance': -0.3, 'dispersion': 0.1},
            'quant': {'stance': 0.5, 'dispersion': 0.2},
        }
        result = aggregate_orchestrator(bundles, 'ranging', 'crypto')
        # Mixed signals should produce lower conviction
        assert result['conviction'] < 0.5


class TestGetDecision:
    def test_risk_veto(self):
        result = get_decision(0.8, 0.9, 'veto', 0.0)
        assert result['decision'] == 'hold'
        assert result['conviction'] == 0.0

    def test_risk_scale_down(self):
        result = get_decision(0.5, 0.8, 'scale_down', 0.5)
        assert result['decision'] in ('buy', 'sell', 'hold', 'wait')

    def test_buy_signal(self):
        result = get_decision(0.5, 0.7, 'pass', 1.0)
        assert result['decision'] == 'buy'

    def test_sell_signal(self):
        result = get_decision(-0.5, 0.7, 'pass', 1.0)
        assert result['decision'] == 'sell'

    def test_low_conviction_wait(self):
        result = get_decision(0.8, 0.1, 'pass', 1.0)
        assert result['decision'] == 'wait'
