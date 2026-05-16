---
type: reference
status: active
created: 2026-04-25
tags: [bundle, f(0), spawn, context-injection, template]
up: README.md
---

> [↑ Readme](README.md) · [⌂ Home](../README.md)

# Bundle Composition for f(0) — Rich Context at Nil Spawn Cost

**Goal:** Agents receive HONEY + NECTAR + task spec + prior work context WITHOUT main paying composition overhead. Bundle system writes context to disk once, agents read from filesystem at spawn time. **Net result: 50 tokens/spawn, unlimited context depth.**

---

## Architecture: Four Layers

### Layer 1: Task Specification (queue metadata)

From `sprint-queue.json`, each task carries:

```json
{
  "task_id": "task-20260425-181259-b831",
  "goal": "Prototype material design icon statusline...",
  "done_looks_like": "Statusline format using 6-8 MDI icons; <80 chars",
  "constraints": ["icon must map to piston signal", "output parseable by 9x_lean_query"],
  "out_of_scope": ["do not modify 9x_lean_query.py itself"],
  "judgment_envelope": "Choose icon set and semantic mapping",
  "seeking": "Icon set that unambiguously encodes phase, cache, queue health",
  "why_now": "User flagged: need live velocity burst indicators",
  "recommended_agent": "documentation-engineer"
}
```

**Key:** This spec is serialized early (queue time). SPAWNING is parameter substitution, not composition.

### Layer 2: Agent Card Discovery

Route determines recommended agent (e.g., `documentation-engineer`).

Read agent card: `~/.claude/agents/documentation-engineer.md`

```yaml
---
name: documentation-engineer
description: "Expertise spans API docs, tutorials, guides..."
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
maps_to_official_type: general-purpose
injection_method: "prompt prefix with doc best practices"
---

You are documentation-engineer per this card.

## Philosophy
...
[Full behavioral protocol]
```

**Key:** Card contains BEHAVIORAL SHAPING, not the full context. Card gets injected as prompt prefix when spawning with official type.

### Layer 3: Crystallized Memory (HONEY + NECTAR)

**HONEY** (~/.claude/HONEY.md, ≤5K tokens):
- Universal methods across all projects
- Principles (f(0), stigmergy, piston waves, compaction)
- Patterns (mutation discipline, pressure phases)
- Frozen at session start → no reads during work (save context)

**NECTAR** (~/.claude/NECTAR.md, tail-30 + recent findings):
- Session-scoped discoveries
- Investigation patterns
- Validated findings from recent work
- Appended during /handoff

**READ PROTOCOL:** Agents read HONEY + NECTAR at **spawn startup**, not during main composition. This is done once per agent, not once per spawn.

### Layer 4: Bundle-Assembled Injection Blocks

`7x_spawn_template.py` auto-constructs and injects FIVE blocks:

#### Block 1: TASK_DIRECTIVE (from task spec)

```
GOAL: [one-sentence WHY]
DONE_LOOKS_LIKE: [verifiable end-state, not procedure]
CONSTRAINTS: [hard boundaries]
OUT_OF_SCOPE: [explicit exclusions]
JUDGMENT_ENVELOPE: [where you exercise discretion]
```

**Cost:** ~80 tokens (from task spec, already serialized).

#### Block 2: DONE_LOOKS_LIKE (extracted to prominence)

```
DONE_LOOKS_LIKE (acceptance criterion):
  Statusline format using 6-8 MDI icons mapping to piston signals; 
  output <80 chars; tested in 9x_lean_query.py --format statusline
```

**Why duplicated?** Ensures agents see acceptance criterion FIRST, before any other context.

#### Block 3: RELEVANT_PRIOR_WORK

Scans `forensics/manifests/` for 3 most-recent tasks matching this task's keywords:

```
RELEVANT_PRIOR_WORK (read-only context):
  - 2026-04-25T17:22:33Z_statusline_task-20260425-160212-a3f4_documentation-engineer_a1df5df1.json: 
    "Tested 80-char limit with 12 icons; feedback: too dense"
  - 2026-04-25T14:11:19Z_research_task-20260425-140611-c3ae_explorer_22cf8a2d.json: 
    "MDI icon set has 2000+ options; recommend filtering by semantic category"
```

**Cost:** ~150 tokens (file references + summaries; discovery via grep).

#### Block 4: ANTI_FAB_CALLOUTS

```
ANTI_FAB_CALLOUTS (critical reminders):
  • mutation→verify: Conflicting instructions = mutations. 
    Measure baseline BEFORE repair.
  • integrity→cite: Every claim of prior work cites real forensics/ 
    evidence (hash, filename, ts).
  • eval→never: Never read or reference your own cached card 
    (Last Training, BASELINE, KPI). Parent reads it after.
  • synthesis: Cross-pollinize ≥2 inputs; attribute each source explicitly.
```

**Cost:** ~50 tokens. Prevents fabrication, ensures chain-of-custody.

#### Block 5: REPUTATION_ANTI_PATTERNS (from agent card)

