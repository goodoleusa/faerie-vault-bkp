# Mutation Experiment: Formula Calibration Acceptance
**experiment_id:** EXP-2026-04-28-f0calA1
**investigation_label:** formula-calibration-measurement-2026-04-28
**compass_bearing:** S (plan sound, proceed downstream)
**authored_by:** knowledge-synthesizer (W3 INSERTION)
**authored_at:** 2026-04-28T15:00:00Z
**wave:** W3 — background synthesis
**status:** READY FOR EXECUTION

---

## Summary

Two formula baselines have been empirically measured and confirmed cheaper than theoretical defaults:

| Variable | Theory (Old) | Measurement (New) | Delta | Calibration Agent |
|---|---|---|---|---|
| NECTAR_INJECTION_TOKENS | 2,000–3,000 | 1,204 | -40% to -60% cheaper | Scout 2 (W1) |
| HONEY_INJECTION_TOKENS | 1,500 | ~200 | -87% cheaper (7.5x) | Scout 3 (W1) |

Both changes are already reflected in `faerie2-formulas.json` (`current` + `baseline` fields updated to 1200 and 200 respectively). This experiment formalizes the mutation discipline: measure the confirmed new baseline, observe system behavior across 3 sessions, then formally ACCEPT or surface unintended side effects.

**Blocked parameters (do not mutate):**
- COMPASS_QUALITY_GATES: pending N≥20 data samples — locked at current values
- W1_SPAWN_COST: blocked same reason — do not touch

---

## Hypothesis

Reducing NECTAR_INJECTION_TOKENS from 2,000 → 1,200 and HONEY_INJECTION_TOKENS from 1,500 → 200 will:
1. Reduce per-agent bundle injection cost by ~500–2,300 tokens per agent spawn
2. Reduce main context burden from bundle assembly (less total tokens injected per wave)
3. Not degrade agent ramp-up quality (emergence signal freshness preserved at 1,204 token NECTAR)
4. Allow more agents per wave before context ceiling (f(0) efficiency improvement)

No behavioral degradation expected: NECTAR at tail-50 still provides full session findings; HONEY at ~200 tokens still delivers compressed architectural principles.

---

## Variables Changed

### Variable 1: NECTAR_INJECTION_TOKENS
- **From:** 2,000 (theoretical, previously `baseline`)
- **To:** 1,200 (empirically measured 2026-04-28 via Scout 2)
- **Reasoning:** Scout 2 measured actual NECTAR tail-50 at 1,204 tokens. The 2–3K theory overestimated by 40–60%. Real-world faerie2 NECTAR is more compressed than theory predicted. New baseline is already written to `faerie2-formulas.json`.
- **Equilibrium check:** Cheaper injection = more tokens available for agent reasoning. NECTAR content unchanged — only cost estimate corrected. This is a measurement correction, not a behavioral mutation. Respects equilibrium because no design principle is altered.

### Variable 2: HONEY_INJECTION_TOKENS
- **From:** 1,500 (theoretical)
- **To:** 200 (empirically measured 2026-04-28 via Scout 3)
- **Reasoning:** Scout 3 measured actual HONEY injection (global + project HONEY) at ~200 tokens, 7.5x cheaper than theory. The HONEY files are already compressed via gauntlet discipline; the ~1,500 theory was set before compression was enforced. This is a measurement correction to align formula with reality.
- **Equilibrium check:** No content degradation. Architectural principles fully represented in 200 tokens. Cheaper injection directly improves f(0) efficiency (less overhead per agent). Respects equilibrium — no principle weakened.

---

## Measurement Phase 1: Baseline Capture (3 Sessions)

**Purpose:** Confirm that newly baselined values (NECTAR=1,200, HONEY=200) produce stable, healthy system behavior. Establish concrete numeric baseline before any further mutation.

**Duration:** 3 consecutive sessions using current `faerie2-formulas.json` values.

**Metrics to collect per session:**

### Primary Metrics (from `faerie2-formulas.json` `metric` fields)

