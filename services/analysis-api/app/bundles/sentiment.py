"""Bundle 4: Sentiment / Positioning / Crowd."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are a Sentiment-confirmation analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that current sentiment and positioning confirm the price move.

Market data and sentiment context:
{context}

Analyze: social sentiment, funding rates, long/short ratios, COT data.
1. Is crowd sentiment aligned with price direction?
2. Are positioning metrics confirming?
3. Your stance: positive = sentiment bullish, negative = bearish.
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are a Contrarian analyst for {asset} ({asset_class}), timeframe {timeframe}.
Argue that sentiment is too crowded and a reversal is likely.

Market data and sentiment context:
{context}

The confirmation analyst argues:
{thesis}

1. Is positioning extreme (everyone on the same side)?
2. Are funding rates signaling a crowded trade?
3. Your stance: positive = contrarian bullish (crowd short), negative = contrarian bearish (crowd long).
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the Positioning referee for {asset} ({asset_class}), timeframe {timeframe}.
Market data:
{context}

Confirmation argues:
{thesis}

Contrarian argues:
{antithesis}

Determine: is positioning extreme enough to favor contrarian, or still confirming?
1. What are the actual long/short ratios and funding rates?
2. Is this level historically extreme or normal?
3. Your stance and confidence.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_sentiment_bundle():
    return create_bundle_graph(
        "sentiment",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("sentiment_quick"),
        get_llm("sentiment_quick"),
        get_llm("sentiment_quick"),
    )
