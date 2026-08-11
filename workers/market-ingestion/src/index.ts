/**
 * Market ingestion worker (Phase 3 scaffold).
 *
 * Periodically pulls candle series for configured symbols through the
 * ResilientMarketClient (which applies cache, coalescing, retry, circuit
 * breaker, fallback, and degrades explicitly). A real worker would push to a
 * queue/DB and expose freshness metrics; this module provides the deterministic
 * scheduler + status tracking and a CLI entry for deployment.
 */
import type { CandleSeries, Timeframe } from "@trading-desk/contracts";
import { ResilientMarketClient } from "@trading-desk/provider-adapters";
import { CoingeckoProvider } from "./providers";

export interface IngestionTarget {
  symbol: string;
  interval: Timeframe;
  limit: number;
}

export interface IngestionStatus {
  symbol: string;
  interval: Timeframe;
  lastOkAtMs: number | null;
  lastErrorAtMs: number | null;
  lastError?: string;
  degraded: boolean;
  candleCount: number;
}

export interface WorkerOptions {
  targets: IngestionTarget[];
  intervalMs: number;
  onSeries?: (series: CandleSeries) => void;
  onStatus?: (status: IngestionStatus[]) => void;
}

export class MarketIngestionWorker {
  private statuses = new Map<string, IngestionStatus>();
  private timer: ReturnType<typeof setInterval> | null = null;
  private running = false;

  constructor(private client: ResilientMarketClient, private options: WorkerOptions) {}

  private key(symbol: string, interval: Timeframe) {
    return `${symbol}:${interval}`;
  }

  private ensureStatus(symbol: string, interval: Timeframe): IngestionStatus {
    const k = this.key(symbol, interval);
    let s = this.statuses.get(k);
    if (!s) {
      s = { symbol, interval, lastOkAtMs: null, lastErrorAtMs: null, degraded: false, candleCount: 0 };
      this.statuses.set(k, s);
    }
    return s;
  }

  /** Syncs one target; returns its status. Never throws. */
  async syncTarget(target: IngestionTarget): Promise<IngestionStatus> {
    const st = this.ensureStatus(target.symbol, target.interval);
    try {
      const res = await this.client.getCandles(target.symbol, target.interval, target.limit);
      if (res.series) {
        st.lastOkAtMs = Date.now();
        st.lastErrorAtMs = null;
        st.lastError = undefined;
        st.candleCount = res.series.candles.length;
        st.degraded = res.degraded || res.providerUsed === null;
        this.options.onSeries?.(res.series);
      } else {
        st.degraded = true;
        st.lastErrorAtMs = Date.now();
        st.lastError = res.reason ?? "no data";
      }
    } catch (e) {
      st.degraded = true;
      st.lastErrorAtMs = Date.now();
      st.lastError = (e as Error).message;
    }
    return st;
  }

  /** Run one full pass over all targets (for a one-shot sync / tests). */
  async syncAll(): Promise<IngestionStatus[]> {
    const statuses: IngestionStatus[] = [];
    for (const target of this.options.targets) {
      statuses.push(await this.syncTarget(target));
    }
    this.options.onStatus?.(statuses);
    return statuses;
  }

  /** Start the periodic scheduler. */
  start() {
    if (this.running) return;
    this.running = true;
    void this.syncAll();
    this.timer = setInterval(() => {
      void this.syncAll();
    }, this.options.intervalMs);
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
    this.running = false;
  }
}

export { _buildClient };

/** Constructs the resilient client with the configured providers. */
function _buildClient(cache?: ConstructorParameters<typeof ResilientMarketClient>[0]["cache"]) {
  return new ResilientMarketClient({
    providers: [CoingeckoProvider],
    cache,
    degradeOnFailure: true,
    cacheTtlMs: 30_000,
    timeoutMs: 15_000,
    maxRetries: 2,
  });
}
