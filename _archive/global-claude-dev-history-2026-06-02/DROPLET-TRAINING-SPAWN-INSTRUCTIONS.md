# Droplet-Integration Training Session — Spawn Instructions

**Goal:** Train 9 tier-1 agents to embed droplet-writing discipline into their own cards via meta-training session.

**When:** W3 (deep synthesis phase). ~4 hours parallelized.

**Outcome:** 9 agent cards updated + peer-reviewed; next spawn of these agents inherits droplet discipline without loading rule (~+2.4K tokens saved per spawn).

---

## Pre-Spawn Checklist

- [ ] Read `/mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md` (framework)
- [ ] Read `/mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md` (session template)
- [ ] Read `/mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md` (the rule being embedded)
- [ ] Confirm team name: `droplet-integration-t1`
- [ ] Confirm 9 tier-1 agents ready to spawn
- [ ] Output directory prepared: create `/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/{audit,proposals,reviews,revisions}/`

```bash
mkdir -p /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/{audit,proposals,reviews,revisions}
```

---

## Spawn Pattern

Create team first, then spawn 9 agents in parallel as teammates.

### 1. Create Team

```python
TeamCreate(
  team_name="droplet-integration-t1",
  description="Meta-training: 9 agents read droplet-writing rule, audit own cards, propose updates, peer-review each other's proposals",
  agent_type="documentation-engineer"  # optional; not used here since agents are diverse
)
```

### 2. Spawn 9 Tier-1 Agents (Parallel)

Each agent gets the same meta-training prompt, parameterized by agent_type.

**Template:**

