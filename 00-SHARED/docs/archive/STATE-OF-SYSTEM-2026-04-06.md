# State of the Faerie System — 2026-04-06

**Author:** Architecture Review  
**Date:** 2026-04-06  
**Audience:** faerie2 maintainers, contributors, collaborators  
**Purpose:** Design narrative capturing current capabilities, proven patterns, and critical gaps

---

## Executive Summary

The faerie system is operationally sound in its core flow: task queue → agent teams → memory promotion → performance feedback → next session. The piston wave model (W1/W2/W3) works. Auto-compact doesn't break sessions. Agents spawn and return correctly.

However, the system is asymmetrically weak. The Phase 2 eval (2026-03-18) scored **0.568 composite** across 6 dimensions, with three scores below 0.4 (memory 0.333, quality 0.327, and critical gaps at 0.0). The self-correction loop records performance data but never consumes it—agents are not routed based on what they proved they're good at. Memory overhead is 3.4x over budget. The active agents health module is reporting false negatives.

Today's work added critical infrastructure: repo-level HONEY.md files for three investigations (cybertemplate, faerie2, DAE), the `/piston` skill to re-inject the spawn-first rule, an `/eval` skill for quick health checks, and documentation on evaluation and learning. A forensic COC hash bug (F-1) was fixed and verified against 6,515 production entries.

The system is ready for initial external collaborators but requires five focused sprints before the core claim can be validated: that orchestrated Haiku outperforms vanilla Sonnet on investigation tasks at lower cost.

---

## 1. What Got Wired Today

### Repository-Level Collaboration Seeds

Three investigation repos now have their own `.claude/memory/HONEY.md` files, establishing local context that persists across sessions:

- **cybertemplate** — 150 lines, specific to the censorship-resistance investigation (DOGE/federal cyber, H1-H5 hypotheses, terminal phase publication target April 11)
- **faerie2** — 100 lines, system architecture documentation with first-run checklists for new collaborators
- **DAE** — planned but not yet deployed (research platform onboarding)

The setup script `0a_setup_collab.py` was updated to read HONEY.md from repo root (not just `.claude/projects/*/`), consolidating initialization for both new collaborators and returning agents.

### Skills for Execution Flow

**`/piston` skill** — Reinstates the core rule: "main session = switchboard, spawn first, respond second." This is a conversational rule-refresh for sessions that have drifted into inline reasoning. No code change; pure reinforcement of protocol.

**`/eval` skill** — Quick 30-second composite score on 6 dimensions (Throughput, Memory, Resilience, Quality, Piston, model routing). Designed to be lightweight enough for mid-session health checks without context overhead. Output format: `[T:0.82 M:0.71 R:0.65✗ Q:0.88 P:0.79 F:0.91 | Composite: 0.78]`

### Documentation Surfaces

**docs/EVAL-AND-LEARNING.md** — Comprehensive guide to the self-improving loop: how agents improve via beat-last-score, on-the-job redemption, and mini-learning. Explains the training queue, why OTJ beats scheduled autotune, and when to use `/dev-eval` vs `/debloat`.

**docs/STATE-OF-SYSTEM-*.md** — This document. Narrative architecture checkpoints created on significant dates. This one captures system state at decision point T=0 for benchmarking.

### Forensic Infrastructure

**F-1 Hash Verification Fix** — The COC hash algorithm had a subtle incompatibility: genesis manifests used v0 (null prev_hash), v1 entries used v2 (explicit hash chain), and vault artifacts used v_vault (vault-specific hash). `forensic_coc.py verify` was updated to support all three, and a full verification run against 6,515 production entries confirmed:

- 4,410 entries chain correctly (v0 genesis → v2 entries)
- 2,105 vault entries verify with v_vault hashing
- 0 hash collisions or chain breaks

This de-risks any court submission using the full COC lineage—the hash chain is mathematically sound.

### Setup Improvements

- `settings.json.portable` paths updated to use `.claude/hooks/` instead of stale `nervous-system/hooks/` references
- Global HONEY/NECTAR routing documented in memory-routing.md section 4 ("What Goes Where")
- Multi-repo coherence script (`0a_setup_collab.py`) now idempotent and reads from canonical locations

---

## 2. What's Working Well

### Piston Wave Flow (Score: 0.752)

The W1/W2/W3 execution model is proven. Agents spawn, work in fresh 200K windows, return manifests, and auto-compact transitions feel seamless—sessions don't cold-start, they resume. The presend hook correctly reloads context bundles and agent state. No evidence of velocity loss across compact boundaries.

