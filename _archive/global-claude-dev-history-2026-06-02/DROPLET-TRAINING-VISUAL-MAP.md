# Droplet Integration — Visual Map of Deliverables

## The Flow: Problem → Solution → Execution → Benefit

```
┌─ PROBLEM ──────────────────────────────────────────────────┐
│                                                            │
│  Long instructive rules (3K+ tokens) loaded every spawn   │
│  ↓                                                         │
│  Spawn agent → Load rule → Agent reads → Apply            │
│  Cost per spawn: +3K tokens (whether agent reads or not)  │
│  Spawning context friction; redundant rule loads          │
│                                                            │
└────────────────────────────────────────────────────────────┘

┌─ SOLUTION ──────────────────────────────────────────────────┐
│                                                             │
│  Train agents once (W3) to internalize rule in cards      │
│  ↓                                                         │
│  Meta-training: agents read rule → audit cards →          │
│  propose updates → peer review → deploy new cards         │
│  ↓                                                         │
│  Next spawn of trained agent reads discipline from card   │
│  Cost per spawn: +200 tokens (brief reminder)             │
│  Payoff: 10 spawns break even; -50K+ tokens saved by 20   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─ EXECUTION ─────────────────────────────────────────────────┐
│                                                             │
│  W3 Training Session (4 hours parallelized)               │
│  ↓                                                         │
│  TeamCreate: droplet-integration-t1                        │
│  ↓                                                         │
│  9 Agent spawns (parallel):                               │
│    Phase 1: Card Audit (15 min)                           │
│    Phase 2: Card Proposal (30 min)                        │
│    Phase 3: Peer Adversarial Review (30 min)             │
│    Phase 4: Revision + Deploy (30 min)                    │
│  ↓                                                         │
│  Main session validates + applies patches to 9 cards     │
│  ↓                                                         │
│  Monitor next 20 spawns for quality improvement           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─ BENEFIT ───────────────────────────────────────────────────┐
│                                                             │
│  Permanent: Trained agents (9) spawn with discipline DNA  │
│  ↓                                                         │
│  -2.4K tokens per spawn (91% reduction)                   │
│  ↓                                                         │
│  Generalizable: Pattern reusable for next 3 long rules   │
│  (citations Q2, stigmergy Q3, model routing Q4)           │
│  ↓                                                         │
│  Q1 + Q2 + Q3 + Q4 training = -7K tokens per spawn (end 2026)
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Map

```
DELIVERABLES (6 files created, 2 files modified)

NEW SAUCE RULE
└─ /mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md
   ├─ Core Signal: When to Write (strong/weak triggers, feeling-based)
   ├─ Categories & High-Value Types (HEADLINE, CONNECTION, etc.)
   ├─ Anti-Patterns (what NOT to write)
   ├─ Moment-Based Heuristics (feeling checklist)
   ├─ Quality Heuristics (what makes droplet worthwhile)
   └─ Examples + FAQ + Checklist
   [3.2K tokens | Load on demand, not every spawn]

META-FRAMEWORK (Generalizable Pattern)
└─ /mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md
   ├─ When to use (rule characteristics)
   ├─ Training session phases (audit → proposal → peer review → revision → deploy)
   ├─ Card update structure (Role + KPI + Discipline section)
   ├─ Success metrics (quantitative + qualitative)
   ├─ Quarterly cadence (Q1 droplets, Q2 citations, Q3 stigmergy, Q4 routing)
   └─ Risk mitigation (peer review catches overcommit, easy rollback)
   [1.8K tokens | For ANY long rule embedding]

EXECUTABLE TRAINING SESSION
├─ /mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md
│  ├─ Part 1: Card Audit (15 min)
│  ├─ Part 2: Card Proposal (30 min)
│  ├─ Part 3: Peer Adversarial Review (30 min)
│  ├─ Part 4: Revision (30 min, if needed)
│  └─ Expected outcomes + FAQ
│  [2.1K tokens | Specification]
│
└─ /mnt/d/0LOCAL/.claude/DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md
   ├─ Pre-spawn checklist
   ├─ TeamCreate + 9 Agent() spawn template
   ├─ Per-agent prompt (meta-training context + 4 phases)
   ├─ Team coordination (shared task list + SendMessage)
   ├─ Manifest contract (status progression)
   ├─ Success criteria for main session
   ├─ Deployment script (apply patches to 9 cards)
   └─ Monitoring plan (next 20 spawns)
   [2.4K tokens | Ready-to-copy-paste]

