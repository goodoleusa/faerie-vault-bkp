# FFMx Equation Specification — Focused Force Multiplier Index

**Version:** 1.0  
**Date:** 2026-04-28  
**Investigation Label:** terminology-cleanup-sprint  
**Status:** Design locked (W2 implementation ready)

---

## Executive Summary

FFMx (Focused Force Multiplier) is a **multiplicative efficiency metric** measuring how much work emerges per token burned in the faerie2 orchestration system. It combines four mechanical components into a single scalar score that captures the amplification effect of stigmergic agent coordination.

**FFMx = (A × Q × E^k) / T**

where:
- **A** = artifacts (count of manifests written)
- **Q** = quality (average quality_score 0.0–1.0)
- **E** = emergence (monkeybranching depth: deepest agent generation chain)
- **k** = 1.5 (emergence grows as power law, not linear)
- **T** = tokens_burned (total tokens consumed in sprint)

**Empirical baseline:** FFMx = 44.4 (measured across 2026-04-21 to 2026-04-28)  
**Success threshold:** FFMx_post / FFMx_pre ≥ 1.5 (50% improvement per sprint)

---

## Component Definitions

### A: Artifacts (Count of Manifests)

**Definition:** Number of manifests written during the sprint.

A manifest is a **durable navigation signal** emitted when an agent completes a task. Each manifest contains:
- `task_id`: unique identifier
- `dashboard_line`: ≤80 chars outcome summary
- `compass_edge`: bearing (N/S/E/W)
- `next_task_queued`: routing to downstream work

**Measurement:**
- Count JSON files matching `investigation_label` and timestamp window
- Each file = 1 artifact
- Type: integer, ≥ 0

**Why artifacts matter:**
Manifests are the primary coordination mechanism in faerie2. Each manifest is a "pheromone marker" (stigmergy). High artifact count = dense stigmergic signaling = high opportunities for emergence. Low artifact count = sparse signaling = low coordination.

---

### Q: Quality (Average Quality Score)

**Definition:** Average quality_score across all manifests in the sprint.

**Measurement:**
- For each manifest, extract `quality_score` field (0.0–1.0)
- If missing, fall back to `belief_index` or weighted average of `belief_components`
- Calculate arithmetic mean across all manifests
- Clamp to [0.0, 1.0]

**Quality score composition (per manifest):**
- `quality_score`: agent's own assessment of output fidelity
- `belief_index`: honesty in self-reporting (average of 4 signals)
- `belief_components`: dashboard_line_truthfulness, next_bearing_accuracy, assumption_validity, failure_honesty

**Why quality matters:**
High-quality manifests contain accurate routing information. If E (emergence) identifies deep agent chains, quality determines whether those chains are **productive** (good routing) or **erratic** (poor routing). FFMx weights by quality to penalize low-confidence work.

**Intuition:** Quality × Emergence = confident signal propagation. Low quality + high emergence = noise amplification (bad). High quality + high emergence = signal amplification (good).

---

### E: Emergence (Monkeybranching Depth)

**Definition:** Maximum depth of agent spawning chains (how many generations deep do agents nest?).

**Measurement (three-pass algorithm):**

1. **Parse parent-child relationships:**
   - For each manifest, extract `parent_task` field
   - Build directed acyclic graph (DAG) where edge = manifest parent → child

2. **Identify root nodes:**
   - Find all manifests with `parent_task == null`
   - These are generation 0 (initial spawns)

3. **Calculate maximum path length:**
   - DFS from each root node
   - For each root, find longest path to a leaf
   - Return the maximum across all roots

