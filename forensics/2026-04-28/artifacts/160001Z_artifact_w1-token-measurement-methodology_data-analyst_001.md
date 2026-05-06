# W1 LIFTOFF Token Measurement Methodology

**Task ID:** w1-spawn-cost-measurement-70pct  
**Investigation Label:** formula-calibration-measurement-2026-04-28  
**Date:** 2026-04-28  
**Context Fill at Spawn:** 70%  
**Agents:** 4 haiku (parallel W1 LIFTOFF)

---

## Executive Summary

This document establishes the measurement framework for W1 LIFTOFF spawn costs. We predict **20,000 tokens** for a 4-agent parallel spawn using "light bundle" composition (minimal context, maximum parallelism). The measurement compares actual token consumption against theory to calibrate the spawn cost formula and validate cache efficiency.

---

## Theoretical Token Budget

### Light Bundle Composition

W1 (LIFTOFF) bundles prioritize **speed + width** over depth. Each agent receives:

| Component | Tokens | Purpose |
|-----------|--------|---------|
| HONEY.md (global) | 1,000 | Universal principles, script references, equilibrium rules |
| NECTAR.md (tail-30 lines) | 500 | Recent HIGH findings, emergent patterns (last session) |
| Pollen (session) | 1,000 | Raw agent observations, MEM blocks from this turn |
| Task Instructions | 1,000 | Specific goal, success criteria, investigation_label |
| Injection Overhead | 1,500 | Bundle rendering, format validation, compass edge injection |
| **Total per Agent** | **5,000** | |
| **4 Agents (W1)** | **20,000** | Parallel spawn (no sequential wait overhead) |

### Token Allocation Rationale

- **HONEY (1K):** Crystallized principles—agents must understand f(0), stigmergy, compass navigation
- **NECTAR (500):** Only tail-30 lines (not full log) to maintain lightness while anchoring recent context
- **Pollen (1K):** Live session observations (e.g., "last 3 tasks found 5 compass S edges")
- **Task (1K):** Goal, rubric, investigation_label, compass bearing expectation
- **Injection (1.5K):** Bundle rendering logic, prescan gating, manifest schema validation

**NOT included in light bundle:**
- Full manifest history (saves ~2-3K)
- Artifact details (saves ~1K)
- Deep forensic analysis (saves ~1K)
- These are included in W2+ (DEEPEN/EXTEND phases)

---

## Measurement Phases

### Phase 1: Baseline Capture

**Objective:** Establish pre-spawn metrics and validate measurement readiness.

**Steps:**
1. Verify 4 bundles exist in `forensics/2026-04-28/bundles/`
2. Record bundle sizes and composition
3. Analyze 4 recent manifests (quality_score, belief_index, compass edges)
4. Document theoretical formula and token allocation

**Expected Output:**
- Baseline snapshot: bundles_ready=8, selected=4
- Manifest sample: avg quality=0.85, avg belief=0.86
- Formula documented with all components

**Status:** ✅ Complete
- Baseline captured: `160000Z_artifact_w1-measurement-baseline_data-analyst_001.json`
- Manifests analyzed: 4 samples with quality range [0.82–0.88]
- Framework documented: 5,000 tokens/agent theory

---

### Phase 2: W1 Spawn Execution

**Objective:** Trigger 4 haiku agents in parallel and record spawn metadata.

**Steps:**
1. Call `0x_mission_graph.py --spawn --wave 1 --max-parallel 4 --model haiku`
2. Pass 4 bundles selected from Phase 1 baseline
3. Record spawn timestamp, agent_run_ids, queue state
4. Allow agents to execute without polling (async discipline)

**Expected Output:**
- Spawn config: wave=W1, agents=4, model=haiku, bundle_paths=[...]
- Agent RUN IDs: each agent receives unique run_id
- Queue latency: time from trigger to first manifest return

**Status:** 🔄 Ready (awaiting user trigger)

**Command Template:**
```bash
python3 .claude/scripts/0x_mission_graph.py --spawn \
  --wave 1 \
  --max-parallel 4 \
  --model haiku \
  --investigation-label "formula-calibration-measurement-2026-04-28" \
  --run-inline true
```

---

### Phase 3: Manifest Collection & Verification

**Objective:** Collect 4 new manifests and verify output quality.

