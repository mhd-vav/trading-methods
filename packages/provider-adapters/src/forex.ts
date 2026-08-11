/**
 * Forex provider adapter.
 *
 * Forex candle sources vary (OANDA, broker feeds, BRS). This adapter exposes the
 * strict normalized contract and plugs in a provider-specific fetcher via
 * injection. The default fetcher returns an explicitly-degraded result so the
 * platform never silently loads forever when forex licensing is unavailable.
 */
import type { Candle, CandleProvider, CandleSeries, Timeframe } from "@trading-desk/contracts";
import { msPerBar } from "@trading-desk/chart-core";
import type { ProviderAdapter, ProviderFetchOptions } from "./adapter";

export type ForexFetcher = (opts: ProviderFetchOptions) => Promise<RawForexCandle[]>;

export interface RawForexCandle {
  tsMs: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v?: number;
}

export class ForexAdapter implements ProviderAdapter {
  readonly provider: CandleProvider = "forex-brs";
  constructor(
    private fetcher: ForexFetcher,
    private middlewareUnavailable = false,
  ) {}

  canNormalize(symbol: string): boolean {
    return /^[A-Z]{6}$|^[A-Z]{3}\/[A-Z]{3}$/.test(symbol.trim());
  }

  async fetchCandles(opts: ProviderFetchOptions): Promise<CandleSeries> {
    if (this.middlewareUnavailable) {
      throw new Error("forex: data middleware currently unavailable — degraded state");
    }
    const raw = await this.fetcher(opts);
    const step = msPerBar(opts.interval);
    const canonical = opts.symbol.includes("/") ? opts.symbol.toUpperCase() : insertSlash(opts.symbol);
    const now = Date.now();
    const candles: Candle[] = raw.map((r, i) => ({
      id: `forex-brs:${canonical}:${opts.interval}:${r.tsMs}`,
      provider: "forex-brs",
      originalSymbol: opts.symbol,
      canonicalSymbol: canonical,
      interval: opts.interval,
      exchangeTimezone: "UTC",
      startMs: r.tsMs,
      endMs: r.tsMs + step,
      o: r.o, h: r.h, l: r.l, c: r.c, v: r.v ?? 0,
      isFinal: i < raw.length - 1,
      retrievedAtMs: now,
      freshnessMs: Math.max(0, now - r.tsMs),
      adjustment: "none",
      qualityWarnings: i < raw.length - 1 ? [] : ["incomplete"],
    }));
    return { candles, symbol: canonical, interval: opts.interval, provider: "forex-brs", generatedAtMs: now };
  }
}

function insertSlash(s: string): string {
  if (s.length !== 6) return s.toUpperCase();
  return `${s.slice(0, 3)}/${s.slice(3)}`;
}

export type { Candle, CandleProvider };
