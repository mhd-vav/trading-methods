import { describe, it, expect, vi } from "vitest";
import { ResilientMarketClient } from "../src/client";
import type { ProviderAdapter, ProviderFetchOptions } from "../src/adapter";
import type { CandleSeries, Timeframe } from "@trading-desk/contracts";

function series(symbol: string, count = 50): CandleSeries {
  const start = 1_700_000_000_000;
  const candles = Array.from({ length: count }, (_, i) => ({
    id: `${symbol}:${i}`, provider: "synthetic" as const, originalSymbol: symbol, canonicalSymbol: symbol,
    interval: "4h" as Timeframe, exchangeTimezone: "UTC", startMs: start + i * 14_400_000, endMs: start + (i + 1) * 14_400_000,
    o: 100, h: 101, l: 99, c: 100, v: 100, isFinal: true, retrievedAtMs: 0, freshnessMs: 0, adjustment: "none" as const, qualityWarnings: [],
  }));
  return { candles, symbol, interval: "4h" as Timeframe, provider: "synthetic" as const, generatedAtMs: Date.now() };
}

function makeProvider(fail = false): ProviderAdapter {
  return {
    provider: "synthetic" as const,
    canNormalize: () => true,
    fetchCandles: async (opts: ProviderFetchOptions): Promise<CandleSeries> => {
      if (fail) throw new Error("provider down");
      return series(opts.symbol);
    },
  };
}

class FakeCache {
  map = new Map<string, string>();
  async get(k: string) { return this.map.get(k) ?? null; }
  async set(k: string, v: string) { this.map.set(k, v); }
}

describe("ResilientMarketClient", () => {
  it("returns data from the primary provider", async () => {
    const client = new ResilientMarketClient({ providers: [makeProvider()], degradeOnFailure: true });
    const res = await client.getCandles("BTC/USDT", "4h", 50);
    expect(res.series).not.toBeNull();
    expect(res.providerUsed).toBe("synthetic");
    expect(res.degraded).toBe(false);
  });

  it("falls back to the second provider", async () => {
    const primary = makeProvider(true);
    const backup = makeProvider();
    const client = new ResilientMarketClient({ providers: [primary, backup], degradeOnFailure: true });
    const res = await client.getCandles("AAA/USD", "4h", 50);
    expect(res.series).not.toBeNull();
    expect(res.providerUsed).toBe("synthetic"); // backup
    // Our two fake providers share the same name; verify via which succeeded.
    expect(res.degraded).toBe(false);
  });

  it("returns explicit degraded result when all providers fail and degradeOnFailure", async () => {
    const client = new ResilientMarketClient({ providers: [makeProvider(true)], degradeOnFailure: true, maxRetries: 0 });
    const res = await client.getCandles("BTC/USD", "4h", 50);
    expect(res.series).toBeNull();
    expect(res.degraded).toBe(true);
    expect(res.reason).toBeTruthy();
  });

  it("throws when degradeOnFailure is disabled", async () => {
    const client = new ResilientMarketClient({ providers: [makeProvider(true)], degradeOnFailure: false, maxRetries: 0 });
    await expect(client.getCandles("BTC/USD", "4h", 50)).rejects.toThrow();
  });

  it("serves from cache on a second call without re-fetching", async () => {
    const cache = new FakeCache();
    const provider = makeProvider();
    const spy = vi.spyOn(provider, "fetchCandles");
    const client = new ResilientMarketClient({ providers: [provider], cache: cache as never, degradeOnFailure: true });
    const first = await client.getCandles("CACHE/1", "4h", 50);
    expect(spy).toHaveBeenCalledTimes(1);
    // bypass coalescer by awaiting completion, then call again
    const second = await client.getCandles("CACHE/1", "4h", 50);
    expect(second.providerUsed).toBe("cache");
    expect(second.series).toEqual(first.series);
  });
});
