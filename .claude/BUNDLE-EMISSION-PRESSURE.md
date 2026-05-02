# mth00107 — Bundle Emission Pressure (Equilibrium Mechanism)

**Tier:** 0x (governance)  
**REPLACES:** Manual bundle prompting, ad-hoc discovery phases  
**METRIC:** bundles_emitted_per_agent, main_context_burden_reduction, mission_formation_speed, discovery_efficiency

---

## Core Principle (f(0) Equilibrium)

**Traditional model (violates f(0)):**
- Main spawns agents → collects results → reads findings → decides next work → renders bundles → repeats
- Main context burned on synthesis + planning
- Throughput limited by main's decision bandwidth

**Stigmergic model (respects f(0)):**
- Agent A completes task, has 40% context remaining
- Presend hook detects: "remaining context > 30%, emit bundle for next agent"
- Agent A renders bundle using 0x_spawn_template.py (~10% of remaining tokens)
- Agent A returns (manifest only, no extra synthesis work)
- Future Agent C discovers bundle via mission graph, starts with full context
- Result: agents do main's synthesis work, zero burden on main

---

## How It Works

**Hook:** `0x_bundle_emission_pressure.sh` (presend stage)

1. **Read altimeter.json** → current context %
2. **Calculate remaining context** = 100% - context_pct
3. **Read formula** BUNDLE_EMISSION_CONTEXT_THRESHOLD (default 30%)
4. **IF remaining > threshold:**
   - Inject bundle-emission instructions into agent prompt
   - Show opportunity: "You have ~X% context. You can emit bundles for next scouts."
   - Provide template: `0x_spawn_template.py --bundle`
5. **IF remaining < threshold:**
   - Silent (no injection), agent focuses on primary task

---

## Formulas

| Formula | Current | Min | Max | Unit | Meaning |
|---------|---------|-----|-----|------|---------|
| BUNDLE_EMISSION_CONTEXT_THRESHOLD | 30 | 20 | 50 | % | Remaining context at which to offer bundle emission |

---

## Real Measurements (2026-04-28)

From W1 LIFTOFF scouts, measured bundle injection costs:

| Component | Measured | Theory | Delta | Impact |
|-----------|----------|--------|-------|--------|
| NECTAR injection | 1,204 | 2-3K | -40-60% | Cheaper than expected; safe to include in all bundles |
| HONEY injection | 200 | 1,500 | -7.5x | Ultra-cheap (compressed); always include |
| Total per agent | ~1.4K | 3.5K | -60% | Bundle cost is half theory prediction |

**Implication:** Bundle emission at 30% remaining context is low-risk. Cost ~1.4K tokens; benefit to next agent ~40% efficiency gain.

---

## Agent Decision Tree

**In your manifest, log bundle decision as prescan_decision field:**

```
prescan_decision: {
  "remaining_context_pct": 42,
  "threshold": 30,
  "decision": "EMIT",
  "bundle_type": "standard",
  "reason": "Discovered unblocking work in same investigation_label; next scout needs context"
}
```

**When to EMIT:**
1. Primary task complete + manifest written (constraint satisfied)
2. Remaining context > 30% (formula gate)
3. Discovered unblocking work in same investigation_label (prescan passed, task <24h old)
4. Bundle type chosen: light (2K) | standard (4K) | rich (7K)

**When NOT to emit:**
- Primary task incomplete
- Prescan finds recent work (>24h, skip to avoid duplication)
- Remaining context < 20% (spend on primary, not bundles)
- No discovered work worth bundling (leave discovered_work empty)

---

## Example: Scout A Emits, Scout B Discovers

```
T=0: Scout A completes primary task (35% context spent)
     Manifest written (constraint ✓)
     Remaining: 65%
     
     Prescan discovers: task-B is unblocked, ready for next phase
     Decision: EMIT bundle (65% > 30% threshold)
     Bundle type: standard (4K tokens, medium investigation continuation)
     Action: calls 0x_spawn_template.py --bundle --type standard
     Cost: ~4K of 65% remaining
     Returns: manifest + bundle
     
T=1: Scout B reads investigation_label="treasury-cert-origins"
     Discovers bundle emitted by Scout A
     Starts with full mission context (not cold start)
     Efficiency: 40% faster onboarding
     
T=2: Scout B completes deeper work, emits their own bundle
     Mission grows emergently (no main involvement)
```

---

## Mutation Protocol

To adjust threshold (e.g., test BUNDLE_EMISSION_CONTEXT_THRESHOLD = 40 instead of 30):

1. **Baseline (3 sessions at 30%):** bundles_emitted_per_agent, main_context_burden, discovery_speed
2. **Edit:** faerie2-formulas.json, change to 40%
3. **Mutation (3 sessions at 40%):** collect same metrics
4. **Analyze:** Did more bundles emit? Did main context stay lighter? Did discovery slow?
5. **Decision:** ACCEPT (higher threshold = even lighter main) | REVERT (30% is optimal)

---

## See Also

- `faerie2-formulas.json` — BUNDLE_EMISSION_CONTEXT_THRESHOLD + all mutable parameters
- `0x_bundle_emission_pressure.sh` — Presend hook implementation
- `SPAWNING-DISCIPLINE.md` (mth00090) — Agent autonomy + bundle emission
- `CONTEXT-GATING-OPERATIONAL.md` (mth00106) — Wave gates (paired mechanism)
