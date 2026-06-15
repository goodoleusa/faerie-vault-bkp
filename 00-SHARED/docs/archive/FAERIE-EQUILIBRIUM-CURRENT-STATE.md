---
status: final
author: knowledge-synthesizer
ts: 2026-04-06T12:00:00Z
type: architecture-analysis
---

# Faerie Equilibrium -- Current State Analysis

## Executive Summary

The faerie system is a solo-researcher multi-agent orchestration platform built on
Claude CLI. It coordinates ~20 specialized agent types through a memory hierarchy
(scratch -> NECTAR -> HONEY), a sprint queue, and stigmergic filesystem coordination.
This document analyzes the energy flow through the system -- where knowledge is
generated, where it accumulates, where it crystallizes, and where bottlenecks form.

**Key finding:** The system generates knowledge faster than it crystallizes. The queue
grows without bound (65 tasks, 0 ever completed/archived), REVIEW-INBOX regrows after
siphoning (50 -> 547 lines in 9 days), and HONEY sits at 95% budget with no room for
new entries. The system is intake-rich and crystallization-poor.

---

## 1. Task Generation -> Claiming -> Execution -> Completion Flow

### Task Origins

Tasks originate from three sources:

| Source | Mechanism | Volume |
|--------|-----------|--------|
| **Human** | `/queue add` or vault Queue/ edits | ~10% of tasks |
| **Agents** | Auto-generated during execution (gap analysis, follow-up threads) | ~70% of tasks |
| **Auto-queue** | `/faerie` startup, `/suggest`, agent returns discovering new work | ~20% of tasks |

Agents are the dominant task generators. Every research-analyst run discovers 2-3 follow-up
threads. Every evidence-curator run identifies gaps. Every data-engineer run surfaces
normalization needs. The system is auto-catalytic: work generates more work.

### Task Lifecycle

```
ORIGIN (human/agent/auto)
  |
  v
QUEUED (sprint-queue.json, status: "queued")
  |  <- /run or faerie assigns
  v
CLAIMED (claimed_by_session, claimed_at fields set)
  |
  v
IN_PROGRESS (agent executing)
  |  <- agent writes manifest
  v
??? (no "completed" status in queue -- tasks stall here)
```

**Critical gap:** The queue has 65 tasks, 4 in_progress, 0 completed, 0 archived.
Tasks are never formally completed or removed. The `sprint-queue.json` file is 72K
and growing. There is no garbage collection, no completion ceremony, no archival flow.

**Evidence:** Grep for `"completed"` in sprint-queue.json returns zero matches. Every
task that was ever added is still present, either as `queued` or `in_progress` (with one
`deferred`). The queue is append-only in practice but not by design -- it just lacks
a completion pathway.

### Energy Flow Diagnosis

```
GENERATION ====> [HIGH FLOW] ====> QUEUE (accumulating)
CLAIMING   ====> [LOW FLOW]  ====> 4 of 65 active (~6% utilization)
EXECUTION  ====> [MODERATE]  ====> agents produce output + more tasks
COMPLETION ====> [ZERO FLOW] ====> no archival, no GC, no "done" state
```

**Bottleneck:** Task completion. The system lacks a formal "done" transition. When an
agent finishes, its output goes to a manifest, but the queue entry stays in_progress
forever. This means:
- Queue depth grows monotonically
- Priority sorting becomes meaningless in a 65-item list
- Human cannot distinguish "done but not cleaned up" from "stuck"
- `/queue` output is noisy with stale tasks

### Recommendation

Add a `completed` status + `completed_at` timestamp. Memory-keeper or `/handoff` should
mark tasks completed when their manifest exists and output is verified. Archive completed
tasks to `sprint-queue-archive.jsonl` (append-only) and remove from active queue. Target:
active queue < 20 tasks at any time.

---

## 2. Crystallization Process (scratch -> NECTAR -> HONEY)

### Current State

| Store | Size | Budget | Pressure |
|-------|------|--------|----------|
| HONEY.md (global) | ~4740 tokens (196 lines) | 5000 tokens (200 lines) | 95% -- near crisis |
| NECTAR.md (global) | ~26K chars (~6500 tokens) | unbounded | healthy (append-only) |
| REVIEW-INBOX.md | ~547 lines (regrown from 50 after 2026-03-29 siphon) | unbounded | needs siphon |
| scratch files | ephemeral per session | ephemeral | healthy |
| Agent cards (30 total) | avg ~1030 tokens each | 800t budget (1200t trained) | many overbudget |

### Crystallization Ratio

NECTAR holds ~6500 tokens of validated findings. HONEY holds ~4740 tokens of crystallized
wisdom. Ratio: HONEY/NECTAR = 0.73. This is surprisingly high -- meaning HONEY is
*already dense* relative to NECTAR. The problem is not that crystallization is lazy; the
problem is that HONEY is nearly full and cannot absorb new knowledge without compression.

