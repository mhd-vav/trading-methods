/**
 * Resilience primitives for provider calls (Phase 3):
 * - hard timeouts with cancellation
 * - bounded retries with exponential backoff + jitter
 * - circuit breaker that fails fast during outages
 * - single-flight coalescing so concurrent identical requests hit the provider once
 */
import type { CandleProvider } from "@trading-desk/contracts";

export class TimeoutError extends Error {
  constructor(message = "provider request timed out") {
    super(message);
    this.name = "TimeoutError";
  }
}

export class CircuitOpenError extends Error {
  constructor(provider: string) {
    super(`circuit open for ${provider}`);
    this.name = "CircuitOpenError";
  }
}

/** Promise that rejects after `ms` ms with TimeoutError, aborting via signal. */
export function withTimeout<T>(promise: Promise<T>, ms: number, signal?: AbortSignal): Promise<T> {
  if (ms <= 0) return promise;
  let timer: ReturnType<typeof setTimeout>;
  const onAbort = () => rejectFn(new Error("aborted"));
  let rejectFn: (r: unknown) => void;
  const timeout = new Promise<never>((_, reject) => {
    rejectFn = reject;
    timer = setTimeout(() => reject(new TimeoutError()), ms);
  });
  if (signal) {
    if (signal.aborted) return Promise.reject(new Error("aborted"));
    signal.addEventListener("abort", onAbort, { once: true });
  }
  return Promise.race([promise, timeout]).finally(() => {
    clearTimeout(timer);
    signal?.removeEventListener("abort", onAbort);
  });
}

/** Small deterministic PRNG-compatible backoff with optional jitter. */
export function backoffMs(baseMs: number, attempt: number, maxMs = 30_000, jitter = true): number {
  const exp = Math.min(baseMs * 2 ** attempt, maxMs);
  return jitter ? Math.floor(exp * (0.5 + Math.random() * 0.5)) : exp;
}

export interface RetryConfig {
  maxAttempts: number;        // total attempts (>=1)
  baseDelayMs: number;
  maxDelayMs: number;
  retryableTypes: string[];   // error names that trigger retry (e.g. TimeoutError, transient)
  jitter: boolean;
}

export const DEFAULT_RETRY: RetryConfig = {
  maxAttempts: 3,
  baseDelayMs: 250,
  maxDelayMs: 30_000,
  retryableTypes: ["TimeoutError", "ProviderTransientError", "CircuitHalfOpenRetry"],
  jitter: true,
};

/** Runs `fn` with bounded retries. Abort propagates for the whole attempt set. */
export async function withRetry<T>(
  fn: (signal: AbortSignal | undefined, attempt: number) => Promise<T>,
  cfg: RetryConfig = DEFAULT_RETRY,
  signal?: AbortSignal,
): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 0; attempt < cfg.maxAttempts; attempt++) {
    if (signal?.aborted) throw new Error("aborted");
    try {
      return await fn(signal, attempt);
    } catch (err) {
      lastErr = err;
      const name = (err as Error)?.name ?? "";
      const retryable = cfg.retryableTypes.some((t) => name.includes(t));
      if (!retryable || attempt === cfg.maxAttempts - 1 || signal?.aborted) throw err;
      await sleep(backoffMs(cfg.baseDelayMs, attempt, cfg.maxDelayMs, cfg.jitter), signal);
    }
  }
  throw lastErr;
}

const sleep = (ms: number, signal?: AbortSignal) =>
  new Promise<void>((resolve) => {
    const t = setTimeout(resolve, ms);
    signal?.addEventListener("abort", () => {
      clearTimeout(t);
      resolve();
    }, { once: true });
  });

export class ProviderTransientError extends Error {
  constructor(message: string, readonly cause?: unknown) {
    super(message);
    this.name = "ProviderTransientError";
  }
}

/**
 * Count-based circuit breaker. Failure threshold in a window trips the circuit;
 * calls fail fast while open, then a probe is allowed after the reset timeout.
 */
export class CircuitBreaker {
  private failures = 0;
  private openedAt = 0;
  private halfOpenProbeInFlight = false;
  readonly name: string;

  constructor(readonly threshold = 5, readonly resetMs = 30_000, provider: CandleProvider | string = "provider") {
    this.name = provider;
  }

  get state(): "closed" | "open" | "half-open" {
    if (this.failures >= this.threshold) {
      if (Date.now() - this.openedAt >= this.resetMs) return "half-open";
      return "open";
    }
    return "closed";
  }

  /** Throws CircuitOpenError when open (unless half-open and a probe starts). */
  beforeCall(): void {
    const st = this.state;
    if (st === "open") throw new CircuitOpenError(this.name);
    if (st === "half-open") {
      if (this.halfOpenProbeInFlight) throw new CircuitOpenError(this.name);
      this.halfOpenProbeInFlight = true;
    }
  }

  onSuccess(): void {
    this.failures = 0;
    this.halfOpenProbeInFlight = false;
  }

  onFailure(): void {
    if (this.halfOpenProbeInFlight) this.halfOpenProbeInFlight = false;
    this.failures += 1;
    if (this.failures >= this.threshold && this.openedAt === 0) {
      this.openedAt = Date.now();
    } else if (this.failures >= this.threshold && Date.now() - this.openedAt >= this.resetMs) {
      this.openedAt = Date.now();
    }
  }
}

/**
 * Single-flight coalescing: concurrent calls for the same key share one upstream
 * promise. Prevents stampede on providers during cache misses.
 */
export class RequestCoalescer<K, V> {
  private inflight = new Map<K, Promise<V>>();
  constructor(private timeoutMs = 10_000) {}

  async run(key: K, fn: () => Promise<V>): Promise<V> {
    const existing = this.inflight.get(key);
    if (existing) return existing;
    const p = withTimeout(fn(), this.timeoutMs).finally(() => this.inflight.delete(key));
    this.inflight.set(key, p);
    return p;
  }
}