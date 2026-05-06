# W1 LIFTOFF Measurement — Execution Checklist

**Task ID:** w1-spawn-cost-measurement-70pct  
**Investigation:** formula-calibration-measurement-2026-04-28  
**Quick Reference:** This checklist guides execution. Full details in sister artifacts.

---

## Pre-Execution Checklist

- [ ] **Bundle Template Created**
  - Location: `forensics/2026-04-28/bundles/160000Z_bundle_w1-spawn-cost-measurement_data-analyst_001.json`
  - Status: ✅ Ready

- [ ] **Manifest Plan Written**
  - Location: `forensics/2026-04-28/manifests/160000Z_manifest_w1-spawn-cost-measurement_data-analyst_001.json`
  - Status: ✅ Ready

- [ ] **Baseline Snapshot Captured**
  - Location: `forensics/2026-04-28/artifacts/160000Z_artifact_w1-measurement-baseline_data-analyst_001.json`
  - Includes: Bundle inventory, manifest sample analysis, theory formula
  - Status: ✅ Ready

- [ ] **Measurement Methodology Documented**
  - Location: `160001Z_artifact_w1-token-measurement-methodology_data-analyst_001.md`
  - Covers: 5 phases, success criteria, data sources
  - Status: ✅ Ready

- [ ] **Formula Calibration Theory**
  - Location: `160002Z_artifact_w1-spawn-formula-calibration_data-analyst_001.md`
  - Covers: Token budget, cache efficiency, scaling, success metrics
  - Status: ✅ Ready

- [ ] **Summary & Decision Logic**
  - Location: `160003Z_artifact_w1-measurement-summary_data-analyst_001.md`
  - Covers: Executive summary, next steps, compass bearings
  - Status: ✅ Ready

---

## Phase 2: Spawn Execution

### Step 1: Verify Prerequisites

```bash
# Confirm bundles exist
ls -lh /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/bundles/ | wc -l

# Expected: >= 8 bundles available
# Confirmed: ✅
```

### Step 2: Trigger W1 Spawn

**Option A: Via Script (Recommended)**

```bash
cd /mnt/d/0local/gitrepos/faerie-vault

python3 .claude/scripts/0x_mission_graph.py --spawn \
  --wave 1 \
  --max-parallel 4 \
  --model haiku \
  --investigation-label "formula-calibration-measurement-2026-04-28" \
  --run-inline true
```

**Option B: Via /run Skill**

```bash
/run formula-calibration-measurement-2026-04-28 --wave 1 --agents 4
```

### Step 3: Record Spawn Metadata

- [ ] Spawn timestamp: __________ UTC
- [ ] Agent 1 run_id: __________
- [ ] Agent 2 run_id: __________
- [ ] Agent 3 run_id: __________
- [ ] Agent 4 run_id: __________
- [ ] Spawn config logged: [ ] Yes [ ] No

---

## Phase 3: Manifest Collection

### Step 1: Wait for Agents (No Polling)

Allow agents 5–10 minutes to complete. Do NOT poll manifests mid-run.

- [ ] Async wait complete
- [ ] Ready to collect manifests

### Step 2: Verify All 4 Manifests Returned

```bash
# List new manifests (should be 4, with expected task_ids)
ls -lh /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/ | tail -10

# Expected task_ids:
#  - coc-script-mapping-w2
#  - manifest-schema-wiring-critical
#  - wormbucket-ci-discovery
#  - hash-tracker-audit

# Or: Count manifests from today with our investigation_label
grep -l "formula-calibration-measurement-2026-04-28" \
  /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/* | wc -l

# Expected: >= 4
```

- [ ] All 4 manifests present
- [ ] Manifest count: ____

### Step 3: Extract Metrics from Each Manifest

```bash
# For each manifest, extract key metrics
for mf in /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/*w2*.json; do
  echo "=== $(basename $mf) ==="
  jq '{task_id, quality_score, belief_index, compass_edge}' "$mf"
done
```

### Step 4: Verify Quality & Belief Gates

Copy results below:

| Task ID | Quality Score | Belief Index | Compass Edge | Pass? |
|---------|---------------|--------------|--------------|-------|
| coc-script-mapping | _______ | _______ | _____ | [ ] |
| manifest-schema-wiring | _______ | _______ | _____ | [ ] |
| wormbucket-ci-discovery | _______ | _______ | _____ | [ ] |
| hash-tracker-audit | _______ | _______ | _____ | [ ] |

**Gate Checks:**
- [ ] All quality_scores >= 0.70
- [ ] All belief_indexes >= 0.70
- [ ] >= 3/4 compass_edges = "S"

---

## Phase 4: Token Measurement

### Step 1: Capture Post-Spawn Usage (if available)

```bash
# If your environment exposes token usage:
# Export usage snapshot
echo "Pre-spawn: _____ tokens"
echo "Post-spawn: _____ tokens"
echo "Delta: _____ tokens"
```

- [ ] Pre-spawn tokens: __________
- [ ] Post-spawn tokens: __________
- [ ] Delta (actual): __________

### Step 2: Compare to Theory

```
Theory Predicted: 20,000 tokens
Actual Consumed:  __________ tokens
Gap:              __________ tokens
Gap %:            __________% (positive = higher, negative = lower)
Cache Efficiency: __________%
```

- [ ] Calculation complete

### Step 3: Assess Against Success Criteria

