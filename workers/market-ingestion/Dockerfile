# market-ingestion worker — TypeScript/Node image
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
COPY packages ./packages
COPY workers/market-ingestion ./workers/market-ingestion

RUN npm ci
RUN cd workers/market-ingestion && npx tsc --outDir dist --noEmit false

FROM node:20-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app

COPY --from=builder /app/workers/market-ingestion/dist ./dist
COPY --from=builder /app/workers/market-ingestion/package.json ./
COPY --from=builder /app/node_modules ./node_modules

CMD ["node", "dist/index.js"]
