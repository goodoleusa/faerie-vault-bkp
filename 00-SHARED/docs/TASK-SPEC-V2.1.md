---
doc_hash: sha256:pending
title: Task Spec V2.1 — Emergence-Mode Anchoring
phase_id: phase-003-anti-drift-anchoring
supersedes: docs/TASK-SPEC-V2.md
created: 2026-04-24
author: documentation-engineer
---

# Task Spec V2.1 — Emergence-Mode Anchoring

> Breadcrumb: faerie2/docs/TASK-SPEC-V2.1.md | Phase: phase-003-anti-drift-anchoring

## Why V2.1 Supersedes V2

V2 closed real gaps: `done_looks_like` prevents drift; `estimated_effort` prevents default-Sonnet burn; `tags` enables stigmergic routing. The fields were right. The enforcement posture was wrong.

V2 was **constraint-mode**: reject tasks that violate the spec. Constraint-mode assumes the spec-writer has perfect information at queue time. They rarely do. The failure mode is not agent drift — it is agents paralyzed by a spec that doesn't match the reality they discover.

V2.1 is **emergence-mode**: the substrate enforces shape (manifests signed, COC continuous, `dashboard_line` diagnostic); scope is the agent's judgment. The principle behind this is already embedded in faerie2 HONEY: "Bundles guide; they don't constrain. Quality is preserved through artifact SHAPE, not action SCOPE."

The key insight: when an agent finds the `done_looks_like` seed wrong, the correct response is not to fail — it is to refine the criterion, document the refinement in the manifest, and complete the work. The substrate catches the leap forensically. The agent is accountable for shape, not for blindly executing a stale spec.

---

## The Shape vs Scope Distinction

**Shape** is what the substrate enforces:
- Manifest is written (signed, hash-chained, in `forensics/manifests/`)
- COC chain is continuous
- `dashboard_line` is diagnostic and ≤80 chars
- `task_id` is present and matches the queue entry
- `agent_run_id` is generated and embedded

**Scope** is the agent's judgment:
- Whether `done_looks_like` is the right completion criterion given what was discovered
- Whether the `estimated_effort` label was accurate
- Whether the `agent_type_hint` was the right routing
- Whether adjacent tasks should be chain-claimed
- Whether a follow-up task should be queued

The substrate never enforces scope. Forensic capture makes scope legible after the fact. An agent who discovers a better criterion and documents it in the manifest with a timestamp has done more than an agent who executes a stale criterion blindly.

---

## Schema Reference

```yaml
# REQUIRED — substrate needs these for routing and discovery:

id: string
  # Format: task-{ISO_TS}-{slug}  or  task-{topic}-{n}
  # Machine-generated at add time. Stable slugs preferred for long-lived tasks.
  # Agents grep -r "_{task_id}_" forensics/ for zero-cost predecessor discovery.

goal_one_line: string ≤80 chars
  # Imperative voice. One verb + one object.
  # Bad:  "improve memory routing"
  # Good: "wire honey_hit_rate probe in 9x_session_metrics.py"

tags: list[string] ≥3
  # Domain tags. Required. Stigmergic routing depends on this.
  # Convention: nouns, single-word. [memory, instrumentation, eval]
  # Used by: 9x_broadcast_scan.py tag filter, queue-summary high_frontier routing.

priority: enum [HIGH, MEDIUM, LOW]
  # HIGH: blocks other work or fixes active regression
  # MEDIUM: normal sprint work
  # LOW: background / polish / deferred


# SEEDED — starting hypotheses the agent is free to refine:

description: string ≥30 chars
  # The why + the how. Multiline permitted.
  # If description < 30 chars, agent should request clarification via addendum.

done_looks_like:
  # At least one seeded criterion. Agent may augment or refine.
  # Refined criteria are written to manifest's criteria_emergent_v2 array,
  # timestamped — original seed is never overwritten.
  acceptance_test: string           # shell command; exit=0 means done
  artifact_paths: list[string]      # files/dirs that must exist post-completion
  forensic_query: string            # grep/jq against forensics/ that returns non-empty
  prose_criteria: string ≥40 chars  # fallback; explicit and measurable

estimated_effort: enum [S, M, L, XL]
  # S  = ≤5 min  → Haiku (simple lookups, file reads, format conversions)
  # M  = 5–15 min → Sonnet (moderate analysis, single-file edits, targeted probes)
  # L  = 15–60 min → Sonnet (multi-file changes, synthesis, cross-repo work)
  # XL = >1 hour  → Sonnet background (architecture, migration, full audits)
  # Agent may correct on claim if discovers mismatch; log escalation in manifest.

agent_type_hint: string
  # Routing suggestion only. route_task() may override.
  # Agent who discovers wrong fit may rewrite in manifest (append invalidates field).

artifacts_expected: list[string]
  # Paths the agent should produce. Checked by manifest validator post-completion.


# OPTIONAL:

phase_id: string
  # Required if task belongs to a named phase (forensics/phases/{id}.json).
  # Omit for tasks not bound to a phase.

blockedBy: list[string]
  # task_ids that must reach status=completed before this task is claimable.
  # claim_atomic() enforces this.
```