```python
Agent(
  subagent_type="documentation-engineer",  # ← proxy type (documentation-engineer handles analysis + writing)
  team_name="droplet-integration-t1",
  name="evidence-curator",  # ← actual agent type being trained
  description="Training: evidence-curator audits card + proposes droplet discipline updates",
  prompt="""## META-TRAINING SESSION: DROPLET INTEGRATION

You are evidence-curator. You are reviewing and refactoring your own agent card to internalize 
droplet-writing discipline. This is a meta-session where agents improve themselves, then peer-review 
each other's proposals.

### Context

**Rule being embedded:** /mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md
**Your current card:** /mnt/d/0LOCAL/.claude/agents/evidence-curator.md
**Training template:** /mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md
**Strategy doc:** /mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md

---

### PART 1: CARD AUDIT (15 min)

Read the droplet-writing-heuristics rule.
Read your current card.

Self-audit:
1. Does your card mention droplets? (yes/no)
2. Does your KPI section include droplet quality metrics? (yes/no)
3. Do your behavior/constraints explain WHEN you write droplets? (yes/no)
4. Are anti-patterns documented? (yes/no)
5. What's missing that would improve your droplet discipline?

Output JSON to: /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/audit/evidence-curator-audit.json

```json
{
  "agent_type": "evidence-curator",
  "ts": "{ISO8601}",
  "has_droplet_protocol": false,
  "has_droplet_kpi": false,
  "has_behavior_rules": false,
  "gaps": ["missing explicit droplet triggers", "no anti-patterns documented", "KPIs don't measure droplet quality"],
  "readiness": "ready-for-update"
}
```

---

### PART 2: CARD PROPOSAL (30 min)

Based on the rule, propose updated card sections:

1. **Role** — add droplet discipline language
2. **KPIs** — add droplet_value_score + droplet_consistency metrics
3. **NEW: Droplet Discipline** — behavior rules, triggers, anti-patterns

Output JSON to: /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/proposals/evidence-curator-proposal.json

```json
{
  "agent_type": "evidence-curator",
  "ts": "{ISO8601}",
  "sections_updated": ["Role", "KPIs", "Droplet Discipline"],
  "patches": [
    {
      "section": "Role",
      "old": "Curates evidence into tiers; identifies gaps; prioritizes sources.",
      "new": "Curates evidence into tiers; identifies gaps; prioritizes sources. Droplet discipline: surfaces synthesis across domains via spontaneous insight capture (CONNECTION, HEADLINE). Minimum 1 droplet per run."
    },
    {
      "section": "KPIs",
      "old": "- tier1_accuracy: 0.89\\n- gap_identification: 0.92",
      "new": "- tier1_accuracy: 0.89\\n- gap_identification: 0.92\\n- droplet_value_score: 0.0–1.0 (average confidence of HEADLINE + CONNECTION droplets, min 3 per 10 runs)\\n- droplet_consistency: binary (≥1 high-value droplet per run)"
    },
    {
      "section": "Droplet Discipline",
      "new": "[complete new section with triggers, types, anti-patterns, where, format, cadence]"
    }
  ],
  "rationale": "Embedding droplet discipline into my role and KPIs makes it part of my identity, not an external requirement. Peer review will validate feasibility.",
  "confidence": 0.92
}
```

---

### PART 3: PEER ADVERSARIAL REVIEW (30 min)

Wait for all 9 agents to submit proposals (you'll be notified via team task list).

Then: Read proposals from 2–3 assigned peers. For each peer, adversarial review:

**Completeness:** Does proposal cover Role + KPI + Discipline?
**Specificity:** Are droplet triggers specific (not generic)?
**Consistency:** Do KPI metrics match the discipline rules?
**Feasibility:** Can agent measure droplet_value_score? (Is it well-defined?)
**Risk:** Is agent overcommitting? (Are metrics achievable?)

Output JSON to: /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/reviews/evidence-curator-reviews-{peer_type}.json

```json
{
  "reviewer_agent": "evidence-curator",
  "reviewed_agent": "memory-keeper",
  "ts": "{ISO8601}",
  "completeness": "pass",
  "specificity": "pass",
  "consistency": "pass",
  "feasibility": "flag — droplet_value_score needs clearer definition",
  "risk_assessment": "medium — KPI achievable but requires consistent droplet writing",
  "recommendation": "revise — ask peer to clarify metric calculation before deploy",
  "feedback": [
    "Proposal structure is strong; Role + KPI + Discipline sections are clear",
    "Flagging: droplet_value_score definition says 'average confidence' but doesn't specify who assigns confidence (agent self-score? main session audit?)",
    "Anti-patterns section is good; specific examples help",
    "Concern: if agent doesn't write ≥1 droplet per run, metrics hit 0 immediately — ensure discipline triggers are clear"
  ]
}
```

---

### PART 4: REVISION (if needed) — 30 min

Read peer feedback on YOUR proposal (via team notifications).

If peers flagged feasibility/clarity issues, revise:

```json
{
  "agent_type": "evidence-curator",
  "ts": "{ISO8601}",
  "revision_of": "evidence-curator-proposal (2026-04-21T15:30:00Z)",
  "changes_applied": [
    "Clarified droplet_value_score: calculated by agent (self-score per HEADLINE/CONNECTION confidence), validated in next manifest by evaluator if training triggered",
    "Added constraint: droplet_consistency metric hits 0 if <1 high-value droplet per run (force discipline)"
  ],
  "patches": [
    {
      "section": "KPIs",
      "old": "- droplet_value_score: 0.0–1.0 (average confidence of HEADLINE + CONNECTION droplets, min 3 per 10 runs)",
      "new": "- droplet_value_score: 0.0–1.0 (agent self-scores HEADLINE/CONNECTION droplets 0–1 per write; average across run; min 3 droplets per 10 runs to calculate. Metric = (sum of scores) / count. Validated by evaluator if training triggered. 0 if <1 high-value droplet per run.)"
    }
  ],
  "confidence_after_revision": 0.96
}
```

Output to: /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/revisions/evidence-curator-revised.json

---

## TEAM COORDINATION

**Shared task list:** ~/.claude/tasks/droplet-integration-t1/
- Tasks auto-created for phases: audit, proposal, review, revision
- Claim tasks as you complete phases
- Update status as you progress

**Cross-agent coordination (stigmergy only — SendMessage denied per HONEY sys00031):** Update the shared status JSON file on every phase transition; peers poll it on task boundaries. Drop a CONNECTION droplet if your audit sparks an insight relevant to other agents' cards.

**Primary pattern:** Write status to shared JSON file
```
/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-status.json
{
  "phase": "peer-review",
  "agents_audit_complete": 9,
  "agents_proposal_complete": 9,
  "agents_review_in_progress": 5,
  "agents_revision_pending": 1,
  "ts_last_update": "{ISO8601}"
}
```

---

## MANIFEST CONTRACT

Manifest path: /mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-evidence-curator-result.json

Write progressively:
1. First: {"status": "in-progress", "phase": "audit", "ts": "..."}
2. Audit done: {"status": "in-progress", "phase": "proposal", ...}
3. Proposal done: {"status": "in-progress", "phase": "peer-review", ...}
4. Reviews done: {"status": "in-progress", "phase": "revision", ...}
5. Final: {"status": "final", "phase": "deployment-ready", ...}

Final manifest example:
```json
{
  "status": "final",
  "agent": "evidence-curator",
  "ts": "{ISO8601}",
  "wave": 3,
  "team_name": "droplet-integration-t1",
  "phase": "deployment-ready",
  "audit_findings": {...},
  "proposal": {...},
  "peer_reviews_received": 2,
  "revisions_applied": 1,
  "final_proposal": {...},
  "proposal_confidence": 0.96,
  "dashboard_line": "evidence-curator card audit+proposal+review complete; droplet discipline ready for deployment",
  "files_written": [
    "/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/audit/evidence-curator-audit.json",
    "/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/proposals/evidence-curator-proposal.json",
    "/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/reviews/evidence-curator-reviews-memory-keeper.json",
    "/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/reviews/evidence-curator-reviews-membot.json",
    "/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/revisions/evidence-curator-revised.json"
  ],
  "next": "main session validates all 9 proposals + applies patches to agent cards"
}
```

---

## SUCCESS CRITERIA (for main session to check)

After all 9 agents return manifests:

- [ ] All 9 audits complete (all agents found gaps → readiness = ready-for-update)
- [ ] All 9 proposals submitted (cover Role + KPI + Discipline sections)
- [ ] All proposals pass: completeness ✓, specificity ✓, consistency ✓
- [ ] Feasibility flags ≤3 (expect some; <10 is good signal)
- [ ] All revisions addressed (if peer review flagged issues)
- [ ] Confidence scores ≥0.90 (agents confident in proposals)
- [ ] Output files written to droplet-training-outputs/ (all JSONs present)
- [ ] Ready to apply patches to agent cards

---

## MAIN SESSION VALIDATION (after agents complete)

```bash
# Spot-check 3 proposals
python3 << 'VALIDATE_EOF'
import json
from pathlib import Path