STAGING MANIFESTS
├─ /mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-training-manifest.json
│  └─ Pre-execution manifest (what will happen)
│
└─ /mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-guidance-result.json
   └─ Final manifest from this work (deliverables + next steps)

SUMMARY DOCS (Integrated View)
├─ /mnt/d/0LOCAL/.claude/DROPLET-WORK-SUMMARY.md
│  └─ Complete summary (problem, solution, deliverables, cost analysis, next steps)
│
└─ /mnt/d/0LOCAL/.claude/DROPLET-TRAINING-VISUAL-MAP.md (this file)
   └─ Visual flow + file map

ENHANCED INFRASTRUCTURE (Modified)
├─ /mnt/d/0local/gitrepos/faerie2/scripts-claude/8x_spawn_boilerplate_injector.py
│  ├─ Added generate_droplet_protocol() function
│  └─ Integrated into inject_boilerplate_into_prompt()
│
└─ /mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md
   ├─ Section 3c: Minimal protocol + reference to full rule
   └─ Note: "Agents trained in droplet discipline have this in their cards"

AGENTS TO BE TRAINED (9 Tier-1)
├─ evidence-curator
├─ memory-keeper
├─ membot
├─ knowledge-synthesizer
├─ research-analyst
├─ report-writer
├─ documentation-engineer
├─ context-manager
└─ workflow-orchestrator
```

---

## Timeline

```
PRE-W3 (NOW)
└─ ✓ Rule created (droplet-writing-heuristics.md)
   ✓ Strategy documented (LONG-RULES-TRAINING-STRATEGY.md)
   ✓ Training session designed (TRAINING-DROPLET-INTEGRATION.md)
   ✓ Spawn instructions ready (DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md)
   ✓ Boilerplate enhanced (8x_spawn_boilerplate_injector.py)
   ✓ Approved + queued

W3 EXECUTION (4 hours parallelized)
└─ T+0:00   TeamCreate: droplet-integration-t1
   T+0:15   9 Agent spawns (parallel)
   T+0:45   Agents complete Phase 1: Audit → 9 JSON outputs
   T+1:30   Agents complete Phase 2: Proposal → 9 JSON outputs
   T+2:30   Agents complete Phase 3: Peer Review → 18-27 JSON outputs
   T+3:30   Agents complete Phase 4: Revision (if needed) → 0-3 JSON outputs
   T+4:00   Main session validates + applies patches to 9 cards
            Deploy 9 updated agent cards (git commit)

POST-W3 MONITORING (ongoing)
└─ Spawns 1-5 of trained agents: monitor droplet count + quality
   Spawns 6-10: measure improvement vs baseline
   Spawns 11-20: track consistency (≥1 droplet/run)
   Document outcomes in NECTAR entry "Droplet Training Results (W3 2026)"
   Decide: proceed with Tier-2 training (Q2 citations) or iterate

Q2 2026 (PLANNED)
└─ Citation Discipline training (5 agents, ~4 hours)
   Cost: 10-15K tokens (training); ROI: -1.5K tokens per spawn

Q3 2026 (PLANNED)
└─ Stigmergy + Coordination training (5 agents, ~4 hours)
   Cost: 12-18K tokens (training); ROI: -1.8K tokens per spawn

Q4 2026 (PLANNED)
└─ Model Routing training (8 agents, ~4 hours)
   Cost: 16-20K tokens (training); ROI: -1.2K tokens per spawn

END OF 2026 PROJECTION
└─ 4 rules embedded in agent cards
   Cumulative baseline spawn cost: -7K tokens per spawn
   All trained agents spawn with discipline in DNA
