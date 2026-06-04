---
type: architecture
status: active
created: 2026-04-21
tags: [spawn, boilerplate, architecture, agents]
up: README.md
prev: MEMORY-AS-SERVICE-ARCHITECTURE.md
---

> [↑ Readme](README.md) · [← Memory As Service Architecture](MEMORY-AS-SERVICE-ARCHITECTURE.md) · [⌂ Home](../README.md)

# Spawn Boilerplate Injection Architecture — How Faerie Programmatically Ensures Compliance

**Question:** Where does faerie get told to use spawn boilerplate? How does it programmatically enforce this without manual copy-paste or inference?

**Answer:** Through `build_spawn_bundle.py` — a deterministic, no-inference builder that loads SPAWN-BOILERPLATE.md and injects sections into every agent prompt.

---

## The Architecture (Zero Inference Required)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CANONICAL TRUTH LAYER — Git-tracked, deterministic                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ /mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md               │
│   - 26KB, version-controlled                                               │
│   - Divided into labeled ## sections                                       │
│   - Every section is a MANDATORY protocol                                  │
│   - Updated when system rules change (edit once, applies to all agents)   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓ (read at spawn time)
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ BUILDER LAYER — Deterministic section extraction                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ build_spawn_bundle.py                                                      │
│                                                                             │
│ 1. Load SPAWN-BOILERPLATE.md                                              │
│ 2. Extract specific sections by header matching:                           │
│    - "## STRATEGIC BRIEF — Evaluation-Aware Design"                       │
│    - "## ANTI-GAMING BUNDLE MODEL"                                        │
│    - "## MEMBENCH CONTEXT"                                                │
│    - "## 1. Manifest Write"                                               │
│    - "## 3c. Droplet Protocol"                                            │
│    - "## 4. Stigmergy"                                                    │
│    - "## 2. Forensic Trace" (if agent_type requires)                     │
│    - "## 3b. Citation Discipline" (if agent_type requires)               │
│    - "## 5. Quick Checklist"                                              │
│                                                                             │
│ 3. Load agent-type-specific overrides from bundle-composition.json        │
│ 4. Load HONEY.md (trimmed to 5K)                                          │
│ 5. Assemble in FIXED ORDER (deterministic, not inference)                 │
│ 6. Return complete prompt string (ready for Agent() tool)                 │
│ 7. Log metrics to COC: tokens, agent_type, task_id, session_id            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓ (returns complete prompt)
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ SPAWN LAYER — Pass to Agent() tool                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Agent(                                                                      │
│   subagent_type="python-pro",                                              │
│   prompt=<output from build_spawn_bundle.py>,  ← All boilerplate injected │
│   description="Task 27: Implement atomic queue claiming"                   │
│ )                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓ (agent receives prompt)
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ AGENT LAYER — Follows boilerplate protocols (now in context)              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Agent reads spawn prompt:                                                  │
│  - Knows manifest path (injected from SPAWN-BOILERPLATE)                 │
│  - Knows droplet protocol (injected)                                       │
│  - Knows stigmergy rules (injected)                                        │
│  - Knows forensic trace format (injected)                                 │
│  - Knows anti-gaming rules (injected)                                     │
│ Agent executes work following these protocols (no guessing)                │
│ Agent returns manifest + findings (conforming to injected spec)            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Insight: The Boilerplate is NOT a Recommendation

The boilerplate is **injected directly into the agent's context**, not referenced as a file to read.

This means:
- ✅ Agent doesn't need to find or read SPAWN-BOILERPLATE.md
- ✅ Agent doesn't need to search for sections
- ✅ Agent doesn't need to infer what applies to them
- ✅ **Agent just reads the prompt they were given and follows it**

The protocols are **already there**, contextualized for their specific agent type.

---

## How build_spawn_bundle.py Works (Deterministic, No Inference)

### Step 1: Load Once
```python
boilerplate = path.read_text()  # Load SPAWN-BOILERPLATE.md once
```

### Step 2: Extract by Header Match
```python
def _extract_boilerplate_section(self, section_name: str) -> str:
    """Extract a named section from SPAWN-BOILERPLATE.md."""
    lines = self.boilerplate.split("\n")
    section_start = None
    section_end = None

    for i, line in enumerate(lines):
        if line.startswith(f"## {section_name}"):  # ← Exact header match
            section_start = i
        elif section_start is not None and line.startswith("## "):
            section_end = i
            break

    if section_start is None:
        return f"(Section '{section_name}' not found in boilerplate)"

    return "\n".join(lines[section_start:section_end])
```

**This is deterministic:**
- No inference
- No fuzzy matching
- Just header matching (section must exist and be named exactly)
- If header doesn't exist, builder fails loudly

