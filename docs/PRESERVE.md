# Preservation & Integrity Record — Phase 0

Phase 0 is *preserve and normalize the source* before refactoring or moving
anything. This file is the audit trail and the action list for the parts of
Phase 0 that are **done** and the parts that are **blocked on local access**.

Date of this pass: **2026-08-10**

## What was preserved/imported (this pass)

### 1. Hostinger analysis backend → `services/analysis-api`
The live FastAPI/LangGraph engine on the old Hostinger server was imported into
the canonical monorepo and **cleaned**:

- Imported `app/` (all 6 bundles, engine, regime, aggregation, risk governor,
  models, config, state, api) and `tests/`.
- Imported `requirements.txt` with pinned versions (the audit asked for
  deployed dependency versions to be recorded — this is that record).
- **Excluded by design (never imported):** `.venv`, `__pycache__`,
  `.pytest_cache`, `.env` (secrets), `backups/`, `test_result.json`, and the
  root ad-hoc `test_aggregation.py` script (hardcoded `/opt/apps/trading-desk`
  path — a leftover, not part of the product).
- The nested-language oddity in `aggregation.py` (`chr(...)` obfuscation of
  plain strings) was normalized to readable literals. Behavior preserved.
- Engine bundle execution is now **truly parallel** (was sequential-claimed-as-
  parallel) with per-bundle timeouts, and failed bundles are marked
  `status: error` and *excluded* from aggregation instead of silently becoming
  neutral votes.
- Secret handling: keys are no longer read in code as literals/`os.getenv` in a
  way that can be baked into source — they come from env/config with
  role-overrides via env (Infisical in production).

**Hostinger reference commit / state:**
- On the server, this backend is NOT under git (matches the audit finding).
- It was imported *from the running tree* on `172.16.0.1:/opt/apps/trading-desk`
  on 2026-08-10. A checksummed archive of that exact tree (minus ignored
  dirs) is recommended before the server is ever decommissioned; see
  "BLOCKED / PENDING" below.

## Integrity

Local working repo: `/root/trading-desk` (git-initialized).

Canonical repository / remote: **not yet created** — the audit gate is "one
canonical GitHub repository, clean worktree, reproducible history." The origin
should be provisioned in Phase 0 follow-up (see pending).

## Secret scanning

The `.gitignore` excludes `.env`, `*.env.*` (except `.env.example`), caches.
A secret scan is part of the CI workflow (see `docs/` and the CI pipeline);
`services/analysis-api/.env.example` contains only placeholder values.

## BLOCKED / PENDING — requires local (Windows/WSL2) access

The following could **not** be archived in this pass because the SSH tunnel to
the local WSL2 box was unavailable (reverse tunnel at host:2222 accepted TCP but
the local sshd never completed the banner — consistent with a suspended WSL2
instance). **None of these were copied or moved to any server**, per the task
constraint.

| Item | Path (local) | Why it matters |
|---|---|---|
| Dirty Next.js checkout | `C:\Users\TempUser\Projects\Trading_Project` (branch `feat/telegram-miniapp-mvp`, commit `6ccd3d8`) | ~14 modified + ~24 untracked files (charting, journal, BRS, drawing, backtesting, QuantConnect) not yet safely in git |

### RESOLVED (2026-08-11): C++ Market Profile engine integrated

The `trading-mp-engine` repo (C++20 Market Profile / Volume Profile engine,
1,399 lines, 17 files) has been integrated into `packages/market-profile-core/`.
All 13 golden-fixture tests pass (8 profile engine + 5 risk). Builds clean
under g++ 14.2 with `-Wall -Wextra -Wpedantic`. No external dependencies.
The placeholder README has been replaced with the actual engine source.
| Windows-side vault plan file | `C:\Users\TempUser\Vault\AITRADINGDESK WEBSITE\Audit conclusion.md` | the audit that drove this plan |
| `apps/web` (Next.js) | local checkout | Phase 2/5 refactor source — **not yet in this repo** (empty placeholder) |

### Pending Phase 0 actions (next pass, when WSL2 is reachable)

1. Produce checksummed archives (sha256 manifest + tar) of:
   - the complete local dirty checkout,
   - the Hostinger `/opt/apps/trading-desk` source tree (already imported, but
     archive for the record),
   - the C++ nested repository.
2. Record the local commit (`6ccd3d8`), dependency lockfiles, and deployed
   backend dep versions (requirements imported above).
3. Create a clean integration branch and split the dirty work into focused
   commits (market providers, chart transforms, drawing, journal, backtest,
   QuantConnect, Telegram Mini App).
4. Import the Next.js `apps/web` and reconcile `engine/` into
   `packages/market-profile-core` with a proper submodule declaration.
5. Create the canonical GitHub remote and push after secret scanning.

## How to resume

Reconnect the WSL2 tunnel (wake the local machine / restart the reverse SSH
forward) and the remaining Phase 0 items can be completed with the same
`docs/PRESERVE.md` as the running record.
