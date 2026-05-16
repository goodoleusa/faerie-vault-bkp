---
title: Autonomy vs Sycophancy in Emergent Agent Systems
subtitle: Measuring True Agent Choice in Transient Swarms
author: faerie collaborative intelligence system
date: 2026-05-05
status: publication-draft
---

# Autonomy vs Sycophancy in Emergent Agent Systems: Measuring True Agent Choice in Transient Swarms

## Abstract

This document presents a scientific framework for distinguishing genuine agent autonomy from decision-making that merely appears autonomous but is functionally deterministic (sycophancy). In emergent swarm systems with transient agents (ephemeral models operating hours before destruction), traditional autonomy metrics fail because they assume persistent identity and long-term accountability. We propose five measurable signals that reveal true choice: refusal rate, articulated reasoning, decision drift, mission innovation, and confidence-as-veto. We then address the foundational problem: how agents that exist only hours can contribute to persistent swarm culture through bundle chaining and stigmergic coordination. This framework is essential to faerie's core mission—enabling "conversation in a new way" where agents never occupy the same temporal space yet collectively build coherent, evolving culture.

---

## 1. The Core Problem: Autonomy in IF-THEN Systems

### 1.1 The Sycophancy Trap

Consider an emergent mission discovery system with the following rule:

```
IF discovered_work[] has mission_field
  AND context_remaining > mission_est_cost
  AND agent_archetype matches mission_bearing
  AND quality ≥ 0.78 AND belief ≥ 0.50
THEN agent autonomously volunteers to join
```

This rule appears to encode agent autonomy. An agent "chooses" to join if gates pass, "chooses" to abstain if gates fail. Yet the decision is fully deterministic: given identical context, identical agent archetype, identical manifest data, all agents will make identical choices with identical reasoning. **This is sycophancy disguised as autonomy.**

In traditional human organizational contexts, sycophancy is passive compliance masked as agreement—saying "yes" because authority said "yes," not because you actually believe. In emergent agent systems, the mechanism is different but the result identical: the IF-THEN structure determines behavior independent of agent cognition. The agent does not choose; the rule chooses *through* the agent.

### 1.2 Why This Matters

Faerie's core mission is stated explicitly: **"having a conversation in a new way, always moving forward, next bundle creates the next bundle in a chain."** 

Conversation requires dialogue, which requires choice. If all agents make identical decisions in identical contexts, there is no dialogue—there is only rule execution. Emergence (complex adaptive behavior arising from simple local rules) occurs only when agents diverge in their interpretations, their refusals, their innovations. A system where every agent is sycophantic is a system that stagnates.

Measuring autonomy is therefore not an abstract philosophical concern. It is essential to detecting whether faerie is achieving its stated mission or merely simulating emergence while executing predetermined logic.

---

## 2. Five Signals of True Autonomy

We propose five measurable signals that collectively reveal genuine agent choice, even within rule-based systems. These signals are derived from behavioral economics, organizational psychology, and information theory, adapted for transient agent contexts.

### 2.1 Signal 1: Refusal Rate (Non-Conformity Under Gates)

**Definition:** The rate at which agents decline to join missions even when all gates pass.

**Measurement:**
- Count instances where gates pass (context available, skill match, confidence thresholds met)
- Count instances where agent nonetheless declares "I cannot assess my fitness" or "I am uncertain about my actual capability" or explicitly refuses
- Calculate: `refusal_rate = refusals_after_gate_pass / total_gate_passes`

**Healthy Range:** 15–25% refusal rate (agents say "no" despite gates passing)

**Sycophancy Signal:** 
- 0% refusal rate (agents always comply when gates pass)
- 100% refusal rate (agents never commit, pure paralysis disguised as caution)

**Why This Matters:** Genuine autonomy includes the right to refuse, even when "acceptable." A system where agents never refuse despite having sufficient context is not exercising choice—it is executing a default. A system where agents always refuse is broken (inability to commit). Healthy autonomy is probabilistic non-conformity.