```

---

## Cost-Benefit Chart

```
TOKENS PER SPAWN (over time)

Before Training (Baseline)
├─ Rule load: +3200 tokens
├─ Task execution: ~2000 tokens
├─ Overhead: ~300 tokens
└─ Total: ~5500 tokens per spawn

W3 Training Session Cost (One-Time)
├─ 9 agents × 2-2.5K tokens avg: 18-22K tokens
├─ Spread across 4 hours (parallelized)
└─ Amortized to 4-5 tokens per spawn if spread over 5000 spawns

After Training (New Baseline)
├─ Rule load: +200 tokens (minimal protocol reminder only)
├─ Task execution: ~2000 tokens (unchanged)
├─ Overhead: ~300 tokens (unchanged)
└─ Total: ~2500 tokens per spawn

Savings Per Spawn: 3200 tokens (91% reduction) ✓

Break-Even Timeline
├─ Training cost: 18-22K tokens
├─ Savings per spawn: 3K tokens
├─ Break-even: 18K / 3K = 6 spawns (conservative)
├─ In reality: 10 spawns (accounting for partial savings ramp-up)
└─ By spawn 20: 50K+ tokens saved ✓

Q1+Q2+Q3+Q4 Cumulative (Full Year)
├─ Q1 (Droplet): 9 agents, -2.4K tokens/spawn
├─ Q2 (Citation): 5 agents, -1.5K tokens/spawn
├─ Q3 (Stigmergy): 5 agents, -1.8K tokens/spawn
├─ Q4 (Model routing): 8 agents, -1.2K tokens/spawn
├─ Total agents trained: 27 (overlap: knowledge-synthesizer, task-distributor, performance-eval)
├─ Effective savings: -7K tokens per spawn (end of 2026)
└─ Annual savings (200 spawns/year × 5500 avg): ~1.1M tokens ✓
```

---

## Agent Card Update Structure (Example: evidence-curator)

```
BEFORE (Current Card)
─────────────────────────
## Role
Curates evidence into tiers; identifies gaps; prioritizes sources.

## KPIs
- tier1_accuracy: 0.89
- gap_identification: 0.92

## Last Training — 2026-04-15
Score: 0.89

AFTER (Trained Card with Embedded Discipline)
──────────────────────────────────────────────
## Role
Curates evidence into tiers; identifies gaps; prioritizes sources.
**Droplet discipline:** Surfaces synthesis across domains via spontaneous 
insight capture (CONNECTION, HEADLINE). Minimum 1 droplet per run.

## KPIs
- tier1_accuracy: 0.89
- gap_identification: 0.92
- droplet_value_score: 0.0–1.0 (avg confidence of HEADLINE/CONNECTION, min 3 per 10 runs)
- droplet_consistency: binary (≥1 high-value droplet per run)

## Droplet Discipline

**Triggers (write immediately when):**
- Connection spans 3+ source documents
- Finding breaks assumption
- Gut feeling before reasoning
- Pattern discovered others can reuse

**High-value types:** HEADLINE, CONNECTION, FIRST_IMPRESSION, TECHNIQUE
**Where:** $CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md
**Format:** ### ISO8601 — {agent_type}, **cat:** X, **pri:** Y, {1–5 sentences}
**Cadence:** Write at moment of insight, not at end
**Manifest:** Include "droplets": [{"path": "...", "count": N, "cats": [...]}]

## Last Training — 2026-04-21
Score: 0.91 (prev: 0.89, delta: +0.02)
Context: Training session: Droplet Integration
Learnings:
- Droplet discipline improves gap-identification by surfacing unexpected patterns
- High-value droplets have 3× info density of generic observations
- Peer review reveals shared synthesis techniques
```

---

## What Changed In Faerie Spawn Behavior

```
BEFORE: Every Spawn Loads Full Rule
──────────────────────────────────

Agent spawn:
  ├─ Load manifest boilerplate
  ├─ Load streaming instructions
  ├─ Load droplet-writing-heuristics.md (3.2K tokens) ← COST
  ├─ Load stigmergy instructions
  ├─ Load task (user prompt)
  └─ Execute

