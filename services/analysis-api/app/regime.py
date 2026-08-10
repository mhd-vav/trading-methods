"""Regime classifier - determines market regime before bundle execution."""

from app.models import get_llm

REGIME_PROMPT = """You are a market regime classifier for {asset} ({asset_class}), timeframe {timeframe}.

Market data:
{market_data}

Classify the current market regime. Respond with exactly ONE of:
- trending (clear directional move, ADX > 25, MAs aligned)
- ranging (sideways, ADX < 20, price oscillating between S/R)
- high_volatility (ATR expanding, VIX/equivalent elevated, large candles)
- low_volatility (ATR contracting, Bollinger squeeze, small candles)
- news_heavy (major economic events imminent or just released)
- risk_off (broad market de-risking, safe haven flows)
- risk_on (broad risk appetite, risk assets bid)

Also provide a one-sentence rationale.

Format: REGIME: <regime_name> | RATIONALE: <one sentence>"""


def classify_regime(asset: str, asset_class: str, timeframe: str, market_data: str) -> dict:
    """Classify the current market regime using the orchestrator LLM."""
    llm = get_llm("orchestrator", temperature=0.1)
    prompt = REGIME_PROMPT.format(
        asset=asset, asset_class=asset_class, timeframe=timeframe, market_data=market_data
    )
    resp = llm.invoke(prompt)
    content = resp.content.upper()

    regimes = [
        "trending",
        "ranging",
        "high_volatility",
        "low_volatility",
        "news_heavy",
        "risk_off",
        "risk_on",
    ]
    regime = "trending"  # default
    for r in regimes:
        if r.upper() in content:
            regime = r
            break

    rationale = resp.content
    return {"regime": regime, "regime_rationale": rationale}
