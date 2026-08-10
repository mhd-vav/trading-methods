"""Aggregation math — the formal formulas from the MAS design.

Normalized (Phase 0): de-obfuscated string handling from the imported Hostinger
source; behavior preserved. Orchestrator aggregation only considers bundles that
have an explicit `status == "ok"` (engine marks failed bundles, they are excluded),
so failures never silently become neutral votes.
"""

from __future__ import annotations

import math


def aggregate_bundle(agents):
    if not agents:
        return {
            "stance": 0.0,
            "confidence": 0.0,
            "dispersion": 0.0,
            "rationale": "No agents",
            "agents": [],
            "status": "ok",
        }
    total_weight = sum(a["weight"] * a["confidence"] for a in agents)
    if total_weight == 0:
        total_weight = 1.0
    stance = sum(a["weight"] * a["confidence"] * a["stance"] for a in agents) / total_weight
    variance = sum(a["weight"] * a["confidence"] * (a["stance"] - stance) ** 2 for a in agents) / total_weight
    dispersion = math.sqrt(max(0.0, variance))
    confidence = sum(a["weight"] * a["confidence"] for a in agents) / len(agents)
    parts = [f"  [{a.get('name', 'agent')}] stance={a['stance']:+.2f}" for a in agents]
    return {
        "stance": round(stance, 4),
        "confidence": round(confidence, 4),
        "dispersion": round(dispersion, 4),
        "rationale": "\n".join(parts),
        "agents": agents,
        "status": "ok",
    }


REGIME_WEIGHTS = {
    "trending": {
        "technical": 0.35,
        "orderflow": 0.15,
        "macro": 0.15,
        "sentiment": 0.10,
        "onchain": 0.10,
        "quant": 0.15,
    },
    "ranging": {
        "technical": 0.25,
        "orderflow": 0.20,
        "macro": 0.10,
        "sentiment": 0.15,
        "onchain": 0.10,
        "quant": 0.20,
    },
    "high_volatility": {
        "technical": 0.20,
        "orderflow": 0.30,
        "macro": 0.15,
        "sentiment": 0.15,
        "onchain": 0.10,
        "quant": 0.10,
    },
    "low_volatility": {
        "technical": 0.30,
        "orderflow": 0.10,
        "macro": 0.20,
        "sentiment": 0.10,
        "onchain": 0.10,
        "quant": 0.20,
    },
    "news_heavy": {
        "technical": 0.15,
        "orderflow": 0.15,
        "macro": 0.35,
        "sentiment": 0.20,
        "onchain": 0.05,
        "quant": 0.10,
    },
    "risk_off": {
        "technical": 0.15,
        "orderflow": 0.10,
        "macro": 0.30,
        "sentiment": 0.25,
        "onchain": 0.05,
        "quant": 0.15,
    },
    "risk_on": {
        "technical": 0.25,
        "orderflow": 0.20,
        "macro": 0.15,
        "sentiment": 0.15,
        "onchain": 0.15,
        "quant": 0.10,
    },
}


def get_regime_weights(regime, asset_class="forex"):
    weights = REGIME_WEIGHTS.get(regime, REGIME_WEIGHTS["trending"]).copy()
    if asset_class == "forex":
        onchain_w = weights.get("onchain", 0)
        weights["onchain"] = 0.0
        remaining = {k: v for k, v in weights.items() if k != "onchain" and v > 0}
        total = sum(remaining.values())
        for k in remaining:
            weights[k] += onchain_w * (remaining[k] / total) if total > 0 else 0
    return weights


def aggregate_orchestrator(bundles, regime, asset_class="forex"):
    """Aggregate only `status == ok` bundles. Missing or errored bundles are excluded."""
    weights = get_regime_weights(regime, asset_class)
    score = 0.0
    considered = []
    for bn, w in weights.items():
        v = bundles.get(bn)
        if v and v.get("status", "ok") == "ok" and v.get("stance") is not None:
            score += w * v["stance"]
            considered.append(v)

    ad = [v["dispersion"] for v in considered if v.get("dispersion") is not None]
    avg_d = sum(ad) / len(ad) if ad else 0.0
    ast = [v["stance"] for v in considered if v.get("stance") is not None]
    if len(ast) > 1:
        ms = sum(ast) / len(ast)
        cd = math.sqrt(sum((s - ms) ** 2 for s in ast) / len(ast))
    else:
        cd = 0.0
    conv = abs(score) * (1 - avg_d) * (1 - cd)
    conv = max(0.0, min(1.0, conv))
    return {
        "orchestrator_score": round(score, 4),
        "avg_dispersion": round(avg_d, 4),
        "cross_divergence": round(cd, 4),
        "conviction": round(conv, 4),
        "regime": regime,
        "weights": weights,
    }


def get_decision(score, conviction, risk_verdict, risk_scale, conviction_threshold=0.3):
    if risk_verdict == "veto":
        return {"decision": "hold", "conviction": 0.0, "rationale": "Risk governor vetoed."}
    es = score * risk_scale if risk_verdict == "scale_down" else score
    ec = conviction * risk_scale if risk_verdict == "scale_down" else conviction
    if ec < conviction_threshold:
        return {"decision": "wait", "conviction": ec, "rationale": f"Conviction {ec:.2f} below threshold."}
    if es > 0.15:
        return {"decision": "buy", "conviction": ec, "rationale": f"Positive stance ({es:+.2f})."}
    elif es < -0.15:
        return {"decision": "sell", "conviction": ec, "rationale": f"Negative stance ({es:+.2f})."}
    else:
        return {"decision": "hold", "conviction": ec, "rationale": f"Neutral ({es:+.2f})."}