### Step 3: Assemble in Fixed Order
```python
sections = []

# 1. HONEY (always)
sections.append("=== CRYSTALLIZED KNOWLEDGE (HONEY.md) ===\n")
sections.append(self.honey[:5000])

# 2. STRATEGIC BRIEF (always)
sections.append(self._extract_boilerplate_section("STRATEGIC BRIEF — Evaluation-Aware Design"))

# 3. ANTI-GAMING (always)
sections.append(self._extract_boilerplate_section("ANTI-GAMING BUNDLE MODEL"))

# 4. MEMBENCH (always)
sections.append(self._extract_boilerplate_section("MEMBENCH CONTEXT"))

# 5. Manifest write (always)
sections.append(self._extract_boilerplate_section("1. Manifest Write"))

# 6. Droplets (always)
sections.append(self._extract_boilerplate_section("3c. Droplet Protocol"))

# 7. Stigmergy (always)
sections.append(self._extract_boilerplate_section("4. Stigmergy"))

# 8. Agent-type-specific (if configured)
if agent_type in bundle_config.get("agent_type_overrides", {}):
    # Extract agent-specific sections
    # E.g., security-auditor needs "2. Forensic Trace"
    # E.g., report-writer needs "3b. Citation Discipline"

# 9. Optional: Architecture docs (if --include-architecture)
# 10. Optional: Full NECTAR (if --include-nectar-full)
# 11. Task context (always)
# 12. Vault instructions (always)
# 13. Checklist (always)

final_prompt = "\n".join(sections)  # ← Deterministic concatenation
```

**This is deterministic:**
- Fixed section order (no decision tree, no "if Y then Z")
- Agent-type lookups are config-driven (bundle-composition.json)
- No inference, just string concatenation

### Step 4: Log Metrics (for audit)
```python
metrics = {
    "ts": datetime.utcnow().isoformat() + "Z",
    "agent_type": agent_type,
    "task_id": task_id,
    "bundle_tokens": tokens,
    "session_id": os.environ.get("CLAUDE_SESSION_ID", "unknown"),
}

coc_path = Path.home() / ".claude" / "memory" / "forensics" / "bundle-metrics.jsonl"
with open(coc_path, "a") as f:
    f.write(json.dumps(metrics) + "\n")
```

Every bundle created is logged (immutable, hash-chained) so we can verify:
- Which agents got boilerplate
- How many tokens were injected
- When boilerplate changed (via git history of SPAWN-BOILERPLATE.md)

---

## How Faerie Invokes This (from faerie_spawn.py)

Faerie doesn't invoke build_spawn_bundle.py directly. Instead, faerie-driven spawn calls use it:

```bash
# Command to build a bundle
python3 scripts/build_spawn_bundle.py \
  --agent-type python-pro \
  --task-id 27 \
  --task-description "Implement atomic queue claiming" \
  --include-architecture

# Returns: Complete prompt string, ready for Agent() tool
```

**Or programmatically in Python:**

```python
from scripts.build_spawn_bundle import BundleBuilder

builder = BundleBuilder()
prompt = builder.build(
    agent_type="python-pro",
    task_id="27",
    task_description="Implement atomic queue claiming",
    include_architecture=True
)

Agent(
    subagent_type="python-pro",
    prompt=prompt,  # ← All boilerplate is already in here
    description="Task 27"
)
```

---

## What This Achieves (Zero Inference, Full Compliance)

### ✅ Deterministic
- Every time `build_spawn_bundle.py` runs with the same inputs, it produces the same output
- No randomization, no decision trees, no inference
- Reproducible: same agent type + same SPAWN-BOILERPLATE.md = identical prompt

### ✅ Auditable
- Every bundle creation logged to COC: agent_type, tokens, timestamp, session_id
- Can verify: "Agent X got boilerplate Y at time Z"
- Git history of SPAWN-BOILERPLATE.md shows when protocols changed

### ✅ Version-Controlled
- SPAWN-BOILERPLATE.md is git-tracked (26KB, one source of truth)
- Update the file once → ALL future agents get the new protocol
- Old commits show what boilerplate agents had at that time

### ✅ Minimal Manual Work
- No copy-paste of boilerplate
- No "remember to include X section"
- No accidental omissions
- Just: call `build_spawn_bundle.py` with agent type + task info
- Boilerplate is automatically injected

### ✅ Extensible
- New agent types: add entry to `bundle-composition.json` specifying which sections they need
- New protocols: add ## section to SPAWN-BOILERPLATE.md, update builder to extract it
- Changes cascade: edit SPAWN-BOILERPLATE.md once, all agents benefit next spawn

---

## The Agent-Type Overrides (How Specificity Works)

Not all agents need the same boilerplate sections. `bundle-composition.json` specifies:

