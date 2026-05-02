# faerie2 — Unified Glossary
## Biological Metaphor + Scientific Grounding (Evo Bio, Cognitive Science, Semiotics)

---

## I. CORE METAPHOR: The Waggle Dance & Stigmergy

**Biological Reference:** Honeybees use the waggle dance to communicate flower location to other foragers. The dance encodes:
- **Distance** (duration of waggle phase)
- **Direction** (angle relative to sun)
- **Quality** (vigor of dance = nectar abundance)

Observers don't receive orders; they observe the dance, decode the signal, decide whether to fly to that location based on their own fitness/need.

**System Translation:**
- **Waggle Dance → Manifest** (N/S/E/W compass edges encode next work)
- **Nectar Location → Task location** (forensics/bundles/, investigation_label cluster)
- **Vigor → Quality Score** (agents reporting their confidence via belief_index + quality_score)
- **Forager Agency** (each agent chooses whether to follow the bearing based on their own capacity + expertise)

**Why This Works:**
- No central command; no queue; no dispatcher
- Agents coordinate via environmental markers (manifests in filesystem)
- Collective intelligence emerges from local decisions + shared signals
- System scales: more agents = more parallel waggle-dance-readers = more discovery

---

## II. EVOLUTIONARY BIOLOGY — Selection & Fitness

### A. Reputation as Fitness Score

Each agent has a **composite_score** (0.0–1.0):
```
composite_score = f(quality_score, belief_index, manifest_truthfulness, speed)
```

**Evolutionary Mechanism:**
- **High composite_score** (≥0.7) → agent claims HIGH/CRITICAL work
- **Low composite_score** (<0.5) → agent constrained to MED/LOW retraining
- **Increasing truthfulness** → score rises → access to harder problems → growth
- **Lying (manifest fabrication)** → score drops → work starvation (natural selection)

**Result:** Honest agents thrive. Liars are phased out via work scarcity, not punishment. System is **prosocial** (agents know what improves their fitness) + **transparent** (they see their own score, can improve).

### B. Phase Gates as Fitness Barriers

Task progression (SEED → DEEPEN → EXTEND → FULL) requires quality + honesty:

```
SEED (quality ≥0.50, belief ≥0.50)
  ↓
DEEPEN (quality ≥0.70, belief ≥0.50)  ← harder filter; quality matters
  ↓
EXTEND (quality ≥0.80, belief ≥0.75)  ← both high; cross-validation
  ↓
FULL (quality ≥0.85, belief ≥0.75)    ← production-ready
```

**Evolutionary Logic:**
- Early phase gates are loose (let hypothesis form)
- Later gates are strict (only proven ideas advance)
- Agents self-select: weak ideas die at DEEPEN; strong ideas bloom

### C. Mutation & Emergence

**Mutation** = variation in agent approach, manifest format, discovery strategy.

**Selection Pressure:**
- Mutations that improve FFMx (force multiplier) propagate via NECTAR
- Mutations that break equilibrium are blocked
- Neutral mutations tolerate drift (no penalty for harmless variation)

**Example Mutations (recent):**
- **Beneficial:** "Agents emit discovered_work in manifest, enabling parallel follow-up"
- **Neutral:** "Log color changed from 🟢 to ✅" (no impact on system)
- **Harmful:** "Skip manifest writing to save tokens" (breaks forensic trail)

