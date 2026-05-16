---
type: reference
status: active
created: 2026-04-21
tags: [model-routing, architecture, agents]
up: README.md
prev: PHILOSOPHY.md
next: MEMORY-AS-SERVICE-ARCHITECTURE.md
---

> [↑ Readme](README.md) · [← Philosophy](PHILOSOPHY.md) · [→ Memory As Service Architecture](MEMORY-AS-SERVICE-ARCHITECTURE.md) · [⌂ Home](../README.md)

# Model Routing Policy — Haiku-Default with Strategic Sonnet/Opus

**Effective: 2026-04-21**

## ⚡ Authoritative Source

**Single source of truth for model + wave assignment:**  
`/.claude/AGENT-TYPE-ROUTING.json`

This document summarizes the policy. For complete routing table with all 15 agent types and promotion conditions, see AGENT-TYPE-ROUTING.json.

## Quick Reference

| Dimension | Default | When Promoted | Metrics |
|-----------|---------|---|---|
| **W1** (Triage) | Haiku | Never | haiku_w1_rate ≥ 0.80 |
| **W2** (Feature) | Haiku/Sonnet* | reasoning_budget=inference_heavy | sonnet_w2_rate ≥ 0.90 |
| **W3** (Synthesis) | Sonnet | reasoning_budget=expert → Opus | opus_rate < 0.05 |

*W2 defaults to Haiku for simple work (formatting, refactoring, ETL). Evidence-curator and research-analyst explicitly require Sonnet.

## Cost Per Spawn (7.5K input tokens)

```
Haiku:  $0.009  (baseline)
Sonnet: $0.034  (3.8× more)
Opus:   $0.170  (19× more)
```

## How It Works

### 1. Agent Card Specifies Model

**Your `~/.claude/agents/{type}.md` frontmatter:**

```yaml
agent_type: evidence-curator
model: sonnet              # ← Faerie honors this
reasoning_budget: inference_heavy
```

### 2. Faerie Injects Into Spawn Prompt

When faerie spawns you, the prompt includes:

```
Model: {your-model} (from agent card)
Reasoning budget: {inference_heavy|expert|none}
Wave: {1|2|3}
```

### 3. Eval Harness Measures Model Routing

After the run, eval_harness.py computes:

- **haiku_w1_rate** — fraction of W1 agents using Haiku (target: 0.80+)
- **sonnet_w2_rate** — fraction of W2 agents using Sonnet when reasoning needed (target: 0.90+)
- **opus_rate** — fraction of all agents using Opus (target: <0.05)

These feed into **Dimension F (Model Routing)** in the 6-dimension eval.

## Agent Type → Wave Mapping

### W1 (Triage & Validation, 45s target)
- workflow-orchestrator
- context-manager
- task-distributor
- error-coordinator
- token-optimizer
- admin-sync

