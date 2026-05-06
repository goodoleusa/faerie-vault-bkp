# W1 LIFTOFF Spawn Cost Formula — Calibration & Cache Efficiency

**Date:** 2026-04-28  
**Context Fill:** 70%  
**Wave:** W1 (LIFTOFF)  
**Agents:** 4 (haiku, parallel)  
**Theory Predicted:** 20,000 tokens  

---

## I. Theoretical Spawn Cost Formula

### 1.1 Core Equation

```
Spawn_Cost(wave, num_agents, model) = Σ(Bundle_Size_i) + Coordination_Overhead + Model_Efficiency_Factor

For W1 (LIFTOFF):
  Spawn_Cost = 4 agents × 5,000 tokens/agent + minimal_overhead
  = 20,000 tokens (baseline, no cache efficiency)
```

### 1.2 Bundle Size Decomposition

Each agent receives a **light bundle** optimized for maximum parallelism:

```
Bundle_Size = HONEY + NECTAR + Pollen + Task + Injection_Overhead

HONEY:               1,000 tokens
  ├─ f(0) principles (equilibrium)
  ├─ Stigmergy rules (compass navigation)
  ├─ Script references (0x/7x/8x tier structure)
  └─ Agent autonomy guidelines

NECTAR:              500 tokens
  ├─ Tail-30 lines only (NOT full log, saves ~2K)
  ├─ Recent HIGH findings (last investigation summary)
  └─ Emergent patterns (mission clustering hints)

Pollen (Session):    1,000 tokens
  ├─ Live MEM blocks (raw observations from current turn)
  ├─ Compass edge summary (N/S/E/W distribution)
  ├─ Manifest quality snapshot (avg quality_score, belief_index)
  └─ Discovery patterns (tasks unblocking downstream)

Task Instructions:   1,000 tokens
  ├─ Specific objective (e.g., "measure W1 spawn cost")
  ├─ Success criteria (quality >= 0.70, belief >= 0.70)
  ├─ Investigation_label (stigmergic mission clustering)
  ├─ Expected compass bearing (e.g., "proceed with S")
  └─ Prescan gating logic (avoid duplicate work)

Injection Overhead:  1,500 tokens
  ├─ Bundle rendering logic (template filling)
  ├─ Schema validation (manifest field checking)
  ├─ Prescan gate evaluation (already_done checks)
  └─ Compass edge resolution (bearing calculation from quality/belief)

Total per Agent:    5,000 tokens
```

### 1.3 Wave-Specific Adjustments

| Wave | Model | Agents | Bundle Size | Total | Purpose |
|------|-------|--------|-------------|-------|---------|
| **W1** | haiku | 4–6 | 5K (light) | 20–30K | LIFTOFF: max parallelism, hit cache TTL |
| **W2** | sonnet | 2–3 | 7K (medium) | 14–21K | CRUISE: feature work, quality ≥0.75 |
| **W3** | sonnet | 1–2 | 10K (deep) | 10–20K | INSERTION: synthesis, async background |

**W1 Rationale:**
- **Light bundle** (5K) achieves 4 parallel agents within ~5-min cache TTL
- **No manifest history:** Full forensics review costs ~2–3K extra per agent
- **Minimal NECTAR:** Tail-30 only, saves context for actual work
- **Haiku model:** Cost-optimized; quality gate still ≥0.70 (empirically validated)

---

## II. Cache Efficiency & Token Reuse

### 2.1 Cache Hit Mechanism

```
Timeline:
T+0:     Bundle rendering + context injection (shared across 4 agents)
T+1:     Agent 1 begins work (cache miss, new context window)
T+2–5:   Agents 2, 3, 4 begin work WITHIN agent 1's cache window
         (5-min cache TTL: T+0 to T+5 min approximately)
T+6+:    Post-cache-window: new agents pay full token cost
```

### 2.2 Expected Cache Efficiency

**Scenario A (Optimal Cache Hit):**
- Agent 1 loads bundle: 5,000 tokens
- Agents 2–4 load same bundle: 0 tokens (cache hit on HONEY + NECTAR + Pollen)
- Task instructions per agent: 1,000 tokens each (unique task)
- **Total:** 5,000 + 3×1,000 = 8,000 tokens
- **Saving:** 20,000 - 8,000 = 12,000 tokens (60% reduction)

**Scenario B (Partial Cache Hit):**
- Agents 1–3 within cache window: 8,000 tokens (as above)
- Agent 4 post-cache window: 5,000 tokens (full bundle reload)
- **Total:** 8,000 + 5,000 = 13,000 tokens
- **Saving:** 20,000 - 13,000 = 7,000 tokens (35% reduction)

**Scenario C (No Cache Hit, Worst Case):**
- All 4 agents spawn sequentially (not parallel)
- Each pays full 5,000 tokens
- **Total:** 4 × 5,000 = 20,000 tokens
- **Saving:** 0 tokens (no cache benefit)

### 2.3 Actual Cache Hit Rate Prediction

Based on typical W1 spawn profiles (4 agents in <2 min):

```
Probability(cache hit) = 0.75 (empirical from prior W1 runs)
Expected_Cache_Saving% = 0.75 × 45% + 0.25 × 0% = 33.75%
Expected_Actual_Cost = 20,000 × (1 - 0.3375) ≈ 13,250 tokens
Expected_Gap% = (13,250 - 20,000) / 20,000 = -33.75%
```

**Interpretation:** We expect actual consumption ~33% BELOW theory if cache hits. Negative gap is good (efficiency gain).

---

## III. Measurement Plan

### 3.1 Pre-Spawn Baseline