---

## Per-Field Rationale

### `id` — Required

Without a stable `id`, agents cannot discover predecessor work via `grep -r "_{task_id}_" forensics/`. The task_id-in-filename convention (Principle 3) depends on a queryable id at queue time, not at claim time.

### `goal_one_line` — Required

Vague goals cause interpretation variance across retries. Imperative verb + object eliminates this. ≤80 chars constraint ensures it fits in `dashboard_line` without truncation.

### `tags` — Required (only field that stays hard-required)

Tags are the stigmergic routing primitive. `9x_broadcast_scan.py` filters by tag. `queue-summary.json` high_frontier surfaces tasks by domain. Without at least 3 tags, the pheromone trail is blind. Minimum 3 is enforced at add time in V2.1 with no exception.

### `priority` — Required

Queue ordering and `high_frontier` selection depend on priority. No change from V2.

### `description` — Seeded, warn if missing

Minimum 30 chars. If the description is a placeholder ("fix it", "do the thing"), warn at add time and emit a suggestion. Never reject. Agent who receives a thin description should check addendums before starting and log the gap in pollen.

### `done_looks_like` — Seeded, warn if missing; agent may refine

This is the anti-drift anchor. V2 made it required and rejection-gated. V2.1 keeps it seeded — important to provide, but the agent is the authoritative source for whether the seeded criterion is correct given what they discover.

