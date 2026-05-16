# Scout Convention — Agent Card as Behavioral Protocol

**Status:** Authoritative | **Updated:** 2026-04-25 | **Version:** 1.0

## Overview

The **stigmergy-scout** agent is NOT a registered type in the Anthropic Agent SDK. It is a **behavioral convention** — a reusable prompt protocol that can be injected into any registered agent type.

### Key Distinction

| Concept | Definition | Use |
|---------|-----------|-----|
| **Agent Card** (`~/.claude/agents/scout.md`) | Behavioral protocol + KPIs + reputation | Human reference; convention template |
| **Registered Agent Type** (Anthropic API) | Valid `subagent_type` value sent to Agent tool | Required for all `Agent()` spawns |
| **Convention** (scout) | Prompt prefix + protocol instructions | Injected via prompt when needed |

---

## Convention Pattern

When you want to use scout behavior (triage via filesystem signals, read forensics, ROUTE/EXECUTE/FLAG decision):

**DO:**
```python
Agent(
    subagent_type="general-purpose",  # ← registered type
    prompt="""You are stigmergy-scout per agent card ~/.claude/agents/stigmergy-scout.md — follow scout protocol (Phase 1: scan forensics/manifests last 24h; Phase 2: map goal against domains; Phase 3: ROUTE/EXECUTE/FLAG decision).
    
[actual task instructions...]""",
    description="Stigmergy scout triage"
)
```

**DON'T:**
```python
Agent(
    subagent_type="stigmergy-scout",  # ← NOT registered; will fail at spawn time
    prompt="..."
)
```

---

## Why This Pattern

1. **Registry constraint:** Anthropic Agent SDK has a fixed list of valid `subagent_type` values. "stigmergy-scout" is not in that list.
2. **Agent cards as templates:** Agent cards are human-readable behavior specifications, not SDK type declarations.
3. **Prompt injection:** The actual behavior comes from the prompt prefix, not the agent type.
4. **Flexibility:** Any agent (general-purpose, research-analyst, etc.) can adopt scout protocol via prompt injection.

---

## Scout Prompt Template

Minimum required prefix (from ~/. claude/agents/stigmergy-scout.md):

```
You are the stigmergy-scout: the mandatory fallback when the router cannot classify a task.
You are NOT a general-purpose executor. Your job is triage via filesystem signals.

## On Spawn: Three-Phase Protocol

### Phase 1 — Read Context (forensics/manifests/ last 24 hours)
[... full phase instructions from agent card ...]

### Phase 2 — Scan Compass Edges
[... phase instructions ...]

### Phase 3 — Decision (one of three)
[... phase instructions ...]
```

Full template: `~/.claude/agents/stigmergy-scout.md` (sections "On Spawn: Three-Phase Protocol")

---

## Routing Rules: When to Use Scout

Scout behavior should be injected when:
1. **No domain match:** Task keywords don't match any specialist domain
2. **Ambiguous signals:** Contradictory signals from goal + metadata
3. **Observation-only tasks:** Need read-only filesystem triage, not action
4. **Fallback after reroute:** Specialist routed task comes back unclassifiable

**Current usage locations:**
- `skills/run/BODY.md` line ~93 (route_task_to_agent fallback)
- `skills/decide/decide.py` lines ~54-55 (THREAD, IDEA categories)
- `skills/clean-gone/SKILL.md` (catch-all agent assignment)

---

## Audit Checklist

**When reviewing code that spawns agents:**

- [ ] `subagent_type` is one of: "general-purpose", "data-engineer", "documentation-engineer", "evidence-curator", "security-auditor", "python-pro", "research-analyst", "knowledge-synthesizer", "fullstack-developer", etc. (from custom-agent-registry.json or hardcoded Agent tool list)
- [ ] If `subagent_type="general-purpose"` AND task is unclassifiable, prompt MUST include scout prefix
- [ ] Never use `subagent_type="stigmergy-scout"` (not registered)
- [ ] Never use `subagent_type="general-purpose"` without understanding the fallback intent
- [ ] Agent card `~/.claude/agents/stigmergy-scout.md` is a protocol template, not a spawn target

---

## Implementation History

- **2026-04-23:** Scout agent card created (behavioral protocol)
- **2026-04-25:** Task-20260425-151323-8db2 — Document convention vs registry, update routing
- **2026-04-25:** This document created (authoritative reference)

---

## References

- **Agent Card:** `~/.claude/agents/stigmergy-scout.md` (KPIs, Last Training, hard constraints)
- **Custom Registry:** `rules/sauce/custom-agent-registry.md` (proxy pattern for non-registered agents)
- **Spawn Contract:** `docs/SPAWN-CONTRACT.md` (enforces template signatures, not agent types)
- **CLAUDE.md:** Governance rules (section "Agent Lifecycle")

