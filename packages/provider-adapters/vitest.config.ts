import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["test/**/*.test.ts"],
    environment: "node",
    globals: true,
    resolve: {
      alias: {
        "@trading-desk/contracts": new URL("../contracts/src/index.ts", import.meta.url).pathname,
        "@trading-desk/chart-core": new URL("../chart-core/src/index.ts", import.meta.url).pathname,
      },
    },
  },
});