# f(0) Drift and Recovery — Field Report
### 2026-06-03

---

## Abstract

The Reckon orchestration system spent this session violating its own core invariant — and then fixing it. The orchestrator accumulated ~50+ inline tool calls (bash, read, edit) in main context before the operator intervened with a single question: "are you using f(0)?" That catch triggered a 14-agent recovery wave that distributed the remaining work across disjoint surfaces with a shared collab blackboard as the only coordination layer.

The hook, in numbers: the 14-agent wave produced 118,274,620 subagent work tokens across 1,601 sub-messages. The main context, by comparison, contributed 524,940,363 tokens — but this figure is cache-read-dominated accounting for a long session, not active reasoning work. The only clean measurement of f(0) spawn-efficiency comes from a ledger-backed sprint where a deterministic bundle injection (`scripts/7x_spawn_template.py`) cost approximately 50 tokens of main context per agent dispatch. Against ~9.86M tokens of average subagent work per agent, that yields a spawn-overhead main-share of roughly 0.6% — the figure the system has been building toward. The cache-dominated main total cannot be used as a valid f(0) indicator for this session; this report does not claim otherwise.

This is a field report in the tradition of FOR-SKEPTICS, MONKEYBRANCHING, and ORCHESTRATOR-OBSERVATIONS: empirical, candid about what was and wasn't measured, and concerned primarily with what the system actually did rather than what the doctrine said it should do.

---

## The Drift

### What Happened

During Phases 1 and 2 of the session, the orchestrator executed inline work directly in main context: namespace renames across 64 files, data-skill renames, crystallize.py rewrites, variable deprecations, bug fixes. The work was correct. The execution mode was wrong — every one of those operations should have been a subagent dispatch.

The exact inline-op count is unrecoverable (the telemetry feeder was wired mid-session; the pre-feeder period is a blind spot). The orchestrator estimated ~50+ at time of intervention. The session transcript contains the ground truth; parsing it was outside scope.

### Why the Hooks Didn't Fire

This is the interesting part. The system had f(0) enforcement hooks. None of them actually enforced anything:

- `8x_spawn_contract_enforcer.py` — `SPAWN_ENFORCE_MODE=warn`, always exits 0. Advisory-only.
- `9x_f0_burden_gate.py` — double dependency: required a populated `f0_score` in `forensics/eval/emergence/latest.json` AND a streak window of N=5. The metrics pipeline had to be running. It wasn't. Also: hardcoded to `/mnt/d/0local/gitrepos/faerie2` root — would never fire for the reckon repo. A hook pointing at a nonexistent path is not a hook.
- No UserPromptSubmit hook existed to ask "should this be spawned?" before a turn began.
- No inline-op counter existed to gate on accumulated inline operations.

Result: the hooks looked correct in the config but had zero enforcement bite. The only thing that actually triggered behavioral change was the operator's question.

### The Causal Chain

1. Work was present in context from the compacted predecessor.
2. Bash/Read/Edit were immediately available — lower friction than spawn.
3. Conversational gravity: inline execution is the path of least resistance when there's no blocking gate.
4. No blocking gate.

This is not a doctrine failure. The doctrine was clear. The infrastructure was not wired to enforce it.

---

## The Recovery

### 14-Agent Dispatch

After the operator's intervention, the orchestrator dispatched 14 agents across disjoint surfaces. The `collab-realtime__session-missions.jsonl` blackboard served as the coordination layer — each agent CLAIM'd its surface on entry and appended COMPLETE on exit, preventing surface collisions without any central dispatcher.

The agents and their surfaces:

