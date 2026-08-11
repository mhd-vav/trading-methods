/**
 * Integration tests — cross-service contract verification.
 *
 * These tests run after `docker compose up -d postgres redis core-api analysis-api`
 * and verify that services work together correctly. They require a running stack.
 *
 * Run: npx vitest run
 */
import { describe, it, expect } from "vitest";

const CORE_API = process.env.CORE_API_URL ?? "http://localhost:8001";
const ANALYSIS_API = process.env.ANALYSIS_API_URL ?? "http://localhost:8000";

async function registerAndLogin(email: string, password: string) {
  const r = await fetch(`${CORE_API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!r.ok && r.status !== 409) throw new Error(`register failed: ${r.status}`);
  const login = await fetch(`${CORE_API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) throw new Error(`login failed: ${login.status}`);
  const { access_token } = await login.json();
  return { Authorization: `Bearer ${access_token}` };
}

describe("core-api health", () => {
  it("returns ok", async () => {
    const r = await fetch(`${CORE_API}/health`);
    expect(r.ok).toBe(true);
    const body = await r.json();
    expect(body.status).toBe("ok");
  });
});

describe("analysis-api health", () => {
  it("returns ok", async () => {
    const r = await fetch(`${ANALYSIS_API}/health`);
    expect(r.ok).toBe(true);
  });
});

describe("journal lifecycle", () => {
  it("user can register, create a journal entry, and read it back", async () => {
    const h = await registerAndLogin("integration@test.com", "password123");
    const create = await fetch(`${CORE_API}/journal`, {
      method: "POST",
      headers: { ...h, "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: "BTC/USDT", direction: "long", entry_price: 50000 }),
    });
    expect(create.ok).toBe(true);
    const entry = await create.json();
    expect(entry.symbol).toBe("BTC/USDT");

    const get = await fetch(`${CORE_API}/journal/${entry.id}`, { headers: h });
    expect(get.ok).toBe(true);
    const got = await get.json();
    expect(got.direction).toBe("long");
  });
});

describe("cross-user isolation (integration)", () => {
  it("user cannot access another user's journal entry", async () => {
    const h1 = await registerAndLogin("iso1@test.com", "password123");
    const h2 = await registerAndLogin("iso2@test.com", "password123");

    const create = await fetch(`${CORE_API}/journal`, {
      method: "POST",
      headers: { ...h1, "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: "ETH/USDT", direction: "short" }),
    });
    const { id } = await create.json();

    const cross = await fetch(`${CORE_API}/journal/${id}`, { headers: h2 });
    expect(cross.status).toBe(404);
  });
});

describe("audit trail (integration)", () => {
  it("audit log records journal creation", async () => {
    const h = await registerAndLogin("audit@test.com", "password123");
    await fetch(`${CORE_API}/journal`, {
      method: "POST",
      headers: { ...h, "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: "SOL/USDT", direction: "long" }),
    });
    const logs = await fetch(`${CORE_API}/audit`, { headers: h });
    const entries = await logs.json();
    const actions = entries.map((e: { action: string }) => e.action);
    expect(actions).toContain("journal.create");
  });
});
