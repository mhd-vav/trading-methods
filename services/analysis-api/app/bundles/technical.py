"""Bundle 1: Technical / Price-Action."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are a Trend-continuation analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue WHY the current trend will continue.

Market data:
{market_data}

Analyze: MAs, structure (HH/HL or LH/LL), momentum indicators.
1. Is the trend UP or DOWN?
2. Your confidence (0.0 to 1.0).
3. What would invalidate your thesis?

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are a Mean-reversion analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue WHY the current move is overextended and will revert.

Market data:
{market_data}

The trend analyst argues:
{thesis}

Analyze: RSI, distance from VWAP, Bollinger position.
1. Is the move overextended?
2. Your stance: positive = bounce up expected, negative = fade down expected.
3. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the Structure referee for {asset} ({asset_class}), timeframe {timeframe}.
Market data:
{market_data}

Trend-continuation argues:
{thesis}

Mean-reversion argues:
{antithesis}

Determine which thesis is supported by market structure.
1. Is price making HH/HL (uptrend) or LH/LL (downtrend)?
2. Is price at a key S/R level?
3. Your stance: positive = structure supports up, negative = supports down/reversal.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_technical_bundle():
    return create_bundle_graph(
        "technical",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("technical_deep"),
        get_llm("technical_deep"),
        get_llm("technical_quick"),
    )
