"""Base bundle infrastructure - shared debate pattern for all 6 bundles.

Phase 4: bundles consume an evidence-derived `context` (rendered from a frozen
EvidenceSnapshot) rather than raw free-form market text. Their numeric outputs
are parsed and validated against a typed Pydantic schema so the engine can
guarantee 100% schema-valid bundle verdicts.
"""

import operator
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class BundleState(TypedDict):
    asset: str
    asset_class: str
    timeframe: str
    context: str  # evidence snapshot rendered text (Phase 4)
    thesis_response: str
    antithesis_response: str
    referee_response: str
    agents_output: Annotated[list[dict], operator.add]


class AgentOutput(BaseModel):
    """Strict, typed agent output schema (Phase 4)."""

    name: str
    stance: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    weight: float = Field(default=1.0, ge=0, le=2)
    rationale: str = ""

    @classmethod
    def parse(cls, name, content, default_weight=1.0) -> "AgentOutput":
        stance = 0.0
        confidence = 0.5
        for line in content.split("\n"):
            lu = line.upper().strip()
            if lu.startswith("STANCE:"):
                try:
                    stance = float(lu.split(":")[1].strip().split("|")[0].strip().split()[0])
                except (ValueError, IndexError):
                    stance = 0.0
            if "CONFIDENCE:" in lu:
                try:
                    cpart = lu.split("CONFIDENCE:")[1].strip().split("|")[0].strip().split()[0]
                    confidence = float(cpart)
                except (ValueError, IndexError):
                    confidence = 0.5
        return cls(
            name=name,
            stance=max(-1.0, min(1.0, stance)),
            confidence=max(0.0, min(1.0, confidence)),
            weight=default_weight,
            rationale=content,
        )

    def to_audit(self) -> dict:
        return self.model_dump()


def _ctx(state, default_context_key="context"):
    """Return the evidence context, falling back to any provided market text."""
    return state.get(default_context_key) or state.get("market_data", "")


def create_bundle_graph(
    bundle_name, thesis_prompt, antithesis_prompt, referee_prompt, thesis_llm, antithesis_llm, referee_llm
):
    """Create a LangGraph subgraph for one MAS bundle.

    Pattern: thesis vs antithesis debate -> referee weighs -> output verdict.
    Prompts reference {asset}, {asset_class}, {timeframe} and {context}.
    """

    def thesis_node(state):
        prompt = thesis_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            context=_ctx(state),
        )
        resp = thesis_llm.invoke(prompt)
        agent = AgentOutput.parse(f"{bundle_name}_thesis", resp.content, 1.0)
        return {"thesis_response": resp.content, "agents_output": [agent.to_audit()]}

    def antithesis_node(state):
        prompt = antithesis_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            context=_ctx(state),
            thesis=state.get("thesis_response", ""),
        )
        resp = antithesis_llm.invoke(prompt)
        agent = AgentOutput.parse(f"{bundle_name}_antithesis", resp.content, 1.0)
        return {"antithesis_response": resp.content, "agents_output": [agent.to_audit()]}

    def referee_node(state):
        prompt = referee_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            context=_ctx(state),
            thesis=state.get("thesis_response", ""),
            antithesis=state.get("antithesis_response", ""),
        )
        resp = referee_llm.invoke(prompt)
        agent = AgentOutput.parse(f"{bundle_name}_referee", resp.content, 0.8)
        return {"referee_response": resp.content, "agents_output": [agent.to_audit()]}

    workflow = StateGraph(BundleState)
    workflow.add_node("thesis", thesis_node)
    workflow.add_node("antithesis", antithesis_node)
    workflow.add_node("referee", referee_node)
    workflow.add_edge(START, "thesis")
    workflow.add_edge("thesis", "antithesis")
    workflow.add_edge("antithesis", "referee")
    workflow.add_edge("referee", END)
    return workflow.compile()


def __getattr__(name):
    # Back-compat for older call sites using market_data key.
    raise AttributeError(name)