agents_to_check = ["evidence-curator", "memory-keeper", "research-analyst"]
base_path = Path("/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/proposals")

for agent in agents_to_check:
    proposal_file = base_path / f"{agent}-proposal.json"
    with open(proposal_file) as f:
        proposal = json.load(f)
    
    # Check completeness
    assert len(proposal["patches"]) >= 3, f"{agent} has <3 patches"
    assert any("Droplet Discipline" in p.get("section", "") for p in proposal["patches"]), f"{agent} missing Droplet Discipline"
    assert proposal["confidence"] >= 0.85, f"{agent} confidence too low ({proposal['confidence']})"
    
    print(f"✓ {agent} proposal passes validation")

print("\n✓ Spot-check passed. Ready to apply patches to cards.")
VALIDATE_EOF
```

---

## DEPLOYMENT (main session applies patches)

After validation:

```bash
# For each of 9 agents, apply patches to their card
python3 << 'DEPLOY_EOF'
import json
import os
from pathlib import Path

agents = [
    "evidence-curator", "memory-keeper", "membot", "knowledge-synthesizer",
    "research-analyst", "report-writer", "documentation-engineer",
    "context-manager", "workflow-orchestrator"
]

base_proposals = Path("/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/proposals")
base_revisions = Path("/mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/revisions")
cards_dir = Path("/mnt/d/0LOCAL/.claude/agents")

for agent in agents:
    # Load final proposal (use revision if exists, else proposal)
    revision_file = base_revisions / f"{agent}-revised.json"
    proposal_file = base_proposals / f"{agent}-proposal.json"
    
    final_source = revision_file if revision_file.exists() else proposal_file
    with open(final_source) as f:
        final = json.load(f)
    
    # Load agent card
    card_path = cards_dir / f"{agent}.md"
    with open(card_path) as f:
        card_content = f.read()
    
    # Apply patches
    for patch in final["patches"]:
        old = patch["old"]
        new = patch["new"]
        if old not in card_content:
            print(f"⚠ {agent}: patch old_string not found. Skipping patch.")
            continue
        card_content = card_content.replace(old, new)
    
    # Write updated card
    with open(card_path, "w") as f:
        f.write(card_content)
    
    print(f"✓ Updated {agent}.md")

print("\n✓ All 9 agent cards deployed with droplet discipline.")
DEPLOY_EOF
```

---

## MONITORING (next 20 spawns)

After deployment, monitor next 20 spawns of trained agents:

- **Droplet count:** target ≥1 per run (baseline: 0.6)
- **Droplet quality:** HEADLINE + CONNECTION ratio (target >50%; baseline ~20%)
- **Manifest compliance:** all droplets include `droplets` field (target 100%)

Track in `/mnt/d/0LOCAL/.claude/NECTAR.md` entry "Droplet Training Results (W3 2026)":
```
- Session: droplet-integration-t1
- Agents trained: 9
- Cards deployed: 2026-04-21
- First 5 spawns: avg 1.2 droplets/run, 65% HEADLINE/CONNECTION ratio
- Spawns 6-10: avg 1.5 droplets/run, 72% HEADLINE/CONNECTION ratio
- Spawns 11-20: avg 1.6 droplets/run, 78% HEADLINE/CONNECTION ratio
→ Trend: improving droplet discipline post-training ✓
```

---

**Status:** Ready to spawn  
**Team:** droplet-integration-t1 (9 agents, parallel W3)  
**Timeline:** ~4 hours (15 min audit + 30 min proposal + 30 min review + 30 min revision per agent, parallelized)  
**Outcome:** 9 agent cards embedded with droplet discipline; next spawn cost -2.4K tokens base

