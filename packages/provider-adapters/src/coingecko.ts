/**
 * CoinGecko adapter — market-chart candle data for crypto.
 *
 * CoinGecko's `/coins/{id}/market_chart` returns un-anchored OHLC arrays with no
 * granularity control beyond `days`. We bucket into the requested interval and
 * mark the last candle incomplete where a newer one is expected. Network I/O is
 * injected (`fetcher`) so tests can run deterministically without a real fetch.
 */
import type { Candle, CandleProvider, CandleSeries, Timeframe } from "@trading-desk/contracts";
import { msPerBar } from "@trading-desk/chart-core";
import type { ProviderAdapter, ProviderFetchOptions } from "./adapter";
import { withTimeout } from "./resilience";

export interface CoinGeckoRawPoint {
  tsMs: number;
  price: number;
}

export type Fetcher = (url: string, signal?: AbortSignal) => Promise<unknown>;

const CANONICAL: Record<string, string> = {
  btc: "BTC/USDT",
  bitcoin: "BTC/USDT",
  eth: "ETH/USDT",
  ethereum: "ETH/USDT",
};

/** Map a user symbol (e.g. "BTC/USDT", "bitcoin", "btc") to a CoinGecko id. */
export function coingeckoId(symbol: string): string | null {
  const base = symbol.split("/")[0].toLowerCase();
  const map: Record<string, string> = {
    btc: "bitcoin", "btc/usdt": "bitcoin", xbt: "bitcoin",
    eth: "ethereum", "eth/usdt": "ethereum",
    sol: "solana", "sol/usdt": "solana",
    ada: "cardano", "ada/usdt": "cardano",
    dot: "polkadot", "dot/usdt": "polkadot",
    avax: "avalanche-2", "avax/usdt": "avalanche-2",
    matic: "matic-network", "matic/usdt": "matic-network",
    link: "chainlink", "link/usdt": "chainlink",
  };
  return map[base] ?? null;
}

export class CoinGeckoAdapter implements ProviderAdapter {
  readonly provider: CandleProvider = "coingecko";
  constructor(
    private baseUrl = "https://api.coingecko.com/api/v3",
    private fetcher: Fetcher = defaultFetcher,
    private timeoutMs = 15_000,
  ) {}

  canNormalize(symbol: string): boolean {
    return coingeckoId(symbol) !== null;
  }

  private async rawPrices(id: string, days: number, signal?: AbortSignal): Promise<CoinGeckoRawPoint[]> {
    const url = `${this.baseUrl}/coins/${id}/market_chart?vs_currency=usd&days=${days}&interval=daily`;
    const data = (await withTimeout(this.fetcher(url, signal), this.timeoutMs, signal)) as {
      prices?: [number, number][];
    };
    if (!data || !Array.isArray(data.prices)) {
      throw new Error("coingecko: unexpected response shape");
    }
    return data.prices.map(([tsMs, price]) => ({ tsMs, price }));
  }

  async fetchCandles(opts: ProviderFetchOptions): Promise<CandleSeries> {
    const id = coingeckoId(opts.symbol);
    if (!id) throw new Error(`coingecko: unsupported symbol ${opts.symbol}`);
    const days = Math.max(1, Math.ceil((opts.limit * msPerBar(opts.interval)) / 86_400_000));
    const points = await this.rawPrices(id, days, opts.signal);
    if (!points.length) throw new Error("coingecko: empty candles");

    const step = msPerBar(opts.interval);
    const canonical = CANONICAL[opts.symbol.split("/")[0].toLowerCase()] ?? `${opts.symbol.toUpperCase()}`;
    const now = Date.now() + opts.limit * step;

    // Bucket daily-ish points into the requested interval via last-observed price.
    const candles: Candle[] = [];
    let curStart: number | null = null;
    let curEstPrice = 0;
    for (const p of points) {
      if (curStart === null || p.tsMs >= curStart + step) {
        // finalize previous
        if (curStart !== null) {
          candles.push(
            makeCandle(canonical, "coingecko", opts.interval, curStart, step, curEstPrice, curEstPrice, true, now),
          );
        }
        curStart = p.tsMs - (p.tsMs % step);
        curEstPrice = p.price;
      } else {
        curEstPrice = p.price;
      }
    }
    if (curStart !== null) {
      candles.push(makeCandle(canonical, "coingecko", opts.interval, curStart, step, curEstPrice, curEstPrice, true, now));
    }
    // Mark the very last candle incomplete (current, forming).
    const last = candles[candles.length - 1];
    if (last) {
      candles[candles.length - 1] = { ...last, isFinal: false, qualityWarnings: ["incomplete"] };
    }
    return {
      candles: candles.slice(-opts.limit),
      symbol: canonical,
      interval: opts.interval,
      provider: "coingecko",
      generatedAtMs: now,
    };
  }
}

function makeCandle(
  symbol: string,
  provider: CandleProvider,
  interval: Timeframe,
  startMs: number,
  step: number,
  price: number,
  _close: number,
  isFinal: boolean,
  retrievedAtMs: number,
): Candle {
  return {
    id: `${provider}:${symbol}:${interval}:${startMs}`,
    provider,
    originalSymbol: symbol,
    canonicalSymbol: symbol,
    interval,
    exchangeTimezone: "UTC",
    startMs,
    endMs: startMs + step,
    o: price, h: price, l: price, c: price, v: 0,
    isFinal,
    retrievedAtMs,
    freshnessMs: Math.max(0, Date.now() - retrievedAtMs),
    adjustment: "none",
    qualityWarnings: isFinal ? [] : ["incomplete"],
  };
}

async function defaultFetcher(url: string, signal?: AbortSignal): Promise<unknown> {
  const res = await fetch(url, { signal });
  if (!res.ok) throw new Error(`coingecko: HTTP ${res.status}`);
  return res.json();
}
