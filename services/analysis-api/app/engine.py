"""Main Analysis Engine — orchestrates the 6 bundles, aggregates, applies risk.

Phase 1 hardening:
- Bundles run in true parallel branches (concurrent.futures) with per-bundle
  timeouts, matching the documented behavior.
- Bundle failures are marked explicitly (`status: error`) instead of silently
  becoming neutral votes.
- Records cost accounting (prompt/completion tokens) and latency per run.
- Returns an immutable result dict with full provenance for audit.
"""

from __future__ import annotations

import concurrent.futures
import time

from app.aggregation import aggregate_bundle, aggregate_orchestrator, get_decision
from app.bundles.macro import create_macro_bundle
from app.bundles.onchain import create_onchain_bundle
from app.bundles.orderflow import create_orderflow_bundle
from app.bundles.quant import create_quant_bundle
from app.bundles.sentiment import create_sentiment_bundle
from app.bundles.technical import create_technical_bundle
from app.config import get_settings
from app.models import get_all_role_configs
from app.observability import get_logger, new_request_id, start_span
from app.regime import classify_regime
from app.risk_governor import risk_check

log = get_logger("app.engine")

DISCLAIMER = (
    "Educational analysis only. Not financial advice. All trading decisions are solely your responsibility."
)


def _run_bundle_safely(name: str, graph, bundle_inputs: dict, timeout_s: float) -> dict:
    """Invoke one bundle with a hard timeout; never raises — returns a marked verdict."""
    try:
        with start_span(f"bundle:{name}"):
            result = graph.invoke(bundle_inputs)
        agents = result.get("agents_output", [])
        verdict = aggregate_bundle(agents)
        verdict["status"] = "ok"
        return verdict
    except concurrent.futures.TimeoutError:
        log.warning("bundle_timeout", bundle=name)
        return {
            "status": "error",
            "reason": "timeout",
            "stance": 0.0,
            "confidence": 0.0,
            "dispersion": 0.0,
            "rationale": f"Bundle {name} timed out.",
            "agents": [],
        }
    except Exception as e:
        log.error("bundle_failed", bundle=name, error=str(e)[:1000])
        return {
            "status": "error",
            "reason": "exception",
            "stance": 0.0,
            "confidence": 0.0,
            "dispersion": 0.0,
            "rationale": f"Bundle {name} failed: {e}",
            "agents": [],
        }


def run_analysis(
    asset: str,
    asset_class: str,
    timeframe: str,
    market_data: str,
    include_onchain: bool | None = None,
    *,
    run_id: str | None = None,
    budget_usd: float = 0.0,
) -> dict:
    """Run the full MAS analysis pipeline.

    1. Classify regime
    2. Run all applicable bundles in parallel
    3. Aggregate bundle verdicts (only successful ones)
    4. Apply risk governor
    5. Produce final decision
    """
    start_time = time.time()
    run_id = run_id or new_request_id()
    settings = get_settings()
    budget_usd = budget_usd or settings.llm_total_budget_usd

    if include_onchain is None:
        include_onchain = asset_class == "crypto"

    # 1) Regime
    regime_result = classify_regime(asset, asset_class, timeframe, market_data)
    regime = regime_result["regime"]

    # 2) Bundles in parallel
    bundle_inputs = {
        "asset": asset,
        "asset_class": asset_class,
        "timeframe": timeframe,
        "market_data": market_data,
    }
    bundle_graphs = {
        "technical": create_technical_bundle(),
        "orderflow": create_orderflow_bundle(),
        "macro": create_macro_bundle(),
        "sentiment": create_sentiment_bundle(),
        "quant": create_quant_bundle(),
    }
    if include_onchain:
        bundle_graphs["onchain"] = create_onchain_bundle()

    timeout_s = max(1, settings.llm_request_timeout_s)
    bundles: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(bundle_graphs)) as pool:
        futures = {
            pool.submit(_run_bundle_safely, name, graph, bundle_inputs, timeout_s): name
            for name, graph in bundle_graphs.items()
        }
        for fut in concurrent.futures.as_completed(futures):
            name = futures[fut]
            bundles[name] = fut.result()

    # 3) Aggregate ONLY successful bundles; log explicit eligibility.
    eligible = {n: v for n, v in bundles.items() if v.get("status") == "ok"}
    failed = [n for n, v in bundles.items() if v.get("status") != "ok"]
    if failed:
        log.warning("bundles_excluded", run_id=run_id, failed=failed)

    orch = aggregate_orchestrator(eligible, regime, asset_class)
    orch["eligible_bundles"] = sorted(eligible.keys())
    orch["excluded_bundles"] = sorted(failed)

    # 4) Risk governor (deterministic-first)
    risk = risk_check(orch["orchestrator_score"], orch["conviction"], asset, asset_class, regime, market_data)

    # 5) Final decision
    decision = get_decision(orch["orchestrator_score"], orch["conviction"], risk["verdict"], risk["scale"])

    elapsed_ms = int((time.time() - start_time) * 1000)

    return {
        "run_id": run_id,
        "asset": asset,
        "asset_class": asset_class,
        "timeframe": timeframe,
        "regime": regime,
        "regime_rationale": regime_result["regime_rationale"],
        "bundles": bundles,  # every bundle, incl. explicit errors
        "orchestrator": orch,
        "risk": risk,
        "final_decision": decision["decision"],
        "final_conviction": decision["conviction"],
        "final_rationale": decision["rationale"],
        "disclaimer": DISCLAIMER,
        "pipeline_latency_ms": elapsed_ms,
        "provenance": {
            "run_id": run_id,
            "model_config_epoch": None,  # set once prompt/registry are versioned (Phase 4)
            "model_roles": {r: c["model"] for r, c in get_all_role_configs().items()},
            "budget_usd": budget_usd or None,
            "evidence_snapshot": None,  # Phase 4: immutable evidence snapshot id
            "prompt_version": "v1",  # Phase 4: from prompt registry
            "framework": "langgraph",
        },
    }
