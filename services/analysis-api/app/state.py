"""
Agent state definitions — the shared state that flows through the LangGraph.

Based on the user's MAS design: 6 bundles, each emitting stance/confidence/dispersion.
Orchestrator weighs bundles by regime. Risk governor can veto/scale.
"""

from typing import Literal

from langgraph.graph import MessagesState
from typing_extensions import TypedDict


# Bundle output — what each of the 6 bundles emits after intra-bundle debate
class BundleVerdict(TypedDict):
    stance: float  # [-1, +1] — weighted average of agent stances
    confidence: float  # [0, 1] — weighted average of agent confidences
    dispersion: float  # std dev of agent stances — internal disagreement
    rationale: str  # human-readable explanation of the debate outcome
    agents: list  # list of individual agent outputs (for audit trail)


# Regime classification — determines bundle weight allocation
RegimeType = Literal[
    "trending", "ranging", "high_volatility", "low_volatility", "news_heavy", "risk_off", "risk_on"
]


class TradingDeskState(MessagesState):
    # Input
    asset: str  # e.g. "EUR/USD" or "BTC/USDT"
    asset_class: str  # "forex" or "crypto"
    timeframe: str  # e.g. "4h", "1d"
    trade_date: str  # YYYY-MM-DD

    # Regime (determined before bundle execution)
    regime: RegimeType
    regime_rationale: str

    # Bundle verdicts (6 bundles, each a BundleVerdict)
    technical_verdict: BundleVerdict | None
    orderflow_verdict: BundleVerdict | None
    macro_verdict: BundleVerdict | None
    sentiment_verdict: BundleVerdict | None
    onchain_verdict: BundleVerdict | None  # None for forex
    quant_verdict: BundleVerdict | None

    # Orchestrator output
    orchestrator_score: float  # S* = sum_b(Omega_b(r) * S_b)
    cross_divergence: float  # disagreement across bundles
    conviction: float  # |S*| * (1 - avg_dispersion) * (1 - cross_divergence)
    orchestrator_rationale: str

    # Risk governor output
    risk_verdict: Literal["pass", "veto", "scale_down"]
    risk_scale: float  # 1.0 if pass, 0.0 if veto, 0.0-1.0 if scale_down
    risk_rationale: str

    # Final decision
    final_decision: Literal["buy", "sell", "hold", "wait"]
    final_conviction: float
    final_rationale: str

    # Educational disclaimer (always present)
    disclaimer: str

    # Audit trail (for LangFuse + knowledge base)
    total_tokens: int
    total_cost: float
    pipeline_latency_ms: int