```
REPUTATION_ANTI_PATTERNS (from agent history):
  ⚠ caught_lying: count 0 (pristine)
  ⚠ mutation_verification_pass_rate: 0.85
```

**Cost:** ~30 tokens. Reminds agent of accountability.

---

## The Bundle Assembly Flow

### Time T=0: Queue Task

```bash
python3 7x_queue_ops.py add \
  --goal "Prototype material design icon statusline..." \
  --priority HIGH \
  --done-looks-like "..." \
  --constraints '["map to piston signals"]' \
  --agent documentation-engineer
```

**Task stored in `sprint-queue.json`.** No agent has been spawned yet.

### Time T=1: /run Claims Task

```bash
python3 ~/.claude/skills/run/run.py --emit-bundles --max-count 1
```

run.py atomically:
1. Reads task from queue
2. Extracts `recommended_agent`
3. Calls `assemble_bundle(agent_type, task_id, task_spec=...)`

### Time T=2: Bundle Assembly (7x_spawn_template.py)

Template engine:

```python
def assemble_bundle(agent_type="documentation-engineer", task_id="..."):
    # 1. Load agent card
    card = read(f"~/.claude/agents/{agent_type}.md")
    official_type = card.frontmatter["maps_to_official_type"]
    
    # 2. Load task spec from queue
    task_spec = load_task(task_id)
    
    # 3. Build TASK_DIRECTIVE block
    directive = _build_task_directive(task_spec)
    
    # 4. Scan forensics/manifests for prior work
    prior_work = _collect_relevant_prior_work(task_id, max_n=3)
    
    # 5. Build ANTI_FAB_CALLOUTS (generic + agent-type-specific)
    anti_fab = _collect_anti_fab_callouts(agent_type)
    
    # 6. Build REPUTATION_ANTI_PATTERNS from agent card
    reputation = _collect_reputation_anti_patterns(agent_type)
    
    # 7. Assemble full context bundle JSON
    bundle = {
        "agent_type": agent_type,
        "official_type": official_type,
        "task_id": task_id,
        "formula": "conservative",  # or "experimental"
        "bundle_knobs": {
            "droplet_awareness": True,
            "honey_injection": True,
            "nectar_injection": True,
            "pollen_discovery": True,
        },
        "components": {
            "task_directive": directive,
            "prior_work": prior_work,
            "anti_fab_callouts": anti_fab,
            "reputation_anti_patterns": reputation,
            "pressure_mode_selector": context_fill_dependent(),  # Queue Autonomy / Caution / Pressure-Response
        },
        "spawn_prompt": f"""You are {official_type} executing task {task_id}.

Read this bundle FIRST. Agent card: ~/.claude/agents/{agent_type}.md

{card.body}

---

{directive}

{prior_work}

{anti_fab}

{reputation}

{pressure_mode_selector}

---

MANIFEST OUTPUT: Write to ~/.claude/hooks/state/agent-manifests/[timestamp]_{task_id}_{agent_type}.json
FIELDS REQUIRED: task_id, status, dashboard_line, next_task_queued, output_path
"""
    }
    
    return bundle
```

### Time T=3: Bundle Written to Disk

```bash
# run.py writes bundle to disk
BUNDLE_PATH="~/.claude/hooks/state/bundles/task-20260425-181259-b831.json"
echo $bundle_json > $BUNDLE_PATH
```

**Cost:** Disk I/O, no token cost.

### Time T=4: Main Spawns Agent with Bundle Reference

```python
import json

# Read JSONL line from run.py output
line = '{"task_id":"...", "bundle_path":"~/.claude/hooks/state/bundles/...", "agent_type":"general-purpose"}'
task = json.loads(line)

# Read bundle path
bundle_path = task["bundle_path"]

# Construct minimal spawn prompt (50 tokens)
spawn_prompt = f"""READ: {bundle_path}

Execute the task. Return MANIFEST at the path specified in the bundle."""

# Spawn with official type, card injected as part of bundle
Agent(
    subagent_type="general-purpose",  # official type
    prompt=spawn_prompt,               # just 50 tokens reference
    run_in_background=True
)
```

**Main context cost for spawning: ~50 tokens.**

### Time T=5: Agent Starts, Reads Bundle

Agent spawns in independent 200K context window:

```python
import json

# Agent's first action: read the bundle
bundle_path = extract_from_prompt("READ: (.*)")
with open(bundle_path) as f:
    bundle = json.load(f)

# Agent now has:
# - Task directive (goal, done_looks_like, constraints)
# - Agent card (behavioral protocol)
# - Prior work context (3 recent manifests in same domain)
# - Anti-fab callouts (integrity reminders)
# - Reputation anti-patterns (accountability)
# - HONEY/NECTAR (if bundle_knobs.honey_injection=True)
# - Pollen discoveries (if bundle_knobs.pollen_discovery=True)
# - Pressure mode (queue autonomy or pressure-response)
# Total agent startup context: ~1500–2000 tokens of rich direction
```