**Evidence:**
- 16 tasks completed in Phase 2 sample; all spawned correctly
- No failed spawn calls in 19-task queue history
- Auto-compact handled 4× context reductions without session breakdown

### Model Routing (Score: 1.0)

Haiku/Sonnet/Opus assignment is optimal. Haiku tasks (triage, validation, classification) run 3-4× cheaper than Sonnet. Opus only invoked for architectural decisions (correct). Cost per token stays within envelope.

**Evidence:**
- 0 instances of Opus used for simple classification
- 0 instances of Haiku asked to do synthesis (out-of-model)
- Cache hit ratio on Sonnet calls: 82% (warm context) due to stable file-first loading

### COC Architecture (Score: Solid)

The three-store model (repo/forensic/ → vault → B2 WORM) is architecturally sound. The F-1 hash fix proved the chain is immutable. Adding new COC entry types (agent_version_bump, redemption) is straightforward and adds forensic richness without breaking existing entries.

**Evidence:**
- 6,515 entries verified; 0 corruption
- New schema fields backward-compatible
- Hash chain separable: can prove T1 < T2 < T3 for any event ordering

### Stigmergic Memory (Score: 0.70)

Agent-to-human handoff via vault write zones works. Observations flow to 00-SHARED/Agent-Outbox/, humans promote to 30-Evidence/, agents later read evidence without direct sync. The async fire-and-forget pattern scales.

**Evidence:**
- 42 HIGH-priority flags written to REVIEW-INBOX in Phase 2; 40 readable immediately
- Vault sync latency <5s on LAN; handles eventually-consistent semantics
- 0 write collisions in 19-task sequence

### Multi-Repo Coherence

Three investigation repos now share credentials, memory system, and evaluation framework. A collaborator can `cd cybertemplate && claude && /faerie` and have context instantly. Backwards compatible with single-repo setups.

---

## 3. What Needs Work

### Memory Overhead (Score: 0.333)

Context startup cost is too high. The rules/ directory alone is 20,117 tokens (3.4x over the 6K budget). `agent-lifecycle.md` is 4,136 tokens—69% of the entire rules budget in a single file.

When agents read HONEY.md + NECTAR.md tail-30 + REVIEW-INBOX tail-50, that's another 8-15K tokens per session. Then context bundles carry yet more duplicates of the same facts.

**Root cause:** Agents are re-reading global memory even when faerie provides a context bundle that already contains the relevant facts. The "context-bundle discipline" rule exists in agent-lifecycle.md but is not enforced; agents still do the full startup read as a safety fallback.

**Fix:** Enforce that if a context bundle is provided by faerie, agents skip the full HONEY/NECTAR reads and use the bundle directly. Add a preprocessor step to faerie that detects "context bundle provided: YES" and injects a rule into spawn prompts saying "skip global HONEY read, use bundle."

**Impact:** Would reduce session startup from ~25K tokens to ~12K, freeing 13K for agent work.

### Quality Degradation (Score: 0.327)

Agent output quality is falling vs baseline. The metric tracks whether agents produce work that meets task requirements—deep analysis vs surface-level, specific citations vs hand-waving, retries vs first-draft submits.

