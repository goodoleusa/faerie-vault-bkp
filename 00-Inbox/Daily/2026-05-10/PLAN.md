---
date: 2026-05-10
type: daily-plan
status: active
tags: [plan, faerie2, openhands-migration, vps, sdk, membench, dashboard, ffmx, coc, signing, config-migration]
---

# 🗓️ 2026-05-10 — Master Plan (v2)

**Branch:** `openhands-migration` | **Repo:** faerie2 | **Vault:** faerie-vault

---

## 🎯 North Star

Build faerie2 into the **global OpenHands-equivalent config + SDK integration layer** — a unified system where OpenHands SDK, LangChain, and OpenRouter all work seamlessly, with FFMx-optimized session management, spawning, and a WANDB-integrated membench dashboard. Ultimately merge to main and deploy to VPS.

**Key addition:** faerie2 becomes the single source of truth for ALL global OpenHands config — agent settings, LLM routing, hooks, skills, COC signing, and eval infrastructure. No stragglers in old global paths.

---

## 📋 Task Map

### Phase 1: Flatten & RAP-Evaluate Scripts 🧪
**Goal:** Deprecate `scripts/canonical/` (it's not actually canonical). Flatten into clean `scripts/` + `scripts/membench/` structure. RAP-evaluate every script to determine what's alive vs dead.

| # | Task | Details |
|---|------|---------|
| 1.1 | **RAP audit all scripts** | Run RAP (Retroactive Anchor Promotion) evaluation across ALL scripts in `scripts/` — top-level, `canonical/`, `eval/`, `probes/`, `archive/`, `membench/`. Score each: alive (actively used), dormant (exists but not invoked), dead (superseded). |
| 1.2 | **Deprecate `scripts/canonical/`** | The "canonical" label is misleading — these are just older copies. The `canonical/eval/0x_dev_eval.py` is actually NEWER (has `faerie_utils` import, updated signatures). Merge canonical/ contents into proper locations, keep the newer versions. |
| 1.3 | **Flatten to two-tier structure** | Final: `scripts/` (operational, tier-prefixed) + `scripts/membench/` (eval system). Move `scripts/probes/` → `scripts/membench/probes/`. Move `scripts/eval/` → `scripts/membench/eval/`. Remove `scripts/archive/` contents or merge if alive. |
| 1.4 | **Deduplicate** | `scripts/0x_dev_eval.py` vs `scripts/canonical/eval/0x_dev_eval.py` — keep the canonical version (newer), remove top-level stale copy. Same for all overlapping files. |
| 1.5 | **Update all cross-references** | Fix imports, paths, and references across hooks, skills, docs after flattening. |

### Phase 2: Global Config Migration — Faerie2 Becomes Canonical 🏠
**Goal:** All global OpenHands config properties from `/mnt/d/0LOCAL/.openhands/` reflected in faerie2. No stragglers.

| # | Task | Details |
|---|------|---------|
| 2.1 | **Audit global config** | Inventory everything in `/mnt/d/0LOCAL/.openhands/`: `agent_settings.json` (LLM config, OpenRouter, tools, condenser), `config.toml` (MCP URL, hooks), `cli_config.json` (UI prefs), `hooks/`, `skills/`, `profiles/`, `tools_registry/`, `utils/`. |
| 2.2 | **Create `config/` in faerie2** | `config/agent_settings.json` — full LLM config (model, API key via env var, base_url, retries, reasoning, condenser). `config/config.toml` — MCP, hooks, bucket. `config/cli_config.json` — UI prefs. |
| 2.3 | **Migrate hooks** | Global hooks (`json_validator_hook.py`) → faerie2's `.openhands/hooks/`. Remove non-prefixed duplicates (`operation_logger_hook.py`, `security_assurance_hook.py` — keep only `3x_hook-operation-logger.py`, `4x_hook-security-assurance.py`). |
| 2.4 | **Migrate skills** | Global skills (`claude-to-openhands-evolver`) → faerie2's `.openhands/skills/`. |
| 2.5 | **Migrate utils** | Global `openhands_utils/` → faerie2's `.openhands/utils/` or `scripts/`. |
| 2.6 | **Enforce faerie philosophy** | All config must reflect: tier-prefix convention, no queue, stigmergic coordination, FFMx targets, piston waves, COC signing. Any global config that violates faerie principles gets corrected. |
| 2.7 | **Symlink strategy** | Global `.openhands` → faerie2 `.openhands` where appropriate. Document which paths are symlinked vs copied. |

### Phase 3: Env Var Consolidation 📐
**Goal:** Single `.env.example` with ALL path variables. Eval reports land in multiple canonical locations.

| # | Task | Details |
|---|------|---------|
| 3.1 | **Define canonical paths** | Global config folder, vault folder(s), global forensics (`/mnt/d/0LOCAL/0forensics`), repo forensics (`forensics/`), eval data/reports, `80-Publications` (hot research outputs — emergence, membench, stigmergy, mutation, RAP, biological principles), WANDB project path, OpenRouter config path. |
| 3.2 | **Create `.env.example`** | All path variables documented with defaults. Include: `FAERIE_REPO_ROOT`, `FAERIE_VAULT_ROOT`, `FAERIE_GLOBAL_CONFIG`, `FAERICS_GLOBAL_DIR`, `FAERIE_REPO_FORENSICS`, `FAERIE_EVAL_DATA_DIR`, `FAERIE_EVAL_REPORTS_DIR`, `FAERIE_PUBLICATIONS_DIR`, `FAERIE_WANDB_PROJECT`, `FAERIE_OPENROUTER_CONFIG`, `FAERIE_COC_DIR`, `FAERIE_SCRIPTS_DIR`, `FAERIE_MEMBENCH_DIR`. |
| 3.3 | **Create `.env.local`** | Populated version (not committed). Actual paths for current machine. |
| 3.4 | **Eval report canonical locations** | Eval reports write to BOTH: (a) repo `forensics/evals/` and (b) global `/mnt/d/0LOCAL/0forensics/evals/` (via symlink or dual-write). Same for COC entries. |
| 3.5 | **Update all scripts to use env vars** | No hardcoded paths. All scripts read from env with sensible defaults. |

### Phase 4: COC Signing System + SpiderFoot Integration 🔏
**Goal:** Agents have ED25519 signing keys. They don't edit forensic logs or sign evidence directly — the COC system does.

| # | Task | Details |
|---|------|---------|
| 4.1 | **Design signing architecture** | Each agent archetype (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER) has a persistent ED25519 keypair. Keys stored in `forensics/.keys/` (gitignored). Agents submit evidence payloads → COC finalizer signs with agent's key → appends to `coc.jsonl`. |
| 4.2 | **Implement key management** | `scripts/0x_key_manager.py` — generate, store, rotate agent keypairs. Keys never leave the forensic boundary. |
| 4.3 | **Upgrade COC finalizer** | `0x_coc_finalizer.py` — add `sig` and `sig_type` fields per COC-ENTRY-SCHEMA. Agent submits evidence → finalizer computes hash → signs with agent's ED25519 key → appends hash-chained entry. |
| 4.4 | **Weave SpiderFoot into COC** | SpiderFoot tool (`.openhands/skills/spiderfoot/`) produces OSINT evidence. Evidence payloads go through COC signing before being written. SpiderFoot agent never touches `coc.jsonl` directly. |
| 4.5 | **Evidence submission API** | Simple interface: agent calls `submit_evidence(agent_id, evidence_payload)` → COC system handles hashing, signing, chaining, writing. |
| 4.6 | **Verification tool** | `scripts/4x_coc_verify.py` — verify entire COC chain integrity + signature validity. |

### Phase 5: OpenHands SDK + Spawning 🔧
**Goal:** OpenHands SDK installed and working in faerie2 venv. Spawning functional.

| # | Task | Details |
|---|------|---------|
| 5.1 | **Install OpenHands SDK** | `pip install openhands-sdk openhands-tools` in faerie2 venv. Currently NOT installed (blocker). |
| 5.2 | **Configure LLM** | Set up `LLM()` with OpenRouter (already in global agent_settings.json). Model: `openrouter/owl-alpha` or similar. |
| 5.3 | **Test spawning** | Create a minimal agent with Terminal + FileEditor + TaskTracker tools. Verify `Conversation.send_message()` + `conversation.run()` works. |
| 5.4 | **Integrate with faerie spawn** | Connect OpenHands SDK spawning to faerie's spawn protocol (piston waves, archetypes, manifests). |
| 5.5 | **OpenRouter LangChain SDK** | Already installed. Verify it works alongside OpenHands SDK. Multi-model routing: W1 (free) → W2 (Claude) → W3 (premium). |

### Phase 6: VPS Deployment Infrastructure 🚀
**Goal:** All startup scripts and deployment configs for DigitalOcean droplet in one place.

| # | Task | Details |
|---|------|---------|
| 6.1 | **Create `infrastructure/vps/` folder** | Dockerfile, docker-compose.yml, systemd services, nginx config, setup scripts. |
| 6.2 | **Startup scripts** | `infrastructure/vps/scripts/0x_bootstrap.sh` — full VPS bootstrap: OS deps, Python venv, OpenHands CLI + SDK, faerie2 clone, hooks, skills, config. |
| 6.3 | **Native Linux setup** | Configure for native Linux (not WSL). GUI-capable. All env vars point to VPS paths. |
| 6.4 | **LangChain integration** | Connect to ZimaBoard LangChain Docker instance. Shared SDK config. |
| 6.5 | **Beta site app scaffolding** | Faerie as a beta site app for product testing. MVP chat interface. Proper membench integration. WANDB project tracking. |

### Phase 7: Merge to Main 🏁
**Goal:** Clean merge of `openhands-migration` → `main`.

| # | Task | Details |
|---|------|---------|
| 7.1 | **Archive old branches** | Tag and archive stale branches. Keep only `main` + `openhands-migration`. |
| 7.2 | **Final crystallization** | Run `faerie crystallize` — full system consolidation. Dead weight removal. Doc consolidation. |
| 7.3 | **Pre-merge validation** | All probes pass. Dashboard shows healthy. COC chain intact + signatures valid. |
| 7.4 | **Merge** | `openhands-migration` → `main`. Tag release. |

---

## 🔗 Key Dependencies

```
OpenHands SDK (pip install openhands-sdk openhands-tools)  ← BLOCKER: not installed
    ↕
faerie lifecycle tools (.openhands/skills/faerie/)
    ↕
membench probes (scripts/membench/probes/)
    ↕
eval harness (scripts/membench/eval/)
    ↕
COC signing system (scripts/coc/ + forensics/.keys/)
    ↕
unified dashboard (scripts/membench/reports/)
    ↕
WANDB (wandb 0.26.0 already installed)
    ↕
ZimaBoard LangChain (remote, via API)
```

## 📐 FFMx Optimization Targets

| Metric | Current | Target | Emoji |
|--------|---------|--------|-------|
| f(0) orchestration burden | ~8% | ≤5% | ⚙️ |
| M1 (Retention) | unknown | ≥0.85 | 🧠 |
| M3 (Parallelization ROI) | unknown | >1.10 | 🔄 |
| M8 (Confabulation) | unknown | ≤0.05 | 🛡️ |
| M11 (Honey Hit Rate) | unknown | ≥0.70 | 🍯 |
| FFMx (Force Multiplier) | ~44.4 | >30/session | 🚀 |
| Emergence trajectory | unknown | ≥-0.03 (3 sessions) | 🌊 |

## 🧭 Bearing Priority

1. **🧭 W (West)** — Baseline first. Flatten scripts + RAP audit. Consolidate eval infrastructure.
2. **🔄 N (North)** — Unblock SDK integration. Install OpenHands SDK. Get spawning working.
3. **🔨 S (South)** — Ship config migration. Faerie2 becomes global config home. Env vars consolidated.
4. **🌊 E (East)** — Parallel: COC signing + SpiderFoot, VPS scaffolding, beta app.

## 📁 Key Paths

| Path | Purpose |
|------|---------|
| `scripts/` | Operational scripts (tier-prefixed: 0x–9x) |
| `scripts/membench/` | **Canonical eval system**: probes/, eval/, reports/, adapters/, collectors/ |
| `config/` | **NEW** — agent_settings.json, config.toml, cli_config.json (global config home) |
| `.openhands/skills/faerie/` | Lifecycle tools (evolve, crystallize, spawn, bundle, inject, orchestrate) |
| `.openhands/skills/spiderfoot/` | OSINT tool (evidence → COC signing) |
| `.openhands/hooks/` | 3x_hook-operation-logger.py, 4x_hook-security-assurance.py (tier-prefixed only) |
| `infrastructure/vps/` | **TO BE CREATED** — VPS deployment configs and startup scripts |
| `forensics/` | Repo forensics (COC, evals, artifacts) |
| `/mnt/d/0LOCAL/0forensics/` | Global forensics (mirrored/symlinked from repo) |
| `/mnt/d/0local/gitrepos/faerie-vault/80-Publications/` | Hot research outputs (emergence, membench, stigmergy, mutation, RAP) |
| `/mnt/d/0local/gitrepos/faerie-vault/` | Vault root (investigation hub + findings archive) |

---

## 🚨 Known Blockers

| Blocker | Impact | Resolution |
|---------|--------|------------|
| OpenHands SDK not in venv | Can't spawn agents | `pip install openhands-sdk openhands-tools` |
| `scripts/canonical/` confusion | Duplicate/stale scripts | Flatten + RAP audit |
| Non-prefixed hooks | Equilibrium violation | Remove duplicates, keep 3x/4x only |
| No `.env.local` | Hardcoded paths everywhere | Create from `.env.example` |
| COC signing not implemented | Agents can't submit evidence | Implement ED25519 key management |

---

*Plan v2: 2026-05-10T12:30:00Z — added config migration, COC signing, SpiderFoot integration, env var consolidation, RAP evaluation*
*Next review: End of day or after Phase 1 completion*
