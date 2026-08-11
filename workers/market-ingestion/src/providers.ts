/**
 * Provider instances for the ingestion worker (Phase 3).
 */
import { CoinGeckoAdapter } from "@trading-desk/provider-adapters";

/** CoinGecko provider with a production default fetcher. */
export const CoingeckoProvider = new CoinGeckoAdapter(
  process.env.COINGECKO_BASE_URL ?? "https://api.coingecko.com/api/v3",
);
