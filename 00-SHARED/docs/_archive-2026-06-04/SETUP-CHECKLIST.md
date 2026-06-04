---
type: guide
status: active
created: 2026-04-21
tags: [setup, checklist, installation]
up: README.md
prev: COMMAND-GUIDE.md
next: ONBOARDING.md
---

> [↑ Readme](README.md) · [← Command Guide](COMMAND-GUIDE.md) · [→ Onboarding](ONBOARDING.md) · [⌂ Home](../README.md)

# Model Routing Setup Checklist

**Status:** ✅ **READY FOR DEPLOYMENT**

## What's Complete

### ✅ Core Infrastructure

- [x] **AGENT-TYPE-ROUTING.json** — Authoritative routing table (15 agents)
  - **Locations:** 
    - Repo-local: `/mnt/d/0local/gitrepos/faerie2/.claude/AGENT-TYPE-ROUTING.json` (git-tracked, definitive)
    - Global: `/mnt/d/0LOCAL/.claude/AGENT-TYPE-ROUTING.json` (runtime access, synced with repo)
  - Contents: wave + model + reasoning_budget for every agent type
  - Machine-readable JSON (can be read by faerie, eval harness, audit tools)

- [x] **SPAWN-BOILERPLATE.md** — Updated with model routing section
  - **Location:** `/mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md` (26KB, git-tracked)
  - Integration: `build_spawn_bundle.py` reads this file at spawn time ✓
  - Tested: `python3 scripts/build_spawn_bundle.py --agent-type python-pro` loads it successfully ✓
  - Contains MODEL ROUTING section with wave-based defaults table and reference to AGENT-TYPE-ROUTING.json

- [x] **8x_roster_update.py** — Captures spawn metadata
  - **Location:** `/mnt/d/0local/gitrepos/faerie2/scripts/8x_roster_update.py` (400 lines, git-tracked)
  - **Function:** Reads Agent() spawn events → looks up AGENT-TYPE-ROUTING.json → extracts wave → appends to roster.json
  - **CLI:** `--register`, `--report [SESSION_ID]`, `--compute-rates`
  - **Status:** Ready for PostToolUse hook integration (needs settings.json wiring)

- [x] **eval_harness.py** — Computes model routing dimension
  - Status: Already implemented (Dimension F)
  - Metrics: haiku_w1_rate, sonnet_w2_rate, opus_rate
  - Tested: `python3 scripts/eval/eval_harness.py` produces eval output ✓
  - Membench: Already integrated via --membench flag ✓

### ✅ Documentation

- [x] **MODEL-ROUTING.md** — Quick reference + examples (254 lines)
- [x] **ARCHITECTURE-MODEL-ROUTING.md** — System diagram + data flows (212 lines)
- [x] **SETUP-CHECKLIST.md** — This file

### ✅ Git Commits

- Commit 44a979a: feat(model-routing): implement Haiku-default policy + 8x_roster_update.py hook
- Commit a3ca8db: refactor(model-routing): centralize routing logic in AGENT-TYPE-ROUTING.json
- Commit c173052: docs(architecture): visual guide to model routing system

## What Needs to Happen Next

### Phase 1: Hook Integration (5 minutes)

**Wire 8x_roster_update.py as PostToolUse hook**

```bash
# Edit ~/.claude/settings.json (or .claude/settings.json in repo)
# Add to hooks.post_tool_use:
{
  "matcher": {"tool_name": "Agent"},
  "script": "/mnt/d/0local/gitrepos/faerie2/scripts/8x_roster_update.py",
  "enabled": true
}
```

**Result:** Every Agent() call automatically appends to `~/.claude/hooks/state/subagent-roster.json`

### Phase 2: Audit Integration (10 minutes)

**Wire audit-equilibrium pre-commit check**

```bash
# Edit .git/hooks/pre-commit
# Add:
python3 -m skills audit-equilibrium --check-routing

# Or via git config:
git config core.hooksPath .claude/hooks
# Then create .claude/hooks/pre-commit with the check
```

**Result:** Commit fails if agent.md:model != AGENT-TYPE-ROUTING.json:default_model

### Phase 3: Faerie Integration (20 minutes)

**Update faerie to read AGENT-TYPE-ROUTING.json at spawn time**

Current flow:
```
build_spawn_bundle.py → reads HONEY.md + SPAWN-BOILERPLATE.md → generates prompt
```

New flow (optional enhancement):
```
faerie_spawn.py reads AGENT-TYPE-ROUTING.json
  → looks up agent_type
  → extracts (wave, model, reasoning_budget)
  → passes to build_spawn_bundle.py
  → injects into prompt context
```

