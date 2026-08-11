/**
 * ResilientMarketClient — the Phase 3 entry point the rest of the platform uses.
 *
 * Composes provider adapters with:
 * - in-process cache (+ optional Redis adapter supplied at construction)
 * - single-flight coalescing
 * - bounded retry + per-provider timeout
 * - circuit breaker per provider
 * - ordered fallback providers
 * - explicit degraded result (never an endless loading state)
 */
import type { CandleSeries, Timeframe } from "@trading-desk/contracts";
import type { ProviderAdapter, ProviderFetchOptions } from "./adapter";
import {
  CircuitBreaker,
  RequestCoalescer,
  withRetry,
  DEFAULT_RETRY,
  ProviderTransientError,
  TimeoutError,
} from "./resilience";
import { auditSeries } from "./quality";

export interface CachePluggable {
  get(key: string): Promise<string | null> | string | null;
  set(key: string, value: string, ttlMs: number): Promise<void> | void;
}

export interface MarketClientOptions {
  providers: ProviderAdapter[];
  cache?: CachePluggable;
  cacheTtlMs?: number;
  timeoutMs?: number;
  maxRetries?: number;
  /** If true, a provider outage yields a degraded result instead of throwing. */
  degradeOnFailure?: boolean;
}

export interface MarketResult {
  series: CandleSeries | null;
  providerUsed: string | null;
  degraded: boolean;
  reason?: string;
  quality?: ReturnType<typeof auditSeries>;
}

function cacheKey(symbol: string, interval: Timeframe, limit: number) {
  return `candles:${symbol}:${interval}:${limit}`;
}

export class ResilientMarketClient {
  private breakers = new Map<string, CircuitBreaker>();
  private coalescer = new RequestCoalescer<string, MarketResult>();
  private opts: Required<Pick<MarketClientOptions, "cacheTtlMs" | "timeoutMs" | "maxRetries" | "degradeOnFailure">>;

  constructor(private options: MarketClientOptions) {
    this.opts = {
      cacheTtlMs: options.cacheTtlMs ?? 30_000,
      timeoutMs: options.timeoutMs ?? 15_000,
      maxRetries: options.maxRetries ?? 2,
      degradeOnFailure: options.degradeOnFailure ?? true,
    };
    for (const p of options.providers) this.breakers.set(p.provider, new CircuitBreaker(5, 30_000, p.provider));
  }

  private breaker(provider: string): CircuitBreaker {
    let b = this.breakers.get(provider);
    if (!b) {
      b = new CircuitBreaker(5, 30_000, provider);
      this.breakers.set(provider, b);
    }
    return b;
  }

  /**
   * Fetch candles for a symbol across the provider chain. Returns a MarketResult
   * that always resolves — degraded when providers fail and `degradeOnFailure`.
   */
  async getCandles(symbol: string, interval: Timeframe, limit = 300, signal?: AbortSignal): Promise<MarketResult> {
    const key = cacheKey(symbol, interval, limit);

    // cache hit
    if (this.options.cache) {
      const cached = await this.options.cache.get(key);
      if (cached) {
        try { return { series: JSON.parse(cached), providerUsed: "cache", degraded: false }; }
        catch { /* fall through to fetch */ }
      }
    }

    const timeoutMs = this.opts.timeoutMs;

    // single-flight coalesce per key
    return this.coalescer.run(key, async () => {
      let lastErr: Error | null = null;

      for (const provider of this.options.providers) {
        if (signal?.aborted) return { series: null, providerUsed: null, degraded: true, reason: "aborted" };

        const breaker = this.breaker(provider.provider);
        try {
          breaker.beforeCall();
        } catch (e) {
          lastErr = e as Error;
          continue; // try next provider
        }

        try {
          const series = await withRetry(
            (sig, attempt) => {
              const opts: ProviderFetchOptions = { symbol, interval, limit, signal: sig };
              // surface transient/timeout so retry applies
              return provider.fetchCandles(opts).catch((e) => {
                const n = (e as Error).name;
                if (n === "TimeoutError" || n.includes("transient")) throw e;
                if (typeof e === "object" && e && (e as { name?: string }).name) throw e;
                throw new ProviderTransientError(String((e as Error).message), e);
              });
            },
            { ...DEFAULT_RETRY, maxAttempts: this.opts.maxRetries + 1, retryableTypes: ["TimeoutError", "ProviderTransientError"] },
            signal,
          );
          breaker.onSuccess();
          const quality = auditSeries(series);
          if (this.options.cache) {
            await this.options.cache.set(key, JSON.stringify(series), this.opts.cacheTtlMs);
          }
          return { series, providerUsed: provider.provider, degraded: quality.degraded, quality };
        } catch (e) {
          breaker.onFailure();
          lastErr = e as Error;
        }
      }

      // All providers failed
      if (!this.opts.degradeOnFailure) throw lastErr ?? new Error("no providers available");
      return {
        series: null,
        providerUsed: null,
        degraded: true,
        reason: lastErr?.message ?? "all providers unavailable",
      };
    });
  }
}