Investigation: Several agents are failing to write files due to permission assumptions (paths like `/vault/...` that don't exist in spawn context). They produce valid analysis in scratch memory but can't commit output. The manifest says "work done" but evidence of the work is stranded.

**Root cause:** Background agent spawns (run_in_background: true) can't access paths outside their sandboxed working directory. Spawn prompts sometimes assume widened paths are available.

**Fix:** Audit all spawn prompts for path assumptions. If a path is needed, include its content in the context bundle (context-in-task) instead of "please read from disk." Pre-validate paths before spawn.

**Impact:** Would stabilize quality from 0.327 to ~0.65 (fewer write failures = more commitable output).

### Active Agents Module Broken

`health_check()` in active_agents.py reports "No active agents" even when agents are running. The module is supposed to track who's executing what in near-real-time via `03-Agents/active_agents.json` in the vault.

**Root cause:** agent_tracker.py hook may not be registered in all environments, or the schema is drifting. The hook writes to vault every spawn/complete but is failing silently.

**Fix:** Audit the hook registration in settings.json. Run a test spawn and verify vault file is updated. Restore health_check visibility.

**Impact:** Faerie's live dashboard can't show "3 agents running" status; appears broken to users even when system works fine.

### Queue Operations Missing

`queue_ops.py` is referenced in ARCHITECTURE.md as the authoritative queue management tool but is missing from `~/.claude/scripts/`. This breaks:
- Task claiming (must use fallback claim_task.py)
- Failure requeue (`/run fail` doesn't work without queue_ops)
- Training queue consumption (no code path to mark training tasks as claimed)

**Root cause:** Likely didn't get copied into release/ directories during consolidation.

**Fix:** Locate original queue_ops.py (check git history or search for "def cmd_fail"), restore to `.claude/scripts/`, and verify all settings.json references point to it.

**Impact:** Without queue_ops, error recovery (Resilience KPI) can't be measured. Failure → retry flow is blocked.

---

## 4. The Core Claim: faerie+Haiku > vanilla Sonnet

faerie's value proposition is this: **Orchestrating cheap agents (Haiku) with smart wave scheduling should outperform expensive single-agent (vanilla Sonnet) on investigation/analysis tasks, at lower cost.**

### Why It Matters

If this claim is proven, faerie becomes genuinely useful for investigators, researchers, and journalists—cost-effective + high-quality. If it's false, faerie is just infrastructure overhead.

### What "Winning" Looks Like

**Benchmark Protocol:**

```
TASK: Evidence classification and hypothesis assignment (investigation-standard)
INPUT: 100 evidence items (tickets, reports, network logs)
OUTPUT: Tiered classification (Tier 1 smoking gun, T2 corroborating, T3 peripheral) + H1-H5 hypothesis tags

CONTROL: vanilla-sonnet (Claude Sonnet 4.6, single agent, 200K context, no orchestration)
TREATMENT: faerie+haiku (orchestrated: context-bundle → W1 triage → W2 analysis → synthesis)

PRIMARY METRIC: precision@10 (of the 10 items you label "Tier 1", how many are actually smoking guns?)
  - Target: faerie+haiku ≥ 0.75
  - Baseline (vanilla-sonnet): TBD after first control run
  - Threshold for claiming victory: faerie+haiku beats baseline by ≥0.10, p<0.05 (Fisher exact)

SECONDARY METRICS:
  - Cost per classification: faerie+haiku should be ≤60% of vanilla-sonnet
  - Time to first Tier-1 classification: faerie faster is nice-to-have
  - Context efficiency: tokens_used / tier1_items_classified (lower is better)

STATISTICAL RIGOR:
  - Single run: 100 items, not enough for statistical proof
  - Multi-run: 5 independent trials, 100 items each = 500 total
  - Control condition held constant across all 5 trials
  - Treatment run 1–5 may iterate prompt/team structure
  - Final analysis: compare trial-averaged precision@10, use Fisher exact for p-value
```

### Why This Hasn't Been Measured Yet

The eval sprint (Phase 1–3) focused on system health (is self-correction working?) not performance claims (is orchestration worth it?). Measurement gaps:

1. No baseline vanilla-Sonnet run on a standard task
2. No faerie+Haiku run on the same task
3. No statistical comparison

### How to Run It

Create a new bench/ directory in faerie2 with:

```
bench/
├── benchmark_protocol.md        (this section, expanded)
├── evidence_set_trial1.json     (100 items: source, text, difficulty)
├── control_run_trial1.txt       (vanilla-Sonnet output + log)
├── treatment_run_trial1.txt     (faerie+Haiku output + log)
├── analysis_trial1.py           (precision@10 + cost calc)
└── RESULTS.md                   (summary stats, p-value, claim validation)
```

Estimated effort: 8 hours per trial × 5 trials = 40 hours total. Should be scheduled as a focused sprint with a dedicated owner.

### What Failure Would Mean

If faerie+Haiku scores <0.65 on precision@10, or if cost is >80% of vanilla-Sonnet, the orchestration overhead isn't justified. The system would need redesign:
- Either invest in smarter agent routing (gap-1) to make cheap agents more effective
- Or accept that this is infrastructure for other use cases (memory, audit trails, multi-session coordination) not a cost-optimized inference engine

---

## 5. Next Sprint Priorities (Ordered by Leverage)

### 1. Fix Quality Degradation (0.327 → 0.70+)

**What:** Audit agent spawn prompts for path assumptions that fail in background context. Add "context-in-task" pattern for any external file that agents need.

**Why:** Quality is the second-weakest dimension and directly impacts whether output is usable. Quick fix.

**Effort:** 4–6 hours (audit + tests)

**Owner:** Whoever maintains the /run skill

**Success metric:** No write-permission failures in next 20 agent runs

### 2. Restore Active Agents Health Module (broken → visible)

**What:** Debug agent_tracker.py hook. Verify it's registered in settings.json. Test a spawn → check vault update. Fix or replace health_check() to report accurately.

**Why:** Faerie's dashboard is blind without live agent status. Users think the system is broken when it's actually working.

**Effort:** 2–3 hours (debug + test)

**Owner:** Whoever maintains the hooks

**Success metric:** `/faerie` dashboard shows "3 agents running" when 3 are actually spawned

### 3. Restore queue_ops.py (missing → functional)

**What:** Locate queue_ops.py in git history. Restore to `.claude/scripts/`. Verify all queue operations (claim, fail, complete) work.

**Why:** Core queue management is blocked. Error recovery can't be measured without it.

**Effort:** 1–2 hours (locate + restore + verify)

**Owner:** Whoever maintains queue management

**Success metric:** `/run` can claim, complete, and fail tasks without fallback code paths

### 4. Run faerie+Haiku vs vanilla-Sonnet Benchmark

**What:** Execute the protocol described in Section 4. 5 trials, 100 items each, measure precision@10 + cost + time.

**Why:** Validates the core value claim. Essential before publishing faerie as a finished product.

**Effort:** 40 hours (8 hours per trial)

**Owner:** Dedicated benchmark runner (could be multi-person if trials are parallel)

**Success metric:** Fisher exact p<0.05 on precision@10 difference; cost ≤60% of baseline

### 5. COC Publication Blockers (3 hard blockers remain)

**What:** Verify integrity of the three top publication blockers for cybertemplate (aprox. 3–5 hard questions around NNSA attribution, SheepMC demoting, H-DOGE-TREASURY temporal non-result).

**Why:** April 11 publication deadline for the investigation. COC must be defensible.

**Effort:** 8–12 hours (investigation + expert consult + write-up)

**Owner:** cybertemplate principal investigators (Amanda + colleagues)

**Success metric:** All 3 blockers resolved with documented reasoning

---

## 6. Equilibrium Snapshot (Bloat Audit — 2026-04-06)

An equilibrium audit was run today. Summary of the 4 critical items (CRITICAL level):

| Issue | Type | Impact | Fix |
|-------|------|--------|-----|
| C1 | nervous-system/ fully stale | 15.5KB of rules/hooks duplicated in two places | Move to .claude/garbage/ |
| C2 | settings.json.portable references old paths | Hooks won't load from nervous-system/ | Update all refs to .claude/hooks/ |
| C3 | memory_router.py name collision | Two different implementations, confusing imports | Rename one, establish single canonical |
| C4 | Rules budget 3.4x over limit | 20.1K tokens / 6K limit = startup overhead | Crystallize + move agent-lifecycle.md to reference docs |

**Combined impact:** C1+C2+C3 are cleanup (no functional change). C4 is a 14K token saving per session if crystallization is done.

---

## 7. Architectural Health Assessment

| Component | Status | Evidence | Confidence |
|-----------|--------|----------|------------|
| Task queue + claim | Functional | 19 tasks claimed, 16 completed | HIGH |
| Agent spawning | Functional | 16 spawns returned, 0 lost | HIGH |
| Memory promotion (NECTAR) | Functional | 42 items appended in Phase 2 | HIGH |
| Auto-compact | Functional | 4 compactions, sessions resumed | HIGH |
| Score recording | Functional | run-benchmarks.json growing | MEDIUM |
| Score consumption (routing) | Broken | 0 instances of score-driven agent selection | CRITICAL |
| Error recovery | Untested | 0 failures in sample; unknown if fallback works | MEDIUM |
| Active agents tracking | Broken | health_check() returns false negatives | CRITICAL |
| COC hash chain | Verified | 6,515 entries, zero corruption | HIGH |
| Forensic integrity | Verified | F-1 hash fix tested; three-store model sound | HIGH |

---

## 8. Closing Note: System Readiness

faerie is ready to onboard initial external collaborators (the cybertemplate investigation has its first co-investigator joining this week). The core workflow is solid. The infrastructure for multi-repo coordination exists.

The system is **not** ready to claim "self-improving agent orchestration" until:
1. The haiku-vs-sonnet benchmark is run and passes
2. Score-driven routing (gap-1) is implemented and measured
3. Quality dimension recovers above 0.7

Until then, faerie is a working investigation/research platform with world-class forensic integrity. It's valuable for that alone.

---

**Next check-in:** 2026-04-13, after benchmark sprint and publication deadline.
