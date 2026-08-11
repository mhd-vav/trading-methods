"""Bundle 5: On-Chain (crypto-only, dormant for Forex)."""

from app.bundles.base import create_bundle_graph
from app.models import get_llm

THESIS_PROMPT = """You are an Exchange-flow analyst for {asset} (crypto), timeframe {timeframe}.
Argue that exchange inflows/outflows signal the next price direction.

On-chain data:
{context}

Analyze: exchange reserves, net flows, whale movements, stablecoin flows.
1. Are coins flowing into exchanges (bearish) or out (bullish)?
2. Are large holders moving coins?
3. Your stance: positive = bullish flows, negative = bearish flows.
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

ANTITHESIS_PROMPT = """You are a Holder-accumulation analyst for {asset} (crypto), timeframe {timeframe}.
Argue that long-term holder behavior overrides short-term exchange flows.

On-chain data:
{context}

The exchange-flow analyst argues:
{thesis}

1. Are long-term holders accumulating or distributing?
2. Is the holder base growing (new addresses, active addresses)?
3. Your stance: positive = holders accumulating (bullish), negative = distributing (bearish).
4. Your confidence (0.0 to 1.0).

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""

REFEREE_PROMPT = """You are the On-chain referee for {asset} (crypto), timeframe {timeframe}.
On-chain data:
{context}

Exchange-flow argues:
{thesis}

Holder-accumulation argues:
{antithesis}

Determine: which signal dominates?
1. Are the signals aligned or diverging?
2. On-chain valuation metrics (MVRV, NVT) - overvalued or undervalued?
3. Your stance and confidence.

Format: STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ..."""


def create_onchain_bundle():
    return create_bundle_graph(
        "onchain",
        THESIS_PROMPT,
        ANTITHESIS_PROMPT,
        REFEREE_PROMPT,
        get_llm("onchain_deep"),
        get_llm("onchain_deep"),
        get_llm("onchain_deep"),
    )
