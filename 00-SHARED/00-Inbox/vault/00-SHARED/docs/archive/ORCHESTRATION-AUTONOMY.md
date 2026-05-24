# Orchestration Autonomy — Decision Engine

**Goal:** Enable the orchestrator to recognize when to spawn subagents autonomously instead of asking the user.

**Mechanism:** `orchestration-heuristics.py` analyzes goals and makes spawn/ask decisions based on three criteria:
1. Independence: Are the goals blocking each other?
2. Agent mapping: Do I know which agent types match each goal?
3. Confidence: Am I >70% sure about the mappings?

---

## How It Works

### Input
```bash
python3 ~/.claude/scripts/orchestration-heuristics.py \
  --goals "vault-org,excalidraw-diagrams,baseline-collection" \
  --parallelizable true \
  --confidence-threshold 0.70
```

### Decision Output
```json
{
  "decision": "spawn",
  "confidence": 0.90,
  "goal_count": 3,
  "independent": true,
  "agent_mappings": [
    ["vault-org", "knowledge-synthesizer", 0.90],
    ["excalidraw-diagrams", "fullstack-developer", 0.90],
    ["baseline-collection", "performance-eval", 0.90]
  ],
  "recommended_agents": ["knowledge-synthesizer", "fullstack-developer", "performance-eval"],
  "blocking_dependencies": [],
  "next_steps": [
    "Spawn 3 agents in parallel: ...",
    "Monitor via TaskNotification for each agent completion",
    "Aggregate results and present dashboard"
  ],
  "timestamp": "2026-04-01T...",
  "notes": "All 3 goals independent, high confidence in agent mappings"
}
```

### Decision Types

| Decision | Meaning | Action |
|----------|---------|--------|
| `spawn` | High confidence, independent goals → go | Launch all agents in parallel |
| `ask` | Low confidence or unknown goals → clarify | Ask user for clarification + learn answer |
| `partial` | Some independent, some blocked → proceed with what's clear | Spawn independent subset, queue sequential work |

---

## Integration into Faerie

### Step: Parse User Intent
When orchestrator sees multiple goals in user message:

```python
# Extract goals from user message (heuristic: comma-separated, "and", or "task" keywords)
goals = extract_goals_from_message(user_message)

if len(goals) >= 2:
    # Multi-goal request → analyze for autonomous spawning
    decision_json = run_heuristics(goals)
    decision = json.loads(decision_json)

    if decision["decision"] == "spawn":
        # Autonomous spawn: silence asking, just do it
        for agent_type in decision["recommended_agents"]:
            spawn_agent(agent_type, corresponding_goal)
        user_message_to_respond = "Launched X agents in parallel..."

    elif decision["decision"] == "partial":
        # Partial spawn: launch independent subset, queue rest
        independent = goal_set - goal_set[dependencies]
        for agent in independent:
            spawn_agent(...)

    elif decision["decision"] == "ask":
        # Ask for clarification
        ask_user(decision["next_steps"])
```

### Integration Point
Add this logic to `~/.claude/scripts/faerie.py` at the "Parse user message" step, BEFORE wave assignment.

---

## Agent Affinity Map (Tunable)

The script uses a keyword-based affinity map. Expand it as you learn patterns:

```python
AGENT_AFFINITY_MAP = {
    "vault-org": ("knowledge-synthesizer", 0.9),
    "excalidraw": ("fullstack-developer", 0.9),
    "baseline": ("performance-eval", 0.9),
    # Add more as patterns emerge
}
```

**How to update:**
1. After a few autonomous spawns, review success rate
2. If certain keywords consistently map to wrong agents → adjust confidence
3. If new patterns emerge (e.g., "partner-prep" → always means dashboard + docs + diagrams) → add entry

---

## Confidence Thresholds

- **>80%:** High confidence, safe to spawn
- **70-80%:** Medium confidence, ok to spawn with note
- **50-70%:** Low confidence, ask for clarification
- **<50%:** Very low confidence, fallback to safest default (research-analyst)

Tunable via `--confidence-threshold` (default: 0.70).

---

## Learning Over Time

### Session 1 (Today)
User says: "Assign subagents to vault org, diagrams, and baselines"
- Heuristics detects: 3 independent goals, average confidence 90%
- Decision: **spawn**
- Outcome: User confirms it was right move

→ Add to HONEY.md: "When user says 'assign subagents to N goals,' confidence in autonomy is high."

### Session 2 (Next week)
Similar pattern appears → heuristics recognizes it earlier, confidence rises.

### Session 3+ (Ongoing)
Patterns converge → decision engine becomes predictive, rarely asks.

---

## Edge Cases

### What if goals are described vaguely?
```bash
python3 orchestration-heuristics.py --goals "stuff,things,updates"
# Output: decision="ask", confidence=0.3
# Action: "Could you be more specific about vault updates, diagram types, and timeline?"
```

### What if confidence is borderline (70-75%)?
```bash
# Output: decision="spawn", confidence=0.72, notes="Borderline confidence; learning feedback welcome"
# Action: Spawn, but monitor closely for feedback
```

### What if dependencies exist but are trivial?
```bash
# Output: decision="partial", blocking_dependencies=[(...), ...]
# Action: Spawn independent agents, queue dependent work for next wave
```

---

## Running Manually (For Testing)

```bash
# Test: vault org + diagrams + baselines (should be independent)
python3 ~/.claude/scripts/orchestration-heuristics.py \
  --goals "vault-org,excalidraw-diagrams,baseline-collection" \
  --print-diagram

# Test: with low confidence
python3 orchestration-heuristics.py \
  --goals "xyzzy,frobozz,whimsy" \
  --print-diagram

# Test: output to JSON
python3 orchestration-heuristics.py \
  --goals "vault-org,diagrams" \
  --output /tmp/heuristics-result.json
```

---

## Future Enhancements

1. **Context-aware confidence:** Read previous faerie logs to boost confidence for recurring patterns
2. **Agent performance calibration:** Track which agents succeed most often, adjust confidence weights
3. **Dependency learning:** Over time, build a richer dependency graph (vault → diagrams → dashboard, etc.)
4. **Cost estimation:** Predict token cost of each goal, warn if total exceeds budget
5. **Deadline awareness:** If user has time pressure, prefer more parallelism; if contemplative, prefer sequential clarity

---

## References

- HONEY.md § pref0008 (Orchestration Autonomy rule)
- faerie.md § Intent-driven piston launch
- CLAUDE.md § Flow (Do, don't ask)