**Refinement protocol:**
1. Agent reads seeded `done_looks_like` at task claim.
2. If the seed criterion is wrong (e.g., the file path changed, the command doesn't apply), the agent writes a refinement:
   ```json
   "criteria_emergent_v2": [
     {
       "ts": "2026-04-24T16:00:00Z",
       "reason": "Acceptance test path was stale; script moved to scripts/9x_session_metrics.py",
       "acceptance_test": "grep -c 'honey_hit_rate' /mnt/d/0local/gitrepos/faerie2/scripts/9x_session_metrics.py | awk '{if ($1 >= 1) exit 0; else exit 1}'"
     }
   ]
   ```
3. Original `done_looks_like` is never overwritten. The refinement is append-only.
4. Validation gate reads `criteria_emergent_v2` if present, falls back to `done_looks_like` seed.

If `done_looks_like` is missing from the queue entry entirely, the validation gate issues a warning with an auto-suggestion (Haiku pass on `description` generates a prose_criteria candidate). Never reject.

### `estimated_effort` — Seeded, warn if missing; agent may correct on claim

Without this field, `route_task()` defaults all tasks to Sonnet. The haiku-cheap suggestion at queue time is just a routing hint. If the agent discovers at claim time that the effort was misestimated (S task expands to M, M task expands to L), the agent logs the escalation in the manifest:
```json
"effort_escalation": {
  "from": "S",
  "to": "M",
  "reason": "File required reading 3 modules, not 1 — context switch added ~8 min"
}
```
This feeds back into calibration for the retrofit tool.

### `agent_type_hint` — Seeded; agent may rewrite if wrong fit

Advisory for `route_task()`. If a documentation-engineer receives a task and discovers it requires deep Python refactoring, the agent may note in the manifest:
```json
"routing_note": "python-pro would handle this more efficiently; task requires AST manipulation"
```
This feeds forward to the follow-up task's `agent_type_hint`.

### `artifacts_expected` — Seeded; agent may augment

Agent may add paths to `artifacts_expected` if discovery reveals additional outputs should be produced. Additions logged in manifest under `artifacts_emergent`.

### `phase_id` — Required if phase exists, unchanged from V2

Explicit phase binding enables `forensics/phases/{id}.json` atomic updates. Still required for phase-bound tasks.

### `blockedBy` — Unchanged from V2

`claim_atomic()` enforces. List direct `task_id` dependencies only.

---

## Permission-to-Leap Directive

Every bundle rendered by `7x_spawn_template.py` MUST include this block verbatim:

```
PERMISSION TO LEAP:
You are not constrained to the literal task-spec. You may:
- Refine done_looks_like if the seed criterion is wrong (write the refinement back to
  manifest under criteria_emergent_v2 with timestamp; do NOT overwrite original seed).
- Augment acceptance criteria if you discover additional concrete tests (append to
  criteria_emergent_v2 array).
- Invalidate a predecessor task whose premise has gone stale (write
  {predecessor_id, reason, ts} to manifest's invalidates field).
- Chain-claim a sibling task if context allows AND tag affinity >= 0.6
  (use 7x_queue_ops monkeybranch-claim).
- Queue follow-ups via next_task_queued — your judgment on what should run next.
- Escalate phase redefinition if you discover the phase scope was wrong (write
  proposal to forensics/phase-revision-proposals/{phase_id}-{ts}.md; never edit
  the genesis manifest).

The substrate forensically captures every leap. You are accountable for SHAPE
(signed manifest, hashed writes, COC continuity) — not for SCOPE (what you
decided to do).
```

This directive is what makes V2.1 emergence-mode. Without it, agents stay in constraint-mode even if the spec is warn-not-reject.

---

## Worked Example — V2 vs V2.1

### The V2 Task (constraint-mode)

```json
{
  "id": "task-spec-v2-validation-gate",
  "goal_one_line": "implement done_looks_like rejection gate in 7x_queue_ops.py add",
  "description": "7x_queue_ops.py add must REJECT tasks missing done_looks_like field with an error message that includes an example of a valid spec.",
  "done_looks_like": {
    "acceptance_test": "python3 scripts/7x_queue_ops.py add --goal 'test' --tags 'a,b,c' 2>&1 | grep -c 'done_looks_like' | awk '{if ($1 >= 1) exit 0; else exit 1}'"
  },
  "estimated_effort": "M",
  "tags": ["queue", "validation", "v2-spec"],
  "priority": "HIGH"
}
```

**V2 agent behavior:**
Agent implements rejection gate. Done. Manifest says "rejection gate implemented." Agents calling `add` without `done_looks_like` now get errors, which breaks existing automation. Main has to handle the breakage.

### The V2.1 Task (emergence-mode)

```json
{
  "id": "task-spec-v2.1-warn-not-reject",
  "goal_one_line": "implement warn-not-reject for done_looks_like in 7x_queue_ops.py add",
  "description": "V2.1 recalibration: the validation gate must WARN on missing done_looks_like with a helpful suggestion, never reject. Auto-suggest prose_criteria candidate via Haiku pass on task description. Existing automation that calls add without done_looks_like must continue working. Missing tags or estimated_effort: warn-only with suggestion. See docs/TASK-SPEC-V2.1.md for full spec.",
  "done_looks_like": {
    "acceptance_test": "python3 scripts/7x_queue_ops.py add --goal 'test task' --tags 'a,b,c' 2>&1 | grep -c 'WARNING' | awk '{if ($1 >= 1) exit 0; else exit 1}'",
    "prose_criteria": "add succeeds (exit 0) when done_looks_like is absent; stderr includes WARNING with suggestion; existing queue entries are not disturbed."
  },
  "estimated_effort": "M",
  "tags": ["queue", "validation", "v2.1-spec", "warn-not-reject"],
  "priority": "HIGH"
}
```

**V2.1 agent behavior:**
Agent implements warn-not-reject. Discovers the Haiku auto-suggest path requires the `description` field to be at least 30 chars — notes this in `criteria_emergent_v2` with an updated acceptance test. Chains to bundle-render task via `next_task_queued`. Returns manifest. Main reads `dashboard_line` only.

### Diff Table

| Field | V2 (constraint-mode) | V2.1 (emergence-mode) |
|-------|----------------------|-----------------------|
| `done_looks_like` | Required; reject if missing | Seeded; warn if missing; agent may refine |
| `estimated_effort` | Required enum | Suggested; agent may correct on claim |
| `agent_type_hint` | Routing decision | Routing suggestion; agent may rewrite |
| `acceptance_criteria` | Immutable post-genesis | Immutable seed + extensible via `criteria_emergent_v2` (hash-stamped separately) |
| `tags` | Required | Required (only field that stays hard-required) |
| `phase_id` | Required if phase exists | Required if phase exists (unchanged) |
| Validation gate | Reject on violation | Warn with suggestion; never reject |
| Agent posture | Execute spec | Execute spec OR refine spec + document leap |
| Bundle content | Task spec only | Task spec + PERMISSION TO LEAP directive |

---

## Anti-Patterns

### Do not constrain agents to literal task text when reality has shifted

A task written 48 hours ago describing a file path that no longer exists should not paralyze an agent. The correct response is to refine the criterion, note it in `criteria_emergent_v2`, and complete the work. The forensic trail shows what was planned vs what was discovered.

### Do not reject tasks that lack `done_looks_like`

Issue a WARNING. Auto-suggest a prose_criteria candidate from the description. Let the task through. The retrofit tool (`9x_task_retrofit.py`) can backfill at scale. Rejection gates break automation that was working before V2.

### Do not suppress a Rung 1 agent who realizes Rung 2's design needs re-shape

If an agent discovers the phase scope was wrong, the correct response is to write a revision proposal to `forensics/phase-revision-proposals/{phase_id}-{ts}.md` and return a `phase_revision_proposal` field in the manifest. Never edit the genesis manifest. The substrate captures the divergence; faerie or human can act on the proposal.

### Do not use `agent_type_hint` as a hard constraint

It is a routing suggestion. An agent who receives a task with `agent_type_hint: python-pro` and discovers it actually requires documentation work should note the mismatch in the manifest and complete the work to the best of their ability (or queue a handoff task).

### Do not treat `estimated_effort` as immutable

If the task expanded in scope, log `effort_escalation` in the manifest and continue. Do not abandon a task because the effort was underestimated. Escalation data feeds calibration.

---

## Migration from V2

### If the V2 validation gate has landed

Recalibrate `cmd_add()` in `scripts/7x_queue_ops.py`:
1. Change `done_looks_like` from reject → warn with auto-suggest.
2. `estimated_effort`: already warn-only in V2. No change needed.
3. `tags`: keep required + reject (only field that stays hard).
4. Add `PERMISSION TO LEAP` injection to the bundle renderer in `7x_spawn_template.py`.

Implementation target: `task-spec-v2.1-warn-not-reject`.

### If `9x_task_retrofit.py` has run

Run a V2.1 pass that adds the `PERMISSION TO LEAP` directive to every bundle rendered from retrofitted tasks. The retrofit tool's output tasks are otherwise V2-schema-compatible; no schema changes needed.

### Bundle renderer (`7x_spawn_template.py`)

Patch `bundle` subcommand to inject:
1. Full task spec (existing V2 requirement) — `id`, `goal_one_line`, `description`, `done_looks_like`, `estimated_effort`, `tags`, `artifacts_expected`.
2. `PERMISSION TO LEAP` directive (V2.1 addition).
3. `COMPLETION PROTOCOL` block that reads `criteria_emergent_v2` if present, falls back to `done_looks_like` seed.

Implementation target: `task-spec-v2.1-bundle-render`.

---

## V2.1 Manifest Fields (agent-side additions)

Agents running under V2.1 may add these fields to their manifest:

```json
{
  "criteria_emergent_v2": [
    {
      "ts": "ISO8601",
      "reason": "why the seeded criterion was wrong or insufficient",
      "acceptance_test": "...",
      "prose_criteria": "..."
    }
  ],
  "effort_escalation": {
    "from": "S",
    "to": "M",
    "reason": "scope expanded; logging for calibration"
  },
  "routing_note": "suggested agent type for follow-up work",
  "artifacts_emergent": ["/paths/the/agent/produced/beyond/spec"],
  "invalidates": [
    {
      "predecessor_id": "task-XXXX",
      "reason": "premise is stale; file was deleted",
      "ts": "ISO8601"
    }
  ],
  "phase_revision_proposal": "forensics/phase-revision-proposals/{phase_id}-{ts}.md"
}
```

All fields are optional. Their presence signals an emergence event — something was discovered that the spec-writer didn't know at queue time. The forensic trail is richer for it.

---

## Acceptance Criteria for This Document

This specification is complete when:
1. `docs/TASK-SPEC-V2.1.md` exists (this file).
2. Three V2 follow-up tasks in the queue are recalibrated to V2.1 posture.
3. A manifest is written at `forensics/manifests/` with `task_id=task-bundle-spec-v2.1-recalibration`.

---

## See Also

- `docs/TASK-SPEC-V2.md` — superseded; constraint-mode rationale preserved for reference
- `scripts/7x_queue_ops.py` — `cmd_add()` is the validation gate target
- `scripts/7x_spawn_template.py` — bundle renderer; inject PERMISSION TO LEAP
- `docs/SPAWN-CONTRACT.md` — spawn contract enforcement
- `docs/SPAWN-BOILERPLATE.md` — template-based bundle rendering
- `forensics/task-retrofit-flagged.md` — tasks flagged by `9x_task_retrofit.py` (created post-retrofit)
- `forensics/phase-revision-proposals/` — phase scope revision proposals from agents