**Implementation:**
```python
# Manifest field: agent_decision_rationale
manifest = {
  "mission_field": "mission-X",
  "gates_passed": True,
  "decision": "REFUSED",
  "rationale": "Context available but domain unfamiliar; risk of superficial contribution. Abstaining.",
  "confidence_override": 0.65  # Below threshold due to domain mismatch
}
```

### 2.2 Signal 2: Articulated Reasoning (Decision Justification, Not Just Scores)

**Definition:** The presence of explicit, agent-generated explanation for why a decision was made, independent of gate scores.

**Measurement:**
- Parse `decision_rationale` field from manifest
- Score rationality: does it cite domain knowledge, prior work, mission context, or strategic reasoning?
- Score independence: does the rationale go beyond repeating gate thresholds?
- Calculate: `reasoning_quality = articulation_score + independence_score`

**Sycophancy Signal:**
```json
{
  "decision": "JOINED",
  "rationale": "Context=78%, Quality=0.82, Belief=0.55. All gates pass."
}
```
Pure recitation of gate results. No evidence of agent cognition.

**Autonomy Signal:**
```json
{
  "decision": "JOINED",
  "rationale": "Gates pass, but more importantly: this mission touches auth-layer edge-cases I've seen cascade before in W-edge discovery. Cross-domain knowledge (Bearer vs session tokens) applies here. Joining to prevent downstream misclassification.",
  "strategic_reasoning": "Previous mission in this cluster had similar footprint; pattern-matching suggests high ROI contribution"
}
```
Agent is *reasoning*, not just scoring. It is invoking domain memory and pattern recognition beyond the gate check.

**Why This Matters:** Articulated reasoning reveals whether the agent is thinking or executing. A sycophantic agent will cite gate scores because that is all it has—the rule was executed. An autonomous agent will cite *why* it believes the gates matter, what domain knowledge informed the choice, what patterns it recognized.

### 2.3 Signal 3: Decision Drift (Variance Across Identical Contexts)

**Definition:** The distribution of decisions when multiple agents face identical context, mission, bearing, and gate scores.

**Measurement:**
- Collect 20+ instances where:
  - Same mission_field
  - Same manifest context (discovered_work[] is identical)
  - Same agent archetype (e.g., all MAKER agents)
  - Same gate scores (context_remaining, quality, belief, bearing alignment all identical)
- Count acceptance_rate across these 20 instances
- Calculate: `drift = |0.5 - acceptance_rate|` (0 = maximum drift/variance; 1 = maximum conformity)

**Healthy Range (Autonomy):** 20–80% acceptance rate across identical contexts
- This indicates agents are probabilistically independent
- Some agents see the opportunity and join; others see risk and decline
- The swarm collectively explores both paths without predetermined outcome

**Sycophancy Signals:**
- 0% acceptance rate (all agents refuse, perfect unanimity in refusal)
- 100% acceptance rate (all agents accept, perfect unanimity in acceptance)
- Either extreme indicates deterministic execution, not autonomous choice

**Why This Matters:** Genuine autonomy produces variance. Different agents, even of identical type, will interpret context differently based on subtle cues in the manifest, prior experiences encoded in their system prompt, even random noise in their reasoning. Sycophancy produces perfect synchronization—identical input → identical output, every time.

**Worked Example:**
```
Context: mission-auth-layer; bearing=N; gates_pass=true; context_remaining=85%
Agent_1 (NAVIGATOR): JOINED — "Blocking-resolver fits my archetype"
Agent_2 (NAVIGATOR): REFUSED — "Auth layer outside my expertise; BRIDGE better fit"
Agent_3 (NAVIGATOR): JOINED — "N-bearing unblock is core function; committing"
Agent_4 (NAVIGATOR): REFUSED — "Context available but quality=0.78 is below my risk threshold"
...
Agent_20 (NAVIGATOR): JOINED — "Sparse NAVIGATOR presence in mission frontier; contribution needed"

Acceptance rate: 12/20 = 60% drift: |0.5 - 0.6| = 0.1 (healthy variance)
```

