"""Bundle 2: Order-Flow / Microstructure."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are a Participation/confirmation analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that the current price move is backed by real order flow.

Market data:
{context}

Analyze: volume profile, cumulative delta, order book imbalance.
1. Is volume confirming the price move?
2. Is delta aligned with direction?
3. Your stance: positive = bullish flow, negative = bearish flow.
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are an Absorption/fakeout analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that the price move is being absorbed by resting liquidity (fakeout).

Market data:
{context}

The participation analyst argues:
{thesis}

1. Is there large resting liquidity absorbing the move?
2. Is volume diverging from price?
3. Your stance: positive = absorption of selling (bullish), negative = absorption of buying (bearish).
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the Imbalance referee for {asset} ({asset_class}), timeframe {timeframe}.
Market data:
{context}

Participation argues:
{thesis}

Absorption argues:
{antithesis}

Determine: is the order flow genuinely directional or being absorbed?
1. Are there sustained imbalances in the order book?
2. Is cumulative delta trending or flat?
3. Your stance and confidence.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_orderflow_bundle():
    return create_bundle_graph(
        "orderflow",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("orderflow_deep"),
        get_llm("orderflow_deep"),
        get_llm("orderflow_deep"),
    )
