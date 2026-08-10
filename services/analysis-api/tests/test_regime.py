"""Test regime classification logic (mocked LLM)."""
import pytest
from unittest.mock import MagicMock, patch
from app.regime import classify_regime


class TestClassifyRegime:
    @patch('app.regime.get_llm')
    def test_trending_regime(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = 'REGIME: trending | RATIONALE: Clear uptrend with aligned MAs'
        mock_get_llm.return_value = mock_llm

        result = classify_regime('EUR/USD', 'forex', '4h', 'price=1.0850')
        assert result['regime'] == 'trending'

    @patch('app.regime.get_llm')
    def test_risk_off_regime(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = 'REGIME: risk_off | RATIONALE: Broad de-risking in markets'
        mock_get_llm.return_value = mock_llm

        result = classify_regime('EUR/USD', 'forex', '4h', 'price=1.0500')
        assert result['regime'] == 'risk_off'

    @patch('app.regime.get_llm')
    def test_defaults_to_trending(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = 'garbled nonsense'
        mock_get_llm.return_value = mock_llm

        result = classify_regime('BTC/USDT', 'crypto', '1d', 'price=60000')
        assert result['regime'] == 'trending'
