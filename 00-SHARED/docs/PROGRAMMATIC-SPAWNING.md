# Programmatic Agent Spawning — The New Workflow

**Problem solved:** Manual prompt assembly was fragile, inconsistent, ad-hoc.
**Solution:** Build bundles programmatically, log metrics to COC, make spawning systematic.

---

## Three-Script Stack

### 1. `build_spawn_bundle.py` — Bundle Assembly

Reads config, assembles bundle per agent-type, injects droplet protocol + vault format.

**Usage:**
```bash
python3 scripts/build_spawn_bundle.py \
  --agent-type python-pro \
  --task-id 27 \
  --task-description "Implement atomic queue claiming" \
  --include-architecture \
  --output-path /tmp/bundle.txt
```

**Output:**
- Complete prompt string (~5.5K tokens baseline)
- Logged to COC: bundle-metrics.jsonl (tokens, agent-type, task-id, session)

**Key features:**
- Reads `bundle-composition.json` (canonical source of truth)
- Selectively injects boilerplate sections per agent-type
- Includes vault write format + task queuing instructions (always)
- Droplet protocol with explicit READ + WRITE timing
- Conditional architecture docs (only if task mentions them)

### 2. `faerie_spawn.py` — Spawn Wrapper

Takes agent-type + task, generates complete Agent() tool call, logs to COC.

**Usage:**
```bash
# Print spawn template (copy-paste ready)
python3 scripts/faerie_spawn.py \
  --agent-type python-pro \
  --task-id 27 \
  --task-description "Implement atomic queue claiming" \
  --print-template

# Output as JSON (for programmatic integration)
python3 scripts/faerie_spawn.py \
  --agent-type evidence-curator \
  --task-id 28 \
  --task-description "Gap analysis" \
  --json | jq .prompt > /tmp/prompt.txt
```

**Output:**
- Formatted Agent() call (ready to copy-paste into Claude Code)
- Logged to COC: spawn-log.jsonl (event, agent-type, task-id, prompt_tokens, wave, session)

### 3. `bundle-composition.json` — Configuration

Single source of truth for what gets injected per agent-type.

**Structure:**
```json
{
  "default_bundle": {...},         // Baseline: ~7.6K tokens
  "agent_type_overrides": {
    "python-pro": {...},           // Add COC hash-chain rules
    "evidence-curator": {...},     // Add citation discipline
    "documentation-engineer": {...} // Add vault frontmatter rules
  },
  "tuning_levers": {...}           // Optional: HONEY trim, NECTAR skip, etc.
}
```

**Key tuning levers:**
1. **HONEY.md reduction** — Currently 54% of baseline. Can trim to tail-50 or section-only (measure beat-last regression).
2. **NECTAR inclusion** — Currently tail-30 for all. Can skip for infrastructure agents.
3. **Architecture docs** — Conditional on task content (already implemented).

---

## New Agent Spawn Workflow

### Old (Manual, Error-Prone)
```
1. Write prompt from scratch
2. Copy-paste boilerplate sections
3. Hope vault format is included
4. No logging to COC
5. Each agent gets different bundle
```

### New (Systematic)
```
1. faerie_spawn.py --agent-type X --task-id N --task-description "..."
2. Reads bundle-composition.json for X
3. Assembles bundle via build_spawn_bundle.py
4. Logs to COC: spawn-log.jsonl + bundle-metrics.jsonl
5. Every agent gets consistent, validated bundle
```

---

## What Every Agent Now Receives (Guaranteed)

✅ **HONEY.md** (crystallized truths)  
✅ **Evaluation context** (strategic brief + baseline awareness)  
✅ **Droplet protocol** (WRITE timing + READ timing)  
✅ **Manifest format** (including hash computation)  
✅ **Vault write rules** (frontmatter, breadcrumb, hash, INDEX)  
✅ **New task queueing format** (stigmergic, no approval needed)  
✅ **Agent-type-specific additions** (COC rules, citation, etc.)  

---

## Integration with Faerie (TODO)

