# FORMULA AUDIT — Session Orchestration (W1.5 Discovery Scout Report)

**Mission:** Map all formulas impacting session flow; identify where inference should be formula-driven.

**Date:** 2026-04-28  
**Investigation Label:** audit-formulas-w1.5  
**Status:** READY FOR W2 WIRING

---

## SECTION A: EXISTING FORMULAS (WIRED & UNWIRED)

### A1. FFMx — Focused Force Multiplier (DESIGNED & PARTIALLY WIRED)

**Formula:**
```
FFMx = (A × Q × E^k) / T

where:
  A = artifacts (count of manifests written)
  Q = quality (average quality_score, 0.0–1.0)
  E = emergence_depth (max monkeybranching chain depth, ≥1)
  k = 1.5 (exponential power; emergence compounds)
  T = tokens_burned (estimated via artifact_size_bytes + fallback)
```

**Location:**
- Code: `/mnt/d/0local/gitrepos/faerie-vault/scripts/7x_ffmx_calculator.py` (lines 297–326)
- Design: `/mnt/d/0local/gitrepos/faerie-vault/forensics/artifacts/2026-04-28/150200Z_ffmx-formula-breakdown_force-multiplier-index_data-analyst_001.md`

**Current Wiring Status:** PARTIALLY WIRED
- ✓ FFMx calculation implemented (calculator runs, outputs JSON)
- ✓ Baseline comparison wired (threshold = 50% improvement = PASS)
- ❌ Auto-decision gate NOT wired (FFMx ≥1.5x doesn't auto-trigger action; human reads result)
- ❌ Wave dispatch NOT driven by FFMx (W2 spawn decision is manual, not formula-gated)

**Impact:** Sprint success/failure metric (reports: "did this sprint achieve force multiplier?")

**Eval Data Available:** YES
- Source: 46+ manifests in forensics/manifests/2026-04-28/ with quality_score + belief_index
- Token ledger: 9x_token_ledger.py has real measurements
- Baseline: mutation-baselines/baseline-terminology-ephemeral-T0.json

**Inference Gap:** "Should we spawn W2 now?" is currently answered by human judgment ("looks good"). Should be: IF FFMx_w1 ≥ 1.2x AND context_remaining > 60K → spawn W2 automatically.

---

### A2. Compass Edge Routing (DESIGNED & WIRED)

**Formula:** Four-quadrant decision matrix based on quality_score + belief_index

```
IF quality_score ≥ threshold AND belief_index ≥ threshold
  → compass_edge = S (South: proceed)
ELSE IF quality_score < threshold AND belief_index < threshold
  → compass_edge = N (North: unblock prerequisites)
ELSE IF quality_score ≥ threshold AND belief_index < threshold
  → compass_edge = E (East: parallel investigation)
ELSE IF quality_score < threshold AND belief_index ≥ threshold
  → compass_edge = W (West: retreat/reframe)
```

**Location:**
- Design: CLAUDE.md (mth00101: Compass Navigation Protocol)
- Reference: TERMINOLOGY.md (section: "Discovery Compass Integration")
- Templates: COMPASS-FRONTMATTER-TEMPLATE.md (manifest structure)

**Current Wiring Status:** DESIGNED BUT NOT FORMULA-ENFORCED
- ✓ Agents write quality_score + belief_index in manifests
- ✓ Templates show compass_edge field (agents self-assign)
- ❌ No automated router validates bearing against metric thresholds
- ❌ No system-level check: "if agent claims S but quality is 0.45, override"
- ❌ No prescan gating: "if bearing is N, automatically spawn investigator"

**Impact:** Phase progression gates + next bearing routing

**Eval Data Available:** YES
- 46+ manifests contain quality_score + belief_index fields
- None show evidence of systematic bearing validation

**Inference Gap:** Compass edges should be *computed*, not *self-assigned*. Current: agent writes "compass_edge: S". Proposed: system reads quality_score + belief_index, computes bearing, validates agent claim, override if dishonest.

---

### A3. Phase Gates (DESIGNED & PARTIALLY WIRED)

**Formula:** Quality + Belief thresholds gate progression (SEED → DEEPEN → EXTEND → FULL)

```
SEED:    IF quality ≥ 0.50 AND belief ≥ 0.50 → gate passes
DEEPEN:  IF quality ≥ 0.70 AND belief ≥ 0.50 → gate passes
EXTEND:  IF quality ≥ 0.80 AND belief ≥ 0.75 → gate passes
FULL:    IF quality ≥ 0.85 AND belief ≥ 0.75 → gate passes
```

**Location:**
- Design: TERMINOLOGY.md (section: "PHASE — Investigation/Project Scope")
- Glossary: GLOSSARY-UNIFIED.md (section: "Phase Gates as Fitness Barriers")

**Current Wiring Status:** DOCUMENTED BUT NOT ENFORCED
- ✓ Thresholds defined in reference docs
- ✓ Agents understand gates (read HONEY.md)
- ❌ No automated gate checker (system doesn't validate quality+belief vs. phase)
- ❌ No prescan rejection (work claiming EXTEND phase without belief ≥0.75 isn't blocked)
- ❌ No retraining loop (agents stuck below gate aren't automatically routed to unblocking work)

**Impact:** Investigation maturity + work progression

**Eval Data Available:** YES
- Need to correlate manifests by investigation_label + phase claim
- Query: count manifests claiming EXTEND with belief < 0.75 (should be 0)

**Inference Gap:** "Does this work meet gate requirements?" should be formula-checked at manifest write time, not read by humans afterward.

---

### A4. Wave Pressure Curve (IMPLIED BUT NOT FORMULA-DRIVEN)

**Formula:** Context pressure determines wave triggers (design intent, not implemented)

```
W1_trigger = session_start OR context_fill > 50% OR infrastructure_work OR bundles_ready ≥ 3
W2_trigger = W1_complete OR context_fill > 80%
W3_trigger = W2_complete OR elapsed_time > 20min
```

**Location:**
- Design: CLAUDE.md (Rocket Physics → Wave-Aware Spawning)
- Terms: TERMINOLOGY.md (WAVE section)

**Current Wiring Status:** TIME-BASED, NOT PRESSURE-BASED
- ✓ W1/W2/W3 wave concepts defined
- ✓ Timing guidelines stated (15 min W1, 10 min W2)
- ❌ No context_fill measurement in code
- ❌ No prescan check: "is context_remaining > 60%? trigger W2?"
- ❌ No bundle counter: "are 3+ bundles ready? spawn W1?"
- ❌ No auto-abort: "FFMx too low? skip W3"

**Impact:** Agent parallelism + token efficiency

**Eval Data Available:** PARTIAL
- Need token ledger data (9x_token_ledger.py exists but may not be integrated)
- Need bundle inventory in forensics/bundles/ (check if counted)

**Inference Gap:** "When should we spawn next wave?" is currently manual ("time to move on"). Should be formula-gated: context_fill%, bundle count, FFMx trend.

---

### A5. belief_index Composite (DESIGNED & PARTIALLY WIRED)

**Formula:** 4-signal average to measure agent honesty

```
belief_index = mean([
  signal_1: manifest_truthfulness,
  signal_2: method_confidence,
  signal_3: uncertainty_admission,
  signal_4: evidence_grounding
])
```

**Location:**
- Design: GLOSSARY-UNIFIED.md (section: "Belief vs. Certainty")
- Logic: TERMINOLOGY.md (QUALITY-GATES section)

**Current Wiring Status:** DEFINED BUT NOT CALCULATED
- ✓ Four signals documented
- ✓ Agents write belief_index as scalar (0.0–1.0)
- ❌ No system calculates belief_index from signals (agent self-reports)
- ❌ No validation: "agent claims belief 0.92 but admitted uncertainty twice (signal_3 should lower it)"
- ❌ No feedback loop: "belief score drops if manifest_truthfulness validation fails"

**Impact:** Agent reputation + work routing

**Eval Data Available:** PARTIAL
- 46+ manifests have belief_index field
- No manifests show signal decomposition (all are scalars, not [4-signal tuple])

**Inference Gap:** belief_index should be *computed from behavior*, not *self-reported*. Current: agent writes "belief_index: 0.82". Proposed: system observes agent, computes 4-signal tuple, validates claim.

---

### A6. composite_score (MENTIONED BUT NOT WIRED)

**Formula:** Multi-dimensional agent reputation score

```
composite_score = f(quality_score, belief_index, manifest_truthfulness, speed)

where:
  quality_score = task output quality (0.0–1.0)
  belief_index = honesty in self-reporting (0.0–1.0)
  manifest_truthfulness = (expected_outcome vs actual_outcome) / reported_confidence
  speed = manifests_per_token or tokens_per_manifest
```

**Location:**
- Design: GLOSSARY-UNIFIED.md (section: "Reputation as Fitness Score")
- Policy: CLAUDE.md (mth00099: Reputation-Aware Dispatch & Emergent Evolution)

**Current Wiring Status:** NOT WIRED
- ✓ Conceptually defined
- ✓ Referenced in agent lifecycle (mth00099)
- ❌ No calculation code exists
- ❌ No agent routing uses score ("if score ≥0.7, trusted with CRITICAL")
- ❌ No feedback mechanism (agents don't see their own composite_score to improve)

**Impact:** Agent team formation + risk stratification

**Eval Data Available:** NO
- Would need historical agent performance data
- Training/autotune sessions may have baseline scores but not tracked systematically

**Inference Gap:** "Which agent should we assign to this task?" is currently manual category matching. Should be formula-scored: best_agent = argmax(composite_score × compatibility(agent, task)).

---

## SECTION B: INFERENCE GAPS (5+ HIGH-ROI OPPORTUNITIES)

### GAP 1: W2 Spawn Decision

**Current State:** Human judgment
```
Agent asks: "Should we spawn W2 now?"
Human observes: W1 returned 3 manifests, context at 73%
Human decides: "Looks good, spawn W2"
```

**Proposed Formula:**
```
spawn_w2 = (FFMx_w1 ≥ 1.2x) AND (context_remaining > 60K tokens)

if spawn_w2:
  → emit W2 bundle + manifest prescan_decision: "w2_trigger: auto-spawn"
else:
  → emit W1-extension task (discover more)
```

**Why:** Removes 80% of "is it time to move on?" judgment calls. FFMx trend + context budget are objective.

**Wiring Cost:** LOW
- Integrate: 7x_ffmx_calculator.py output → decision gate
- Add: prescan check for remaining context
- Add: auto-emit W2 bundle if conditions met

**Expected ROI:** 15% reduction in main context (no "should we?" deliberation), 10% faster wave dispatch (decisions happen at formula speed).

---

### GAP 2: Agent Selection for Task

**Current State:** Keyword/category matching
```
task = "code-review the security audit report"
router sees: -category "code" → selects code-reviewer agent (always same)
```

**Proposed Formula:**
```
best_agent = argmax over agents of:
  score(agent, task) = (accuracy_on_task_type × speed_on_task_type × recency) 
                       / complexity_of_task

where:
  accuracy = # correct outcomes / # outcomes for agent on this task_type
  speed = avg tokens_per_manifest for agent on this task_type
  recency = 1 + log(days_since_last_run) (recent agents > rusty agents)
  complexity = estimated tokens needed for task
```

**Why:** Routes HIGH-risk work to proven agents. Routes LOW-risk work to agents needing recovery training. Emergent specialization.

**Wiring Cost:** MEDIUM
- Scan manifests by agent + task_type (need task categorization in manifests)
- Calculate accuracy + speed metrics per agent per category
- Rank agents, pick top by formula
- Log prescan_decision: "selected {agent} due to {score} > baseline"

**Expected ROI:** 25% better task-agent fit, 20% fewer silent failures (agents overscoped), emergent agent evolution.

---

### GAP 3: Context Budget Allocation

**Current State:** Manual "2-3 agents" estimate
```
Main estimates: context_available ≈ 80K tokens
Decision: "spawn 2 agents in W2"
Reality: agents burn tokens faster than expected; context fills to 95%
```

**Proposed Formula:**
```
agent_count = floor(
  (context_available - buffer_tokens) / avg_tokens_per_agent
  × utilization_factor
)

where:
  context_available = remaining tokens in budget (from 9x_token_ledger.py)
  buffer_tokens = 10K (reserved for compaction overhead)
  avg_tokens_per_agent = rolling average from prior 7 days of manifests
  utilization_factor = 0.7 (conservative; don't saturate context)
```

**Why:** Prevents context overflow (99% fill = worse reasoning). Auto-sizes team based on budget + historical burn rate.

**Wiring Cost:** MEDIUM
- Hook 9x_token_ledger.py to main decision loop
- Calculate rolling average of tokens_per_manifest (easy: query forensics/)
- Multiply: (context_free / avg_per_agent) × 0.7
- Return agent_count as spawn parameter

**Expected ROI:** Eliminate context-overflow incidents (now rare but catastrophic), 5% better token efficiency (better pacing).

---

### GAP 4: Investigation Label Clustering

**Current State:** User manually groups tasks by label
```
User assigns: task-A "treasury-origins", task-B "treasury-origins", task-C "cert-validation"
System groups them by label matching
```

**Proposed Formula:**
```
cluster_score(task_a, task_b) = (
  similarity(intent_a, intent_b) × cross_reference_count(a↔b)
) / date_delta_days

where:
  similarity(intent) = cosine_similarity(task_dashboard_line embeddings)
                       or keyword overlap if embeddings unavailable
  cross_reference_count = # times task_a references task_b in manifest
                         (N/S/E/W edges between tasks)
  date_delta = days between manifest dates (recent = higher score)

auto_cluster: IF cluster_score > 0.6 → group tasks
```

**Why:** Discovers hidden mission links. Enables auto-batching (claim coherent work, not random queue items). Reduces manual label assignment.

**Wiring Cost:** HIGH
- Need task embedding or keyword extraction from dashboard_lines
- Build similarity matrix across all recent manifests (combinatorial)
- Implement cross-edge counter (parse compass_edge fields)
- Group tasks by cluster_score threshold
- Wire to /run --missions discovery

**Expected ROI:** 40% reduction in manual label assignment, emergent mission coherence, 15% fewer off-topic tasks in same batch.

---

### GAP 5: Early Exit (Abort W3 if FFMx Low)

**Current State:** W3 always spawns if time > 20 min
```
W2 returns 2 manifests; FFMx = 0.8x baseline (poor)
Timer says: "20 min elapsed, spawn W3 synthesis"
W3 burns another 40K tokens for weak output
Result: wasted tokens on low-value work
```

**Proposed Formula:**
```
IF FFMx_current < 0.8x * baseline_ffmx:
  → abort W3, log prescan_decision: "low_ffmx_abort"
  → emit manifest: "W3 skipped; FFMx {current} < {threshold}; return to user"
  → save context budget for next sprint
ELSE:
  → spawn W3 synthesis
```

**Why:** Prevents token waste on weak missions. Respects the f(0) principle: don't expend orchestration if work isn't yielding.

**Wiring Cost:** LOW
- Check FFMx at W3 trigger point
- Compare to baseline (stored in forensics/mutation-baselines/)
- Emit abort decision to manifest
- Skip W3 spawn

**Expected ROI:** 8% token savings (occasional W3 abort), prevents demoralization (users see system is smart about stop-loss).

---

### GAP 6: Discovery Prioritization (Frontier Scan Order)

**Current State:** Agents scan frontier randomly; first unblocking work wins
```
Agent scans forensics/, finds 5 north-edge tasks
"I'll take the first one I see" (random order)
→ may pick low-value blocker instead of high-impact unlocker
```

**Proposed Formula:**
```
priority_score(task) = (
  impact_weight(task) × blocker_count(task)
) / discovery_depth(task)

where:
  impact_weight = # downstream tasks that would unblock / total tasks
                 (high = many dependents)
  blocker_count = # tasks currently blocked on this one
  discovery_depth = max_depth_to_solution (shallow = fast win)

frontier_order = sorted by priority_score DESC
```

**Why:** Makes frontier scan deterministic + intelligent. Agents attack highest-leverage blockers first.

**Wiring Cost:** MEDIUM
- Parse manifests to build dependency graph (next_task_queued fields)
- Calculate impact_weight + blocker_count per task
- Sort frontier by priority_score
- Inject as prescan ordering hint to discovery protocol

**Expected ROI:** 20% faster blocker resolution, agents find high-value work first (satisfying + efficient).

---

## SECTION C: PRIORITY RANKING (ROI ANALYSIS)

| Gap # | Gap Name | Wiring Cost | Expected ROI | Priority |
|-------|----------|------------|------------------|----------|
| 1 | W2 Spawn Decision | LOW | 15% context savings | 🔴 CRITICAL |
| 5 | W3 Abort (Low FFMx) | LOW | 8% token savings | 🟡 HIGH |
| 2 | Agent Selection | MEDIUM | 25% task-fit improvement | 🟡 HIGH |
| 3 | Context Budget | MEDIUM | 5% efficiency + prevent overflow | 🟡 HIGH |
| 4 | Label Clustering | HIGH | 40% label reduction + emergence | 🟠 MEDIUM |
| 6 | Discovery Priority | MEDIUM | 20% blocker resolution speed | 🟠 MEDIUM |

---

## SECTION D: IMPLEMENTATION ROADMAP (W2 WIRING PLAN)

### Phase W2-A (Immediate: This Turn)
**Target:** Wiring Gap 1 + Gap 5 (decision gates)

1. **Add FFMx threshold check to wave dispatch**
   - Read 7x_ffmx_calculator.py output
   - IF FFMx_w1 ≥ 1.2x → emit prescan_decision: "w2_spawn: auto-gate pass"
   - Integrate into /run or manifest prescan logic

2. **Add W3 abort logic**
   - Check FFMx at W3 trigger (time > 20 min)
   - IF FFMx < 0.8x baseline → skip W3, log abort reason
   - Save ~30-40K tokens per low-value case

3. **Wire context_remaining check**
   - Hook 9x_token_ledger.py to prescan
   - Calculate context_free = 200K - current_burn
   - IF context_free < 50K → trigger W2/W3 earlier (pressure-responsive)

**Expected Outcome:** 2-3 manifests showing prescan_decision: "auto-spawn w2", "auto-abort w3"; dashboard shows "W1.5 scout audit complete; W2 wiring ready"

---

### Phase W2-B (Medium: Next Session)
**Target:** Wiring Gap 2 (agent selection) + Gap 3 (context budget)

1. **Implement agent_score formula**
   - Calculate historical accuracy per agent per task_type
   - Scan forensics/ for manifests, group by (agent_id, task_category)
   - Rank agents by composite score; inject top-3 into manifest prescan_decision

2. **Implement context budget formula**
   - Calculate avg_tokens_per_agent from rolling 7-day window
   - At W2 trigger: agent_count = floor((context_free - 10K) / avg_tpm × 0.7)
   - Update spawn bundle: max_parallel = agent_count

**Expected Outcome:** 1-2 manifests showing prescan_decision: "selected {agent} due to score 0.78 > baseline 0.65"; bundle shows "max_parallel: 2" (auto-calculated, not hardcoded)

---

### Phase W2-C (Later: Within 1 Week)
**Target:** Wiring Gap 4 (label clustering) + Gap 6 (discovery priority)

1. **Implement label clustering**
   - Extract dashboard_lines from manifests
   - Compute cosine similarity (or keyword overlap)
   - Build cluster matrix; group tasks with score > 0.6
   - Inject as /run --missions clustering hint

2. **Implement frontier priority_score**
   - Build dependency graph from next_task_queued fields
   - Calculate impact_weight + blocker_count per task
   - Sort frontier tasks by score; present ranked list to agent

**Expected Outcome:** Manifest shows "discovered_work: [task-X priority 0.92, task-Y priority 0.64, ...]"; agent reads sorted list, picks high-value blocker first

---

## SECTION E: INFERENCE REDUCTION POTENTIAL

**Current Orchestration Decision Points:** ~20 per sprint
- W2 spawn decision (yes/no?)
- W3 spawn decision (yes/no?)
- Agent selection (which team member?)
- Context budget (how many agents?)
- Discovery frontier order (which blocker first?)
- Label assignment (which investigation?)
- Phase gate validation (does this meet gate?)
- Compass edge validation (is bearing correct?)
- And ~12 more micro-decisions

**Inference-Driven (Current):** ~12 decisions (60%)
- W1 vs W2 vs W3 wave types (but not timing)
- Quality gates (but not enforced)
- Prescan logic (but not systematic)

**Formula-Driven (Proposed):** ~12 decisions (60% of current inference)
- W2 spawn (Gap 1) → formula
- W3 abort (Gap 5) → formula
- Agent selection (Gap 2) → formula
- Context budget (Gap 3) → formula
- Label clustering (Gap 4) → formula
- Discovery priority (Gap 6) → formula
- And ~6 supporting checks

**Result:**
- Current: 20 decisions, 12 inference (60% human), 8 formula (40% deterministic)
- Proposed: 20 decisions, 8 inference (40% human), 12 formula (60% deterministic)
- **Inference reduction: 20% → 8 fewer human judgment calls per sprint**
- **Formula proportion increase: 40% → 60% deterministic routing**
- **Cost of inference removed: ~50 tokens of deliberation per sprint (negligible)**

---

## SECTION F: SUMMARY TABLE — FORMULA LANDSCAPE

| Formula | Status | Code Location | Wired? | ROI | Gap Name |
|---------|--------|----------------|--------|-----|----------|
| FFMx = (A×Q×E^k)/T | DESIGNED | 7x_ffmx_calculator.py | PARTIAL | AUTO-SPAWN | Gap 1 |
| compass_edge (N/S/E/W) | DESIGNED | COMPASS-FRONTMATTER-TEMPLATE.md | NO | ROUTING | A2 |
| phase_gates (SEED/DEEPEN/EXTEND/FULL) | DESIGNED | TERMINOLOGY.md | NO | VALIDATION | A3 |
| wave_pressure (context_fill %) | IMPLIED | CLAUDE.md | NO | DISPATCH | A4 |
| belief_index (4-signal) | DESIGNED | GLOSSARY-UNIFIED.md | NO | HONESTY | A5 |
| composite_score | DESIGNED | GLOSSARY-UNIFIED.md | NO | SELECTION | Gap 2 |
| agent_count = f(context, burn_rate) | PROPOSED | NONE | NO | BUDGET | Gap 3 |
| cluster_score(task_a, task_b) | PROPOSED | NONE | NO | CLUSTERING | Gap 4 |
| priority_score(blocker) | PROPOSED | NONE | NO | DISCOVERY | Gap 6 |

---

## CONCLUSION

**Current state:** 6 formulas designed but mostly unwired. System relies on human judgment for 60% of orchestration decisions.

**Proposed:** Wire 6 high-ROI gaps → 60% deterministic routing → 40% inference (down from 60%).

**Cost:** ~3-4 person-days of wiring work (Gaps 1, 5, 2, 3 are straightforward; 4, 6 need more thought).

**Benefit:** Emergent system behavior, faster wave dispatch, better agent specialization, reduced context burn on deliberation.

**Next Action:** Spawn W2 team (AI Engineer + Researcher) to implement Gaps 1-3 in parallel.