### The Gauntlet (entry criteria for HONEY)

```
recurrence (3+ sessions) -> multi-agent validation -> human review -> proven impact -> universality
```

This gauntlet is philosophically sound but operationally invisible. There is no tracking
of which NECTAR entries have been through 3 sessions, which have multi-agent validation,
which the human has reviewed. The gauntlet is a set of principles, not a pipeline.

**Consequence:** Crystallization happens when the human manually invokes `/crystallize`,
which requires the human to remember that pressure has built. There is no dashboard showing
"5 NECTAR entries have met gauntlet criteria and are candidates for crystallization."

### HONEY Budget Crisis

At 95% budget, HONEY cannot absorb new crystallized knowledge. The system has two options:
1. **Compress existing entries** (make each entry denser, merge related bullets)
2. **Evict stale entries** (some entries may have TTLs that expired)

Current HONEY has entries from multiple domains:
- Principles (5 entries, permanent TTL)
- Collaboration prefs (8 entries, 2yr TTL)
- Investigation methods (15+ entries, 1yr TTL)
- Architecture principles (12+ entries, permanent TTL)
- Faerie design philosophy (4 entries, 2yr TTL)
- Operational lessons (4 entries, permanent TTL)
- pref_bridge entries (10+ entries, 1yr TTL -- these are the newest and least crystallized)

The `pref_bridge` entries at the bottom are the most compressible. They are raw feedback
from a single session (2026-03-28) that was promoted rapidly. Several are redundant with
existing principles or method entries. A compression pass on pref_bridge alone could free
~800 tokens (~16% of budget).

### Recommendation

1. Compress pref_bridge entries -- many restate existing principles
2. Build a `/dev-pressure` command that shows gauntlet progress for NECTAR entries
3. Add TTL checking to `/faerie` startup -- entries past TTL should be flagged for review
4. Target HONEY at 70-80% utilization, leaving 20-30% for new knowledge absorption

---

## 3. Agent Selection and Routing

### Agent Roster (30 cards)

The system has 30 agent card files across categories:
- **Core (5):** workflow-orchestrator, memory-keeper, membot, context-manager, performance-eval
- **Investigation (6):** evidence-curator, data-scientist, data-engineer, security-auditor,
  report-writer, research-analyst
- **Infrastructure (5):** fullstack-developer, token-optimizer, task-distributor,
  error-coordinator, knowledge-synthesizer
- **Specialist (8):** admin-sync, coc-manager, evidence-analyst, frontend-design,
  ipfs-publisher, team-builder, python-pro, vision-ingest
- **External/Niche (6):** evalbot, spiderfoot, spiderfoot-toronto, plus reference docs

### Training State

| Agent | Score | Context | Status |
|-------|-------|---------|--------|
| knowledge-synthesizer | 0.834 | training | gap: -0.016 from target |
| workflow-orchestrator | 1.00 | training | likely too-easy benchmark |
| Others | varies | unknown | many have no Last Training section |

Per HONEY mth00037: first run >= 0.95 means criteria too easy. The workflow-orchestrator
at 1.00 confirms this -- the benchmark needs tightening.

### Agent Budget Compliance

Agent cards are budgeted at 800 tokens (1200 when trained). With 30 cards, that is
~24K-36K tokens of potential T1 context load. In practice, only the spawned agent's
card is loaded, so per-spawn cost is ~1K tokens. But several cards appear overbudget
based on their length (knowledge-synthesizer at 44 lines, workflow-orchestrator at 57
lines -- both near or above 1K tokens).

### Routing Quality

Task routing uses `recommended_agent` in the queue entry plus `routing_advisor.py` for
score-aware selection. The routing_advisor integration into `_pick_agent()` is still
queued (task-20260406-070419-3aa2). Currently, routing is based on keyword matching
from `subagent-options.json`, which is adequate for well-categorized tasks but blind
to agent performance history.

### Recommendation

1. Complete routing_advisor integration (already queued)
2. Tighten workflow-orchestrator benchmark
3. Audit all 30 cards for budget compliance
4. Ensure all investigation agents have deployment scores, not just training scores

---

## 4. Stigmergy and Manifest Returns

### Pheromone Layer

The system uses three pheromone surfaces:

| Surface | Writers | Readers | Mechanism |
|---------|---------|---------|-----------|
| Manifest files (`wave{N}-{type}-result.json`) | Agents | Faerie/main session | TaskNotification trigger |
| scratch files (`scratch-{SID}.md`) | Agents | Memory-keeper at /handoff | MEM block format |
| Vault Agent-Outbox | Agents | Human (Obsidian) | Syncthing eventual consistency |

### Cross-Agent Coordination

Currently, agents coordinate through the filesystem:
- Agent 1 writes output to a known path
- Agent 2 reads that path (if spawned with knowledge of where to look)
- No direct agent-to-agent messaging exists