Currently, these scripts are standalone tools. Next step: wire them into faerie so spawning is **automatic + systematic**.

**Proposed integration:**
```python
# In faerie's spawn logic:
from scripts.faerie_spawn import generate_agent_spawn_command

spawn_config = generate_agent_spawn_command(
    agent_type="python-pro",
    task_id="27",
    task_description="...",
    include_architecture=task_references("queue"),
    run_in_background=is_background_task()
)

# Execute Agent() with assembled bundle
Agent(
    subagent_type=spawn_config["agent_type"],
    description=spawn_config["description"],
    prompt=spawn_config["prompt"],
    run_in_background=spawn_config["run_in_background"],
)
```

---

## Tuning the Bundle

**Measure before/after** any tuning to ensure beat-last rate doesn't regress.

### Lever 1: HONEY.md Trim

**Current:** Full HONEY.md (~5K tokens, 54% of baseline)
**Option:** Trim to tail-50 lines or "System Principles" section only

**Test:**
```bash
# Baseline: spawn 5 agents with full HONEY, measure beat-last rate
# Trim: spawn 5 agents with HONEY tail-50, measure beat-last rate
# If regression < 2%: adopt trim
```

### Lever 2: Skip NECTAR for Infrastructure Agents

**Current:** tail-30 NECTAR for all agents
**Option:** Skip for python-pro, data-engineer (infrastructure-only agents)

**Impact:** -500 tokens from infrastructure spawns (20+ per session)

### Lever 3: Architecture Docs Conditional

**Already implemented:** QUEUE-CLAIMING-ARCHITECTURE.md only injected if task mentions "queue" or "claim"

**Works:** No tuning needed

---

## Monitoring & Metrics

**Metrics logged automatically:**
- **spawn-log.jsonl:** Every Agent() spawn with agent-type, task-id, prompt_tokens, wave, session
- **bundle-metrics.jsonl:** Every bundle built with agent-type, task-id, tokens
- **bundle-composition.json:** Source of truth for what gets injected

**Audit trail:**
```bash
# Count agents spawned per session
jq 'select(.session_id == "abc123")' ~/.claude/memory/forensics/spawn-log.jsonl | wc -l

# Measure avg prompt tokens by agent-type
jq 'group_by(.agent_type) | map({type: .[0].agent_type, avg_tokens: (map(.bundle_tokens) | add / length)})' ~/.claude/memory/forensics/bundle-metrics.jsonl
```

---

## Benefits

✅ **Consistency:** Every agent gets the same bundle structure (no ad-hoc sections)  
✅ **Measurability:** Bundle size and composition logged to COC  
✅ **Maintainability:** Bundle config is centralized (bundle-composition.json)  
✅ **Tuning:** Can A/B test different bundle mixtures (HONEY trim, NECTAR skip, etc.)  
✅ **Scaling:** Adding 50 agents to a wave is now systematic, not manual  
✅ **Debuggability:** If an agent fails, we know exactly what bundle it received  

---

## Quick Start

**To spawn an agent manually (copy-paste style):**
```bash
python3 scripts/faerie_spawn.py \
  --agent-type python-pro \
  --task-id 27 \
  --task-description "Implement atomic queue claiming" \
  --print-template
```

**To spawn programmatically (for faerie integration):**
```bash
python3 scripts/faerie_spawn.py \
  --agent-type python-pro \
  --task-id 27 \
  --json | python3 -c "
import json, sys
config = json.load(sys.stdin)
print(f'Agent(subagent_type=\"{config[\"agent_type\"]}\", prompt=\"{config[\"prompt\"]}\", ...)')
"
```

**To tune the bundle:**
1. Edit `bundle-composition.json` (e.g., set HONEY_TRIM=true, NECTAR_SKIP_FOR=[infrastructure])
2. Spawn 5 agents with new config
3. Measure beat-last rate vs baseline
4. Commit if improvement > 1% or neutral

---

**Status:** Live and working. python-pro is using this for queue-claiming Phase 1 implementation.