**Agent context cost: HIGH, but in isolated 200K window (doesn't affect main).**

---

## Bundle Formula: Conservative vs. Experimental

### Conservative (default)

Minimum composition cost; maximum safety:

- ✅ TASK_DIRECTIVE
- ✅ DONE_LOOKS_LIKE
- ✅ RELEVANT_PRIOR_WORK
- ✅ ANTI_FAB_CALLOUTS
- ✅ REPUTATION_ANTI_PATTERNS
- ✅ Pressure mode selector
- ❌ Full HONEY (summary-only)
- ❌ Full NECTAR (tail-10 only, if applicable)
- ❌ Full pollen (filtered to task tags only)

**Typical size: 1.2–1.8K tokens of startup context for agent.**

### Experimental

Richer context for complex synthesis tasks:

- ✅ All of conservative
- ✅ Full HONEY (~2K tokens)
- ✅ Full NECTAR tail-30 (~3K tokens)
- ✅ Full pollen discoveries (unfiltered)
- ✅ Sibling context (compass_s/compass_n recent completions)
- ✅ Investigation label braiding context

**Typical size: 6–8K tokens of startup context.**

**Switch:** Add `synthesis-heavy` tag to task spec to get experimental formula.

---

## Key Design Decisions

### 1. Write Bundle to Disk, Not to Main Prompt

**Why:** Disk I/O is cheap. Inline context in main's prompt is expensive.

- Old (bad): Main composes bundle in prompt, spawns. Cost: ~800 tokens/spawn.
- New (good): Template writes bundle to disk, main references path. Cost: ~50 tokens/spawn.
- **Savings: 94%.**

### 2. Task Spec is Serialized Early

**Why:** Declarative shape is finalized at queue time, not spawn time.

Once in queue, task spec does not change. Template substitution is pure parameter injection, not inference.

### 3. Agent Cards are Discovery Metadata, Not Spawn Types

**Why:** Decouples behavioral composition from platform agent types.

- Card defines behavioral protocol (stigmergy-scout, python-pro)
- Card frontmatter maps to official type (general-purpose)
- Bundle injects card content as prompt prefix
- Main spawns with official type

### 4. Relevant Prior Work is Discovered via Grep

**Why:** Zero-cost at template time; filesystem is the coordination layer.

```bash
grep -r "task-keyword" forensics/manifests/ --max-count 3
```

No task database, no query overhead. Just filesystem glob + grep.

### 5. Pressure Mode is Auto-Selected, Not Configured

**Why:** Context fill is the primary clock.

Bundle reads current `piston-checkpoint.json`:
- `context_pct < 80%` → Queue Autonomy Block (agent can claim more tasks)
- `80% ≤ context_pct < 92%` → Caution Block (capture droplets)
- `context_pct ≥ 92%` → Pressure-Response Block (finish + return; no new claims)

Agent doesn't choose; system injects the right guardrails.

---

## Checklist: When Adding a New Agent Type

1. **Create card file:** `~/.claude/agents/myagent.md`
2. **Add frontmatter:**
   ```yaml
   maps_to_official_type: general-purpose  # (or other official type)
   injection_method: "prompt prefix + behavioral protocol"
   ```
3. **Test bundle assembly:**
   ```bash
   python3 7x_spawn_template.py show --template myagent
   python3 7x_spawn_template.py render --template myagent \
     --params '{"task_id":"test-task","agent_type":"myagent"}'
   ```
4. **Verify official type exists:** `Agent(subagent_type="general-purpose")` must succeed
5. **Validate integrity:** Card should NOT reference its own Last Training or cached baseline

---

## Token Accounting (Per Spawn Cycle)

| Component | Cost | Location |
|-----------|------|----------|
| **Main composition** | ~50 tok | `prompt="READ: {bundle_path}..."` |
| **Disk I/O** | 0 tok | Template writes bundle, no token cost |
| **Agent startup** | ~1500–2000 tok (isolated 200K window) | Agent reads bundle at spawn time |
| **Bundle assembly** | Amortized across all spawns via template | Not charged to any single spawn |
| **Total per spawn** | **~50 tok (main only)** | f(0) achieved ✓ |

**At n=50 spawns per session:**
- Old approach (inline composition): ~40K tokens to main context
- New approach (bundle + template): ~2.5K tokens to main context
- **Savings: 93.75% context preservation, 50 agents per session now feasible**

---

## Cross-References

- **docs/SPAWN-CARD-PROTOCOL.md** — Agent types vs. cards
- **scripts/7x_spawn_template.py** — Template engine and bundle assembly
- **scripts/run.py** — Queue consumer that triggers bundle assembly
- **.claude/HONEY.md** — Global crystallized methods and principles
- **.claude/NECTAR.md** — Recent session findings
- **forensics/manifests/** — Forensic chain, prior work discovery source

---

*Bundle composition pattern established 2026-04-25 · f(0) foundation: disk instead of prompt.*
