# Membench v0.3 Proposal — Mutation & Emergent Behavior Metrics

**Purpose:** Extend the Membench v0.2 framework with seven metrics that measure the *instruction substrate* underneath memory. Current membench (M1–M11) measures memory-system health assuming the instruction layer (rules, hooks, scripts) is stable. In practice, the instruction layer mutates constantly — duplicate scripts, rule contradictions, silent overlaps — and those mutations can be beneficial (redundant paths, graceful fallback), neutral (drift without effect), or harmful (racing hooks, shadowed canonicals). Memory metrics can score perfect while the substrate corrupts silently.

**Status:** Proposal for user review — not yet merged into MEMBENCH-STRATEGY.md or wired into eval_harness.

**Framing:** Evolutionary, not sanitary. A conflict-detector cleans up all overlap and destroys beneficial redundancy along with the harmful kind. A mutation metric *classifies* drift and *preserves* the beneficial mutations explicitly.

---

## Why A New Metric Family

Membench v0.2 already has a silent-corruption detector for memory facts: **M8 Confabulation** (false facts in NECTAR). M8 asks *"is memory lying about the world?"* The mutation metrics ask *"is the instruction set lying to itself?"* — same shape of question, different layer.

Existing metrics do not see:
- Two scripts with identical names and contradictory LOAD declarations
- Hooks firing sequentially on the same event with overlapping side-effects
- Rules pointing agents at a header-less ancestor while a tier-prefixed, evolved version exists elsewhere
- Near-duplicate scripts where one has equilibrium headers and one does not
- CLAUDE.md references to files that do not exist

These corruptions do not degrade memory retrieval; they degrade *agent execution*. Without a metric, f(0) optimization sprints keep accumulating them.

---

## Core Metrics (MDR, MC, EBI, FD, PR)

### **MDR — Mutation Detection Rate**