**Model:** Haiku only (routing/decision work doesn't need reasoning)

### W2 (Feature Work & Research, 180s target)
- python-pro (Haiku OK for simple refactors; Sonnet for architecture)
- data-engineer (Haiku OK for pipelines; Sonnet for optimization)
- documentation-engineer (Haiku OK for writes; Sonnet for synthesis)
- evidence-curator (**Sonnet required** — gap analysis needs reasoning)
- research-analyst (**Sonnet required** — OSINT synthesis needs context)
- fullstack-developer (Haiku for UI; Sonnet for complex features)

**Model:** Haiku by default; Sonnet if `reasoning_budget: inference_heavy`

### W3 (Deep Synthesis, async background, 600s target)
- knowledge-synthesizer (Haiku for basic correlation; Sonnet for expert synthesis)
- membot (Haiku for reads; Sonnet for NECTAR promotion; Opus for crystallization)
- security-auditor (Haiku only — hash verification is read-only)
- performance-eval (Haiku for basic scoring; Sonnet for cross-session analysis; Opus for rare multiway synthesis)

**Model:** Sonnet by default; Opus if `reasoning_budget: expert`

## Promotion Criteria

An agent is promoted FROM Haiku TO Sonnet/Opus **only if**:

1. **Agent card explicitly specifies it** (`model: sonnet` or `model: opus`)
   ```yaml
   # Example: evidence-curator.md
   model: sonnet
   ```

2. **OR task includes reasoning_budget tag**
   ```
   Task context: "reasoning_budget: inference_heavy" → Sonnet
   Task context: "reasoning_budget: expert" → Opus
   ```

3. **OR faerie detects 3+ inference-heavy operations**
   - Multi-source synthesis
   - Hypothesis testing across domains
   - Security auditing with hash chain validation

### What Does NOT Trigger Promotion

- Code formatting, refactoring, simple ETL ← stays Haiku
- Generic documentation writes ← stays Haiku
- Data pipeline setup ← stays Haiku
- Read-only audit work ← stays Haiku

## Eval Impact

### Model Routing Dimension (F)

Weighted into final composite score:

```
composite = 0.22×T + 0.18×M + 0.18×R + 0.18×Q + 0.14×P + 0.10×F
            (throughput, memory, resilience, quality, piston, model_routing)
```

### How Score Is Computed

```python
# F1: haiku_w1_rate
haiku_w1_rate = count(W1 agents using haiku) / len(W1 agents)
score_f1 = min(haiku_w1_rate / 0.80, 1.0)  # target 0.80

# F2: sonnet_w2_rate
sonnet_w2_rate = count(W2 agents using sonnet when needed) / len(W2 agents)
score_f2 = min(sonnet_w2_rate / 0.90, 1.0)  # target 0.90

# F3: opus_rate
opus_rate = count(opus agents) / count(all agents)
penalty = max(0, (opus_rate - 0.05) / 0.05)  # over-use penalty

# Final F score
F = (score_f1 * 0.5 + score_f2 * 0.4 - penalty * 0.1)
```

### Example: How Misrouting Damages Score

**Scenario A (Good):** W1 has 5 agents, all Haiku. W2 has 8 agents, 7 Sonnet (evidence-curator, research-analyst) + 1 Haiku (python-pro simple refactor).

```
haiku_w1_rate = 5/5 = 1.0 → score_f1 = 1.0
sonnet_w2_rate = 7/8 = 0.875 → score_f2 = 0.972
opus_rate = 0 → penalty = 0
F = 0.5×1.0 + 0.4×0.972 = 0.889
```

**Scenario B (Bad):** Same work, but python-pro used Sonnet for a simple refactor and membot over-used Opus for basic read.

```
haiku_w1_rate = 5/5 = 1.0
sonnet_w2_rate = 8/8 = 1.0  # all W2 agents now use sonnet (including python-pro)
opus_rate = 1/14 = 0.071 > 0.05 → penalty = 0.015
F = 0.5×1.0 + 0.4×1.0 - 0.1×0.015 = 0.899
```

**Impact:** Scenario B scores 0.899 vs 0.889 composite (slight gain from sonnet_w2 hit, loss from opus over-use). Over many runs, repeated misrouting accumulates cost without quality gain.

## Cluster Behavior

Agents naturally cluster by model when:

1. **W1 agents all use Haiku** (triage is fast, deterministic)
2. **W2 agents split Haiku/Sonnet by complexity**
3. **W3 agents mostly use Sonnet, rarely Opus**

This clustering is **healthy**. It means agents are making principled choices.

Clustering is **unhealthy** if:

- W1 agents accidentally using Sonnet (routing doesn't need reasoning)
- W2 Haiku agents doing gap analysis (evidence-curator must promote)
- W3 Opus being used for simple reads (read-only doesn't need expert synthesis)

## Monitoring

### Per-Session Report

```bash
python3 scripts/8x_roster_update.py --report [SESSION_ID]
```

Output shows:
- W1 Haiku count + % (target ≥80%)
- W2 Sonnet count + % (target ≥90% when inference needed)
- Opus count + % (target <5%)
- Estimated cost in USD

### Per-Run in Eval Harness

```bash
python3 scripts/eval/eval_harness.py
```

Output includes:
```
MODEL_ROUTING     0.50     haiku_w1=0.0 sonnet_w2=? opus=?
```

## Integration Points

1. **Agent Card** (`~/.claude/agents/{type}.md`)
   - Specifies `model: haiku|sonnet|opus`
   - Specifies `reasoning_budget: none|inference_heavy|expert`

2. **SPAWN-BOILERPLATE.md**
   - "MODEL ROUTING" section (this document's source)
   - Linked from every spawn prompt

3. **8x_roster_update.py Hook**
   - Captures every Agent() call with model selection
   - Appends to `~/.claude/hooks/state/subagent-roster.json`

4. **eval_harness.py (Dimension F)**
   - Reads roster.json
   - Computes haiku_w1_rate, sonnet_w2_rate, opus_rate
   - Blends into final composite score

## FAQ

**Q: Can I override my agent card model in the task?**
A: No. Agent card is authoritative. If a task needs Sonnet, your agent type should be promoted (evidence-curator, research-analyst). One-off task overrides create unmeasurable drift.

**Q: What if my Haiku agent isn't reasoning enough?**
A: Update your agent card to specify `model: sonnet` and `reasoning_budget: inference_heavy`. Then faerie spawns you with Sonnet going forward.

**Q: How do I know if I'm over-using Opus?**
A: Check eval output. If `opus_rate > 0.05`, look at recent `wave3-*-result.json` manifests. If any are read-only (no inference), demote to Haiku/Sonnet.

**Q: Does cost impact the composite score?**
A: Indirectly. Model Routing (F) is 10% of composite. Over-using Sonnet/Opus lowers haiku_w1_rate and sonnet_w2_rate metrics, which lowers F, which lowers composite. The system incentivizes cost-appropriate choices without explicit cost-scoring.

**Q: What if Haiku genuinely isn't enough?**
A: Be honest in your agent card. Add `model: sonnet` + `reasoning_budget: inference_heavy`. Eval harness will measure whether the promotion was justified (higher beat-last score = justified; same score = unjustified).

## References

- **Policy:** `/mnt/d/0local/gitrepos/faerie2/.claude/model-routing-policy.json`
- **Hook:** `/mnt/d/0local/gitrepos/faerie2/scripts/8x_roster_update.py`
- **Boilerplate:** `/mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md` (MODEL ROUTING section)
- **Eval Metrics:** `/mnt/d/0local/gitrepos/faerie2/scripts/eval/eval_harness.py` (compute_model_routing function)
- **Agent Cards:** `/mnt/d/0local/gitrepos/faerie2/agents/*.md` (frontmatter `model:` field)

---

**Last updated:** 2026-04-21  
**Adopted by:** Haiku 4.5 agent team  
**Status:** Active (integrated into all spawns)
