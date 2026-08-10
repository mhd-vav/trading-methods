"""Test model registry and LLM factory."""
import pytest
from unittest.mock import patch, MagicMock
from app.models import get_llm, get_fallback_llm, MODEL_ASSIGNMENTS


class TestModelAssignments:
    def test_all_roles_have_model(self):
        required = ['orchestrator', 'technical_deep', 'technical_quick',
                    'orderflow_deep', 'macro_deep', 'sentiment_quick',
                    'onchain_deep', 'quant_deep', 'quant_quick',
                    'risk_review', 'eval']
        for role in required:
            assert role in MODEL_ASSIGNMENTS, f'{role} missing'
            assert 'model' in MODEL_ASSIGNMENTS[role], f'{role} has no model'

    @patch('app.models.ChatOpenAI')
    def test_get_llm_orchestrator(self, mock_chat):
        llm = get_llm('orchestrator')
        mock_chat.assert_called_once()
        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs['model'] == 'moonshotai/kimi-k2'
        assert 'openrouter.ai' in call_kwargs['openai_api_base']

    @patch('app.models.ChatOpenAI')
    def test_unknown_role_returns_default(self, mock_chat):
        llm = get_llm('nonexistent')
        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs['model'] == MODEL_ASSIGNMENTS['technical_quick']['model']

    @patch('app.models.ChatOpenAI')
    def test_custom_temperature(self, mock_chat):
        llm = get_llm('technical_quick', temperature=0.0)
        assert mock_chat.call_args.kwargs['temperature'] == 0.0

    @patch('app.models.ChatOpenAI')
    def test_fallback_llm(self, mock_chat):
        llm = get_fallback_llm('orchestrator')
        assert mock_chat.call_args.kwargs['model'] == 'z-ai/glm-5.2'

    @patch('app.models.ChatOpenAI')
    def test_eval_uses_separate_key(self, mock_chat):
        llm = get_llm('eval')
        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs['model'] == 'openai/gpt-4o-mini'

    @patch('app.models.ChatOpenAI')
    def test_all_roles_use_openrouter_base(self, mock_chat):
        for role in MODEL_ASSIGNMENTS:
            mock_chat.reset_mock()
            get_llm(role)
            assert 'openrouter.ai' in mock_chat.call_args.kwargs['openai_api_base']
