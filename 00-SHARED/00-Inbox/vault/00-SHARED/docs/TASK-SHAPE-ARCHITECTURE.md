# Task Shape Architecture — Declarative vs Imperative

**Citation:** mth00096 (HONEY.md) + task-shape-declarative-v1.json (schemas/)

**Status:** Core faerie principle (non-negotiable). All tasks in sprint-queue.json MUST conform to 5-field declarative shape.

---

## The Principle

Tasks are **goals with boundaries**, not step lists. Agents are intelligence, not robots.

**Imperative (❌ old pattern):**
```
Task: "Analyze vulnerability in ORNL cert"
Steps:
  1. Read the cert file at /path/to/cert.pem
  2. Parse the X.509 structure
  3. Extract the signature algorithm
  4. Write results to /mnt/d/0local/findings.json
```

**Why this fails:** Agent can't monkeybranch. If they discover a more efficient parsing tool, they're boxed in. If they find related evidence, they can't pursue it. Step lists constrain intelligence.

---

## The 5-Field Declarative Shape

Every task in faerie queue MUST have these 5 fields:

### 1. **goal_one_line** (REQUIRED, ≥20 chars, ≤280 chars)

The WHY in one sentence. What problem does this solve? Why now?

**Good:**
- "Audit sprint-queue.json for 5-field declarative task schema; backfill missing constraints/out_of_scope/judgment_envelope fields"
- "Extract cross-domain droplet citations (past 7 days) and compute M6 metric (droplet citation rate)"

**Bad (step-list):**
- "Read the queue file, parse JSON, check for missing fields, add defaults, write back"

### 2. **done_looks_like** (REQUIRED, ≥20 chars, ≤500 chars)

HOW YOU KNOW YOU'RE DONE. Verifiable end-state. Not procedure—outcome.

**Good:**
- "All unclaimed tasks have constraints + out_of_scope + judgment_envelope fields; schema validation passes; manifest documents which tasks were updated and what defaults were applied"
- "M6 metric computed and wired to 9x_droplet_citation_probe.py; reputation boost formula validated; 3+ example droplets checked for citation links"

**Bad (step-list):**
- "Write the code, test it, push it, create a PR"

### 3. **constraints** (OPTIONAL, ≤300 chars)

Hard boundaries. What MUST NOT be touched? What MUST be used?

**Examples:**
- "Do not modify completed or archived tasks. Use atomic file locking. Write COC entry for each update via 4x_coc_writer.py."
- "Must use Ed25519 for signing. Do not commit directly to forensics/*.jsonl; use hook API."

### 4. **out_of_scope** (OPTIONAL, ≤300 chars)

Explicit exclusions. What should the agent NOT attempt?

**Examples:**
- "Out of scope: user-facing UI changes, database schema migrations, deployment to production"
- "Out of scope: changing task priorities, reassigning ownership, deleting tasks from queue"

### 5. **judgment_envelope** (OPTIONAL, ≤300 chars)

Where agent exercises discretion. What decisions are theirs to make?

**Examples:**
- "Your call on: whether to merge findings or keep separate, how to weight evidence, when to flag for human review, which tools to use"
- "Your call on: whether to fill missing fields with sensible defaults or flag for human input, how verbose constraints should be"

---

## Schema Definition

**Location:** `schemas/task-shape-declarative-v1.json`

Full JSON schema with required/optional fields, constraints, examples.

**Validation:** 7x_queue_ops.py MUST validate on task creation (add command).

---

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **goal_one_line + done_looks_like** | ✅ ACTIVE | Injected into bundle (spawn-template.py) |
| **constraints** | ⏳ BACKFILL | Schema defined, janitor task queued |
| **out_of_scope** | ⏳ BACKFILL | Schema defined, janitor task queued |
| **judgment_envelope** | ⏳ BACKFILL | Schema defined, janitor task queued |
| **Schema validation** | 📋 TODO | Wire JSON schema into 7x_queue_ops.py add command |

---

## Migration Path

1. **Codify schema** (DONE) → `task-shape-declarative-v1.json`
2. **Backfill existing tasks** (IN PROGRESS) → queue janitor task
3. **Wire validation** (TODO) → 7x_queue_ops.py add validates all 5 fields
4. **Document enforcement** (TODO) → Update CLAUDE.md + this doc with enforcement rules
5. **Communicate to agents** (TODO) → Agent spawn templates reference this doc

---

## Why This Matters (f(0) Alignment)

Per sys00034 (Programmatic Composition): "Claude should not be composing anything a script could render deterministically. Where Claude MUST add inference (reasoning, synthesis, judgment), that's intentional and belongs in subagent context."

**Old pattern:** Main writes step lists (inference cost: 200-400 tokens per task). Agent follows steps robotically.

**New pattern:** Main writes goal + done_looks_like + boundaries (deterministic, ~100 tokens). Agent reasons within envelope, monkeybranche freely.

**Result:** Agents are smarter, main is lighter, inference cost drops, quality rises.

---

## Example Task (Full 5-Field Shape)

```json
{
  "id": "task-20260425-140600-a1b2",
  "goal_one_line": "Audit sprint-queue.json for 5-field declarative task schema; backfill missing constraints/out_of_scope/judgment_envelope fields",
  "done_looks_like": "All unclaimed tasks have all 5 fields populated; schema validation passes; manifest documents which tasks were updated and defaults applied",
  "constraints": "Do not modify completed or archived tasks; use atomic file locking; write COC entry for each update",
  "out_of_scope": "Out of scope: changing task priorities, reassigning ownership, deleting tasks",
  "judgment_envelope": "Your call on: whether to fill missing with sensible defaults or flag for human input; how verbose constraints/envelopes should be",
  "priority": "HIGH",
  "wave": "W2",
  "category": "schema-enforcement",
  "claim_state": "unclaimed"
}
```

Agent reads this and thinks: "I have clear goal, clear done criterion, clear boundaries, clear discretion points. I can monkeybranch within these guardrails."

---

## References

- **HONEY.md:** mth00096 (DECLARATIVE-TASK-SHAPE-OVER-IMPERATIVE)
- **Schema:** schemas/task-shape-declarative-v1.json
- **Enforcement:** 7x_queue_ops.py (validate on add)
- **Bundle injection:** 7x_spawn_template.py (_build_task_directive_block)
- **Related:** sys00034 (programmatic composition), mth00086 (main-inference heuristic)

---

## Enforcement Rules (Going Forward)

1. **All new tasks** MUST have goal_one_line + done_looks_like (minimum 2/5 fields)
2. **Recommended:** Add constraints + judgment_envelope (minimum 4/5 fields)
3. **Backfill drive:** Janitor task audits existing unclaimed tasks and fills missing fields with sensible defaults
4. **Validation gate:** 7x_queue_ops.py add command MUST validate against schema; refuse tasks that violate required fields
5. **COC audit:** Every backfill write generates COC entry (immutable record of field additions)

---

**Last updated:** 2026-04-25 | **Status:** Foundational, all teams | **Enforcement:** Mandatory going forward
