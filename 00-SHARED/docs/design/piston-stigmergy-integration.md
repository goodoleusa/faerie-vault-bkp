# Piston-Stigmergy Integration

## Feedback Loop: Eval → Piston → Wave Adjustment

Current state:
- eval_harness.py computes 7 dimensions (A-G)
- stigmergy_score = 0.053 (critical) — memory flow broken
- piston currently reads static waves-config.json

Goal:
- piston reads system-eval.json stigmergy_score
- If stigmergy < 0.4: shift W1 to repair agents (memory-keeper, vault-checker)
- If stigmergy >= 0.4: increase parallel load safely

Implementation:
1. Add stigmergy_score to system-eval.json (done via 9x_stigmergy_scorer.py)
2. Piston reads system-eval.json in Step 0 (Orient phase)
3. Piston computes "memory_repair_needed" = (1.0 - stigmergy_score) * 100
4. If memory_repair_needed > 50%: insert memory agents into W1 roster
5. Log decision to piston-checkpoint.json for audit

## Wave Adjustment Rules

### Stigmergy Score Tiers

| Score | Status | W1 Priority | Action |
|---|---|---|---|
| < 0.2 | Broken | memory-repair | Full memory rebuild: memory-keeper, vault-checker, context-manager |
| 0.2-0.4 | Critical | memory+analysis | Memory repair + 1 analysis agent |
| 0.4-0.6 | Weak | memory+feature | 50% memory, 50% feature work |
| 0.6-0.8 | Healthy | balanced | Standard roster (mix all) |
| >= 0.8 | Strong | feature-heavy | Can increase parallel load to 8-12 agents safely |

### Example W1 Adjustment

**If stigmergy_score = 0.053:**
```
Standard W1: [state-roundup, vault-checker, code-reviewer]
Adjusted W1:  [state-roundup, vault-checker, memory-keeper, evidence-curator, droplet-scanner]
Reason:       Memory repair + analysis to understand memory loss patterns
```

## Implementation in Piston

```python
def compute_w1_roster(eval_state: dict) -> list[AgentSpec]:
    """Dynamically compute W1 roster based on eval scores."""
    stigmergy_score = eval_state.get("dimensions", {}).get("coordination", {}).get("score", 0.5)
    memory_repair_needed = max(1.0 - stigmergy_score, 0.0)

    base_w1 = [
        AgentSpec("context-manager", "haiku", "state-roundup", awaited=True),
        AgentSpec("security-auditor", "haiku", "vault-checker", awaited=True)
    ]

    if memory_repair_needed > 0.5:
        # Critical or weak stigmergy: add memory agents
        base_w1.append(AgentSpec("memory-keeper", "haiku", "pollen-scanner", awaited=True))
        base_w1.append(AgentSpec("evidence-curator", "sonnet", "memory-gap-analysis", awaited=True))

    if memory_repair_needed > 0.8:
        # Broken stigmergy: add droplet scanner
        base_w1.append(AgentSpec("general-purpose", "haiku", "droplet-scanner", awaited=False))

    return base_w1
```

## Monitoring

- Each piston run logs: stigmergy_score → W1 roster decision → actual agents spawned
- piston-checkpoint.json includes "memory_repair_needed" percentage
- Faerie dashboard shows: "Memory health: {stigmergy_score}; repair priority: {percentage}%"

## Expected Outcome

**Before:** stigmergy = 0.053 (broken), 157 droplets written, 11 cited, 6 orphaned
**After 2-3 cycles with memory repair:** stigmergy > 0.4 (weak), NECTAR grows, droplets get cited
**Target:** stigmergy >= 0.6 (healthy), parallel agent load increases safely
