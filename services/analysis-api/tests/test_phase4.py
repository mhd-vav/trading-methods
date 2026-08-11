"""Phase 4 tests — evidence snapshot, idempotency, checkpointing, engine."""
import pytest
from app.evidence import EvidenceSnapshot, build_snapshot, OhlcEvidence, CandleWindowEvidence
from app.checkpoint import CheckpointStore, RunProgressTracker, IdempotencyStore, MemoryStoreBackend
from app.engine import run_analysis


class _FakeGraph:
    """Stub LangGraph: invoke() returns no agents (neutral verdicts)."""
    def invoke(self, _state, **kw):
        return {"agents_output": []}


@pytest.fixture(autouse=True)
def _no_llm(monkeypatch):
    """Replace bundle-graph constructors and regime/risk with stubs so engine
    tests exercise orchestration/idempotency/provenance without real LLM I/O."""
    from app import engine
    for name in ("create_technical_bundle", "create_orderflow_bundle", "create_macro_bundle",
                 "create_sentiment_bundle", "create_onchain_bundle", "create_quant_bundle"):
        monkeypatch.setattr(engine, name, lambda: _FakeGraph())
    monkeypatch.setattr(engine, "classify_regime", lambda *a, **k: {"regime": "trending", "regime_rationale": "r"})
    monkeypatch.setattr(engine, "risk_check", lambda *a, **k: {"verdict": "pass", "scale": 1.0, "rationale": "r"})


def make_candle_window():
    return {
        "symbol": "BTC/USDT",
        "interval": "4h",
        "candles": [
            {"id": "c0", "symbol": "BTC/USDT", "interval": "4h", "startMs": 0, "o": 100, "h": 101, "l": 99, "c": 100, "v": 10, "isFinal": True},
            {"id": "c1", "symbol": "BTC/USDT", "interval": "4h", "startMs": 14400000, "o": 100, "h": 102, "l": 98, "c": 101, "v": 12, "isFinal": True},
        ],
        "indicators": {"sma20": [100.5, 100.8]},
        "dataQualityFlags": [],
    }


class TestEvidenceSnapshot:
    def test_build_flags_missing_evidence(self):
        snap = build_snapshot("BTC/USDT", "crypto", "4h", candle_data=make_candle_window())
        assert snap.snapshot_id.startswith("ev_")
        assert "onchain_unavailable" in snap.missing_evidence_flags
        assert "news_unavailable" in snap.missing_evidence_flags
        assert snap.candle_window is not None
        assert snap.candle_window.symbol == "BTC/USDT"

    def test_content_hash_deterministic(self):
        a = EvidenceSnapshot(asset="X", asset_class="forex", timeframe="1h", snapshot_id="a", createdAtMs=0)
        b = EvidenceSnapshot(asset="X", asset_class="forex", timeframe="1h", snapshot_id="b", createdAtMs=0)
        assert a.content_hash() == b.content_hash()

    def test_create_derives_distinct_ids(self):
        s1 = build_snapshot("X", "forex", "1h")
        s2 = build_snapshot("X", "forex", "1h")
        assert s1.snapshot_id != s2.snapshot_id  # nonce-salted

    def test_to_agent_context_contains_snapshot(self):
        snap = build_snapshot("BTC/USDT", "crypto", "4h", candle_data=make_candle_window())
        ctx = snap.to_agent_context()
        assert "SNAPSHOT:" in ctx
        assert "LAST 2 CANDLES" in ctx

    def test_build_accepts_news_and_flags_nothing(self):
        snap = build_snapshot("X", "crypto", "1h",
                              news=[{"id": "n1", "headline": "Fed hikes", "source": "r", "publishedAtMs": 0}],
                              onchain={"symbol": "X", "available": True})
        assert "news_unavailable" not in snap.missing_evidence_flags
        assert snap.onchain is not None


class TestIdempotency:
    def test_store_and_replay(self):
        store = IdempotencyStore()
        assert store.try_resume("k1") is None
        store.put("k1", {"final_decision": "buy"})
        assert store.try_resume("k1")["final_decision"] == "buy"

    def test_missing_is_none(self):
        assert IdempotencyStore().try_resume("nope") is None


class TestCheckpoint:
    def test_tracker_records_progress(self):
        store = CheckpointStore()
        tracker = RunProgressTracker("run-1", store)
        tracker.mark("started", "ok")
        tracker.mark("done", "ok", {"decision": "hold"})
        snap = tracker.snapshot()
        assert snap["statuses"]["started"] == "ok"
        assert store.read("run-1", "progress") is not None


class TestEngineIdempotency:
    def test_replays_identical_result_for_same_key(self, monkeypatch):
        # Force run_analysis' LLM-dependent pieces to be deterministic/no-op.
        from app import engine
        calls = {"n": 0}

        def fake_classify(*a, **k):
            return {"regime": "trending", "regime_rationale": "r"}

        def fake_risk(*a, **k):
            return {"verdict": "pass", "scale": 1.0, "rationale": "r"}

        monkeypatch.setattr(engine, "classify_regime", fake_classify)
        monkeypatch.setattr(engine, "risk_check", fake_risk)

        # Build a snapshot that has no candle window so bundles get empty context
        snap = build_snapshot("X/USD", "forex", "4h")
        store = IdempotencyStore()

        r1 = run_analysis("X/USD", "forex", "4h", snapshot=snap,
                          idempotency_key="idem-1", idempotency_store=store)
        # second call — bundles still run (no LLM here; they return empty agents => neutral)
        r2 = run_analysis("X/USD", "forex", "4h", snapshot=snap,
                          idempotency_key="idem-1", idempotency_store=store)
        assert r2["_replayed_from_idempotency_key"] == "idem-1"
        assert r2["final_decision"] == r1["final_decision"]


class TestEngineProvenance:
    def test_result_carries_snapshot_provenance(self, monkeypatch):
        from app import engine
        monkeypatch.setattr(engine, "classify_regime", lambda *a, **k: {"regime": "trending", "regime_rationale": "r"})
        monkeypatch.setattr(engine, "risk_check", lambda *a, **k: {"verdict": "pass", "scale": 1.0, "rationale": "r"})
        snap = build_snapshot("BTC/USDT", "crypto", "4h", candle_data=make_candle_window())
        res = run_analysis("BTC/USDT", "crypto", "4h", snapshot=snap)
        assert res["provenance"]["snapshot_id"] == snap.snapshot_id
        assert res["provenance"]["prompt_version"] == "v1"
        assert "model_roles" in res["provenance"]
        assert res["progress"]["statuses"]["evidence_frozen"] == "ok"