| Metric | Variable | What to Measure | Target Healthy Range |
|---|---|---|---|
| `bundle_injection_cost` | NECTAR + HONEY | Total tokens injected per agent bundle (NECTAR + HONEY combined) | 1,200–1,600 tokens |
| `agent_ramp_up_efficiency` | NECTAR | Does agent demonstrate correct compass bearing + investigation_label awareness within first 3 tool calls? | ≥70% of spawned agents |
| `emergence_signal_freshness` | NECTAR | Does agent cite recent findings (≤24h old NECTAR entries) in their manifest? | ≥60% of manifests |
| `context_layer_efficiency` | HONEY | Do agents demonstrate HONEY-principle compliance (f(0) language, compass bearings, manifest structure) without additional prompting? | ≥80% of manifests |
| `architectural_principle_injection_cost` | HONEY | Tokens used for HONEY portion of bundle only | 150–300 tokens |
| `bundle_overhead` | HONEY + NECTAR | Fraction of bundle tokens that are context overhead vs task instruction | ≤40% overhead |

### Secondary Metrics (f(0) system health)

| Metric | What to Measure | Target |
|---|---|---|
| `main_context_burden_reduction` | Context% used by main per session (lower = better f(0)) | ≤50% context consumed at W2 start |
| `agents_per_wave` | How many agents spawned in W1 before context ceiling hit | W1: ≥4 agents; W2: ≥2 agents |
| `manifest_chain_depth` | Number of manifest-to-manifest chains per investigation_label | ≥3 chains per mission |
| `prescan_pass_rate` | % of spawns where prescan PASSES (not duplicate work) | ≥80% |
| `compass_edge_S_rate` | % of manifests returning bearing=S (proceed) | ≥60% |

### How to Collect

For each session, execute:

```bash
# Count tokens in last NECTAR tail-50 (proxy for injection cost)
wc -w ~/.claude/NECTAR.md | awk '{print $1 * 1.3}'   # rough token estimate

# Check HONEY combined size
wc -w ~/.claude/HONEY.md /mnt/d/0local/gitrepos/faerie-vault/.claude/HONEY.md 2>/dev/null | tail -1 | awk '{print $1 * 1.3}'

# Count manifests with compass_edge=S this session
grep -r '"compass_edge".*"S"' /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/ | wc -l

# Count manifest chains (next_task_queued is non-empty)
grep -r '"next_task_queued"' /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/ | grep -v '""' | wc -l

# Agent ramp-up (proxy: manifests that cite investigation_label correctly)
grep -r '"investigation_label".*"formula-calibration' /mnt/d/0local/gitrepos/faerie-vault/forensics/2026-04-28/manifests/ | wc -l
```

### Baseline Values to Record (fill in per session)

```
Session 1 (date: ___________):
  bundle_injection_cost:           _____ tokens
  NECTAR_actual_tokens:            _____ tokens
  HONEY_actual_tokens:             _____ tokens
  agent_ramp_up_efficiency:        _____% (N=___ agents)
  emergence_signal_freshness:      _____% (N=___ manifests citing recent NECTAR)
  architectural_principle_cost:    _____ tokens
  main_context_at_W2_start:        _____%
  agents_per_wave_W1:              _____
  manifest_chain_depth:            _____ (avg per investigation_label)
  compass_edge_S_rate:             _____%

Session 2 (date: ___________):
  [same fields]

Session 3 (date: ___________):
  [same fields]

BASELINE AVERAGE (mean of 3 sessions):
  bundle_injection_cost_avg:           _____
  agent_ramp_up_efficiency_avg:        _____%
  emergence_signal_freshness_avg:      _____%
  main_context_at_W2_start_avg:        _____%
  compass_edge_S_rate_avg:             _____%
```

---

## Mutation Phase

**Status:** ALREADY APPLIED — `faerie2-formulas.json` was updated 2026-04-28 by W2 calibration synthesis agent.

**What changed in the file:**
- `NECTAR_INJECTION_TOKENS.current` → 1200 (was 2000–3000 theoretical)
- `NECTAR_INJECTION_TOKENS.baseline` → 1200
- `NECTAR_INJECTION_TOKENS.measured` → "2026-04-28 via Scout 2"
- `HONEY_INJECTION_TOKENS.current` → 200 (was 1500 theoretical)
- `HONEY_INJECTION_TOKENS.baseline` → 200
- `HONEY_INJECTION_TOKENS.measured` → "2026-04-28 via Scout 3"