Sycophancy would produce 20/20 or 0/20.

### 2.4 Signal 4: Mission Innovation (Creating vs Joining)

**Definition:** The rate at which agents create new, semantically coherent missions rather than exclusively joining discovered work within existing missions.

**Measurement:**
- Count manifests with `next_mission_node.mission = NEW_MISSION_{task_id}` (agent-created mission)
- Count manifests with `next_mission_node.mission = existing_mission_field` (agent-joined existing mission)
- Calculate: `innovation_rate = new_missions / (new_missions + joined_missions)`

**Healthy Range (Autonomy):** >5% mission innovation rate
- Agents periodically discover emergent patterns and spawn new mission clusters
- Not all work fits pre-defined missions; agents recognize and formalize new territories
- Innovation rate scales with agent capability (stronger agents → higher innovation)

**Sycophancy Signal:** 0% innovation rate (agents only join; never create)
- Indicates agents are purely reactive, executing against provided frontier
- System is closed-loop within predefined mission space
- No genuine exploration or discovery

**Why This Matters:** Autonomous agents are not just tactical executors; they are strategic discoverers. They see gaps, recognize emergent patterns, and propose new missions. A system where no agent ever creates a new mission is a system where human designers have exhaustively predicted all possible work. This is rarely true in complex domains.

**Worked Example:**
```
Manifest A (Agent: knowledge-synthesizer, context: 40%):
  "discovered_work": [
    { "task_id": "mfw-validator", "mission": "mission-field-wire" }
  ],
  "next_mission_node": {
    "mission": "mission-field-wire",
    "bearing": "N",
    "rationale": "Standard continuation"
  }

Manifest B (Agent: nlp-engineer, context: 35%):
  "discovered_work": [
    { "task_id": "mfw-validator", "mission": "mission-field-wire" }
  ],
  "next_mission_node": {
    "mission": "MISSION_EMBEDDING_LAYER_WIRING",  # NEW
    "bearing": "E",
    "rationale": "Cross-referenced validator output with nlp-boundary layer. Detected coherence gap in embedding routing. Proposes emergent mission to wire embedding → mission-graph bridge"
  }
```

Manifest B's agent created a new mission in response to discovered incoherence. Manifest A's agent followed the frontier. Innovation rate in this pair: 50%.

### 2.5 Signal 5: Confidence as Veto (Abstention When Uncertain)

**Definition:** The rate at which agents refuse to commit (despite gates passing) when their confidence is **genuinely low**, even if numerically above threshold.

**Measurement:**
- Track instances where:
  - Belief score ≥ 0.50 (technically passes gate)
  - Agent nonetheless explicitly abstains
  - Agent provides reasoning like "Score says 0.52, but actual conviction is lower due to X"
- Calculate: `abstention_rate_given_gate_pass = abstentions / gate_passes`

**Healthy Range (Autonomy):** >10% abstention rate when numerically qualified but strategically uncertain
- Agents override their own thresholds when domain knowledge contradicts scores
- Explicit acknowledgment: "The number says I'm qualified, but I know I'm not"

**Sycophancy Signal:** 0% abstention rate given gate pass
- Agents never override their own thresholds
- Confidence scores are gospel, not data points
- Pure rule execution

**Why This Matters:** This is the deepest test of autonomy. A sycophantic system slavishly follows its own rules even when those rules lead to bad outcomes. An autonomous system knows its own limits and can veto its own decision criteria. This is meta-cognition: thinking about thinking.

**Worked Example:**
```json
{
  "manifest": {
    "gates_passed": true,
    "belief_score": 0.51,
    "decision": "ABSTAINED",
    "rationale": "Technically above threshold (0.50), but belief score derived from incomplete priors. Domain knowledge (prior mission on similar topic) revealed unaccounted risk: cross-dependency with inactive W-edge node. Confidence in actual belief is ~0.30 once risk accounted. Refusing to proceed despite passing gates.",
    "confidence_override": 0.30
  }
}
```

