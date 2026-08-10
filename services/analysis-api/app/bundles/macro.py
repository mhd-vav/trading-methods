"""Bundle 3: Macro / Fundamental."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are a Monetary-policy analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that central bank policy and fundamentals support the current price direction.

Market data and macro context:
{market_data}

Analyze: interest rates, central bank stance, yield curves, economic calendar.
1. Is monetary policy supportive or restrictive?
2. Are upcoming events likely to reinforce or disrupt?
3. Your stance: positive = fundamentals bullish, negative = bearish.
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are a Data-surprise analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that only unexpected data surprises move price, and fundamentals are priced in.

Market data and macro context:
{market_data}

The monetary-policy analyst argues:
{thesis}

1. Is the fundamental backdrop already reflected in price?
2. What recent data surprised vs consensus?
3. Your stance: positive = surprise was bullish, negative = bearish, near 0 = priced in.
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the Intermarket referee for {asset} ({asset_class}), timeframe {timeframe}.
Market data:
{market_data}

Monetary-policy argues:
{thesis}

Data-surprise argues:
{antithesis}

Weigh using cross-asset context:
1. Are related markets (equities, bonds, DXY) confirming or diverging?
2. Is risk sentiment (VIX, credit spreads) supportive or cautionary?
3. Your stance and confidence.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_macro_bundle():
    return create_bundle_graph(
        "macro",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("macro_deep"),
        get_llm("macro_deep"),
        get_llm("macro_deep"),
    )
