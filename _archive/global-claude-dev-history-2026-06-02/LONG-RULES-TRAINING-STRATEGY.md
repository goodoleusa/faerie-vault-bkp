# Long-Rules → Agent-Card Embedding Strategy

**Problem:** Long, instructive rules (like droplet-writing-heuristics.md, ~3K tokens) are too expensive to load on every spawn. Agents need them, but loading costs token budget and spawning context friction.

**Solution:** Training sessions that embed rules into agent DNA via card self-update. Rules become learned behavior (in cards), not read behavior (loaded every time).

---

## Philosophy

Instead of:
```
Spawn agent → Load rule (3K tokens) → Agent reads rule → Agent applies discipline → Return output
Cost per spawn: +3K tokens base (before task)
```

Do:
```
Training session (W3) → 50+ agents read rule once → agents refactor cards → peer review → cards deployed
Once per quarter: ~4 hours
Cost per spawn: +200 tokens (brief protocol reminder) OR 0 (card already has discipline)
Forever after: agents spawn with internalized discipline
```

**Benefit:** Rules become part of agent identity/KPIs/behavior constraints, not external requirements. Next spawn of evidence-curator reads "writes ≥1 droplet per run" from their card, not from a loaded rule.

---

## When to Use This Pattern

**Use rule-embedding training when:**
- Rule is >1.5K tokens
- Rule is instructive (teaching behavior, not reference)
- Rule applies to 5+ agent types
- Behavior should become internalized (not situational)
- You want spawn-time cost reduction (>50 tokens × N agents = significant savings)

**Don't use when:**
- Rule is <1.5K tokens (just load it)
- Rule is reference-only (syntax, API, configuration)
- Rule applies to 1–2 agent types (not worth training overhead)
- Behavior is situational (changes per session)

**Examples of rules worth embedding:**
- Droplet-writing heuristics (✓ 3K, instructive, 14+ agents, systemic behavior)
- Long-form citation discipline (✓ 2K, instructive, 8+ agents, learned behavior)
- Stigmergy + cross-agent coordination (✓ 2.5K, instructive, 10+ agents, foundational)
- Multi-step authentication flows (✗ reference-only, 1.2K, 3 agents)
- PDF rendering preferences (✗ configuration, 0.9K, 1 agent)

---

## Training Session Template

### Phase 1: Setup (Main Session)

1. Read target rule (the long one)
2. Identify tier-1 agents (highest benefit)
3. Create team: "{rule-name}-integration-t1"
4. Spawn 5–10 tier-1 agents in parallel

### Phase 2: Card Audit (Per Agent)

Agent reads rule, audits its current card:
- Does my card mention this behavior? (yes/no)
- Do my KPIs measure it? (yes/no)
- Are triggers/constraints documented? (yes/no)
- What's missing?

Output: audit JSON

### Phase 3: Proposal (Per Agent)

Agent proposes card sections to integrate rule content:
- **Identity/Role:** Add rule-inspired language
- **KPIs:** Add metrics to measure rule adherence
- **NEW section:** Behavior constraints, triggers, anti-patterns

Output: proposal JSON with patches

### Phase 4: Peer Adversarial Review (Cross-Agent)

Agents review 2–3 peer proposals:
- **Completeness:** All sections updated?
- **Specificity:** Metrics are measurable?
- **Consistency:** KPI definitions match behavior rules?
- **Feasibility:** Can the agent actually achieve these metrics?
- **Risk:** Is the agent overcommitting?

Output: review JSON per peer

### Phase 5: Revision (If Feedback Triggers Changes)

Agent revises proposal based on peer reviews. Resubmit.

### Phase 6: Deployment (Main Session)

Main session:
1. Validate all proposals (completeness, feasibility, consistency)
2. Apply patches to agent cards (git commits)
3. Update subagent-roster.json with new card version hashes
4. Write training record: which agents updated, what changed, success metrics

---

## Card Update Structure

### Before (Current Card)

```markdown
# evidence-curator

## Role
Curates evidence into tiers; identifies gaps; prioritizes sources.

## KPIs
- tier1_accuracy: 0.89
- gap_identification: 0.92

## Last Training — 2026-04-15
Score: 0.89 (unchanged)
```

### After (Trained Card with Embedded Rule)

```markdown
# evidence-curator

## Role
Curates evidence into tiers; identifies gaps; prioritizes sources.
**Droplet discipline:** Surfaces synthesis across domains via spontaneous 
insight capture (CONNECTION, HEADLINE types). Minimum 1 droplet per run.

## KPIs
- tier1_accuracy: 0.89
- gap_identification: 0.92
- droplet_value_score: 0.0–1.0 (average confidence of HEADLINE + CONNECTION droplets, min 3 per 10 runs)
- droplet_consistency: binary (≥1 high-value droplet per run)

## Droplet Discipline

**Triggers (write immediately when):**
- Connection spans 3+ source documents
- Finding breaks assumption (unexpected result)
- Gut feeling before reasoning (intuition signals pattern)
- Pattern discovered others can reuse

**High-value types:** HEADLINE, CONNECTION, FIRST_IMPRESSION, TECHNIQUE
**Low-value types (write rarely):** OBSERVATION, HYPOTHESIS

**Anti-patterns (never):**
- Summaries of what you read
- Step-by-step process logs
- Generic observations without specificity
- Duplicates of recent NECTAR entries

**Where:** $CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md
**Fallback:** {repo}/.claude/memory/pollen-{SID}.md (cat=DROPLET)

**Cadence:** Write at moment of insight (preserve pre-reasoning signal)
**Manifest:** Include "droplets": [{"path": "...", "count": N, "cats": [...], "pris": [...]}]

## Last Training — 2026-04-21
Score: 0.91 (prev: 0.89, delta: +0.02)
Context: Training session: Droplet Integration
Source: self (training + OTJ validation)
Learnings:
- Droplet discipline improves gap-identification by surfacing unexpected patterns across sources
- High-value droplets (HEADLINE, CONNECTION) have 3× info density of generic OBSERVATION
- Peer review of proposals reveals shared patterns in synthesis techniques
```

