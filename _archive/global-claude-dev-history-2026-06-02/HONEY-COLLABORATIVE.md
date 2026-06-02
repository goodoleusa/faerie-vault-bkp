---
honey_version: 3-prototype
style: cognitive-collaborative
purpose: "Shared vocabulary for cross-domain collaboration. If 2+ people compare their HONEY.md, they see complementarity immediately."
source_entries: "mth00403-00424, ws00001-00004, INVARIANTS#6"
---

# HONEY.md v3 — Cognitive Collaboration Framework

> Read this with a partner. Where do your blindspots match their strengths?

---

## COGNITIVE PROFILES (Agent Archetypes)

### 🧭 NAVIGATOR Archetype
**Cognitive style:** Thinks in autonomous discovery via manifest trails. Reads bearing signals (N/S/E/W). Follows compass DAG without central direction.

**Validates via:** manifest-first execution, stigmergic discovery, W-edge absence (no backtracking = solid baseline)

**Blindspot:** Cross-domain pattern transfer. Navigators get tunnel vision within their mission cluster. Miss insights from parallel domains.

**Complementary archetype:** BRIDGE (synthesis + cross-domain thinker)

**Source patterns:**
- mth00403: "23/23 discovered_work entries were agent-initiated discoveries, not human-assigned" → 100% autonomous routing works
- mth00404: "W1 phase (14 south + 8 east + 5 north + 0 west)" → W-edge absence = health signal
- mth00405: "Mission clustering isolation 0.82; throughput 3-4× vs linear queue" → clustering amplifies discovery

---

### 🔗 BRIDGE Archetype
**Cognitive style:** Thinks in pattern transfer. Sees a technique in Domain A, asks "could this apply to Domain B?" Connects across silos.

**Validates via:** cross-domain droplets, generalizability scoring (applicable_to: [domain1, domain2, ...]), recurrence across 3+ sessions

**Blindspot:** Within-domain depth. Bridges jump between domains, sometimes miss nuance when they should go deep.

**Complementary archetype:** DEEP-DIVER (domain expert who validates depth before transfer)

**Source patterns:**
- mth00421: "Spawn leverage threshold ≥10× across 4 events, avg 1,955×" → Pattern holds cross-project
- ws00002: "JSON + Markdown as companion formats...confirmed 3 sessions, universality 0.82" → Transfer pattern validated
- ws00004: "Pollen = signals not storage...prevents dumping ground" → Applies to ALL artifact types

---

### 🔬 DEEP-DIVER Archetype
**Cognitive style:** Thinks in domain mastery. Goes deep on one problem. Validates causation, not just correlation. Builds rigorous baselines.

**Validates via:** baseline-before-mutation, 7-day observation windows, measured actual_result (not claimed improvement)

**Blindspot:** Generalization. Deep-divers validate one case perfectly but struggle to say "this will apply elsewhere."

**Complementary archetype:** BRIDGE (proposes transfer, deep-diver validates)

**Source patterns:**
- mth00301: "BASELINE BEFORE BLINDNESS—record baseline_metrics BEFORE fix...after 7-day window, fill actual_result" → Rigor archetype
- mth00300: "Every 5 bundles, run crystallization pass" → Measurement discipline validates transfer eligibility

---

### ✨ MAKER Archetype
**Cognitive style:** Thinks in implementation momentum. "What if we tried this?" Prototypes fast. Captures droplets (inspiration) in-flight.

**Validates via:** manifest-first execution, droplet writes (speculative, not conclusive), bearing-rank prioritization (N>S>E>W)

**Blindspot:** Validation overhead. Makers move fast; sometimes leave measurement behind.

**Complementary archetype:** DEEP-DIVER (validates what maker built)

**Source patterns:**
- mth00415: "pre-wave unblock: if unblocks >= W1_agents×0.3 → unblocker_first()" → Heuristic-driven prioritization
- ws00001: "Mission-based bundle paths prevent task-ID clobbering" → Structural insight (maker prototyped, bridge generalized)

---

## CROSS-DOMAIN LEXICON (Shared Vocabulary)

**Routing signal** = `mission` field + `bearing` (direction). Used in manifests, droplets, discovered_work[], stage scheduling. Same semantic across forensics, NECTAR, bundle discovery.

**Bearing** = compass direction. N=unblock (prerequisites), S=ship (deliverable), E=parallel (sister work), W=backtrack (assumption reversal). Illegal chains: S→N (can't un-conclude), W→S (can't conclude after backtrack without re-anchoring).

**Pressure point** = context fill >80K triggers W2/W3 conservation (lower parallelism). <25K triggers W1 LIFTOFF (max burn). Applies to all tier selection.

