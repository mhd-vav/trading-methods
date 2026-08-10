"""Risk Governor - mathematical constraint engine + LLM review for edge cases.

The risk governor does NOT debate direction. It constrains action.
It can: pass, veto, or scale_down any verdict from the orchestrator.
"""

from app.models import get_llm


def risk_check(
    orchestrator_score: float,
    conviction: float,
    asset: str,
    asset_class: str,
    regime: str,
    market_data: str = "",
) -> dict:
    """Run risk checks on the orchestrator verdict.

    Returns: {verdict: pass|veto|scale_down, scale: float, rationale: str}
    """
    # --- Rule-based checks (deterministic, no LLM) ---

    # Rule 1: Extreme conviction with high divergence = veto
    # (the system is very confident but bundles strongly disagree -> dangerous)
    if conviction > 0.7 and abs(orchestrator_score) > 0.5:
        # High conviction but we should check cross-divergence externally
        # For now, pass this through to LLM review
        pass

    # Rule 2: Near-zero conviction = pass (orchestrator will say WAIT anyway)
    if conviction < 0.1:
        return {
            "verdict": "pass",
            "scale": 1.0,
            "rationale": "Very low conviction - no risk action needed, orchestrator will recommend WAIT.",
        }

    # Rule 3: Extreme regime-based risk reduction
    if regime == "high_volatility" and conviction < 0.3:
        return {
            "verdict": "scale_down",
            "scale": 0.5,
            "rationale": "High volatility regime with moderate conviction - scaling position to 50%.",
        }

    if regime == "risk_off" and orchestrator_score > 0.3:
        return {
            "verdict": "scale_down",
            "scale": 0.3,
            "rationale": "Risk-off regime with bullish signal - reducing exposure to 30%.",
        }

    # Rule 4: Default pass for normal conditions
    # If conviction is reasonable and regime is not extreme, let it through
    if 0.1 <= conviction <= 0.7 and regime in ("trending", "ranging", "low_volatility", "risk_on"):
        return {
            "verdict": "pass",
            "scale": 1.0,
            "rationale": "Normal conditions - risk governor passes verdict.",
        }

    # --- LLM review for edge cases ---
    # If we reach here, conditions are ambiguous - use LLM to review
    llm = get_llm("risk_review", temperature=0.1)
    review_prompt = f"""You are the Risk Governor for a trading analysis system.

Asset: {asset} ({asset_class})
Regime: {regime}
Orchestrator score: {orchestrator_score:+.4f}
Conviction: {conviction:.4f}

Market data:
{market_data[:2000]}

Assess the risk of acting on this verdict:
1. Is the conviction justified given the regime?
2. Are there any red flags (extreme positioning, upcoming events, low liquidity)?
3. Should this verdict be: pass (proceed), scale_down (reduce size), or veto (do not trade)?

Respond: VERDICT: pass|scale_down|veto | SCALE: 0.0-1.0 | RATIONALE: ..."""

    try:
        resp = llm.invoke(review_prompt)
        content = resp.content.upper()
        verdict = "pass"
        scale = 1.0

        if "VETO" in content:
            verdict = "veto"
            scale = 0.0
        elif "SCALE_DOWN" in content or "SCALE" in content:
            verdict = "scale_down"
            # Try to extract scale
            for line in resp.content.split("\n"):
                if "SCALE:" in line.upper():
                    try:
                        s = float(line.upper().split("SCALE:")[1].strip().split("|")[0].strip().split()[0])
                        scale = max(0.0, min(1.0, s))
                    except (ValueError, IndexError):
                        scale = 0.5

        return {"verdict": verdict, "scale": scale, "rationale": resp.content}
    except Exception as e:
        # If LLM fails, be conservative
        return {
            "verdict": "scale_down",
            "scale": 0.3,
            "rationale": f"Risk LLM unavailable ({e}). Conservative scale-down to 30%.",
        }
