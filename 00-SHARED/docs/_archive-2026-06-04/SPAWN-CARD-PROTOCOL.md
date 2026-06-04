---
type: reference
status: active
created: 2026-04-25
tags: [spawn, agent-types, custom-cards, routing, protocol]
up: README.md
---

> [↑ Readme](README.md) · [⌂ Home](../README.md)

# Spawn Card Protocol — Official Types vs. Custom Cards

**Critical distinction that was conflated:** Custom agent cards (~/.claude/agents/*.md) are **discovery metadata**, not spawn types. The `Agent()` tool accepts only official Claude platform types.

---

## The Confusion

**WRONG:**
```python
Agent(subagent_type="stigmergy-scout")  # ❌ "stigmergy-scout" is not an official platform type
```

**RIGHT:**
```python
# Read the card's frontmatter:
# maps_to_official_type: general-purpose
Agent(subagent_type="general-purpose", 
      prompt="You are stigmergy-scout per agent card ~/.claude/agents/stigmergy-scout.md:\n[card content]\n\n" + task_prompt)
```

---

## Architecture: Two-Layer Agent System

### Layer 1: Official Agent Types (Platform)

These are registered with Claude Code and accepted by the `Agent()` tool:

- `general-purpose`
- `ai-engineer`
- `data-scientist`
- `code-reviewer`
- `documentation-engineer`
- `context-manager`
- ...and others

**You spawn with these.**

### Layer 2: Custom Agent Cards (User)

Files in ~/.claude/agents/*.md that provide:

1. **Routing metadata** — when to use this agent
2. **Behavioral protocol** — what the agent should do
3. **Constraints** — what it should NOT do
4. **Reputation tracking** — KPIs, caught-lying counter, etc.
5. **Mapping** — `maps_to_official_type` field linking to official type

**You discover/route WITH these, then map to official types.**

---

## Card Frontmatter Structure

Every custom agent card MUST have:

```yaml
---
name: <unique-identifier>
description: "<one-line purpose>"
tools: Read, Bash, Glob, Grep  # (tools available)
model: haiku              # (model preference)
maps_to_official_type: <official_type>
injection_method: "prompt prefix (behavioral shaping) + card content"
---
```

**Example: stigmergy-scout.md**

```yaml
---
name: stigmergy-scout
description: "Triage agent for unclassifiable tasks."
tools: Read, Bash, Glob, Grep
model: haiku
maps_to_official_type: general-purpose
injection_method: "prompt prefix (scout protocol) + phase 1-3 behavioral rules"
---

You are stigmergy-scout per this card...
[full behavioral protocol follows]
```

---

## Spawn Flow

### Step 1: Task Routed to Custom Card

Queue → routing logic → "this task should use stigmergy-scout"

```json
{
  "task_id": "task-20260425-123456",
  "goal": "Triage this ambiguous queuing anomaly",
  "suggested_agent": "stigmergy-scout",  // ← custom card name
  "...": "..."
}
```

### Step 2: Read Card's Mapping

```bash
grep "maps_to_official_type" ~/.claude/agents/stigmergy-scout.md
# Output: maps_to_official_type: general-purpose
```

### Step 3: Spawn with Official Type + Injected Card

```python
# Pseudo-code
import yaml

card_path = Path.home() / ".claude" / "agents" / "stigmergy-scout.md"
with open(card_path) as f:
    frontmatter, body = parse_frontmatter(f.read())

official_type = frontmatter.get("maps_to_official_type")  # "general-purpose"
model = frontmatter.get("model")  # "haiku"

# Construct spawn prompt with card injected as behavioral template
spawn_prompt = f"""You are stigmergy-scout per agent card {card_path}:

{body}

---

Your task:
{task_goal}

MANIFEST: {manifest_path} | dashboard_line: [result]
"""

Agent(
    subagent_type=official_type,  # "general-purpose" (official type)
    model=model,                   # "haiku" (from card)
    prompt=spawn_prompt,           # card content + task
    run_in_background=True
)
```

---

## Concrete Example: stigmergy-scout

### Card Name
`stigmergy-scout` (custom identifier)

### Official Type Mapping
```yaml
maps_to_official_type: general-purpose
```

### Routing Signal
When a task is ambiguous or requires pure observation (no code changes), route to stigmergy-scout.

### Spawn Call
```python
Agent(
    subagent_type="general-purpose",  # Official type
    prompt="""You are stigmergy-scout per agent card ~/.claude/agents/stigmergy-scout.md:

[Full scout protocol from card, including:]
- Phase 1: Read forensic context
- Phase 2: Scan compass edges
- Phase 3: Decision (ROUTE/EXECUTE/FLAG)
- Hard constraints
- Autocompact continuity protocol

Your task:
Triage task-20260425-anomaly: ...

[Rest of task prompt]
"""
)
```

---

## Implementation: /spawn and /run Skills

### /spawn Skill (`spawn/BODY.md`)

When user invokes `/queue-and-spawn` or `/spawn`:

1. Queue task with goal
2. Claim next task via run.py
3. Read JSONL `agent_type` field (custom card name)
4. **NEW:** Read that card's `maps_to_official_type` 
5. Call `Agent(subagent_type=<official_type>, prompt=<card_content> + <task>)`

### /run Skill (`run/BODY.md`)

When user invokes `/run`:

1. run.py emits JSONL with `agent_type` (custom card name)
2. **NEW:** For each line, read the card's `maps_to_official_type`
3. Call `Agent(subagent_type=<official_type>)` with card injected

---

## Why This Design

### Problem Solved
- **Before:** Tried to spawn with custom card name directly. Failed because platform doesn't recognize it.
- **After:** Map custom cards to official types, inject card content as behavioral template. Works.

### Benefits
1. **Unlimited custom cards** — you can define as many behavioral variants as needed without waiting for platform updates
2. **Behavioral composition** — combine official type + custom protocol (don't rewrite the whole agent, just shape it)
3. **Routing clarity** — cards are the discovery mechanism; official types are the execution mechanism
4. **Decoupling** — if Claude updates agent types, your cards still work (they map to the new types)

---

## Checklists

### Creating a New Custom Card

- [ ] Write ~/.claude/agents/myagent.md
- [ ] Add frontmatter with `maps_to_official_type: <official_type>`
- [ ] Include `injection_method` describing how to use the card
- [ ] Test: read card → call Agent with mapping
- [ ] Add to HONEY.md if it's a universal agent type

### Updating /spawn and /run

- [ ] Read JSONL `agent_type` field (custom card name)
- [ ] **Before spawning:** Lookup card file
- [ ] **Read frontmatter:** Extract `maps_to_official_type`
- [ ] **Call Agent:** Use official type, inject card content
- [ ] **Fallback:** If card missing, use official type directly (fail safe)

### Debugging Spawn Failures

If spawn fails with "agent type not found":

1. Check JSONL `agent_type` field — is it a custom card name or official type?
2. If custom card name: verify ~/.claude/agents/{name}.md exists
3. Verify card has `maps_to_official_type` field
4. Verify official type in field is recognized (test: `Agent(subagent_type="<type>")`)
5. If all else fails, use `general-purpose` as fallback with full card content in prompt

---

## Cross-References

- **CLAUDE.md** — "Agent Types vs. Custom Cards" section
- **spawn/BODY.md** — Agent type mapping section
- **run/BODY.md** — Defaults section (agent_type handling)
- **~/.claude/agents/stigmergy-scout.md** — Example card with full behavioral protocol
- **~/.claude/agents/python-pro.md** — Example card for specialized Python work

---

*Protocol established 2026-04-25 · Closes custom-card-as-spawn-type confusion.*