**Symbol:** MDR
**Unit:** pairs per 100 active scripts+rules
**Formal definition:** Number of conflicting or overlapping instruction pairs detected per 100 active scripts+rules in the current working set. An instruction pair is *conflicting* if both are reachable at runtime AND operate on the same observable (file path, hook event, env var, queue entry) AND their behaviors diverge. An instruction is *active* if (a) cited in settings.json hooks, (b) referenced by path in rules/core/* or rules/sauce/*, (c) referenced by a commit in the last 30 days.

**Formula:**
```
MDR = (count(conflicting_pairs) / count(active_instructions)) × 100
```

**Measurement protocol:**
1. Enumerate active instruction set: parse settings.json hook commands, grep rules/core/* and rules/sauce/* for absolute paths, collect `git log --since='30 days' --name-only` unique entries
2. Build a signature index keyed by (filename stem, observable target)
3. For each signature with ≥2 entries, compare behavior stubs (docstring LOAD, REPLACES, first 20 lines, tool side-effects)
4. Classify each overlap as conflicting / duplicate / delegate-stub

**Data source:**
- `~/.claude/hooks/settings.json`
- `~/.claude/rules/core/*.md`, `~/.claude/rules/sauce/*.md`
- `git log --since='30 days ago' --name-only`
- Script headers (TIER, LOAD, REPLACES, METRIC)

**Integration with existing composite:**
MDR does *not* enter the composite directly. It is a *substrate metric* analogous to M10 (Instruction Coverage) — but where M10 is a multiplier (scales composite downward if inputs missing), MDR is a *separate scoreline* reported alongside composite. Rationale: composite measures memory system; MDR measures instruction system; mixing them hides which layer is degrading.

**Example measurement (this audit):**
- Active instructions counted: ≈200 scripts (global + faerie2) + 12 rule files + 24 hook entries in settings.json ≈ 236
- Conflicting/overlapping pairs detected: 11 (see audit narrative)
- MDR = (11 / 236) × 100 = 4.66 pairs per 100 active instructions

---

### **MC — Mutation Classification**

**Symbol:** MC
**Unit:** % breakdown, four-class
**Formal definition:** For each mutation pair detected by MDR, classify into one of four classes based on runtime behavior:

| Class | Definition |
|---|---|
| **BENEFICIAL** | Enables emergent capability: redundant path that gracefully degrades, intentional delegate stub, layered safety net (e.g. settings.json `2>/dev/null || true` wrappers) |
| **NEUTRAL** | Harmless drift: duplicate docs, same instruction in two places, near-identical copies with no runtime divergence |
| **HARMFUL** | Causes conflict or error: contradictory guidance, racing hooks, silent shadowing (rule points at pre-evolution copy) |
| **UNCERTAIN** | Not yet triggered in production OR requires empirical observation to classify (novel combination, path-resolution ambiguity) |

**Formula:**
```
MC = {beneficial_pct, neutral_pct, harmful_pct, uncertain_pct}
    where each = count(class) / count(all_pairs) × 100
```

**Measurement protocol:**
1. Start from MDR pair list
2. For each pair, run three runtime probes:
   - **Fallback probe:** delete the apparent duplicate, re-run a canonical faerie cycle; does behavior degrade gracefully?
   - **Race probe:** inspect hook ordering; do two hooks write to the same file with different content?
   - **Reachability probe:** which rule or caller cites each copy? Does the citation match the evolved variant?
3. Assign class based on observed runtime outcome, not stated intent
4. Flag UNCERTAIN if any probe is inconclusive

**Data source:**
- MDR pair list
- Hook execution order in settings.json
- Grep-based citation map (which rules/skills/scripts call which variant)
- Optional: controlled isolation test (move one copy, re-run)

**Integration with existing composite:**
Reported alongside MDR. Harmful_pct acts as a *gate*: if harmful_pct > 15%, flag substrate instability; membench composite is still valid but should be annotated with "MC-WARN: N% harmful mutations present" so downstream readers know whether memory scores reflect real system health or masked substrate rot.

**Example measurement (this audit):**
- 11 pairs classified: 3 BENEFICIAL, 4 NEUTRAL, 3 HARMFUL, 1 UNCERTAIN
- MC = {27%, 36%, 27%, 10%}

---

### **EBI — Emergent Behavior Index**

**Symbol:** EBI
**Unit:** novel-capability count per cycle
**Formal definition:** Number of observed capabilities that emerge from the *interaction* of two or more instructions and are not expressible by any single instruction alone. Requires empirical observation, not static analysis — this is the metric that formalizes "the whole is more than the sum of the parts."

**Formula:**
```
EBI = count(observed_emergent_behaviors) per measurement window
     where observed_emergent_behavior = {
       derived_from: [instruction_A, instruction_B, ...],
       not_expressible_by: single instruction alone,
       verified_in: concrete agent run / manifest / COC entry
     }
```

**Measurement protocol:**
This is the only metric that *cannot* be computed purely from static artifacts. It requires:
1. **Baseline catalog** of per-instruction capabilities (what each rule/script does alone)
2. **Observation window** (one faerie cycle, one sprint, or one calendar month)
3. **Post-hoc audit** of agent manifests, COC entries, and droplets: find behaviors that required ≥2 instructions to produce
4. **Exclusion rule:** coordination (A calls B, then B calls C) is NOT emergent — it's composed. Emergent means the *combination* produces a capability neither A nor B names.

**Data source:**
- Agent manifests (output_path, dashboard_line, next_task)
- COC entries (agent_run_id, prev_run_hash chain)
- Droplets tagged #shared or CONNECTION category
- Post-hoc narrative reviews in vault ONBOARDING folders

**Integration with existing composite:**
EBI is *separate from composite* — it is a leading indicator of system vitality. A stable system has EBI ≈ 0–2 per cycle (mature, predictable). A system in rapid evolution has EBI ≥ 5 per cycle (high mutation pressure producing novel combinations). Interpretation is context-dependent; the metric exists to *see* the phenomenon, not score it.

**Example measurement (hypothetical):**
- Window: one 3-day sprint
- Observed emergent behaviors: (a) manifest_task_autocompletion + 8x_manifest_auto_continue combine to produce zero-inference task chaining; (b) 9x_lean_query + faerie BODY.md combine to produce sub-5-token startup status; (c) 9x_piston_model_router + 9x_stigmergy_tracker combine to produce cost-aware stigmergy discovery (free models on low-stakes probes)
- EBI = 3

---

### **FD — Flag Delay**

**Symbol:** FD
**Unit:** hours (mean time)
**Formal definition:** Mean elapsed time from the introduction of a mutation (git commit introducing a duplicate, contradiction, or shadow) to the first systemic flag that the mutation exists — whether by audit script, hook error, rule contradiction alert, or human discovery.

**Formula:**
```
FD = mean( t_flag - t_commit )
   across all mutations detected in the measurement window
   where t_flag = first timestamp a signal fires about the mutation
         t_commit = git commit timestamp introducing the mutation
```

**Measurement protocol:**
1. For each mutation classified under MC (except UNCERTAIN), locate the commit that introduced it (`git log --follow`, `git blame`)
2. Find the earliest systemic signal about it: audit report entry, hook error log, rule review session, equilibrium audit output
3. Compute delta; aggregate as mean + median (median is more robust for long-tail mutations)
4. Decompose by class: FD_harmful, FD_neutral, FD_beneficial — harmful mutations with long FD are the highest priority to shrink

**Data source:**
- Git log on rule/script/hook files
- `~/.claude/memory/forensics/` audit results
- `scripts/9x_equilibrium_audit.py` output history
- COC entries and session_stop_hook logs

**Integration with existing composite:**
Reported as a diagnostic timeseries. FD is analogous to the MTTD (mean time to detection) concept from incident response: a *falling* FD indicates the audit infrastructure is catching mutations faster; a *rising* FD indicates silent accumulation. Pairs naturally with MC — harmful_pct × FD_harmful yields a "mutation risk exposure" scalar.

**Example measurement (this audit):**
- 3 HARMFUL mutations with introduction commits on 2026-04-21, 2026-04-22, 2026-04-22
- First systemic flag: this mutation audit (2026-04-23)
- FD_harmful = mean([48h, 24h, 24h]) = 32h
- This is the *first* measurement — future audits should drive FD_harmful < 24h

---

### **PR — Preservation Rate**

**Symbol:** PR
**Unit:** % of beneficial mutations preserved across debloat passes
**Formal definition:** Of the mutations classified BENEFICIAL in audit T, what fraction remain BENEFICIAL (still present, still functioning) in audit T+1 after intervening debloat/crystallize/equilibrium-audit passes?

**Formula:**
```
PR = count(beneficial_still_present_at_T+1) / count(beneficial_at_T) × 100
```

**Measurement protocol:**
1. At audit T, snapshot the BENEFICIAL mutation set (path + signature + observed capability)
2. Between T and T+1, normal cleanup passes run (debloat.py, equilibrium audits, PR reviews, user-driven refactors)
3. At audit T+1, re-run MDR+MC on the current instruction set
4. For each prior BENEFICIAL entry, check: is the redundant path still present? Does it still function? Was it *preserved intentionally* or survived by accident?
5. If a BENEFICIAL mutation was removed AND the capability it enabled disappeared, that is a preservation failure

**Data source:**
- Audit T snapshot (JSON: mutation_id, paths, class, capability)
- Audit T+1 current state scan
- `git log` between T and T+1 on audited paths
- Downstream functional tests (did the capability actually degrade?)

**Integration with existing composite:**
PR is a *long-horizon quality gate*. A system where PR < 80% is actively destroying its own emergent capabilities via well-meaning cleanup. PR < 60% indicates the cleanup infrastructure is hostile to beneficial redundancy — debloat is too aggressive, equilibrium audit doesn't know which duplicates to preserve. This metric requires at least two audits (cannot be measured in a single pass) — it is a time-separated differential.

**Example measurement:** Not yet available — this audit is T=0. First PR value computed at next audit (T+1).

---

## Extended Metrics (SR, CCI)

Two additional metrics proposed for early adoption alongside the core five:

### **SR — Shadow Rate**

**Symbol:** SR
**Unit:** fraction of citations pointing at pre-evolution copies
**Formal definition:** Of all path citations in rules/core/*, rules/sauce/*, CLAUDE.md, skills/*, and hook commands, what fraction point at an ancestor copy when a tier-prefixed evolved variant exists elsewhere in the tree?

**Formula:**
```
SR = count(citations_to_ancestor_when_evolved_exists) / count(all_citations) × 100
```

**Measurement protocol:**
1. For every absolute path cited in rules/skills/settings.json, resolve the file
2. Check: does a file with same stem + tier prefix (`4x_`, `7x_`, `9x_`) exist elsewhere with equilibrium headers (TIER/LOAD/REPLACES/METRIC)?
3. If yes, and the citation targets the un-prefixed / un-evolved copy, count as shadow
4. Report SR + shadow-path list

**Data source:**
- Grep across rules/*, skills/*, settings.json
- Directory scan of ~/.claude/scripts/ and faerie2/scripts/ for tier prefixes
- Script header compliance check

**Integration with existing composite:**
SR is a *specific* subset of MDR — the shadow subclass of HARMFUL mutations. Reported as a dedicated metric because it is the single most actionable mutation class: fixing a shadow is a rule-line edit, not a code refactor. If SR > 5%, prioritize citation reconciliation before other substrate work.

**Example measurement (this audit):**
- queue_ops.py cited in rules/core/agents.md points at `~/.claude/hooks/state/queue_ops.py` (header-less); faerie2/scripts/7x_queue_ops.py is the evolved variant with headers and monkeybranching
- 5 distinct rule lines cite the ancestor
- Of ≈50 path citations total across rules: SR = 5/50 = 10%

**Why it matters here:** A 10% shadow rate means one in ten agent-protocol instructions is pointing at an un-evolved copy. Memory retention can be 100% while the agents are still operating on obsolete tooling.

---

### **CCI — Capability Composition Index**

**Symbol:** CCI
**Unit:** ratio (composite capabilities / atomic capabilities)
**Formal definition:** Measures the leverage ratio of the instruction substrate. How many *compound* capabilities (requiring instruction A + instruction B to produce outcome X) exist per *atomic* capability (single instruction → outcome)?

**Formula:**
```
CCI = count(compound_capabilities) / count(atomic_capabilities)
```

**Measurement protocol:**
1. Build the atomic capability catalog: for each active script/rule/hook, record the singular outcome it produces
2. Build the compound capability catalog from EBI observations + known composition patterns (hook chains in settings.json Stop/PostToolUse arrays are obvious compositions)
3. Compute ratio

**Data source:**
- Script docstrings (METRIC field)
- Hook chain definitions in settings.json
- EBI observation log

**Integration with existing composite:**
CCI measures the *f(0) gain* directly: composition without inference. Low CCI (< 0.3) means most capabilities require human orchestration or agent inference to combine instructions. High CCI (> 1.0) means the substrate has *more* emergent outcomes than raw instructions — this is the definition of a compounding system. CCI pairs with M3 Work Efficiency: M3 measures memory leverage, CCI measures instruction leverage. Together they describe the full compounding picture.

**Example measurement (this audit):**
- Atomic capabilities ≈ 200 (one per active script/rule/hook block)
- Observed compound capabilities ≈ 80 (hook chains, rule+script combinations, queue+manifest flows)
- CCI = 80 / 200 = 0.40

---

## Metric Summary Table

| Symbol | Name | Unit | Scope | Veto? | Integrates with composite? |
|---|---|---|---|---|---|
| **MDR** | Mutation Detection Rate | pairs/100 | instruction | no | separate line |
| **MC** | Mutation Classification | 4-class % | instruction | soft gate | annotation only |
| **EBI** | Emergent Behavior Index | novel-cap count | observational | no | leading indicator |
| **FD** | Flag Delay | hours | time-to-detect | no | diagnostic timeseries |
| **PR** | Preservation Rate | % | differential | no | long-horizon gate |
| **SR** | Shadow Rate | % | citation-reach | no | subset of MDR |
| **CCI** | Capability Composition Index | ratio | leverage | no | pairs with M3 |

---

## Proposed Composite-Layer Treatment

Membench v0.2 composite reports *memory substrate* quality. Mutation metrics report *instruction substrate* quality. Two substrates, two composite lines:

```
MEMBENCH COMPOSITE (v0.2 unchanged):
  composite = (M1×0.25 + M2×0.20 + M3×0.30 + (100-M4)×0.10 + M5×0.15) × M10
  veto gates: M8 > 5% (confabulation), M11 < 70% (bootstrap)

MUTATION COMPOSITE (v0.3 proposed):
  mutation_score = reported as four-tuple: (MDR, MC.harmful_pct, FD_harmful_mean_hours, SR)
  no single-number collapse — these measure different risk dimensions
  soft gates:
    MC.harmful_pct > 15%  → annotate composite "SUBSTRATE-WARN"
    SR > 10%              → annotate composite "CITATION-DRIFT"
    FD_harmful > 72h      → annotate composite "SLOW-DETECT"

VITALITY INDICATORS (no gates, observational only):
  EBI, PR, CCI — these describe system evolution, not health
```

Dual-composite reporting means operators see memory health AND substrate health separately, without either masking the other.

---

## Measurement Cadence

| Cadence | Metrics |
|---|---|
| **Per session** | (none — mutation drift is slow; session-level measurement is noise) |
| **Per faerie cycle** | MDR, SR (fast static analysis) |
| **Weekly** | MC, FD, CCI (requires runtime probes or EBI observation window) |
| **Monthly** | EBI, PR (require observation window + prior snapshot) |
| **Per commit to rules/** | SR (one-liner regression check) |

---

## Integration Plan (if approved)

1. **Phase 0** — operator review of this proposal; adjust metric definitions based on feedback
2. **Phase 1** — implement `scripts/eval/eval_mutation.py` computing MDR + MC + SR (static-analysis subset, no runtime probes yet)
3. **Phase 2** — wire into eval_harness.py as optional `--mutation` flag, mirror output to W&B alongside membench
4. **Phase 3** — add FD timeseries tracking (requires git log integration + snapshot store)
5. **Phase 4** — EBI + PR require observation protocol + snapshot tooling; defer until Phases 1-3 stable
6. **Phase 5** — crystallize selected metrics into MEMBENCH-STRATEGY.md and retire this proposal

---

## Relationship to Existing Membench Documents

- **MEMBENCH-METRICS-EXPLANATORY.md:** mutation metrics are a separate family; this proposal does not modify the M1-M11 definitions
- **MEMBENCH-STRATEGY.md:** upon approval, add a "Substrate Health (Mutation Family)" section mirroring the existing "Memory Health" sections
- **MEMBENCH-QUICK-REFERENCE.md:** add a quick-reference row for each mutation metric after approval
- **MEMBENCH-VISUAL-GUIDE.md:** add decision matrix entries for `MC.harmful_pct > 15%` and `SR > 10%` warning states

No existing metric is modified, reweighted, or retired by this proposal. Mutation metrics are additive.

---

**Document version:** v0.3.0 proposal | **Date:** 2026-04-23 | **Status:** Awaiting operator review before merge into MEMBENCH-STRATEGY.md
