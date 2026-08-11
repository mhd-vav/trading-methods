import { describe, it, expect, vi } from "vitest";
import { withTimeout, withRetry, CircuitBreaker, RequestCoalescer, TimeoutError, CircuitOpenError, backoffMs } from "../src/resilience";

describe("withTimeout", () => {
  it("resolves on time", async () => {
    await expect(withTimeout(Promise.resolve(42), 1000)).resolves.toBe(42);
  });
  it("rejects with TimeoutError when slower than timeout", async () => {
    await expect(
      withTimeout(new Promise((r) => setTimeout(() => r(1), 200)), 20),
    ).rejects.toBeInstanceOf(TimeoutError);
  });
  it("propagates a provided abort signal", async () => {
    const ac = new AbortController();
    ac.abort();
    await expect(withTimeout(Promise.resolve(1), 1000, ac.signal)).rejects.toThrow("aborted");
  });
});

describe("backoffMs", () => {
  it("grows exponentially and respects max", () => {
    expect(backoffMs(250, 0, 30_000, false)).toBe(250);
    // cap: choose base so 2^5 exceeds max
    expect(backoffMs(1000, 5, 30_000, false)).toBe(30_000); // 1000*32=32000 -> capped
    expect(backoffMs(100, 2, 1000, false)).toBe(400);
    expect(backoffMs(250, 5, 30_000, false)).toBe(8000); // below cap, raw 2^5
  });
});

describe("withRetry", () => {
  it("retries transient errors then succeeds", async () => {
    let calls = 0;
    const fn = vi.fn(async () => {
      calls += 1;
      if (calls < 3) throw new TimeoutError();
      return "ok";
    });
    const result = await withRetry(
      (_s) => fn(),
      { maxAttempts: 4, baseDelayMs: 1, maxDelayMs: 5, jitter: false, retryableTypes: ["TimeoutError"] },
    );
    expect(result).toBe("ok");
    expect(calls).toBe(3);
  });
  it("gives up after maxAttempts", async () => {
    const fn = vi.fn(async () => { throw new TimeoutError(); });
    await expect(
      withRetry((_s) => fn(), { maxAttempts: 2, baseDelayMs: 1, maxDelayMs: 3, jitter: false, retryableTypes: ["TimeoutError"] }),
    ).rejects.toBeInstanceOf(TimeoutError);
    expect(fn).toHaveBeenCalledTimes(2);
  });
  it("does not retry non-retryable errors", async () => {
    const fn = vi.fn(async () => { throw new Error("boom"); });
    await expect(
      withRetry((_s) => fn(), { maxAttempts: 3, baseDelayMs: 1, maxDelayMs: 3, jitter: false, retryableTypes: ["TimeoutError"] }),
    ).rejects.toThrow("boom");
    expect(fn).toHaveBeenCalledTimes(1);
  });
});

describe("CircuitBreaker", () => {
  it("opens after threshold and fails fast", () => {
    const cb = new CircuitBreaker(2, 1000, "test");
    cb.beforeCall();
    cb.onFailure();
    cb.beforeCall();
    cb.onFailure();
    expect(cb.state).toBe("open");
    expect(() => cb.beforeCall()).toThrow(CircuitOpenError);
  });
  it("resets on success", () => {
    const cb = new CircuitBreaker(3, 1000, "test");
    cb.onFailure();
    cb.onFailure();
    cb.onSuccess();
    expect(cb.state).toBe("closed");
  });
});

describe("RequestCoalescer", () => {
  it("coalesces concurrent identical calls", async () => {
    let calls = 0;
    const c = new RequestCoalescer<string, string>(1000);
    const fn = async () => { calls += 1; await new Promise((r) => setTimeout(r, 30)); return "v"; };
    const [a, b] = await Promise.all([c.run("k", fn), c.run("k", fn)]);
    expect(a).toBe("v");
    expect(b).toBe("v");
    expect(calls).toBe(1);
  });
  it("allows distinct keys to run separately", async () => {
    let calls = 0;
    const c = new RequestCoalescer<string, number>(1000);
    const fn = async () => { calls += 1; return calls; };
    const [a, b] = await Promise.all([c.run("k1", fn), c.run("k2", fn)]);
    expect(a).not.toBe(b);
    expect(calls).toBe(2);
  });
});