- [ ] Gap <= 10%? (Formula within tolerance)
- [ ] Gap >= -35%? (Reasonable cache efficiency)
- [ ] Gap >= -60%? (Excellent cache efficiency)
- [ ] Gap > 25%? (⚠️ Flag: Formula needs recalibration)

---

## Phase 5: Analysis & Decision

### Step 1: Classify Outcome

**Option A: ✅ All Gates Pass**
- All 4 manifests present
- Quality >= 0.70, belief >= 0.70
- >= 3/4 compass = "S"
- Gap <= 10%
- **Bearing:** S (Proceed to calibration analysis)

**Option B: 🟡 Quality Degradation**
- Any manifest quality < 0.70
- Any manifest belief < 0.70
- **Bearing:** N (Return to prerequisites, enhance bundle)

**Option C: 🟠 Cache Efficiency Surprise**
- Gap < -35% (better than expected)
- **Bearing:** E (Parallel investigation: characterize cache pattern)

**Option D: 🔴 Formula Significantly Off**
- Gap > 25%
- **Bearing:** W (Retreat: recalibrate bundle composition)

**Selected:** ______ (A / B / C / D)

### Step 2: Create Results Artifact

```bash
cat > /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/artifacts/160005Z_artifact_w1-measurement-results_data-analyst_001.md << 'RESULTS'
# W1 LIFTOFF Measurement Results

**Date:** 2026-04-28  
**Task ID:** w1-spawn-cost-measurement-70pct  

## Metrics Collected

| Metric | Value |
|--------|-------|
| Manifests Returned | ____ |
| Avg Quality Score | ____ |
| Avg Belief Index | ____ |
| Compass Edge S Count | __/4 |
| Actual Tokens Consumed | ____ |
| Theory Predicted | 20,000 |
| Gap | ____ |
| Cache Efficiency | ____% |

## Outcome Classification

- Selected Bearing: ____
- Success Criteria Met: [ ] Yes [ ] No
- Recommended Next Action: ________________________

## Key Findings

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

## Compass Navigation Decision

**Current Bearing:** ____  
**Recommendation:** _________________________________

RESULTS

cat /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/artifacts/160005Z_artifact_w1-measurement-results_data-analyst_001.md
```

- [ ] Results artifact created
- [ ] Path: `160005Z_artifact_w1-measurement-results_data-analyst_001.md`

---

## Post-Execution Handoff

### Step 1: Update NECTAR (Session Memory)

Add to `/mnt/d/0LOCAL/.claude/NECTAR.md`:

```markdown
## W1 LIFTOFF Token Formula Calibration (2026-04-28)

- **Task ID:** w1-spawn-cost-measurement-70pct
- **Theory Predicted:** 20,000 tokens (4 haiku agents)
- **Actual Consumed:** __________ tokens
- **Cache Efficiency:** _________%
- **Outcome:** Bearing = ____
- **Key Finding:** ___________________________________
- **Artifacts:** forensics/2026-04-28/artifacts/160000–160005Z_*

Next investigation: formula-calibration-analysis (W2 phase)
```

- [ ] NECTAR updated

### Step 2: Archive for Future Reference

```bash
# Create recovery bundle for next W1 calibration
tar czf /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/bundles/w1-measurement-archive-2026-04-28.tar.gz \
  /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/artifacts/160000–160005Z_*

echo "Archive created: w1-measurement-archive-2026-04-28.tar.gz"
```

- [ ] Archive created
- [ ] Location: `forensics/2026-04-28/bundles/w1-measurement-archive-2026-04-28.tar.gz`

### Step 3: Next Wave Planning

- [ ] Compass bearing determined (N/S/E/W)
- [ ] Next task queued in manifest
- [ ] Investigation label passed forward
- [ ] Artifacts discoverable via forensic grep

---

## Quick Reference: Key File Paths

```
Setup Phase (Phase 1):
  Bundle:    forensics/2026-04-28/bundles/160000Z_bundle_...json
  Manifest:  forensics/2026-04-28/manifests/160000Z_manifest_...json
  Baseline:  forensics/2026-04-28/artifacts/160000Z_artifact_baseline...json

Documentation:
  Methodology: 160001Z_artifact_w1-token-measurement-methodology...md
  Formula:     160002Z_artifact_w1-spawn-formula-calibration...md
  Summary:     160003Z_artifact_w1-measurement-summary...md
  This Check:  160004Z_artifact_w1-measurement-execution-checklist...md

Results Phase (Phase 5):
  Results:     160005Z_artifact_w1-measurement-results...md
  Archive:     forensics/2026-04-28/bundles/w1-measurement-archive-2026-04-28.tar.gz
```

---

## Status Summary

| Component | Status |
|-----------|--------|
| Bundle Template | ✅ Created |
| Manifest Plan | ✅ Created |
| Baseline Captured | ✅ Complete |
| Methodology Doc | ✅ Complete |
| Formula Calibration | ✅ Complete |
| Summary & Decisions | ✅ Complete |
| This Checklist | ✅ Complete |
| **W1 Spawn Execution** | 🔄 Ready |
| **Manifest Collection** | 🔄 Pending |
| **Token Measurement** | 🔄 Pending |
| **Analysis & Results** | 🔄 Pending |

---

**Overall Status:** Framework deployed. Ready to execute.

**Next Action:** Trigger W1 spawn via script or `/run` command.

**Expected Timeline:** 5–10 min (agents run async)

**Expected Compass Bearing (Post-Execution):** **S (Proceed to calibration analysis)**
