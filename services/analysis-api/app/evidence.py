"""EvidenceSnapshot — the immutable evidence contract for the analysis engine.

Phase 4 replaces the old free-form `market_data` string with a versioned,
frozen EvidenceSnapshot. Every analysis run references a snapshot ID; agents
never receive unstructured market text. Factors are optional and carry
missing-evidence flags, so the engine can represent degraded runs explicitly.

Immutability is enforced by convention (frozen dataclasses / pydantic models)
and by a content-hash snapshot ID.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid

from pydantic import BaseModel, Field


class NewsEvidence(BaseModel):
    id: str
    headline: str
    source: str
    publishedAtMs: int
    url: str = ""
    impact: float | None = None  # -1..1 sentiment score if available


class CalendarEvidence(BaseModel):
    id: str
    event: str
    currency: str
    impact: str  # high | medium | low
    scheduledAtMs: int
    forecast: str | None = None
    previous: str | None = None


class OhlcEvidence(BaseModel):
    id: str
    symbol: str
    interval: str
    startMs: int
    o: float
    h: float
    l: float  # noqa: E741  (OHLC 'low' field)
    c: float
    v: float
    isFinal: bool


class CandleWindowEvidence(BaseModel):
    symbol: str
    interval: str
    candles: list[OhlcEvidence] = Field(default_factory=list)
    indicators: dict[str, list[float]] = Field(default_factory=dict)
    dataQualityFlags: list[str] = Field(default_factory=list)


class OrderFlowEvidence(BaseModel):
    symbol: str
    cumulativeDelta: float | None = None
    volumeImbalance: float | None = None
    orderBookImbalance: float | None = None
    available: bool = False


class SentimentEvidence(BaseModel):
    symbol: str
    socialScore: float | None = None
    fundingRate: float | None = None
    longShortRatio: float | None = None
    available: bool = False


class OnChainEvidence(BaseModel):
    symbol: str
    exchangeNetflow: float | None = None
    whaleMovements: float | None = None
    stablecoinFlows: float | None = None
    available: bool = False


class EvidenceSnapshot(BaseModel):
    """Frozen evidence for one analysis run."""

    snapshot_id: str
    createdAtMs: int
    asset: str
    asset_class: str  # forex | crypto
    timeframe: str
    candle_window: CandleWindowEvidence | None = None
    news: list[NewsEvidence] = Field(default_factory=list)
    calendar: list[CalendarEvidence] = Field(default_factory=list)
    orderflow: OrderFlowEvidence | None = None
    sentiment: SentimentEvidence | None = None
    onchain: OnChainEvidence | None = None
    prompt_version: str = "v1"  # prompt registry version used
    model_policy_version: str = "v1"
    missing_evidence_flags: list[str] = Field(default_factory=list)

    def content_hash(self) -> str:
        """Deterministic snapshot id from content (excludes snapshot_id itself)."""
        payload = self.model_dump(exclude={"snapshot_id"})
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return "ev_" + hashlib.sha256(canonical.encode()).hexdigest()[:20]

    @classmethod
    def create(cls, **kwargs) -> EvidenceSnapshot:
        """Build a snapshot, deriving snapshot_id from content + time + nonce."""
        kwargs.setdefault("createdAtMs", int(time.time() * 1000))
        obj = cls.model_validate({"snapshot_id": "pending", **kwargs})
        nonce = uuid.uuid4().hex
        snapshot_id = hashlib.sha256(
            (obj.content_hash() + obj.createdAtMs.__str__() + nonce).encode()
        ).hexdigest()[:24]
        return obj.model_copy(update={"snapshot_id": "ev_" + snapshot_id})

    def to_agent_context(self, max_candles: int = 120) -> str:
        """Render a compact, stable text block for prompts (still evidence-based)."""
        lines = [
            f"ASSET: {self.asset} ({self.asset_class}) TF: {self.timeframe}",
            f"SNAPSHOT: {self.snapshot_id}",
        ]
        if self.candle_window:
            recent = self.candle_window.candles[-max_candles:]
            lines.append(
                f"LAST {len(recent)} CANDLES ({self.candle_window.symbol} {self.candle_window.interval}):"
            )
            for c in recent:
                lines.append(
                    f"  {c.startMs} O:{c.o:.5f} H:{c.h:.5f} L:{c.l:.5f} C:{c.c:.5f} V:{c.v:g} final={c.isFinal}"
                )
            for k, vals in self.candle_window.indicators.items():
                lines.append(f"  {k}: {', '.join(f'{v:.4f}' for v in vals[-8:])}")
            if self.candle_window.dataQualityFlags:
                lines.append(f"  DATA-QUALITY: {', '.join(self.candle_window.dataQualityFlags)}")
        if self.news:
            lines.append("NEWS:")
            for n in self.news[-10:]:
                lines.append(f"  [{n.publishedAtMs}] {n.source}: {n.headline}")
        if self.calendar:
            lines.append("CALENDAR:")
            for e in self.calendar[-5:]:
                lines.append(f"  [{e.scheduledAtMs}] {e.currency} {e.event} impact={e.impact}")
        if self.orderflow and self.orderflow.available:
            lines.append(
                f"ORDERFLOW: delta={self.orderflow.cumulativeDelta} imb={self.orderflow.volumeImbalance}"
            )
        if self.sentiment and self.sentiment.available:
            lines.append(
                f"SENTIMENT: social={self.sentiment.socialScore} funding={self.sentiment.fundingRate}"
            )
        if self.onchain and self.onchain.available:
            lines.append(
                f"ONCHAIN: netflow={self.onchain.exchangeNetflow} whale={self.onchain.whaleMovements}"
            )
        if self.missing_evidence_flags:
            lines.append(f"MISSING-EVIDENCE: {', '.join(self.missing_evidence_flags)}")
        return "\n".join(lines)


def build_snapshot(
    asset: str,
    asset_class: str,
    timeframe: str,
    *,
    candle_data: dict | None = None,
    news: list[dict] | None = None,
    calendar: list[dict] | None = None,
    orderflow: dict | None = None,
    sentiment: dict | None = None,
    onchain: dict | None = None,
    prompt_version: str = "v1",
    missing_evidence_flags: list[str] | None = None,
) -> EvidenceSnapshot:
    """Construct an EvidenceSnapshot from whatever evidence the caller has.

    Missing factors are left unset and flagged, so the engine knows exactly what
    evidence a given analysis actually had. This is the basis for auditable,
    reproducible runs.
    """
    flags: list[str] = list(missing_evidence_flags or [])
    cw = None
    if candle_data:
        try:
            cw = CandleWindowEvidence.model_validate(candle_data)
        except Exception:
            flags.append("candle_window_invalid")
    if not orderflow and asset_class == "forex":
        flags.append("orderflow_unavailable")
    if not onchain and asset_class == "crypto":
        flags.append("onchain_unavailable")
    if not news:
        flags.append("news_unavailable")
    if not calendar:
        flags.append("calendar_unavailable")

    return EvidenceSnapshot.create(
        asset=asset,
        asset_class=asset_class,
        timeframe=timeframe,
        candle_window=cw,
        news=[NewsEvidence.model_validate(n) for n in (news or []) if n],
        calendar=[CalendarEvidence.model_validate(e) for e in (calendar or []) if e],
        orderflow=OrderFlowEvidence.model_validate(orderflow) if orderflow else None,
        sentiment=SentimentEvidence.model_validate(sentiment) if sentiment else None,
        onchain=OnChainEvidence.model_validate(onchain) if onchain else None,
        prompt_version=prompt_version,
        missing_evidence_flags=flags,
    )