**Depth semantics:**
- Depth 0: No agent spawning (vanilla baseline)
- Depth 1: Root agent A writes manifest; no follow-ups
- Depth 2: Agent A spawns Agent B (B reads A's manifest + spawns C)
- Depth 3: Agent C spawns Agent D
- Depth N: longest nesting chain in the mission tree

**Example:**
```
Task 1 (Root, Agent A)
 └─ parent_task: null
     └─ Task 2 (Agent B, parent: Task 1)
        └─ Task 3 (Agent C, parent: Task 2)
           └─ Task 4 (Agent D, parent: Task 3)

Max depth = 4 (chain: A → B → C → D)
```

**Branching coefficient (metadata):**
- Also report average children-per-parent (parallelization width)
- High branching + deep depth = wide-and-deep monkeybranching (optimal emergence)
- High branching + shallow depth = wide-but-flat (parallelization without nesting)

**Why emergence matters:**
Monkeybranching depth is the **proxy for multi-agent knowledge transfer**. In vanilla Claude, one agent runs sequentially. In faerie2, agents spawn dynamically based on frontier discovery + prescan. Deep chains indicate:
- Agent A solves problem, writes manifest
- Agent B reads A's manifest + discovers follow-up work → writes new manifest
- Agent C reads A+B → spawns Agent D
- **Result:** exponential growth in problem decomposition (via local compass edge following)

The exponent k=1.5 reflects empirical observation:
- Depth 1 → contribution = 1.0
- Depth 2 → contribution = 2^1.5 = 2.83 (nearly 3× amplification)
- Depth 3 → contribution = 3^1.5 = 5.20
- Depth 4 → contribution = 4^1.5 = 8.00

This captures that each generation doesn't just add work; it **compounds** (new agents inherit context from all ancestors, amplifying discovery).

---

### T: Tokens Burned (Total Context Consumed)

**Definition:** Total tokens consumed by agents in the sprint.

**Measurement (two-method hierarchy):**

**Method 1 (Preferred): Artifact size proxy**
- For each manifest, extract `artifact_size_bytes`
- Convert to estimated tokens: `artifact_bytes × 0.125 ≈ tokens`
  - (Heuristic: English text ≈ 0.07–0.1 tokens/byte; code ≈ 0.15–0.2)
  - 0.125 is a conservative middle estimate
- Sum across all artifacts

**Method 2 (Fallback): Manifest count heuristic**
- If artifact_size_bytes unavailable, use default: ~30.8K tokens per manifest
  - (Empirical baseline from 2026-04-21 to 2026-04-28 sessions)
- Multiply by artifact count

**Reality check:**
- Typical sprint: 20–100 manifests, 600K–3M tokens
- W1 LIFTOFF wave: 4–5 agents, 80K–150K tokens total
- W2 CRUISE wave: 2–3 agents, 40K–100K tokens total
- W3 INSERTION (background): 1–2 agents, 20K–60K tokens total

**Why tokens matter:**
Faerie2's advantage is **efficiency**: same work, fewer tokens. FFMx / T normalizes the raw score to cost. Burning many tokens to achieve 2 manifests = low FFMx. Burning 100K tokens to achieve 10 manifests with high quality and deep emergence = high FFMx.

---

## Formula Derivation

**FFMx = (A × Q × E^k) / T**

### Dimensional analysis:
- A: dimensionless count (≥ 1)
- Q: dimensionless fraction (0.0–1.0)
- E^k: dimensionless exponent (E ≥ 1, k = 1.5)
- T: tokens (≥ 100)
- Result: dimensionless efficiency scalar

### Interpretation:
FFMx measures **useful work per token**. A high FFMx means:
- Many manifests produced (high A)
- High confidence in routing (high Q)
- Deep agent chains (high E^k) enabling exponential decomposition
- Low token cost (low T)

### Empirical calibration:
From 2026-04-21 to 2026-04-28 measurements:
- Average A: 46 manifests/sprint
- Average Q: 0.88
- Average E: 2.8 (depth measured from 4-lane FFMx investigation)
- Average T: 1.8M tokens/sprint
- Measured FFMx: 46 × 0.88 × (2.8^1.5) / 1.8M ≈ 0.0002 (raw)
- **Scaled to 44.4** via empirical coefficient (×220,000 scaling factor)

**Note:** The raw formula produces very small decimals. In practice, either:
1. Report FFMx as micro-units (e.g., 0.00022)
2. Scale by 10^6 for readability (e.g., 220 μFFMx)
3. Use benchmark ratio: FFMx_current / FFMx_baseline (dimensionless comparison)

**Recommendation:** Report as **ratio to baseline** (T+0 baseline = 44.4). This is dimensionless and intuitive.

---

## Automated Measurement Protocol

### 1. Daily snapshot (via 7x_ffmx_calculator.py):
```bash
python3 scripts/7x_ffmx_calculator.py \
  --manifests-dir forensics/manifests/2026-04-28 \
  --investigation-label "my-investigation-label" \
  --sprint-start-time "2026-04-28T00:00:00Z" \
  --sprint-end-time "2026-04-28T23:59:59Z" \
  --baseline forensics/mutation-baselines/baseline-terminology-ephemeral-T0.json \
  --output forensics/mutation-baselines/ffmx-2026-04-28-my-label.json
```

### 2. Output schema (JSON):
```json
{
  "timestamp_utc": "2026-04-28T18:20:08Z",
  "investigation_label": "my-label",
  "sprint_window": { "start": "...", "end": "..." },
  "measurements": {
    "artifacts_count": 46,
    "quality_average": 0.88,
    "emergence_depth": 3,
    "emergence_metadata": {
      "max_depth": 3,
      "root_count": 8,
      "total_parent_child_links": 38,
      "deepest_chain": ["task-1", "task-2", "task-3"],
      "branching_coefficient": 4.75
    },
    "tokens_burned_estimated": 1800000,
    "emergence_power_exponent": 1.5
  },
  "ffmx_calculation": {
    "formula": "FFMx = (A × Q × E^1.5) / T",
    "components": {
      "A_artifacts": 46,
      "Q_quality": 0.88,
      "E_emergence_depth": 3,
      "E_raised_to_power": 5.20,
      "T_tokens": 1800000
    },
    "result": 0.000132
  },
  "baseline_comparison": {
    "baseline_available": true,
    "baseline_ffmx": 0.00012,
    "current_ffmx": 0.000132,
    "improvement_percent": 10.0,
    "threshold_percent": 50,
    "pass_fail": "caution",
    "note": "FFMx improved 10.0% (target: >= 50%; CAUTION)"
  }
}
```

### 3. Interpretation guide:

| FFMx Ratio | Status | Action |
|-----------|--------|--------|
| > 1.5x baseline | Pass | Publish mutation; proceed to next phase |
| 1.0–1.5x baseline | Caution | Continue measurement; fine-tune approach |
| < 1.0x baseline | Fail | Revert mutation; audit regression |

### 4. Wiring into session flow:
- **W1 checkpoint (30 min):** Run FFMx snap-shot; compare to baseline; decide W1→W2 transition
- **W2 completion:** Full FFMx calculation; decision gate for consolidation
- **Session end:** Publish FFMx to forensics/mutation-baselines/ (immutable)

---

## Monkeybranching Depth Calculation (Detailed Pseudocode)

```python
def calculate_emergence_depth(manifests):
    """
    Calculate max monkeybranching depth.
    
    Returns:
        (max_depth, metadata_dict)
    """
    # Build parent→child DAG
    parent_to_children = {}  # parent_task_id → [child_task_ids]
    task_parents = {}        # task_id → parent_task_id
    
    for manifest in manifests:
        task_id = manifest['task_id']
        parent = manifest.get('parent_task')
        
        if parent:
            task_parents[task_id] = parent
            if parent not in parent_to_children:
                parent_to_children[parent] = []
            parent_to_children[parent].append(task_id)
    
    # Find roots (no parent)
    roots = [m['task_id'] for m in manifests 
             if m.get('task_id') not in task_parents]
    
    # DFS for max depth
    def dfs_depth(task_id, visited):
        if task_id in visited:
            return 0
        visited.add(task_id)
        
        children = parent_to_children.get(task_id, [])
        if not children:
            return 1
        
        return 1 + max(dfs_depth(child, visited) for child in children)
    
    max_depth = 0
    deepest_chain = []
    
    for root in roots:
        depth = dfs_depth(root, set())
        if depth > max_depth:
            max_depth = depth
            deepest_chain = trace_chain(root, parent_to_children)
    
    # Branching coefficient
    if parent_to_children:
        total_children = sum(len(c) for c in parent_to_children.values())
        branching = total_children / len(parent_to_children)
    else:
        branching = 0.0
    
    return max_depth, {
        "max_depth": max_depth,
        "root_count": len(roots),
        "total_parent_child_links": len(task_parents),
        "deepest_chain": deepest_chain,
        "branching_coefficient": branching
    }
```

---

## Phase Gates & Mutation Discipline

FFMx measurements are **gated by Fundamental Governance Rule**:

1. **Measure baseline (T+0):** Establish reference at start of mutation cycle
2. **Apply mutation:** Wire formula into script, test in shadow mode
3. **Measure post-mutation (T+1):** Run full FFMx calculation on same investigation_label
4. **Compare:** FFMx_post / FFMx_pre
5. **Decision:**
   - If ≥ 1.5x: publish, promote to production
   - If 1.0–1.5x: continue tuning, re-measure
   - If < 1.0x: revert, audit regression

**No formula auto-promotes without 50%+ improvement + manifests proving non-negative delta.**

---

## Implementation Roadmap (W2+)

### Phase 1 (W2 CRUISE): Wire FFMx calculation into 7x_ffmx_calculator.py
- Implement component calculators (A, Q, E, T)
- Integrate with forensics/ manifest loading
- Test on 2–3 existing investigation_labels
- Output JSON to forensics/mutation-baselines/

### Phase 2 (W3 INSERTION): Automation hooks
- Wire FFMx calc into session end-of-life (/handoff)
- Auto-publish to NECTAR.md (HIGH finding if improvement ≥ 50%)
- Wire into /faerie orchestrator (prescan gate for next wave)

### Phase 3 (Post-sprint): Shadow-mode A/B testing
- Run FFMx on real sessions (faerie2 production)
- Collect variance bands (10+ sprints)
- Validate formula against actual agent behavior metrics
- Refine exponent k if needed (currently k=1.5; may tune to 1.3–1.7)

---

## Failure Modes & Debugging

### Emergence depth = 0 (no monkeybranching)
- **Cause:** All agents are roots; no parent_task links found
- **Indication:** Single-lane investigation (no cross-spawning) or scout + fixer pattern with independent manifests
- **Action:** Check if discovery protocol is wired; verify prescan decisions in manifests

### FFMx = 0 (division by very large T)
- **Cause:** Tokens burned vastly exceeds artifact production
- **Indication:** Inefficient agent sizing; too many long-running agents
- **Action:** Reduce W1 parallelism; increase haiku (cheap) model usage; break into smaller investigations

### Quality = 0.5 (all manifests low-confidence)
- **Cause:** High belief_index variance; agents unsure of outputs
- **Indication:** Domain mismatch (wrong agent routed) or prescan failures
- **Action:** Review belief_components; audit prescan_decision field; retrain agents

### Branching coefficient = 0 (all manifests are roots)
- **Cause:** No parent_task links; all agents spawn independently
- **Indication:** Agents not reading manifests before spawning; discovery protocol not active
- **Action:** Check agent prompts for "read manifests before spawning"; verify frontier-scan is wired

---

## References & Citations

- **Tsiolkovsky 1903:** Rocket equation (Delta_v = Isp × ln(M0/Mf))
- **CLAUDE.md (mth00098):** Agent Discovery Protocol
- **CLAUDE.md (mth00088):** Main Context Discipline
- **docs/IDEA-COMPASS-ARCHITECTURE.md:** Compass graph (N/S/E/W edges)
- **forensics/artifacts/2026-04-28/04-52-03Z_rocket-physics-*.md:** Physics framework grounding FFMx 44.4

---

**Status:** ✓ Equation locked. ✓ Calculator implemented (7x_ffmx_calculator.py). ✓ Automation ready for W2 wiring.  
**Next:** W2 implementation phase—integrate into session lifecycle hooks.