This enables:
- Model selection is data-driven (from routing table)
- Faerie can warn if agent_type is not in routing table
- Cost estimation can be automatic

## Verification Steps

### 1. Routing Table is Accessible

```bash
python3 -c "import json; print(json.load(open('/.claude/AGENT-TYPE-ROUTING.json')))['agent_types']['python-pro']"
```

Expected output:
```json
{
  "wave": 2,
  "default_model": "claude-haiku-4-5-20251001",
  "reasoning_budget": "none",
  ...
}
```

### 2. Boilerplate is Loadable by Faerie

```bash
python3 scripts/build_spawn_bundle.py --agent-type python-pro --task-id 1 --task-description "test" 2>&1 | grep -A 2 "MODEL ROUTING"
```

Expected: Shows MODEL ROUTING section from boilerplate ✓

### 3. Roster Capture Works (after hook integration)

```bash
# Spawn an agent (any agent)
# Then check:
cat ~/.claude/hooks/state/subagent-roster.json | python3 -m json.tool | tail -20
```

Expected: Latest entry shows the agent you just spawned

### 4. Eval Computes Model Routing (after roster data exists)

```bash
python3 scripts/eval/eval_harness.py
```

Expected: Dimension F shows haiku_w1_rate, sonnet_w2_rate, opus_rate values

## How It Works Once Wired

### Scenario: Spawn python-pro agent

```
1. Faerie reads AGENT-TYPE-ROUTING.json["python-pro"]
2. Extracts: wave=2, model=haiku, reasoning_budget=none
3. Calls build_spawn_bundle.py
4. build_spawn_bundle.py loads SPAWN-BOILERPLATE.md
5. Injects MODEL ROUTING section into prompt:
   "Model: claude-haiku-4-5-20251001 (from AGENT-TYPE-ROUTING)
    Reasoning budget: none
    Wave: 2"
6. Agent spawned via Agent() tool
7. Hook captures: {agent_type: "python-pro", model: "haiku", wave: 2, ...}
8. Appends to roster.json
9. Next eval run computes: haiku_w1_rate = X/Y
10. Dimension F score reflects model routing efficiency
```

## Cost Baseline (Before Optimization)

Current system (vanilla Sonnet by default):
```
6 W1 agents × $0.034 = $0.204
5 W2 agents × $0.034 = $0.170
4 W3 agents × $0.034 = $0.136
────────────────────────
Total per session: $0.510
```

Optimized (Haiku-first):
```
6 W1 agents × $0.009 = $0.054
5 W2 agents × $0.022 = $0.110 (4 haiku @ $0.009, 1 sonnet @ $0.034)
4 W3 agents × $0.060 = $0.240 (1 haiku @ $0.009, 2 sonnet @ $0.034, 1 opus @ $0.170)
────────────────────────
Total per session: $0.404
```

**Savings: 20.8%** (or ~$0.10 per session, ~$2.50/week)

## Files Ready to Go

| File | Size | Status | Used By |
|------|------|--------|---------|
| AGENT-TYPE-ROUTING.json | 18KB | ✓ Complete | faerie, eval, audit |
| SPAWN-BOILERPLATE.md | 26KB | ✓ Complete | build_spawn_bundle.py |
| 8x_roster_update.py | 8KB | ✓ Complete | PostToolUse hook |
| eval_harness.py | 139KB | ✓ Complete | eval suite |
| MODEL-ROUTING.md | 16KB | ✓ Complete | Human reference |
| ARCHITECTURE-MODEL-ROUTING.md | 9KB | ✓ Complete | System documentation |

## Success Criteria

After integration:

- [ ] Hook fires on every Agent() call
- [ ] Roster captures spawn metadata (agent_type, model, wave, cost)
- [ ] eval_harness.py computes haiku_w1_rate ≥ 0.80, sonnet_w2_rate ≥ 0.90, opus_rate < 0.05
- [ ] Turn 0 dashboard shows "model_routing: 0.XX" in composite score
- [ ] Cost per session drops 20% vs vanilla (measurable via roster)
- [ ] Audit tool flags any agent.md ↔ routing table mismatch at commit time

---

**Next Action:** Wire 8x_roster_update.py as PostToolUse hook in settings.json (5 min)

Then: Verify roster.json gets populated on next Agent() spawn

Then: Run eval and see haiku_w1_rate, sonnet_w2_rate computed

**Status:** All code ready; awaiting hook integration.