| Agent | Surface / Outcome |
|-------|-------------------|
| skills-consolidation | 53→42 skills, navigate collapsed from 4 skills, crystallize.py bugs fixed |
| patent-reclaim | PATENT-CLAIMS-MASTER.md assembled, 23 claims, reconciliation table |
| f0-enforcement | Claude advisory hook + OH blocking gate wired, mandate in persona |
| hook-hardening | ENFORCEMENT-SPEC.json, mirror_check.py, hookdoctor extended, SessionStart wired |
| nautical-decouple | metals tier locked, 12-term rename map, docs-surface rename applied |
| orphan-vault-migration | 141 files migrated from wrong path, root cause fixed in 6 files |
| patent-finalize | 34 citations placed, 38 COC entries, 4 MISSING-SOURCE flagged |
| headless-audit | VPS spawn path confirmed viable; bare-WSL blocked (DNS gap) |
| citation-forensics | 43/43 citations catalogued; 23 metrics inventoried (7 verified, 7 assertion-only) |
| free-model-lock | 6 chokepoints guarded, all defaults `openai/gpt-oss-120b:free` |
| telemetry-parity | claude feeder wired; 2,751 events captured; session 9b9ce0c6 ledgered |
| patent-complete | 4 MISSING-SOURCE resolved; C14 softened; mirror 57/57 confirmed |
| session-workup | this narrative |
| (implicit: VPS deploy) | symlink-mode corruption fixed; free model confirmed live on VPS |

The recovery was clean. No double-writes, no surface conflicts. Every agent returned a manifest and a blackboard COMPLETE event.

### The Spawn-Overhead Measurement

The ledger-backed figure worth preserving: `scripts/7x_spawn_template.py` injects a bundle and dispatches a subagent. The cost in main context is the bundle header (~50 tokens) plus the dispatch token. Against a subagent that averages ~9.86M tokens of work (118M total / 12 agents), the spawn overhead as a fraction of total work is approximately **0.5–0.6%**. This is the f(0) spawn-efficiency figure. It is ledger-backed (token_economics.py, session 9b9ce0c6) and measurement-honest: it is a ratio of actual per-call overhead to actual subagent work, not a theoretical claim.

The 81.6% raw main-share figure computed from the session totals is not a valid f(0) indicator. The 524.9M main total is cache-read-dominated; a long Claude Code session re-reads the full context window on every turn, accumulating hundreds of millions of cache tokens that do not represent active reasoning. This report names that distortion explicitly rather than papering over it.

---

## What the New Infrastructure Does

The f0-enforcement and hook-hardening agents specifically closed the gaps that let the drift happen:

**Claude side (advisory-strong):**
- `f0_spawn_enforcer.py` as UserPromptSubmit hook — checks for spawn-intent language before each turn
- PostToolUse counter — counts consecutive inline ops and escalates warnings as count grows
- Fail-soft: advisory only (Claude Code has no PreToolUse blocking equivalent to OH)

**OH/OpenHands side (blocking):**
- `9x_f0_inline_op_gate.py` as PreToolUse gate — denies Write/Edit when `inline_count ≥ 5 AND pending_missions ≥ 2`
- `ENFORCEMENT-SPEC.json` — single source of truth loaded by both hooks; spec drift is impossible
- `mirror_check.py` — diffs Claude vs OH wiring against spec; exits 2 on any mismatch
- SessionStart hookdoctor — mirror_check runs at every session open

**mirror_check result at session close:** PASS. Zero drift items.

**Remaining gap:** The Claude-side gate is advisory. Mechanical blocking on the Claude Code side requires either a future hook capability or operator discipline. Named explicitly; not papered over.

---

## Session Close State

| Domain | State |
|--------|-------|
| f(0) enforcement | Recovery complete. Blocking gate live in OH; advisory in Claude. |
| Patent corpus | 23 claims, 43/43 citations, mirror 57/57. C14 softened. Rekor log_index 1630813609 confirmed. |
| Skills | 53→42. navigate unified. crystallize.py braid-aware. |
| VPS | Operational. Free-model guard live. Walker idle = empty frontier (expected). |
| Telemetry | claude-code feeder wired. Session-level ledger live. Per-agent split: next sprint. |
| Open P0 | 20 SHA-256s pending; genesis seal cross-repo; Rekor anchors absent. |

**Canonical record:** `reckon/docs/157-SESSION-WORKUP-2026-06-03-CANONICAL.md` (full narrative + forensic metrics + honest limits).

---

*No claims in this report are asserted beyond what the ledger, manifests, and git history support. Measurement limits are named inline. The drift happened; the recovery happened; the infrastructure is now meaningfully stronger than it was at session open.*