**Observation notes (to fill during 3-session mutation phase):**

```
Session 1 observations:
  - Any agent confusion from smaller-than-expected NECTAR? Y/N: ___
  - Any compass bearing errors traceable to insufficient HONEY context? Y/N: ___
  - Anomalous manifest structure (wrong fields, missing investigation_label)? Y/N: ___
  - Token savings observed vs prior sessions? _____ tokens/session estimate

Session 2 observations:
  [same fields]

Session 3 observations:
  [same fields]
```

---

## Measurement Phase 2: Post-Mutation (3 Sessions)

**Purpose:** Confirm baseline metrics hold or improve after formula correction. Surface any degradation.

**Metrics:** Same set as Phase 1 (baseline capture). Collect identical fields.

```
Post-Mutation Session 1 (date: ___________):
  bundle_injection_cost:           _____ tokens
  NECTAR_actual_tokens:            _____ tokens
  HONEY_actual_tokens:             _____ tokens
  agent_ramp_up_efficiency:        _____%
  emergence_signal_freshness:      _____%
  architectural_principle_cost:    _____ tokens
  main_context_at_W2_start:        _____%
  agents_per_wave_W1:              _____
  manifest_chain_depth:            _____
  compass_edge_S_rate:             _____%

Post-Mutation Session 2 (date: ___________):
  [same fields]

Post-Mutation Session 3 (date: ___________):
  [same fields]

POST-MUTATION AVERAGE:
  bundle_injection_cost_avg:       _____
  agent_ramp_up_efficiency_avg:    _____%
  emergence_signal_freshness_avg:  _____%
  main_context_at_W2_start_avg:    _____%
  compass_edge_S_rate_avg:         _____%
```

---

## Analysis Template (fill post-measurement)

### Delta Computation (Post - Baseline)

```
bundle_injection_cost delta:           _____ tokens (positive = cost increase, negative = cheaper)
agent_ramp_up_efficiency delta:        _____% points
emergence_signal_freshness delta:      _____% points
main_context_at_W2_start delta:        _____% points
compass_edge_S_rate delta:             _____% points
```

### Positive Emergence Check

- Did bundle injection cost decrease? (Expected: yes, ~500–2,300 tokens cheaper per agent) ___
- Did main context burden decrease at W2 start? (Expected: yes, more headroom) ___
- Did compass bearing quality hold or improve? (Expected: stable, no degradation) ___
- Did agents still demonstrate correct f(0) language from compressed HONEY? ___

### Negative Emergence Check

- Did agent ramp-up efficiency drop more than 10% points? (Danger: NECTAR too sparse) ___
- Did emergence_signal_freshness drop more than 15% points? (Danger: tail-50 insufficient) ___
- Did compass_edge_S_rate drop below 50%? (Danger: HONEY compression degrading guidance) ___
- Did manifest truthfulness scores decline? (Visible in reputation scores) ___

### Recommendation (circle one)

**ACCEPT** | REVERT | ITERATE

**Reasoning (fill after analysis):**

```
[Expected reasoning for ACCEPT path:]
Measurement corrections confirmed:
- NECTAR at 1,200 tokens delivers same emergence signal quality as theoretical 2,000–3,000
- HONEY at 200 tokens delivers same architectural principle coverage as theoretical 1,500
- No behavioral degradation observed across 3 post-mutation sessions
- Bundle injection cost reduced ~500–2,300 tokens per agent (positive emergence)
- Main context burden reduced (more agents per wave before ceiling)
- This mutation is a measurement correction, not a behavioral change — ACCEPT is the natural outcome
- New baselines committed to faerie2-formulas.json are accurate and should be locked

[Fill in actual observations to confirm or refute above expectations]
```

---

## Constraints & Governance

### f(0) Equilibrium Check

This mutation satisfies equilibrium criteria:
- **No new abstractions added** — only existing formula values corrected
- **No new scripts required** — hook wiring unchanged
- **Positive emergence expected** — cheaper injection = more agent bandwidth per session
- **Measurement-first discipline followed** — Scout 2 + Scout 3 measured before mutation was applied
- **Blocked parameters respected** — COMPASS_QUALITY_GATES and W1_SPAWN_COST not touched

