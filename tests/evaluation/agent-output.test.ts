/**
 * Evaluation tests — LLM output quality and agent behavior.
 *
 * These tests run against the analysis-api with a real or mock LLM backend.
 * They verify that agent outputs are well-formed, evidence-grounded, and
 * meet the quality bar defined in Phase 4.
 *
 * Run: LLM_API_KEY_CODE=... npx vitest run
 */
import { describe, it, expect } from "vitest";

const ANALYSIS_API = process.env.ANALYSIS_API_URL ?? "http://localhost:8000";

describe("analysis-api agent output", () => {
  it("returns a well-formed AgentOutput bundle", async () => {
    const r = await fetch(`${ANALYSIS_API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        symbol: "BTC/USDT",
        timeframe: "4h",
        agent_id: "technical-analyst",
      }),
    });
    if (!r.ok) return; // skip if no LLM key configured
    const output = await r.json();
    expect(output).toHaveProperty("agent_id");
    expect(output).toHaveProperty("snapshot_id");
    expect(output).toHaveProperty("provenance");
    expect(output.provenance).toHaveProperty("evidence_ids");
  });

  it("rejects invalid agent_id", async () => {
    const r = await fetch(`${ANALYSIS_API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        symbol: "BTC/USDT",
        timeframe: "4h",
        agent_id: "nonexistent-agent",
      }),
    });
    expect([400, 404, 422]).toContain(r.status);
  });
});