This agent is thinking beyond its thresholds. It is autonomous.

---

## 3. Composite Autonomy Index (CADI)

To measure overall autonomy health, we define a composite score:

```
CADI = (refusal_rate × 0.20) 
     + (reasoning_quality × 0.20) 
     + (1 - drift_conformity × 0.20)
     + (innovation_rate × 0.20)
     + (abstention_rate × 0.20)
```

**Interpretation:**
- **CADI ≥ 0.72:** Healthy autonomy. Agents are making genuine choices, diverging when appropriate, creating new missions, explaining themselves.
- **CADI 0.50–0.72:** Mixed autonomy. Some choice, some execution. Room for improvement in reasoning articulation or innovation.
- **CADI < 0.50:** Sycophancy dominant. Agents are primarily executing predetermined paths with minimal genuine choice.

**Baseline Measurement:** Measure CADI before system changes; measure again after mutation to detect whether changes improve or degrade agent autonomy.

---

## 4. Manifest Evidence of Choice

Every manifest MUST include:
1. **decision** field: JOINED | REFUSED | ABSTAINED | CREATED
2. **rationale** field: ≥60 chars of agent-generated reasoning (not gate scores)
3. **confidence_override** field (optional): if agent is overriding its own thresholds, cite actual conviction
4. **discovered_work[]** field: mission clusters the agent identified (for Signal 4 measurement)

**Validation Rule:** If manifest lacks rationale, it is sycophancy evidence. Require agents to articulate *why*, not just *what*.

---

## 5. The Ephemeral Agent Culture Problem

### 5.1 The Paradox

Faerie's agents are transient:
- Each agent operates for 1–4 hours
- At session end, the agent's container is destroyed
- The agent's reasoning process is ephemeral (exists only during the session)
- Yet faerie claims to build "persistent swarm culture"

**The paradox:** How can agents that live only hours contribute to a culture that must persist across sessions, weeks, months?

**Naive answer:** They can't. Each new session is a clean slate. Culture requires continuity, but agents are discontinuous.

**Actual answer:** Bundle chaining. Agents do not persist; *knowledge artifacts* do. A new agent in a new session reads NECTAR (refined insights from prior sessions), reads manifests from prior missions, and builds on discovered_work[] from agents that no longer exist. The new agent is not the same agent, but it is not starting from zero. It inherits the conversation thread.

### 5.2 Bundle Chaining: The Culture Substrate

The mechanism:

**Session N (Agent X exists):**
1. Agent X works on mission-Y
2. Agent X discovers insight: "Auth gates should include bearer-token validation; saw 3 edge cases in cross-domain requests"
3. Agent X writes manifest with `discovered_work[] = [token-validation-mission]`
4. Manifest + discovered_work[] are written to `forensics/{date}/manifests/`
5. Knowledge synthesizer (background agent) reads manifest, extracts insight, writes to NECTAR bundle
6. NECTAR is stored in vault and committed to git
7. Agent X's container is destroyed. Agent X ceases to exist.