**Baseline** = metric snapshot BEFORE any change. Measured simultaneously with implementation; compared to AFTER snapshot at 7-day window. Required for crystallization eligibility.

**Emergence health** = (edge_density × 0.35) + (clustering_coeff × 0.30) + (linearity × 0.25) + (1 - W_ratio × 0.10). Target ≥0.80. Declines if W-edges >5% (regression signal).

**Droplet** = pre-reasoning insight (aha moment); CROSS-DOMAIN inspiration. Not data, not findings. Example: "Manifest indexing (forensics) applies to: bundle discovery, frontier scanning, any read-all-then-filter pattern." Droplets spark mutations when agents read them.

**Crystallization gate** = "Is this fact true across ALL future sessions of ALL projects, independent of context?" YES → HONEY (permanent). NO → NECTAR (this session) or DROPLET (inspiration, waiting for validation).

---

## COLLABORATION MATRIX (Who Works Best Together?)

| Pair | Outcome | Why |
|------|---------|-----|
| NAVIGATOR + BRIDGE | 🟢 Amplifies routing + pattern transfer | Navigator discovers N/S/E edges; Bridge identifies cross-cluster E/S bridges that scale throughput 3-4× |
| DEEP-DIVER + MAKER | 🟢 Validation + momentum | Maker prototypes droplets fast; Deep-diver validates with baseline/7-day window; together: speed + rigor |
| NAVIGATOR + DEEP-DIVER | 🟡 Complementary but slow | Both are domain-focused; risk tunnel vision; need BRIDGE to unblock multi-domain patterns |
| BRIDGE + MAKER | 🟡 Creative but unvalidated | Bridges generalize droplets; Makers prototype fast; risk: brilliant ideas without measurement gates |
| All Four | 🟢 Self-correcting swarm | Navigators route, Bridges transfer, Makers prototype, Deep-divers validate. Emergence health ≥0.87 observed. |

---

## VALIDATED PATTERNS (Confidence ≥0.90)

**mth00403 | 0.95** Agents read manifests, navigate via compass bearings. 100% autonomous (23/23 discoveries self-initiated).

**mth00407 | 0.92** Emergence formula (edge_density + clustering + linearity) predicts actual observed emergence (predicted 0.87, observed 0.87).

**mth00410 | 0.92** Charter scope bounds discovery; phase gates maintain ordering. Proven: 100% tasks phase-ordered, zero skips.

**mth00421 | 0.88** Spawn leverage justified ≥10×. Measured across 4 events: 177×–6,644×, avg 1,955×. Threshold holds.

**mth00423 | 0.97** /spawn execution protocol: parse directives → call Agent() in parallel → wait TaskNotification → read manifest. Atomic, no monitoring.

**mth00424 | 1.0** Mission field is canonical routing key. discovered_work[] entries without mission= are unroutable. investigation_label deprecated.

**ws00002 | 0.92** JSON + Markdown dual format works across 3 sessions; zero extra cost; enables human indexing + machine routing.

---

## UNPACKING mth00088 (Low Signal Example)

Original: "droplet-quality-doctrine"
Problem: Vague. Doesn't show WHY droplets matter or how agents USE them.

Reframed (cross-domain version):
- **What it is:** Pre-reasoning inspiration (not data/findings)
- **When to write:** Any "what if we tried X?" moment
- **Where agents read it:** At startup, before manifests (inspiration shapes bearing choices)
- **Cross-domain example:** "Manifest indexing (Domain A) applies to bundle discovery, frontier scanning, queue filtering (Domains B/C/D)"
- **Complementary archetype:** BRIDGE creates droplets by asking generalization questions
- **Validation gate:** Droplet becomes HONEY only after DEEP-DIVER runs 3+ sessions, confirms pattern, measures delta ≥+0.05

**Result:** Signal restored. Now teams know: write droplets if you're seeing cross-domain patterns; BRIDGE role is natural; DEEP-DIVER validates before promotion.

---

## Usage: Comparing HONEYs Across Teams

**Person A's HONEY:**
- Cognitive style: NAVIGATOR + DEEP-DIVER (route + validate)
- Blindspot: Cross-domain transfer
- Validates via: bearing chains, W-edge absence

**Person B's HONEY:**
- Cognitive style: BRIDGE + MAKER (synthesize + prototype)
- Blindspot: Within-domain rigor
- Validates via: droplet recurrence, generalizability scoring

**Outcome:** "A's blindspot is B's specialty. Pair on cross-domain droplet validation. A provides bearing rigor; B provides pattern transfer."

---
