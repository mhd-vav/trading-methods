/**
 * E2E tests — full user journeys through the nginx edge proxy.
 *
 * These tests require the full stack running via `docker compose up -d`.
 * They exercise the real nginx routing, auth flow, and service interactions.
 *
 * Run: npx vitest run
 */
import { describe, it, expect } from "vitest";

const EDGE = process.env.EDGE_URL ?? "http://localhost:8080";

async function registerViaEdge(email: string, password: string) {
  const r = await fetch(`${EDGE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!r.ok && r.status !== 409) throw new Error(`register via edge failed: ${r.status}`);
  const login = await fetch(`${EDGE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) throw new Error(`login via edge failed: ${login.status}`);
  const { access_token } = await login.json();
  return { Authorization: `Bearer ${access_token}` };
}

describe("E2E: health via edge", () => {
  it("nginx proxies /health to core-api", async () => {
    const r = await fetch(`${EDGE}/health`);
    expect(r.ok).toBe(true);
    const body = await r.json();
    expect(body.status).toBe("ok");
  });
});

describe("E2E: full user journey", () => {
  it("register → create journal → create alert → read audit", async () => {
    const h = await registerViaEdge("e2e-journey@test.com", "password123");

    // Create journal entry
    const journal = await fetch(`${EDGE}/api/journal`, {
      method: "POST",
      headers: { ...h, "Content-Type": "application/json" },
      body: JSON.stringify({
        symbol: "BTC/USDT",
        direction: "long",
        entry_price: 50000,
        notes: "E2E test entry",
      }),
    });
    expect(journal.ok).toBe(true);

    // Create alert
    const alert = await fetch(`${EDGE}/api/alerts`, {
      method: "POST",
      headers: { ...h, "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: "BTC/USDT", condition: ">", price: 55000 }),
    });
    expect(alert.ok).toBe(true);

    // Read audit trail
    const audit = await fetch(`${EDGE}/api/audit`, { headers: h });
    expect(audit.ok).toBe(true);
    const logs = await audit.json();
    const actions = logs.map((e: { action: string }) => e.action);
    expect(actions).toContain("journal.create");
    expect(actions).toContain("alert.create");
  });
});

describe("E2E: unauthenticated access blocked", () => {
  it("rejects journal access without token", async () => {
    const r = await fetch(`${EDGE}/api/journal`);
    expect([401, 403]).toContain(r.status);
  });
});