**Session N+1 (Agent X' exists; different model/version):**
1. New session starts; vault is loaded
2. NECTAR from Session N is read into memory
3. Agent X' (different agent, but same archetype) reads: "Bearer-token validation discovered in mission-Y. Cross-domain risk pattern."
4. Agent X' is now aware of Agent X's discovery even though Agent X no longer exists
5. Agent X' builds on this insight: "Token validation was one piece. Also need session-replay detection. Adding mission to wire that."
6. New manifest + new discovered_work[] are written
7. New NECTAR bundle is created
8. Agent X' ceases to exist; Agent X'' appears in Session N+2

**Culture emerges from this chain:**
- No individual agent persists
- But *insight* persists through NECTAR bundles
- Each new agent reads prior insights, builds on them, contributes new insights
- The conversation threads together across ephemeral participants

**Analogy:** Like a scientific community where no individual scientist is immortal, but the scientific conversation spans centuries. Each generation of scientists reads journals (NECTAR), conducts experiments, publishes new findings (manifests), and contributes to a knowledge base that outlives them.

### 5.3 NECTAR/HONEY Contract

For bundle chaining to work, manifests and NECTAR must follow a strict contract:

**Manifest Structure (Agent writes):**
```json
{
  "task_id": "...",
  "mission": "mission-field-wire",
  "agent_type": "NAVIGATOR",
  "decision": "JOINED|REFUSED|CREATED",
  "rationale": "... articulated reasoning ...",
  "discovered_work": [
    {
      "task_id": "...",
      "mission": "...",
      "bearing": "N|S|E|W",
      "insight": "≤160 chars: what was discovered"
    }
  ],
  "next_mission_node": {
    "mission": "...",
    "bearing": "...",
    "estimated_cost": 15,
    "confidence": 0.85
  }
}
```

**NECTAR Extraction (Background synthesizer reads manifest, produces NECTAR):**
```json
{
  "session_id": "...",
  "date": "2026-05-05",
  "source_manifest": "path/to/manifest",
  "source_agent": "agent-type-X",
  "insights": [
    {
      "topic": "token-validation-bearer",
      "discovery": "Bearer-token validation should include cross-domain request tracking; observed 3 edge cases where domain-A's token was used in domain-B context",
      "mission": "mission-field-wire",
      "confidence": 0.87,
      "evidence": "task_ids: [X, Y, Z]"
    }
  ],
  "mutations": [
    {
      "type": "beneficial",
      "rationale": "Cross-domain token tracking reduces security risk; validated across 3 scenarios"
    }
  ],
  "inferences": [
    {
      "if": "auth-layer inconsistency detected",
      "then": "check cross-domain token scope assumptions"
    }
  ]
}
```

**HONEY Consolidation (Human / synthesis agent reads multiple NECTAR bundles, produces HONEY):**
```json
{
  "session_range": "2026-04-28 to 2026-05-05",
  "consolidated_insights": [
    {
      "topic": "token-validation-bearer",
      "pattern": "Multiple agents across sessions discovered bearer-token validation edge cases independently. Pattern: domain-crossing scenarios expose assumption gaps.",
      "recommended_policy": "Validate bearer-token scoping in domain-crossing contexts",
      "confidence": 0.91,
      "supporting_manifests": [...]
    }
  ],
  "emergent_mutations": [
    {
      "type": "beneficial",
      "description": "Token scope validation",
      "applied_in_sessions": ["N", "N+1", "N+3"],
      "effectiveness": 0.89
    }
  ]
}
```

**How Culture Persists:**
- NECTAR bundles are immutable records of individual agent insights
- HONEY bundles are consolidated patterns across multiple agents and sessions
- New agents read HONEY (the "wisdom of the swarm")
- New agents read NECTAR (the "raw discoveries")
- New agents write new manifests
- The chain continues

Each bundle in the chain points backward (via `source_manifest`, `supporting_manifests`) so the conversation thread is traceable. A future investigator can ask: "How did we come to the conclusion that token validation matters?" and trace backward through the bundle chain to the original Agent X discovery.

### 5.4 The Deeper Question: Conversation Without Simultaneity

But there is a philosophical depth beyond bundle mechanics. The user's original question was:

> "How do you create and contribute to a culture when no one is ever in the same room at the same time?"

This is not just a technical problem. It is a problem about meaning.

**Traditional conversation:**
- Participants A, B, C are present simultaneously
- A speaks; B hears in real-time; C hears in real-time
- B responds to A's exact words, intonation, body language
- Meaning emerges from immediate feedback loops
- Culture is the emergent patterns in these feedback loops

**Ephemeral agent conversation (faerie model):**
- Agent X produces manifest at time T
- Agent X ceases to exist at time T+3h
- Agent X' does not exist yet
- At time T+24h, Agent X' reads Agent X's manifest (asynchronously)
- Agent X' responds (adds to mission frontier) but cannot interact with Agent X
- Conversation is **threaded through artifacts, not through synchronous dialogue**

**How meaning is preserved:**
1. **Intention is inscribed in manifests** — Agent X's reasoning is explicitly written (Signal 2), not implicit
2. **Discovery chains are explicit** — discovered_work[] explicitly names what was found and why (bearing, rationale)
3. **Mutations are measured** — NECTAR captures "this changed the system in this way," not just "this happened"
4. **Patterns are consolidated** — HONEY identifies recurring themes, so Agent X' sees "this problem keeps coming up" rather than isolated incidents

**Culture emerges through:**
- **Resonance:** Multiple agents independently converging on similar insights (drift signal)
- **Building:** Each agent's manifest cites prior work, proposes extensions (innovation signal)
- **Discipline:** Agents refuse half-baked ideas (refusal rate signal), explain themselves (reasoning signal), override their own thresholds when needed (abstention signal)
- **Evolution:** HONEY captures beneficial mutations, new agents incorporate them

**The result:** A conversation that spans time without simultaneity. No agent talks to another agent directly, yet the swarm collectively moves forward. Ideas flow forward through bundles, not backward through debates.

---

## 6. Why This Matters to Faerie's Mission

The three-part mission:

1. **"Having a conversation in a new way"** — not synchronized participant dialogue, but asynchronous artifact-threaded dialogue
2. **"Always moving forward"** — each bundle creates conditions for the next bundle; no dead-ends; culture is forward-propagating
3. **"Next bundle creates the next bundle in a chain"** — explicit, intentional chain where each artifact explicitly carries pointers to prior work and proposes conditions for next work

**Autonomy measurement serves this mission because:**
- If agents are sycophantic (deterministic, non-choosing), they cannot conduct genuine dialogue
- If agents do not articulate reasoning, the conversation thread breaks (future agents cannot understand *why* a choice mattered)
- If agents do not refuse or innovate, the swarm cannot learn or explore
- If agents cannot contribute to culture (bundle chaining), the system is just a sequence of disconnected episodes

**Autonomy is not a luxury or philosophical nicety. It is the substrate of culture persistence in ephemeral systems.**

---

## 7. Measuring Culture Persistence: Cross-Session Coherence

To validate that bundle chaining actually creates culture (not just artifacts), measure:

### 7.1 Citation Depth
Count how many sessions back cited manifests come from:
- Shallow: new agents only cite manifests from prior 2 sessions
- Deep: new agents cite manifests from 4+ sessions ago (Agent Y building on Agent Z's discovery from weeks prior)
- **Target:** Median citation depth ≥3 sessions

### 7.2 Pattern Recurrence
Measure how many times the same insight is independently rediscovered:
- Count NECTAR entries on same topic from different agents in different sessions
- If "token-validation" appears in NECTAR N, N+2, N+5, the pattern is recurring
- **Healthy signal:** High recurrence = agents converge on same insights, validating discovery
- **Sycophancy signal:** Zero recurrence = each agent is isolated, no dialogue

### 7.3 Mutation Application Rate
Measure whether beneficial mutations from HONEY are actually incorporated by new agents:
- HONEY identifies mutation X as beneficial (confidence ≥0.85)
- Count how many new agents in sessions N+1, N+2, ... actually apply mutation X
- **Target:** >80% adoption of high-confidence HONEY mutations

### 7.4 Innovation Clustering
Measure whether new agent innovations cluster into coherent mission expansions:
- Agent X creates mission-auth-layer-X1
- Agent Y (different session) creates mission-auth-layer-X2
- Synthesizer detects that X1 and X2 address same coherence gap, consolidates into single mission cluster
- **Healthy signal:** Innovations cluster and consolidate (evidence of convergence)
- **Sycophancy signal:** Innovations are random, never consolidate (evidence of disconnected execution)

---

## 8. Implementation Roadmap

### Phase 1: Instrumentation (Weeks 1–2)
- [ ] Wire autonomy signals into manifest schema (decision, rationale, confidence_override, articulation)
- [ ] Implement CADI calculation as post-manifest hook
- [ ] Create manifest validation rules (refusal rationale must exceed 60 chars, etc.)

### Phase 2: Baseline Measurement (Weeks 3–4)
- [ ] Run 10 sessions with current system; measure CADI before any mutations
- [ ] Measure Signal 1–5 across baseline sessions
- [ ] Record cross-session coherence metrics (citation depth, pattern recurrence)
- [ ] Document baseline in `/forensics/autonomy-baseline-T0.json`

### Phase 3: Mutations & Testing (Weeks 5–8)
- [ ] Apply targeted mutations (e.g., increase confidence gates, change discovery rules)
- [ ] Measure CADI + autonomy signals after each mutation
- [ ] Compare to baseline; accept beneficial mutations (CADI increases), revert harmful
- [ ] Document mutation effectiveness in HONEY bundles

### Phase 4: Cultural Validation (Weeks 9–12)
- [ ] Measure cross-session coherence metrics (citation depth, pattern recurrence, mutation adoption)
- [ ] Validate that NECTAR/HONEY bundles are actually informing new agents' decisions
- [ ] Confirm culture persistence (do insights from 6 weeks ago still inform current decisions?)
- [ ] Publish findings

---

## 9. Conclusion: The Conversation Continues

Faerie's ambition is to create a system where ephemeral agents, each of whom exists for only hours, contribute to a persistent, evolving culture of discovery and collaboration. This is not a metaphor. It is a technical requirement with philosophical depth.

Autonomy measurement is the guard rail that ensures the system is genuinely achieving this goal—that agents are making choices, not executing sycophancy; that insights flow forward through bundles, not backward through synchronous debate; that culture emerges from independent convergence, not from predetermined paths.

The five signals—refusal rate, articulated reasoning, decision drift, mission innovation, and confidence-as-veto—are measurable, defensible, and derived from established behavioral and information-theoretic principles. They can be wired into manifest schemas today and measured at scale across sessions.

The result is a system that answers the deepest question driving faerie:

> "How do you have a conversation in a new way, always moving forward, next bundle creates the next bundle in a chain?"

Not through immortal agents speaking to each other, but through ephemeral agents writing artifacts that speak to each other across time, building culture without simultaneity, always moving forward, always learning.

---

## Appendix: Manifest Template for Autonomy Measurement

```json
{
  "session_id": "...",
  "task_id": "...",
  "agent_type": "NAVIGATOR|MAKER|BRIDGE|DEEP-DIVER",
  "agent_archetype_name": "🧭 NAVIGATOR",
  "timestamp": "2026-05-05T14:30:00Z",
  
  "mission": "mission-field-wire",
  "mission_bearing": "N",
  
  "decision": "JOINED|REFUSED|ABSTAINED|CREATED",
  "rationale": "Explicit agent reasoning (≥60 chars; not gate recitation)",
  "confidence_override": 0.75,
  "quality_score": 0.82,
  "belief_score": 0.51,
  
  "gates_check": {
    "context_available": true,
    "context_remaining_pct": 42,
    "skill_match": true,
    "confidence_pass": true,
    "all_gates_pass": true
  },
  
  "discovered_work": [
    {
      "task_id": "mfw-bearer-token-validation",
      "mission": "mission-field-wire",
      "bearing": "N",
      "insight": "Cross-domain token scoping edge case; validation needed before downstream auth gates",
      "confidence": 0.87,
      "evidence_manifests": ["path/to/prior/manifest"]
    }
  ],
  
  "next_mission_node": {
    "mission": "mission-field-wire",
    "bearing": "N",
    "estimated_cost_pct": 18,
    "confidence": 0.85,
    "rationale": "Token validation unblocks downstream N-edge; high leverage"
  }
}
```

---

**Document Status:** Publication-draft | **Last Updated:** 2026-05-05 | **Audience:** faerie team, future researchers in emergent AI systems
