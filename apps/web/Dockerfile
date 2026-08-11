# web (Next.js) — multi-stage production image
# Stage 1: install deps + build
FROM node:20-alpine AS builder
WORKDIR /app

# Copy workspace root for npm workspaces
COPY package.json package-lock.json ./
COPY packages ./packages
COPY apps/web ./apps/web

RUN npm ci --workspaces --if-present
RUN cd apps/web && npx next build

# Stage 2: minimal runtime
FROM node:20-alpine AS runtime
ENV NODE_ENV=production
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app

COPY --from=builder /app/apps/web/.next ./.next
COPY --from=builder /app/apps/web/public ./public
COPY --from=builder /app/apps/web/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/apps/web/next.config.* ./

USER app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

CMD ["npx", "next", "start", "-p", "3000"]