This works well for sequential pipelines (data-engineer -> evidence-curator -> report-writer)
but breaks for parallel agents that might produce conflicting outputs. The "read first,
then build on it" instruction in spawn prompts is the mitigation.

### Manifest Sufficiency

Manifests contain: `output_path`, `dashboard_line`, `files_written`, `next`. This is
sufficient for parent-to-child coordination but insufficient for sibling coordination.
If two agents are working on related tasks in the same wave, neither sees the other's
progress until both return to the parent.

### Recommendation

Consider a lightweight "wave bulletin board" file that agents append progress to.
Each agent reads the bulletin before starting deep work. This enables late-arriving
agents to adapt to early-arriving results without parent mediation.

---

## 5. Vault and Obsidian Sync

### Current State

- `$CT_VAULT/00-SHARED/` is the agent write zone
- Syncthing syncs to ZimaBoard and collaborators
- Human reads in Obsidian, annotates via `.ann.md` siblings
- Queue in `00-SHARED/Queue/` is theoretically bidirectional

### Source of Truth Fragmentation

The queue has two representations:
1. `~/.claude/hooks/state/sprint-queue.json` (CLI authoritative)
2. `$CT_VAULT/00-SHARED/Queue/sprint-queue.md` (human-editable)

There is no documented sync mechanism between them. If the human edits the vault queue,
does it flow back to CLI? The answer appears to be: no automated sync. The vault copy
is a display artifact, not a bidirectional interface.

### Recommendation

Either:
1. Make the vault queue read-only (agent-generated, human reads in Obsidian)
2. Build a sync script that merges vault queue edits back to sprint-queue.json

Option 1 is simpler and avoids conflict resolution. Human task creation should go through
`/queue add` in CLI, not vault edits.

---

## 6. Pressure Points Summary

| Pressure Point | Severity | Current Value | Target | Action |
|----------------|----------|---------------|--------|--------|
| HONEY budget | HIGH | 95% (4740/5000t) | 70-80% | Compress pref_bridge entries |
| Queue depth | HIGH | 65 tasks, 0 completed | <20 active | Add completion + archival |
| REVIEW-INBOX | MED | 547 lines (regrown) | <100 lines | Siphon to NECTAR + vault flags |
| Agent cards overbudget | MED | avg ~1030t vs 800t budget | <800t each | Compression pass |
| Queue file size | MED | 72K chars | <20K | Archive completed tasks |
| Memory fragments | LOW | 3 detected | 0 | Consolidate via memory-keeper |
| Routing advisor | LOW | not integrated | wired into _pick_agent() | Complete queued task |
| Task completion flow | HIGH | nonexistent | formal done state | Build completion pathway |

---

## 7. Energy Flow Diagram

```
                    GENERATION (high volume)
                         |
          human -----> queue <----- agents (auto-generate 70%)
                         |
                    CLAIMING (low: 6%)
                         |
                    EXECUTION (moderate)
                    /          \
              manifests     scratch MEM blocks
                |                |
          [parent reads]    [memory-keeper]
                |                |
          next wave         NECTAR (append)
                                 |
                           [human /crystallize]
                                 |
                           HONEY (95% full)
                                 |
                         [next session startup]
                                 |
                           agent context load
```

**Energy accumulation points (red):**
- Queue: tasks pile up, never complete (65 and growing)
- REVIEW-INBOX: regrows between siphons (547 lines)
- HONEY: at capacity, cannot absorb new knowledge

**Energy flow points (green):**
- Stigmergy: manifests work well for sequential coordination
- NECTAR: unbounded, healthy accumulation
- Agent execution: good throughput when tasks are claimed

**Energy leaks (yellow):**
- Completed work not feeding back to queue state
- Gauntlet criteria not tracked -- crystallization happens ad hoc
- Agent training scores stale for most agents

---

## 8. System Maturity Assessment

| Dimension | Maturity | Evidence |
|-----------|----------|----------|
| Memory architecture | HIGH | Three-tier (scratch/NECTAR/HONEY) is well-designed and philosophically sound |
| Forensic integrity | HIGH | Hash-chained COC, three-store architecture, HMAC-SHA256 |
| Agent specialization | HIGH | 20+ typed agents with distinct KPIs and cards |
| Task lifecycle | LOW | No completion state, no archival, no metrics on task throughput |
| Crystallization pipeline | MED | Design is excellent, execution is ad hoc (human-triggered only) |
| Cross-agent coordination | MED | Stigmergy works for sequential; weak for parallel |
| Budget enforcement | MED | Budgets defined but not automatically enforced |
| Performance feedback | LOW | Training scores exist for few agents; deployment scores rare |

The system excels at knowledge architecture and forensic rigor. It is weakest at
lifecycle closure (completing tasks, retiring knowledge, enforcing budgets automatically).
This is characteristic of a system optimized for generation over maintenance -- which
makes sense for a solo researcher during active investigation, but will not scale.
