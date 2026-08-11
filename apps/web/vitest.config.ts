import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["chart/**/*.test.{ts,tsx}"],
    environment: "jsdom",
    globals: true,
    resolve: {
      alias: {
        "@trading-desk/contracts": new URL("../../packages/contracts/src/index.ts", import.meta.url).pathname,
        "@trading-desk/chart-core": new URL("../../packages/chart-core/src/index.ts", import.meta.url).pathname,
      },
    },
  },
});