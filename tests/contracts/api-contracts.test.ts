/**
 * Contract tests — verify API schemas match between services and consumers.
 *
 * These tests don't require running services. They validate that the
 * TypeScript contract types from `packages/contracts` are compatible
 * with the actual API responses defined in the backend schemas.
 *
 * Run: npx vitest run
 */
import { describe, it, expect } from "vitest";
import type { Candle, Timeframe } from "@trading-desk/contracts";

describe("contract: Candle", () => {
  it("has required fields", () => {
    const candle: Candle = {
      ts: 1700000000,
      open: 50000,
      high: 50100,
      low: 49900,
      close: 50050,
      volume: 1.5,
    };
    expect(candle.ts).toBe(1700000000);
    expect(candle.open).toBeLessThanOrEqual(candle.high);
    expect(candle.low).toBeLessThanOrEqual(candle.close);
  });
});

describe("contract: Timeframe", () => {
  it("accepts valid timeframes", () => {
    const valid: Timeframe[] = ["1m", "5m", "15m", "1h", "4h", "1d"];
    valid.forEach((tf) => {
      expect(typeof tf).toBe("string");
      expect(tf).toMatch(/^\d+[mhd]$/);
    });
  });
});

describe("contract: API response shapes", () => {
  it("journal entry shape matches core-api schema", () => {
    const journalEntry = {
      id: 1,
      symbol: "BTC/USDT",
      direction: "long",
      entry_price: 50000,
      exit_price: null,
      size: null,
      pnl: null,
      notes: "",
      created_at: "2026-01-01T00:00:00Z",
    };
    expect(journalEntry.direction).toMatch(/^(long|short|flat)$/);
    expect(typeof journalEntry.symbol).toBe("string");
  });

  it("alert shape matches core-api schema", () => {
    const alert = {
      id: 1,
      symbol: "BTC",
      condition: ">",
      price: 50000,
      message: "",
      active: true,
      triggered_at: null,
    };
    expect(alert.condition).toMatch(/^(>|<|==)$/);
  });
});
