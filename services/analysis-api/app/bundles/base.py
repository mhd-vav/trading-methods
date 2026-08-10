"""Base bundle infrastructure - shared debate pattern for all 6 bundles."""

import operator
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class BundleState(TypedDict):
    asset: str
    asset_class: str
    timeframe: str
    market_data: str
    thesis_response: str
    antithesis_response: str
    referee_response: str
    agents_output: Annotated[list[dict], operator.add]


def _parse_agent_output(name, content, default_weight=1.0):
    """Parse STANCE: X.XX | CONFIDENCE: X.XX | RATIONALE: ... from LLM output."""
    stance = 0.0
    confidence = 0.5
    for line in content.split("\n"):
        lu = line.upper().strip()
        if lu.startswith("STANCE:"):
            try:
                stance = float(lu.split(":")[1].strip().split("|")[0].strip().split()[0])
                stance = max(-1.0, min(1.0, stance))
            except (ValueError, IndexError):
                pass
        if "CONFIDENCE:" in lu:
            try:
                cpart = lu.split("CONFIDENCE:")[1].strip().split("|")[0].strip().split()[0]
                confidence = float(cpart)
                confidence = max(0.0, min(1.0, confidence))
            except (ValueError, IndexError):
                pass
    return {
        "name": name,
        "stance": stance,
        "confidence": confidence,
        "weight": default_weight,
        "rationale": content,
    }


def create_bundle_graph(
    bundle_name, thesis_prompt, antithesis_prompt, referee_prompt, thesis_llm, antithesis_llm, referee_llm
):
    """Create a LangGraph subgraph for one MAS bundle.

    Pattern: thesis vs antithesis debate -> referee weighs -> output verdict.
    """

    def thesis_node(state):
        prompt = thesis_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            market_data=state["market_data"],
        )
        resp = thesis_llm.invoke(prompt)
        agent_out = _parse_agent_output(f"{bundle_name}_thesis", resp.content, 1.0)
        return {"thesis_response": resp.content, "agents_output": [agent_out]}

    def antithesis_node(state):
        prompt = antithesis_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            market_data=state["market_data"],
            thesis=state.get("thesis_response", ""),
        )
        resp = antithesis_llm.invoke(prompt)
        agent_out = _parse_agent_output(f"{bundle_name}_antithesis", resp.content, 1.0)
        return {"antithesis_response": resp.content, "agents_output": [agent_out]}

    def referee_node(state):
        prompt = referee_prompt.format(
            asset=state["asset"],
            asset_class=state["asset_class"],
            timeframe=state["timeframe"],
            market_data=state["market_data"],
            thesis=state.get("thesis_response", ""),
            antithesis=state.get("antithesis_response", ""),
        )
        resp = referee_llm.invoke(prompt)
        agent_out = _parse_agent_output(f"{bundle_name}_referee", resp.content, 0.8)
        return {"referee_response": resp.content, "agents_output": [agent_out]}

    workflow = StateGraph(BundleState)
    workflow.add_node("thesis", thesis_node)
    workflow.add_node("antithesis", antithesis_node)
    workflow.add_node("referee", referee_node)
    workflow.add_edge(START, "thesis")
    workflow.add_edge("thesis", "antithesis")
    workflow.add_edge("antithesis", "referee")
    workflow.add_edge("referee", END)
    return workflow.compile()
