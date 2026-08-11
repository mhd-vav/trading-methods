-- Trading Desk — PostgreSQL initialization
-- Run once on a fresh database. SQLAlchemy's create_all handles table creation;
-- this script sets up extensions, roles, and indexes that complement the ORM.

-- UUID extension for future migration to UUID primary keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pg_trgm for fuzzy symbol search on watchlists/journals
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Optimized indexes for owner-scoped queries (supplement ORM indexes)
CREATE INDEX IF NOT EXISTS idx_journal_owner_created
    ON journal_entries (owner_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_watchlist_owner
    ON watchlist_entries (owner_id, symbol);

CREATE INDEX IF NOT EXISTS idx_alerts_owner_active
    ON alerts (owner_id, active)
    WHERE active = true;

CREATE INDEX IF NOT EXISTS idx_audit_actor_created
    ON audit_logs (actor_id, created_at DESC);

-- GIN index for symbol fuzzy search
CREATE INDEX IF NOT EXISTS idx_journal_symbol_trgm
    ON journal_entries USING gin (symbol gin_trgm_ops);