AFTER: Agents Spawn With Discipline in DNA
───────────────────────────────────────────

Agent spawn (evidence-curator example):
  ├─ Load manifest boilerplate
  ├─ Load streaming instructions
  ├─ Load MINIMAL droplet protocol (300 tokens) ← NEW: brief reminder
  │  └─ "Write ≥1 droplet/run. Types: HEADLINE, CONNECTION, etc. Full heuristics available in rules/sauce/droplet-writing-heuristics.md"
  ├─ Load stigmergy instructions
  ├─ Load task (user prompt)
  ├─ Agent reads OWN CARD (already loaded in context)
  │  └─ Sees "Droplet Discipline" section with triggers, types, anti-patterns
  └─ Execute with embedded discipline ← NO NEED TO LOAD FULL RULE

Cost savings:
  Before: +3200 tokens
  After: +200 tokens
  Reduction: 3000 tokens (94%) ✓
```

---

## Key Metrics

```
TRAINING SESSION (W3)
├─ Timeline: 4 hours (parallelized, not sequential)
├─ Agents trained: 9
├─ Audit outputs: 9
├─ Proposal outputs: 9
├─ Peer reviews: 18-27 (2-3 per agent)
├─ Revisions: 0-3 (based on feedback)
├─ Cards deployed: 9
├─ Success rate target: 100% (all 9 cards updated + peer-approved)
└─ Token cost: 18-22K

POST-DEPLOYMENT MONITORING (Next 20 Spawns)
├─ Droplet count per run: baseline 0.6 → target ≥1.0 (+67%)
├─ HEADLINE + CONNECTION ratio: baseline ~20% → target >50% (+150%)
├─ Manifest compliance: target 100% (all manifests include droplets field)
├─ KPI improvement: droplet_consistency → expect 90%+ (≥1 per run)
└─ Success gate: improvement visible by spawn 10 ✓

CUMULATIVE (By End of 2026 with Full Rollout)
├─ Rules embedded: 4 (droplet, citation, stigmergy, model routing)
├─ Agents trained: 27
├─ Baseline spawn cost reduction: -7K tokens (per spawn)
├─ Annual token savings (200 spawns/yr × 5500 avg): ~1.1M tokens
└─ Side benefit: agents improve each other via peer review ✓
```

---

## How to Execute (Quick Checklist)

```
1. REVIEW (30 min)
   ☐ Read /mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md
   ☐ Read /mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md
   ☐ Read /mnt/d/0LOCAL/.claude/DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md
   ☐ Approve strategy + training design

2. SETUP (15 min)
   ☐ Create output directories:
     mkdir -p /mnt/d/0LOCAL/.claude/hooks/state/droplet-training-outputs/{audit,proposals,reviews,revisions}
   ☐ Verify 9 tier-1 agent cards exist:
     ls /mnt/d/0LOCAL/.claude/agents/{evidence-curator,memory-keeper,membot,...}.md

3. SPAWN (5 min)
   ☐ Copy TeamCreate + 9 Agent() spawn code from DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md
   ☐ Execute in W3 session
   ☐ Monitor TaskNotifications for completion

4. VALIDATE (15 min)
   ☐ Run spot-check script (in spawn instructions) on 3 proposals
   ☐ Verify completeness, specificity, feasibility
   ☐ Flag any issues for manual review

5. DEPLOY (15 min)
   ☐ Run deployment script to apply patches to 9 agent cards
   ☐ Commit to git: "train(agents): embed droplet-writing discipline in 9 cards"
   ☐ Verify cards updated in git history

6. MONITOR (Ongoing)
   ☐ Track next 20 spawns of trained agents
   ☐ Measure: droplet count, quality ratio, manifest compliance
   ☐ Document results in NECTAR

Total time: 1.5 hours (review) + 4 hours (W3 execution) + ongoing (monitoring)
```

---

**Status:** Complete and ready to execute  
**Owner:** Team lead  
**Next action:** Queue W3 training session