**Steps:**
1. Poll `forensics/2026-04-28/manifests/` for new manifests post-spawn
2. Extract 4 manifests with matching task_ids:
   - `coc-script-mapping-w2`
   - `manifest-schema-wiring-critical`
   - `wormbucket-ci-discovery`
   - `hash-tracker-audit`
3. Verify quality_score >= 0.70 and belief_index >= 0.70 on all 4
4. Extract compass_edge (expect "S" for proceed)

**Expected Output:**
- Manifest count: 4
- Quality scores: all >= 0.70
- Belief indices: all >= 0.70
- Compass edges: all "S" (proceeding)

**Status:** 🔄 Pending spawn completion

---

### Phase 4: Usage Metrics Capture

**Objective:** Measure actual token consumption and calculate delta.

**Steps:**
1. Record post-spawn context usage (if available via API/CLI)
2. Calculate: actual_tokens = post_usage - pre_usage
3. Note: If exact usage unavailable, estimate from bundle sizes + agent output length

**Expected Output:**
- `actual_tokens`: measured consumption (target ~20,000)
- `pre_usage`: baseline snapshot
- `post_usage`: final snapshot
- `delta`: post - pre

**Status:** 🔄 Pending post-spawn measurement

---

### Phase 5: Analysis & Formula Calibration

**Objective:** Compare actual vs. predicted and validate formula accuracy.

**Steps:**
1. Load predicted value: 20,000 tokens (theory)
2. Compare to actual value from Phase 4
3. Calculate gap: (actual - 20,000) / 20,000 × 100%
4. Assess cache efficiency: 1 - |gap%| (perfect = 0%)
5. Document findings and recommendations

**Expected Output:**
```json
{
  "theory_predicted": 20000,
  "actual_consumed": 19500,
  "gap_tokens": -500,
  "gap_percent": -2.5,
  "cache_efficiency": 97.5,
  "assessment": "Formula accurate within 3%; cache hit positive"
}
```

**Status:** 🔄 Pending Phases 2–4 completion

---

## Success Criteria (Measurement Gating)

| Criterion | Gate | Status |
|-----------|------|--------|
| **All 4 agents spawn** | Quality | 🔄 Pending |
| **Quality score >= 0.70** | Quality | 🔄 Pending |
| **Belief index >= 0.70** | Quality | 🔄 Pending |
| **Compass edge = S** | Routing | 🔄 Pending |
| **Usage delta measured** | Measurement | 🔄 Pending |
| **Gap <= 10%** | Formula | 🔄 Pending |

---

## Compass Navigation (Next Bearing)

**Current Bearing:** S (Proceed)

The measurement framework is validated and ready. After W1 spawn completes and manifests return:
- **S bearing:** All criteria met → proceed to formula calibration analysis
- **N bearing:** Quality failure → investigate agent issues, capture enhanced pollen
- **E bearing:** Positive outlier (gap < -5%) → measure cache efficiency gains
- **W bearing:** Major divergence (gap > 15%) → reframe bundle composition

---

## Related Artifacts

- **Measurement Bundle:** `forensics/2026-04-28/bundles/160000Z_bundle_w1-spawn-cost-measurement_data-analyst_001.json`
- **Baseline Snapshot:** `forensics/2026-04-28/artifacts/160000Z_artifact_w1-measurement-baseline_data-analyst_001.json`
- **This Document:** `160001Z_artifact_w1-token-measurement-methodology_data-analyst_001.md`

---

## References

- **f(0) Principles:** CLAUDE.md § Rocket Physics — Piston Wave Operational Frame
- **Bundle Composition:** CLAUDE.md § Programmatic Composition & Bundle Emission
- **Light Bundle Definition:** CLAUDE.md § W1 (LIFTOFF) — Max Burn, Max Parallelism
- **Manifest Structure:** forensics/2026-04-28/manifests/ (recent examples)

---

## Next Steps (After W1 Execution)

1. **Phase 2:** Trigger spawn via `/run` or manual CLI
2. **Phase 3:** Collect manifests (verify in `forensics/2026-04-28/manifests/`)
3. **Phase 4:** Capture usage delta
4. **Phase 5:** Generate calibration report
5. **Handoff:** Summarize findings in NECTAR for next investigation

---

**Measurement Status:** Framework deployed. Ready for W1 LIFTOFF execution.

**Expected Compass Bearing After Spawn:** S (Proceed to analysis phase)
