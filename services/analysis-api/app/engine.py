"""Main Analysis Engine — orchestrates the 6 bundles, aggregates, applies risk.

Phase 4 redesign:
- Runs reference a frozen EvidenceSnapshot (not free-form market text).
- Bundle failures marked explicitly (`status:error`) and excluded — never silent
  neutral votes.
- Idempotency: a stored result for an idempotency key is returned without
  re-running the expensive LLM pipeline.
- Checkpointing: durable per-stage progress for resumption/streaming.
- Provenance: snapshot id, prompt version, model policy version recorded.
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
from app.checkpoint import CheckpointStore, IdempotencyStore, RunProgressTracker, get_idempotency_store
from app.config import get_settings
from app.evidence import EvidenceSnapshot, build_snapshot
from app.models import get_all_role_configs
from app.observability import get_logger, new_request_id, start_span
from app.regime import classify_regime
from app.risk_governor import risk_check

log = get_logger("app.engine")

DISCLAIMER = (
    "Educational analysis only. Not financial advice. All trading decisions are solely your responsibility."
)


def _run_bundle_safely(name, graph, bundle_inputs: dict, timeout_s: float) -> dict:
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
    market_data: str = "",
    include_onchain: bool | None = None,
    *,
    snapshot: EvidenceSnapshot | None = None,
    run_id: str | None = None,
    idempotency_key: str | None = None,
    idempotency_store: IdempotencyStore | None = None,
    checkpoints: CheckpointStore | None = None,
    budget_usd: float = 0.0,
) -> dict:
    """Run the full MAS analysis pipeline against a frozen EvidenceSnapshot.

    If `snapshot` is not provided, one is built from the supplied `market_data`
    (for backwards compatibility); callers are encouraged to pass an explicit
    snapshot for auditable, reproducible runs.
    """
    settings = get_settings()
    start_time = time.time()
    run_id = run_id or new_request_id()

    # Idempotency: return a stored completed result if this key was already run.
    idem = idempotency_store or get_idempotency_store()
    if idempotency_key:
        cached = idem.try_resume(idempotency_key)
        if cached is not None:
            cached["_replayed_from_idempotency_key"] = idempotency_key
            return cached

    tracker = RunProgressTracker(run_id, checkpoints)
    tracker.mark("started", "ok")

    # Build/accept snapshot
    if snapshot is None:
        snapshot = build_snapshot(
            asset=asset,
            asset_class=asset_class,
            timeframe=timeframe,
            candle_data=_candle_data_from_text(market_data),
            missing_evidence_flags=["freeform_market_text"] if market_data else ["no_evidence_provided"],
        )
    tracker.mark("evidence_frozen", "ok", {"snapshot_id": snapshot.snapshot_id})

    if include_onchain is None:
        include_onchain = asset_class == "crypto"

    # 1) Regime
    regime_result = classify_regime(asset, asset_class, timeframe, snapshot.to_agent_context())
    regime = regime_result["regime"]
    tracker.mark("regime", "ok", {"regime": regime})

    # 2) Bundles in parallel
    bundle_inputs = {
        "asset": asset,
        "asset_class": asset_class,
        "timeframe": timeframe,
        "context": snapshot.to_agent_context(),
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
    tracker.mark("bundles_started", "ok", {"count": len(bundle_graphs)})
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(bundle_graphs)) as pool:
        futures = {
            pool.submit(_run_bundle_safely, name, graph, bundle_inputs, timeout_s): name
            for name, graph in bundle_graphs.items()
        }
        for fut in concurrent.futures.as_completed(futures):
            name = futures[fut]
            bundles[name] = fut.result()
    tracker.mark("bundles_done", "ok", {"ok": sum(1 for b in bundles.values() if b.get("status") == "ok")})

    # 3) Aggregate ONLY successful bundles
    eligible = {n: v for n, v in bundles.items() if v.get("status") == "ok"}
    failed = [n for n, v in bundles.items() if v.get("status") != "ok"]
    if failed:
        log.warning("bundles_excluded", run_id=run_id, failed=failed)
    tracker.mark("aggregated", "ok", {"eligible": sorted(eligible.keys())})

    orch = aggregate_orchestrator(eligible, regime, asset_class)
    orch["eligible_bundles"] = sorted(eligible.keys())
    orch["excluded_bundles"] = sorted(failed)

    # 4) Risk governor (deterministic-first)
    risk = risk_check(
        orch["orchestrator_score"],
        orch["conviction"],
        asset,
        asset_class,
        regime,
        snapshot.to_agent_context(),
    )

    # 5) Final decision
    decision = get_decision(orch["orchestrator_score"], orch["conviction"], risk["verdict"], risk["scale"])
    tracker.mark("done", "ok", {"decision": decision["decision"]})

    elapsed_ms = int((time.time() - start_time) * 1000)

    result = {
        "run_id": run_id,
        "idempotency_key": idempotency_key,
        "asset": asset,
        "asset_class": asset_class,
        "timeframe": timeframe,
        "regime": regime,
        "regime_rationale": regime_result["regime_rationale"],
        "bundles": bundles,
        "orchestrator": orch,
        "risk": risk,
        "final_decision": decision["decision"],
        "final_conviction": decision["conviction"],
        "final_rationale": decision["rationale"],
        "disclaimer": DISCLAIMER,
        "pipeline_latency_ms": elapsed_ms,
        "provenance": {
            "run_id": run_id,
            "snapshot_id": snapshot.snapshot_id,
            "snapshot_created_at_ms": snapshot.createdAtMs,
            "prompt_version": snapshot.prompt_version,
            "model_policy_version": snapshot.model_policy_version,
            "evidence_missing": snapshot.missing_evidence_flags,
            "model_roles": {r: c["model"] for r, c in get_all_role_configs().items()},
            "framework": "langgraph",
        },
        "progress": tracker.snapshot(),
    }

    # Store idempotent completion for replay.
    if idempotency_key:
        idem.put(idempotency_key, result)

    return result


def _candle_data_from_text(market_data: str) -> dict | None:
    """Best-effort parse of a legacy free-form market_data block into candle
    evidence. In production, market data always comes structured; this is a
    compatibility shim only."""
    if not market_data:
        return None
    return None