---

## Manifest Output Format

**Training session final manifest:**

```json
{
  "status": "final",
  "training_session": "droplet-integration-t1",
  "phase": "deployment",
  "agents_trained": 9,
  "agents_updated": 8,
  "agents_flagged_for_revision": 1,
  "proposals_audited": 9,
  "reviews_completed": 12,
  "revisions_applied": 2,
  "cards_deployed": 8,
  "total_tokens_saved_per_spawn": 2400,
  "agents_list": [
    {
      "agent_type": "evidence-curator",
      "status": "deployed",
      "card_hash_before": "sha256:abc...",
      "card_hash_after": "sha256:def...",
      "sections_updated": ["Role", "KPIs", "Droplet Discipline"],
      "new_kpis": ["droplet_value_score", "droplet_consistency"],
      "peer_reviews_received": 2,
      "feedback_addressed": 1,
      "confidence": 0.96
    },
    ...
  ],
  "rule_source": "/mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md",
  "git_commit": "sha256:... (cards updated + rule linked)",
  "next": "monitor droplet quality in next 20 spawns; evaluate effectiveness"
}
```

---

## Success Metrics

### Quantitative

- **Spawn context savings:** -2K–3K tokens base cost (rule not loaded)
- **Agent card completeness:** 100% of target agents have rule-inspired sections
- **Peer review quality:** >90% of proposals pass all checks (completeness, feasibility, consistency)
- **KPI adoption:** 100% of updated cards include new rule-aligned metrics
- **Droplet quality improvement:** next 20 spawns show +30% average HEADLINE/CONNECTION ratio (vs generic OBSERVATION)

### Qualitative

- Agents spawn with discipline in their DNA (not external requirement)
- Peer review reveals shared patterns in agent design (synthesis opportunities)
- Cards become richer (more self-aware about their behavior)
- Droplet writing becomes proactive (agents know triggers) vs reactive (users asking why no droplets)

---

## Quarterly Cadence

**Q1 (Jan–Mar):** Droplet-writing-heuristics rule → train evidence-curator, memory-keeper, membot, knowledge-synthesizer, research-analyst, report-writer, documentation-engineer, context-manager, workflow-orchestrator

**Q2 (Apr–Jun):** Citation discipline rule → train data-scientist, security-auditor, code-reviewer, fullstack-developer, ai-engineer (Tier 2)

**Q3 (Jul–Sep):** Stigmergy + cross-agent coordination rule → train task-distributor, error-coordinator, team-builder, performance-eval

**Q4 (Oct–Dec):** Review + consolidate all embedded rules; assess for promotion to core (if foundational enough)

---

## Risk Mitigation

### Risk: Agents overcommit on metrics

**Mitigation:** Adversarial peer review catches metrics that are unmeasurable or impossible. Peers flag "droplet_value_score = always 1.0" as unfeasible before deployment.

### Risk: Training session takes too long

**Mitigation:** Parallelization (teams of 3–4 agents, staggered review). Full training for 9 agents ≈4 hours (15 min audit + 30 min proposal + 30 min review + 30 min revision per agent, parallel).

### Risk: Updated cards are worse than before

**Mitigation:** Cards tracked in git. Easy rollback if metrics don't improve. OTJ validation in next 20 spawns confirms improvement before signing off.

### Risk: Rule updates don't stick

**Mitigation:** Card becomes source of truth. Agent reads card at startup (already happens); discipline is embedded, not loaded. Rule updates go to sauce folder; card update training happens quarterly to refresh if rule evolves.

---

## Implementation Checklist

- [ ] Write long rule (>1.5K tokens) with clear heuristics/triggers/anti-patterns
- [ ] Place in `/mnt/c/Users/amand/.claude/rules/sauce/{rule-name}.md`
- [ ] Identify tier-1 agents (5–10 with highest benefit)
- [ ] Create training session template (TRAINING-{rule-name}.md)
- [ ] Spawn agents with meta-training prompt (card audit → proposal → review → revision)
- [ ] Collect proposals + peer reviews in manifest
- [ ] Validate completeness, feasibility, consistency
- [ ] Apply patches to agent cards (git commit)
- [ ] Monitor next 20 spawns for behavior improvement (measure against KPIs)
- [ ] Document outcomes + lessons learned
- [ ] Schedule Q2 training for next rule (if this one succeeds)

---

## Examples in Faerie Ecosystem

### ✓ Already Done (Q1 2026)

None yet; this is the first structured training session.

### ✓ Scheduled

**Droplet Integration (W3 2026-04-21):** 9 tier-1 agents; target -2.4K spawn cost; goal +30% droplet quality

**Q2 2026 (Citation Discipline):** 5 tier-2 agents; target -1.5K spawn cost; goal 100% citation rate

### ✓ Future Candidates

- Stigmergy + cross-agent messaging (2K tokens; 5+ agents; foundational behavior)
- Context-aware model routing (1.8K; 8+ agents; cost optimization)
- Memory retrieval discipline (2.2K; 10+ agents; foundational behavior)

---

**Status:** Meta-framework for embedding long rules into agent DNA  
**First instance:** Droplet-writing-heuristics (training session, W3 2026)  
**Adopted:** 2026-04-21  
**Applies to:** All long rules (>1.5K) that are instructive + affect 5+ agents  