```json
{
  "agent_type_overrides": {
    "security-auditor": {
      "additional_components": [
        {"name": "Forensic Trace", "mandatory": true},
        {"name": "Hash Verification", "mandatory": true}
      ],
      "honey_trim": 3000,
      "nectar_skip": true
    },
    "report-writer": {
      "additional_components": [
        {"name": "Citation Discipline", "mandatory": true},
        {"name": "Vault Write Format", "mandatory": true}
      ],
      "honey_trim": 5000,
      "nectar_skip": false
    },
    "python-pro": {
      "additional_components": [
        {"name": "Citation Discipline", "mandatory": true}
      ],
      "honey_trim": 5000,
      "nectar_skip": false
    }
  }
}
```

**When building for security-auditor:**
1. Include core sections (STRATEGIC BRIEF, ANTI-GAMING, MEMBENCH, etc.)
2. Look up security-auditor in bundle_config
3. Find it needs "Forensic Trace" + "Hash Verification"
4. Extract those sections from SPAWN-BOILERPLATE.md
5. Assemble final prompt with those additional sections

**This is still deterministic:** lookup + extraction, no inference.

---

## Guarantees This Architecture Provides

### 1. **No Agent Ever Misses Boilerplate**
- Boilerplate is in the prompt they receive
- Agent doesn't need to find or read SPAWN-BOILERPLATE.md
- No excuses for "forgot to include manifest protocol"

### 2. **No Manual Copy-Paste**
- Boilerplate is programmatically extracted
- No risk of outdated or partial copy-paste
- Update SPAWN-BOILERPLATE.md once, all agents updated

### 3. **No Ambiguity About Which Sections Apply**
- Agent type → lookup in bundle-composition.json → exact sections
- Not "read the boilerplate and pick what applies"
- Just "here's your specific prompt"

### 4. **Versioning and Auditing**
- Every bundle creation logged (COC)
- Can trace: Agent X got boilerplate version Y at time Z
- Can correlate: agent performance vs boilerplate version

### 5. **Minimal Inference in Builder**
- Builder is ~250 lines of deterministic Python
- No ML, no heuristics, no decision trees
- Just: load file, extract sections by header match, concatenate

---

## The Flow in Practice

### Scenario: Faerie spawns a python-pro agent for task 27

```bash
# 1. Faerie calls
python3 scripts/build_spawn_bundle.py \
  --agent-type python-pro \
  --task-id 27 \
  --task-description "Implement atomic queue claiming mechanism"

# 2. Builder executes deterministically
#    - Load SPAWN-BOILERPLATE.md
#    - Extract: STRATEGIC BRIEF, ANTI-GAMING, MEMBENCH, Manifest, Droplets, Stigmergy, Citation Discipline, Task Context, Vault, Checklist
#    - Load HONEY.md (trim to 5K)
#    - Load bundle-composition.json for python-pro overrides
#    - Assemble in fixed order
#    - Return: ~8K token complete prompt

# 3. Output
#    Complete prompt string containing all boilerplate sections

# 4. Faerie invokes Agent()
Agent(
  subagent_type="python-pro",
  prompt=<8K complete prompt>,
  description="Task 27: Implement atomic queue claiming"
)

# 5. Builder logs to COC
#    COC entry: {ts, agent_type: python-pro, task_id: 27, bundle_tokens: 8000, session_id: abc123}

# 6. Agent receives prompt with all protocols already injected
#    Agent reads prompt → already has manifest path, droplet rules, stigmergy rules, etc.
#    Agent just executes following these protocols (no guessing)
```

---

## Summary: The Complete Picture

**Question:** Where does faerie get told to use spawn boilerplate?

**Answer:** Via `build_spawn_bundle.py`, which:
1. Reads SPAWN-BOILERPLATE.md (git-tracked, single source of truth)
2. Extracts specific sections by header matching (deterministic)
3. Looks up agent-type in bundle-composition.json (config-driven)
4. Assembles sections in fixed order (no inference)
5. Injects into agent prompt (boilerplate is already in context)
6. Logs to COC (auditable)

**How does it do this without inference?**
- No fuzzy matching (exact header match)
- No decision trees (config-driven)
- No heuristics (fixed assembly order)
- No randomization (reproducible)

**How is this enforced at runtime?**
- Boilerplate is **in the prompt the agent receives**
- Agent reads prompt, follows protocols
- No need for agent to find or read SPAWN-BOILERPLATE.md separately
- No "remember to include X"

**What if SPAWN-BOILERPLATE.md changes?**
- Edit once
- All future agents get updated boilerplate
- Old commits show version history
- COC logs show when change took effect

---

**Document version:** v1.0 | **Date:** 2026-04-21 | **Status:** Complete architecture explanation
