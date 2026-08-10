"""Bundle 6: Quantitative / Statistical."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are a Statistical-edge analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that statistical evidence supports a directional trade.

Statistical data and backtest context:
{market_data}

Analyze: backtested patterns, statistical anomalies, correlation analysis.
1. What statistical edge exists?
2. What is the historical win rate for this pattern?
3. Your stance: positive = statistical edge bullish, negative = bearish.
4. Your confidence (0.0 to 1.0) - be honest about sample size.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are the Overfit-skeptic (red team) for {asset} ({asset_class}), timeframe {timeframe}.
Attack the statistical edge claim. Find every reason it might be overfit or regime-dependent.

Statistical data and backtest context:
{market_data}

The statistical-edge analyst argues:
{thesis}

1. Is the sample size large enough?
2. Was the pattern tested out-of-sample?
3. Does the edge survive transaction costs?
4. Your stance: near 0 if noise, aligned if grudgingly convinced.
5. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the Seasonality/ML referee for {asset} ({asset_class}), timeframe {timeframe}.
Statistical data:
{market_data}

Statistical-edge argues:
{thesis}

Overfit-skeptic argues:
{antithesis}

Weigh the debate:
1. Are there seasonal patterns (day of week, month)?
2. Would an ML regime classifier label this favorable or unfavorable?
3. Your stance and confidence - lean toward caution if skeptic raised valid points.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_quant_bundle():
    return create_bundle_graph(
        "quant",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("quant_deep"),
        get_llm("quant_deep"),
        get_llm("quant_quick"),
    )