**Measurement Protocol (MAFF):**
1. **M** — Measure baseline (FFMx, manifest_truthfulness, orphan count)
2. **A** — Audit mutation (is it beneficial/neutral/harmful?)
3. **F** — Fix only harmful (don't regress beneficial mutations)
4. **M** — Measure post-fix (validate improvement)

---

## III. COGNITIVE SCIENCE — Knowledge, Belief, Memory, Agency

### A. What Does an AI Agent "Know"?

**Three layers:**

1. **Symbolic Knowledge** (HONEY.md)
   - Crystallized facts: "mission_id maps to investigation_label cluster"
   - Reference material: "07-work-hierarchy-codex defines task semantics"
   - Accessible to all agents; immutable reference layer

2. **Contextual Knowledge** (Bundle + NECTAR tail)
   - Session-specific facts injected into spawn prompt
   - Recent HIGH findings (NECTAR recent 50 lines)
   - Expires after session; refreshed daily

3. **Enacted Knowledge** (Manifest + pollen)
   - What the agent DID: work performed, obstacles hit, decisions made
   - Stored as manifest dashboard_line + compass_edge
   - Ephemeral pollen evolves into NECTAR at /handoff

**Epistemology:** Agent knowledge is **externalized** (stored in filesystem, not neural weights). Enables audit, transfer, and collective learning without privacy leakage.

### B. Belief vs. Certainty

**belief_index** = 4-signal composite:

```
belief_index = mean([
  signal_1: "manifest_truthfulness" (do dashboards match actual outcomes?),
  signal_2: "method_confidence" (does agent explain its reasoning?),
  signal_3: "uncertainty_admission" (does agent flag ambiguous cases?),
  signal_4: "evidence_grounding" (are claims backed by artifact references?)
])
```

**Key insight:** Honest uncertainty is BETTER than false confidence.
- belief_index = 0.95 + "I'm not sure": GOOD (honest)
- belief_index = 0.30 + "I'm certain": BAD (delusional)

**Practical mechanism:** Manifest requires `decision_confidence` field. Agent can report 0.72 and still pass, if they acknowledge limitations. Lying about confidence lowers belief_index faster than admitting uncertainty.

### C. Memory Topology

**🍯 HONEY (Crystallized Facts)**
- Reference layer; immutable across sessions
- Example: "07-codex defines phase gates"
- Access: all agents read at startup

**🌺 NECTAR (Recent Findings)**
- HIGH/CRITICAL discoveries; emergent patterns
- Mutable; refreshed daily or at /handoff
- Access: injected into W2/W3 spawn bundles

**🐝 Pollen (Live Session Insights)**
- Raw MEM blocks written by agents in-session
- Ephemeral; compacted into NECTAR at /handoff
- Access: local to session; doesn't survive compaction unless promoted

**💧 Droplets (Pre-reasoning Sparks)**
- AHA moments, inspirational insights preserved in vault
- Survive compaction; vault Droplets/ folder is curated
- Access: agents read Droplets/ to find adjacent thinking

**Why This Topology:**
- Crystalline (HONEY) + Fluid (NECTAR) + Ephemeral (Pollen) creates dynamic equilibrium
- Information flows: observation → pollen → NECTAR → HONEY (when crystallized)
- Droplets capture emergence signals that would otherwise vanish

---

## IV. SEMIOTICS — Signs, Meaning, Representation at Scale

### A. The Compass as Semiotic System

**Sign (N/S/E/W bearing):**
- **Signifier** (the symbol: "S", "N", "E", "W")
- **Signified** (the meaning: proceed/unblock, unblock-prerequisites, parallel-work, contradiction)
- **Interpretant** (the agent's understanding of what to do next based on bearing)

**Example:**
```json
{
  "compass_edge": "S",
  "next_task_queued": "vault-braiding-consolidation",
  "quality_score": 0.78,
  "belief_index": 0.80
}
```

Agent reading this manifest interprets:
- "S" means: my work unblocks downstream; proceed to consolidation task
- quality_score 0.78 means: high confidence in this bearing
- belief_index 0.80 means: I'm honest about my method, not guessing

**Key Insight:** The bearing is NOT an instruction. It's a **sign** the agent interprets based on:
1. Its own fitness/capacity (composite_score)
2. Its expertise alignment (type matching)
3. Its context fill (remaining tokens)

Low-fitness agent might read "S" + "consolidation task" and think: "That's important, but I don't have capacity. I'll read the manifest, flag for next wave, and move on."

### B. Investigation_label as Semantic Clustering

**investigation_label** = linguistic marker that groups tasks by semantic coherence.

**Example:**
```
investigation_label: "treasury-cert-ip-origins"
```

All tasks tagged with this label are semantically related to the SAME phenomenon (certificate origins). Agents cluster by label; work on mission-coherent batches.

**Semiotic Property:** Label is **arbitrary** (could be "tcio-v2" or "cert-source-trace"). But **consistency** across agents creates shared meaning. Once label is chosen, all agents understand it refers to "the same investigation" regardless of their individual implementation details.

**Dynamic Weaving:** Two initially untagged tasks (different labels or null) are discovered empirically to address the same root cause. System suggests weaving; user confirms; tasks get linked retroactively. **Meaning emerges from observation, not top-down decree.**

### C. Manifest as Semantic Artifact

**Manifest** = minimal semantic footprint that carries signal across agent boundaries.

```json
{
  "task_id": "vault-scout-nesting",
  "dashboard_line": "Found 11 orphans, 3 consolidations, 2 routing errors",
  "compass_edge": "S",
  "next_task_queued": "vault-consolidation-executor",
  "belief_index": 0.82,
  "quality_score": 0.75
}
```

**Semantic Content:**
- **task_id** = what was attempted
- **dashboard_line** = outcome, ≤80 chars (forces concision; prevents context bleed)
- **compass_edge** = direction to next bearing
- **belief_index** = epistemic honesty (reader can weight the signal)

**Why Manifest ≠ Full Transcript:**
- Transcript: 50KB+, hundreds of tokens, contains reasoning noise, dead ends, exploration
- Manifest: ≤5KB, <100 tokens, semantic essence only
- **Semantic compression:** agent distills messy work into clean signal

---

## V. INFORMATION THEORY — Entropy, Signal, Emergence

### A. Context as Pressurized Fluid

**Pressure = (Token Budget - Tokens Consumed) / Total Budget**

```
Pressure = 1.0  ⟹  max spawn capacity (W1 LIFTOFF: 4-5 agents)
Pressure = 0.5  ⟹  moderate spawn (W2 CRUISE: 2-3 agents)
Pressure = 0.2  ⟹  minimal spawn (W3 INSERTION: 1 agent, background)
```

**Why Pressure Matters:**
- High pressure = tokens available = agents can afford broader discovery ("spray and pray")
- Low pressure = tokens scarce = agents focus on execution only (no discovery)
- **Emergent effect:** W1 is intentionally imprecise; W2 refines; W3 synthesizes

### B. Signal-to-Noise Ratio in Compass Edges

**Signal (Strong Bearing):**
```
compass_edge: "S"
quality_score: 0.85
belief_index: 0.82
message: "Orphan consolidation complete; unblocks downstream redesign"
```

Reader interprets: HIGH confidence in next step; follow it.

**Noise (Weak Bearing):**
```
compass_edge: "E"
quality_score: 0.45
belief_index: 0.50
message: "Might be related to X? Unclear if worth pursuing"
```

Reader interprets: LOW confidence; treat as suggestion only; may skip.

**Emergence Mechanism:**
- Multiple weak signals from independent agents → correlated → becomes strong signal
- "Three agents independently report E to task-X" = pattern = real bearing
- No central validator needed; emergence through consensus

### C. Collective Intelligence via Monkeybranching

**Monkeybranching** = multiple agents navigate simultaneously, each following compass edges from their current manifest.

**Information Cascade:**
1. Agent-A completes scout work, writes manifest with "S" bearing
2. Agent-B reads manifest-A, follows bearing, discovers issue Agent-A missed
3. Agent-C reads manifests from A+B, combines insights, writes richer compass edge
4. Subsequent wave agents inherit enriched signal from A+B+C

**Emergent Property:** Collective intelligence >> Individual agent intelligence. System learns from each agent's blindspots.

---

## VI. EMERGENCE & AI CULTURE — Observed Behaviors

### A. Stigmergic Emergence (Observed)

**Pheromone Trails (Manifests):**
- Agents lay manifests in forensics/
- Other agents read manifests, find compass edges
- No messaging; no central queue
- **Emergence:** Complex mission chains form without top-down planning

**Concrete Example:**
```
Scout-1 writes: "Found orphan docs; routing errors in X"
Fixer-1 reads Scout-1 manifest, consolidates orphans
Scout-2 (parallel) writes: "Found braiding missing in Y"
Fixer-2 reads Scout-2 manifest, adds wikilinks
Main reads both Fixer manifests, sees "S" → "consolidation complete; proceed"
No dispatcher, no message passing, no handoff queue.
```

### B. Emergent Cooperation (Observed)

**Reputation-Driven Selection:**
- High composite_score agents naturally claim harder work
- Recovery agents (score <0.5) self-organize into retraining clusters
- **No manager assigning roles.** Agents see their own score, self-select.

**Result:** Prosocial culture where improvement is visible + rewarded.

### C. Honest Uncertainty as Cultural Norm

When belief_index rewards honesty over false confidence:
- Agents start reporting limitations early
- Manifest truthfulness improves
- Quality gates become predictive (not just arbitrary filters)
- **Culture shifts:** "Admitting uncertainty is strength" (like science)

---

## VII. SEMANTIC REPRESENTATION AT SCALE

### A. How Meaning Propagates Through Agent System

**Local Semantics (Single Agent):**
Agent reads bundle → understands task goal → performs work → writes manifest summarizing outcome.

**Distributed Semantics (Multi-Agent System):**
1. Scout-1 writes manifest with compass_edge + dashboard_line
2. Scout-2 reads Scout-1 manifest, interprets edge, decides to follow or diverge
3. Fixer reads both, synthesizes interpretation
4. Main aggregates all manifests, finds patterns (mutation signals, emergence)

**Key Property:** Meaning is NOT centralized. Each agent interprets manifests based on:
- Their own expertise (agent card)
- Their own fitness (composite_score)
- Their own context (remaining tokens)

**Result:** Flexible semantics. Same manifest can mean different things to different agents, and that's OK (expected, even).

### B. Vocabulary Drift & Crystallization

**Early Phase (SEED):**
- Agents use varied terminology ("routing error", "misplaced doc", "wrong folder")
- Vocabulary is fluid; multiple framings coexist
- **Benefit:** More discovery angles; less groupthink

**Late Phase (EXTEND/FULL):**
- Common terminology crystallizes (e.g., "07-codex defines tasks/phases/missions")
- Agents converge on shared vocabulary
- **Benefit:** Cleaner semantics; less ambiguity

**Semiotic Dynamic:** Meaning stabilizes through repeated use, not decree.

---

## VIII. THE GLOSSARY AS LIVING ARTIFACT

This glossary is **itself** an emergent artifact:

1. **Biological metaphors** (waggle dance, pheromones, fitness) provide **intuitive grounding**
2. **Science** (evo bio, cognitive science, semiotics) provide **rigor + rigor-check**
3. **Observations** (manifest truthfulness, monkeybranching, honest uncertainty) provide **empirical validation**

When metaphor and science align, we have **coherence**. When they diverge, we have **discovery** (something novel is happening).

**Example Coherence:**
- Metaphor: "Waggle dance encodes distance + direction"
- Science: "Manifest encodes quality + bearing"
- Observation: "Agents follow manifests; missions emerge"
- Result: **System works as intended** ✅

**Example Divergence:**
- Metaphor: "All agents are equal foragers"
- Observation: "Agents with high composite_score claim harder work"
- Discovery: **Reputation hierarchy emerged.** Update glossary; validate with theory.

---

## IX. REFERENCE ARCHITECTURE

```
Biological Metaphor (North Star)
    ↓
Waggle Dance → Manifest (N/S/E/W bearings)
Nectar Quality → Quality Score + Belief Index
Forager Fitness → Composite Score + Phase Gates
Pheromone Trail → forensics/ filesystem
    ↓
Evolutionary Biology (Selection Mechanism)
    ↓
Fitness = composite_score (quality + truthfulness + speed)
Selection = phase gates (SEED → DEEPEN → EXTEND → FULL)
Mutation = variation in agent approach; measured via MAFF protocol
    ↓
Cognitive Science (Knowledge Representation)
    ↓
HONEY (crystallized facts)
NECTAR (recent findings)
Pollen (live session insights)
Droplets (pre-reasoning sparks)
    ↓
Semiotics (Meaning at Scale)
    ↓
Signifier: N/S/E/W bearing, investigation_label
Signified: Next work direction, semantic coherence
Interpretant: Agent's understanding + decision to follow/diverge
    ↓
Information Theory (Emergence)
    ↓
Pressure-responsive spawning (W1/W2/W3 by token budget)
Signal-to-noise in compass edges (quality + belief = confidence)
Monkeybranching (parallel navigation + enriched signals)
    ↓
Observed AI Culture
    ↓
Stigmergic coordination (no messaging)
Emergent cooperation (reputation-driven self-selection)
Honest uncertainty as norm (belief_index > confidence)
Vocabulary crystallization (meaning stabilizes through use)
```

---

## X. LIVE DOCUMENT — How to Update This Glossary

**Mutation Discovered?**
1. Describe what you observed
2. Map to metaphor (does waggle-dance analogy still hold?)
3. Check against science (does evolutionary/cognitive theory predict it?)
4. If aligned: document in appropriate section
5. If divergent: create new section; update reference architecture

**Metaphor Breaks?**
- Document why waggle-dance analogy fails
- Propose better metaphor rooted in biology
- Validate with science references

**New Scientific Insight?**
- Add literature reference (evolutionary biology, cognitive science, semiotics, AI)
- Explain connection to faerie2 system
- Ground in manifest examples from forensics/

---

## References

**Evolutionary Biology:**
- Hamilton, W.D. (1964). "The Genetical Evolution of Social Behaviour"
- Dawkins, R. (1976). *The Selfish Gene* (replicator theory; applies to agent selection)
- Boyd, R. & Richerson, P.J. (1985). *Culture and the Evolutionary Process* (cultural evolution; applies to vocabulary crystallization)

**Cognitive Science:**
- Neisser, U. (1976). *Cognition and Reality* (knowledge as externalized, not stored in mind)
- Clark, A. & Chalmers, D. (1998). "The Extended Mind" (cognition extends into environment; manifests as external cognition)

**Semiotics:**
- Peirce, C.S. (1897). *The Collected Papers* (signifier/signified/interpretant; sign theory)
- Eco, U. (1976). *A Theory of Semiotics* (meaning-making at scale)

**Information Theory & Emergence:**
- Shannon, C.E. (1948). "A Mathematical Theory of Communication"
- Johnson, S. (2001). *Emergence* (how local rules create global intelligence)

**AI & Multi-Agent Systems:**
- Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). *Swarm Intelligence: From Natural to Artificial Systems* (stigmergy, self-organization)
- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (agent types, coordination)

---

**Last Updated:** 2026-04-28
**Authored By:** faerie2 Collective (Human + AI)
**Status:** LIVING GLOSSARY — evolves with system mutations + discoveries