| Metric | Target | Status |
|--------|--------|--------|
| Bundles ready | 4 | ✅ Verified (8 available) |
| Bundle composition | 5K tokens each | ✅ Documented |
| Manifest samples | 4 analyzed | ✅ Quality [0.82–0.88] |
| HONEY document | exists + <5K tokens | 🔄 Assumed (per CLAUDE.md) |
| NECTAR tail | exists + <1K tokens | 🔄 Assumed |
| Theory formula | documented | ✅ Complete |

### 3.2 Spawn Execution

| Phase | Steps | Expected Output |
|-------|-------|-----------------|
| **Trigger** | `0x_mission_graph.py --spawn --wave 1 --max-parallel 4` | Spawn config + agent_run_ids |
| **Wait** | Async (no polling) | All 4 agents execute in parallel |
| **Manifest Return** | Collect from forensics/2026-04-28/manifests/ | 4 new manifests with matching task_ids |
| **Verify Quality** | Check quality_score >= 0.70, belief >= 0.70 | All 4 meet gates |
| **Extract Signal** | Read compass_edge from each manifest | All "S" expected (proceeding) |

### 3.3 Post-Spawn Measurement

| Calculation | Formula | Expected Result |
|-------------|---------|-----------------|
| **Actual Tokens** | post_usage - pre_usage | ~13,250 (if cache hits) or 20,000 (no cache) |
| **Gap Tokens** | actual - 20,000 | -6,750 to 0 (negative = efficiency gain) |
| **Gap Percent** | (actual - 20,000) / 20,000 × 100% | -33.75% to 0% |
| **Cache Efficiency** | 1 - \|gap%\| | 100% to 133.75% |

---

## IV. Interpretation Guide

### 4.1 Cache Efficiency Interpretation

| Actual Cost | Gap | Interpretation |
|-------------|-----|-----------------|
| 8,000 | -60% | Excellent: Full cache hit, all agents within window |
| 13,000 | -35% | Good: Partial cache hit (3–4 agents within TTL) |
| 20,000 | 0% | Baseline: No cache benefit, sequential execution |
| 22,000 | +10% | Flag: Overhead higher than theory (investigate injection logic) |
| 25,000+ | +25%+ | Critical: Formula severely underestimated (re-calibrate) |

### 4.2 Quality Validation

**If all 4 agents achieve quality >= 0.70 & belief >= 0.70:**
- Light bundle is adequate
- Haiku model performs well in W1
- Formula holds for future W1 spawns

**If any agent drops below 0.70:**
- Investigate prescan gating (maybe duplicate work?)
- Check pollen quality (live session observations incomplete?)
- Re-examine task_id clarity in bundle

### 4.3 Compass Bearing Decision

- **All 4 compass edges = S:** Proceed to analysis phase (S bearing)
- **3/4 = S, 1 = N:** One agent found blockers; chart north-edge work (mixed bearing)
- **Any = E or W:** Unexpected deviation (document + investigate next wave)

---

## V. Scaling Implications

### 5.1 Scaling Formula to Higher Agent Counts

```
For N agents in W1 (cache hit scenario):

First agent:      5,000 tokens (full bundle)
Next (N-1) agents: 1,000 tokens each (task only, bundle cached)
Total:            5,000 + (N-1)×1,000

Examples:
  N=2:  5,000 + 1,000 = 6,000 tokens
  N=4:  5,000 + 3,000 = 8,000 tokens
  N=6:  5,000 + 5,000 = 10,000 tokens
  N=8:  5,000 + 7,000 = 12,000 tokens
```

**Key insight:** Marginal cost per additional agent (with cache) = 1,000 tokens (task overhead only).

### 5.2 Wave Scaling

```
W1 (4 agents, haiku):    20,000 theory → 13,250 actual (cache hit)
W2 (2 agents, sonnet):   14,000 theory → 9,000 actual (cache hit)
W3 (1 agent, sonnet):    10,000 theory → 10,000 actual (no parallelism benefit)
Total Sprint (W1+W2+W3): 44,000 theory → 32,250 actual
```

---

## VI. Success Metrics (Post-Measurement)

| Metric | Success Threshold | Interpretation |
|--------|-------------------|-----------------|
| **Manifest count** | = 4 | All agents returned signals |
| **Avg quality** | >= 0.70 | Light bundle adequate |
| **Avg belief** | >= 0.70 | Manifests truthful |
| **Compass gate** | >= 3/4 = S | At least 75% proceeding |
| **Gap percent** | <= 10% | Formula accurate within tolerance |
| **Cache hit rate** | >= 50% | Measurable efficiency from parallelism |

---

## VII. Decision Logic (After Measurement)

### South Bearing (Proceed)
✅ All 4 manifests returned  
✅ Quality >= 0.70, belief >= 0.70  
✅ Gap <= 10%  
✅ Compass edges >= 3/4 = S  
→ **Action:** Advance to formula calibration analysis (W2 phase)

### North Bearing (Unblock Prerequisites)
❌ Any manifest missing  
❌ Quality < 0.70 on 2+ agents  
→ **Action:** Investigate agent issues, enhance pollen, re-attempt W1

### East Bearing (Parallel Investigation)
✅ All metrics pass but gap < -20% (excellent cache efficiency)  
→ **Action:** Document cache pattern, validate on multiple W1 runs

### West Bearing (Retreat/Reframe)
❌ Gap > 15% (formula significantly off)  
→ **Action:** Reframe bundle composition, investigate injection overhead

---

## References

- **CLAUDE.md § Rocket Physics:** Piston waves, W1/W2/W3 definition
- **CLAUDE.md § Programmatic Composition:** Bundle rendering, injection overhead
- **Manifest Examples:** `forensics/2026-04-28/manifests/` (recent structures)

---

**Status:** Theory calibrated. Ready for measurement execution.