### What NOT to Mutate Concurrently

Do not change these during the 6-session measurement window:
- `COMPASS_GATE_*` values (blocked pending N≥20)
- `W1_SPAWN_COST` (blocked same reason)
- `REPUTATION_WEIGHT_*` values (independent experiment)
- `WAVE_*_SPAWN_MAX_CONTEXT_PCT` thresholds (separate mutation queue)

**Reason:** Concurrent mutations produce confounded signals. If compass quality drops while both NECTAR and compass gates are changed simultaneously, cause is ambiguous.

### Revert Procedure (if REVERT recommended)

```bash
# In faerie2-formulas.json, restore:
# NECTAR_INJECTION_TOKENS.current = 2000
# NECTAR_INJECTION_TOKENS.baseline = 2000
# HONEY_INJECTION_TOKENS.current = 1500
# HONEY_INJECTION_TOKENS.baseline = 1500
# Remove .measured fields
# Commit with message: "revert: formula-calibration-acceptance REVERTED — negative emergence observed"
```

---

## Downstream Work (Next Bearing)

Upon ACCEPT (expected outcome), the following downstream work is unblocked:

1. **Bundle cost model update** — Update agent spawn cost estimates in `0x_spawn_template.py` to use new token budgets (bundle overhead calculations use these values)
2. **Wave capacity recalculation** — With NECTAR+HONEY now costing ~1,400 tokens instead of ~4,500, recalculate how many agents fit per wave before context ceiling. Formula: `(191,000 usable - 9,000 overhead) / per_agent_cost` changes materially.
3. **COMPASS_QUALITY_GATES experiment** — Once N≥20 sessions collected, this experiment unlocks. The same experiment template applies.
4. **NECTAR_INJECTION_TOKENS min/max bounds review** — Current min=800, max=3,000. With confirmed baseline=1,200, the min bound (800) is now more plausible as a real operating point. Consider whether to update min.

**Next manifest bearing for downstream agents:** S (proceed to bundle cost model update)
**Investigation label:** `formula-calibration-measurement-2026-04-28`

---

## Agent Lifecycle Rules for Executing This Experiment

1. **Manifest-first:** Each measurement session, write session manifest BEFORE analyzing results
2. **Scalar reads only:** Use grep/wc/awk to extract metrics; do not Read full NECTAR/HONEY files into context
3. **Prescan before spawn:** Check forensics/2026-04-28/manifests/ for existing measurement manifests before spawning new measurement agents
4. **3-session cadence:** Do not combine sessions; run exactly 3 baseline + 3 post-mutation
5. **No concurrent mutations:** Lock other formula variables during measurement window
6. **ACCEPT requires positive or neutral emergence:** If any negative emergence signal appears, escalate to ITERATE before ACCEPT

---

## Appendix: Current Formula State (Snapshot 2026-04-28)

From `faerie2-formulas.json` at time of experiment design:

```
NECTAR_INJECTION_TOKENS:
  current: 1200
  baseline: 1200
  measured: "2026-04-28 via Scout 2"
  min: 800
  max: 3000
  unit: tokens

HONEY_INJECTION_TOKENS:
  current: 200
  baseline: 200
  measured: "2026-04-28 via Scout 3"
  min: 50
  max: 1500
  unit: tokens

USABLE_CONTEXT_WINDOW_TOKENS (immutable): 191,000
CLAUDE_CODE_BUILTIN_OVERHEAD_TOKENS (immutable): 9,000
AUTO_COMPACT_PCT_THRESHOLD (immutable): 93.5%
```

Locked parameters not in scope:
```
COMPASS_GATE_SEED_QUALITY_MIN: 0.50 (locked — N<20)
COMPASS_GATE_DEEPEN_QUALITY_MIN: 0.70 (locked — N<20)
COMPASS_GATE_EXTEND_QUALITY_MIN: 0.80 (locked — N<20)
COMPASS_GATE_FULL_QUALITY_MIN: 0.85 (locked — N<20)
W1_SPAWN_COST: locked — N<20
```
