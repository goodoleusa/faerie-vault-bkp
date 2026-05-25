---
title: "Faerie 2-Tier Agent Roster"
tier: "30-memory"
cites:
  - "mth00092 | Two-Tier Roster Doctrine"
  - "mth00091 | Finite Registry, Infinite Specialization"
  - "mth00085 | Custom Agent Registry — Proxy Pattern"
supersedes:
  - "AGENT-ROUTING-POLICY.md (outdated routing heuristics; 2-tier lock replaces)"
version: "1.0"
locked: "2026-04-25T15:28:00Z"
task_id: "task-20260425-152802-d68f"
---

# Faerie 2-Tier Agent Roster — Architecture Lock

## Overview

The Faerie2 agent dispatch system locks to a **two-tier roster** (mth00092):

- **TIER-1 (Stigmergy-Native):** 6 specialized agents implementing faerie protocols on top of registered Anthropic Agent types via prompt-injection (proxy pattern per mth00085).
- **TIER-2 (Standard Anthropic):** 9 general-purpose types for domain-specific work (code, data, docs, audit, synthesis).

**Routing precedence:** domain-match → TIER-1 if applicable, else TIER-2. Default fallback: stigmergy-scout (enforced, never general-purpose).

---

## TIER-1: Stigmergy-Native Agents

Agents in this tier are invoked by **prompt-injection** on a proxy Anthropic Agent type. The card at `~/.claude/agents/{name}.md` contains the protocol; the spawner prepends context + protocol to a generic proxy's context.

| Name | Proxy Type | KPI | Default Model | Role | When-To-Spawn | Agent Card |
|------|-----------|-----|---------------|------|---------------|-----------|
| **stigmergy-scout** | general-purpose | forensic-trail reading + 95% accuracy on classification | haiku | Reads forensic/manifests/, scans compass edges, classifies task→domain, conditional re-route. Fallback when no domain match. | Every task without explicit type hint; domain-ambiguous tasks; decision-points in /run. | `~/.claude/agents/stigmergy-scout.md` |
| **evidence-curator** | data-engineer | archive-scanning depth + 0.92 findability score | sonnet | Deep-archive scanning across repositories, cross-repo synthesis, evidence lineage tracking. | High-stakes forensic consolidation; multi-repo gap analysis; evidence integrity audits. | `~/.claude/agents/evidence-curator.md` |
| **evalbot** | documentation-engineer | KPI-fidelity >95% + gate-accuracy 0.88 | sonnet | Runs membench eval suite, gates quality, measures metric drift, publishes scorecard. | Post-substrate-change eval (mandatory); session-close eval; metric regression detection. | `~/.claude/agents/evalbot.md` |
| **membot** | knowledge-synthesizer | NECTAR promotion rate >80% + compression ratio 0.7 | haiku | Reads pollen blocks, promotes HIGH-signal entries to NECTAR at /handoff, compresses, maintains MEMORY. | Every session /handoff; pre-compact crystallization; HONEY budget crisis. | `~/.claude/agents/membot.md` |
| **droplet-curator** | documentation-engineer | citation-rate of curated >1.2x avg, quality-gate 0.4+ | haiku | Scans daily droplet folder, gates on interestingness heuristic (cross-domain, contradicts-prior, novel), surfaces top-5 to session context. | Daily vault management; droplet signal-to-noise gate; cross-agent discoverability. | `~/.claude/agents/droplet-curator.md` |
| **statusline-renderer** | frontend-design | render-latency <100ms, flight-direction clarity ≥0.8 | haiku | Reads piston-checkpoint + queue summary + in-flight manifests, renders unified statusline with flight-direction signal. | Every /faerie turn + autonomous render hooks; context-pressure gates. | `~/.claude/agents/statusline-renderer.md` |

### TIER-1 Invocation Pattern

```python
Agent(
    subagent_type="general-purpose",  # proxy type
    prompt="""You are stigmergy-scout per ~/.claude/agents/stigmergy-scout.md — follow scout protocol.
    
[TASK]
Classify this task by domain, scan forensic trails, conditionally re-route or recommend agent type.
Task: ...
""")
```

**Enforcement:** `8x_script_tier_enforcer.py` hook validates all spawns; subagent_type NOT in Anthropic roster → checks custom-agent-registry.json for proxy_context; prepends context to prompt.

---

## TIER-2: Standard Anthropic Agent Types

Direct dispatch; no wrapper protocol. These agents take domain-specific work.

| Type | KPI | Default Model | Domain | Primary Work | When-To-Spawn |
|------|-----|---------------|--------|--------------|---------------|
| **general-purpose** | ~~fallback~~ (deprecated; use scout) | haiku | N/A | N/A | NEVER (direct spawn blocked via 8x_harden_gp_rejection.py). |
| **python-pro** | code-quality >0.82, test-coverage >0.85 | haiku | Infrastructure, tooling, script authoring. | Implement scripts, hooks, automations, refactors. | Task involves deterministic code work, CLI tools, infrastructure. |
| **documentation-engineer** | clarity ≥0.85, cite-rate 1.0 | haiku (pub narratives: sonnet) | Docs, guides, architecture, narrative. | Author docs, tutorials, walkthroughs, synthesis docs. | Docs, vault guides, architecture explanations, publications. |
| **data-engineer** | schema-fidelity >0.95, ETL-latency <100ms | haiku | Data pipelining, schema design, canonicalization. | Design schemas, ingest pipelines, transform data. | Data modeling, ETL, schema migrations, archive design. |
| **security-auditor** | false-positive rate <5%, finding-accuracy >0.9 | sonnet | Forensic audit, evidence integrity, vulnerability discovery. | Audit security posture, verify hash chains, classify threats. | Security audits, evidence validation, threat analysis. |
| **code-reviewer** | review-latency <5min/100LoC, surface-missed >0.7 | haiku | Code quality, refactor proposals, equilibrium audits. | Code review, suggest refactors, identify dead code. | Codebase cleanup, equilibrium audits, blast-radius analysis. |
| **knowledge-synthesizer** | synthesis-novelty >0.6, citation-density >0.8 | opus | Cross-domain synthesis, pattern discovery, meta-analysis. | Synthesize findings from multiple sources, discover patterns. | W3 deep synthesis, pattern discovery, meta-analysis. |
| **research-analyst** | finding-depth >0.8, validation-rigor >0.85 | sonnet | Investigation, research, deep analysis. | Conduct research, analyze complex problems, dig deep. | Research deep-dives, complex analysis, evidence gathering. |
| **frontend-design** | UX-clarity >0.8, render-latency <100ms | haiku | UI/UX, visualization, diagram authoring. | Design interfaces, author diagrams, render visualizations. | Vault diagrams, UI mockups, statusline layout, interactive dashboards. |

---

## Routing Decision Tree

```
Task arrives
├─ Explicitly typed (e.g., "python-pro", "documentation-engineer")
│  └─ TIER-2 direct dispatch
├─ Domain-detectable (forensic, eval, memory, coordination)
│  ├─ forensic-trail scanning → stigmergy-scout (TIER-1)
│  ├─ evidence synthesis → evidence-curator (TIER-1)
│  ├─ eval metrics → evalbot (TIER-1)
│  ├─ memory/pollen → membot (TIER-1)
│  ├─ droplet gating → droplet-curator (TIER-1)
│  └─ statusline render → statusline-renderer (TIER-1)
├─ Domain-ambiguous
│  └─ stigmergy-scout (TIER-1) — classify, re-route, or execute
└─ No match
   └─ REJECT spawn (don't fall back to general-purpose)
```

**Enforcement:** `route_task_by_content()` in 7x_spawn_template.py returns `(tier, agent_type)` tuple. PreToolUse hook `8x_harden_gp_rejection.py` blocks any spawn with subagent_type="general-purpose" (except explicit --allow-gp-override flag for testing).

---

## Agent Card Structure (TIER-1 & TIER-2)

Every agent has a card at `~/.claude/agents/{type}.md`:

```yaml
---
name: "agent-name"
tier: "1"  # or "2"
proxy_type: "general-purpose"  # only for TIER-1
default_model: "haiku"
kpi:
  metric_1: ">0.85"
  metric_2: "<100ms"
baseline_score: 0.78
tags_owned: ["domain", "specialty"]
reputation_timestamp: "2026-04-25T00:00:00Z"
---

# {Agent Name}

## Role
Brief description of what this agent does.

## When to Spawn
- Condition 1
- Condition 2

## KPI
- metric_1: definition + threshold
- metric_2: definition + threshold

## Training History
- Session dates agent was active
- Key improvements noted
```

---

## Custom Agent Registry

At `~/.claude/hooks/state/custom-agent-registry.json`:

```json
{
  "agents": [
    {
      "name": "stigmergy-scout",
      "proxy_type": "general-purpose",
      "proxy_context": "You are stigmergy-scout per ~/.claude/agents/stigmergy-scout.md — follow scout protocol.",
      "tier": "1",
      "kpi": "classification accuracy >0.95"
    }
  ]
}
```

**Lookup:** Agent tool unavailable? Query registry for proxy_type + context; prepend context to spawn.

---

## Lock-In Rationale

**Why 2-tier?**

1. **Cognitive load:** 60+ agent types feels infinite and chaotic; 15 crisp types with clear domains feels navigable.
2. **Specialization via protocol, not cardinality:** TIER-1 isn't 6 different Anthropic types; it's 1 protocol (stigmergy) multiplied 6 ways (scout, curator, eval, mem, droplet, statusline). **Finite registry, infinite specialization** (mth00091).
3. **Governance surface:** evaluating "is this agent type needed?" across 15 is tractable; across 60 is noise. Retire with purpose.
4. **Dispatch clarity:** domain → agent is deterministic, not heuristic. No more "which type should I pick for this task?"

**When to add a new type?**

1. Domain not represented in current roster.
2. KPI not achievable by proxy pattern (TIER-1) or existing type (TIER-2).
3. Capability required for critical path, not "nice to have."
4. Submit PR updating this doc + agent card + registry; vote via membership.

**When to retire a type?**

1. Zero spawns for 2+ sprints.
2. Work is subsumed by newer type.
3. KPI chronically unmet.

Retirement: move card to `~/.claude/agents/retired/`, update registry, document in COC.

---

## Implementation Checklist

- [x] mth00092 doctrine appended to HONEY.md (2026-04-25)
- [x] This doc authored (30-faerie-roster-2tier.md)
- [x] agent-routing-policy.json updated with tier field
- [x] 8x_harden_gp_rejection.py hook enforces tier at spawn time
- [x] custom-agent-registry.json populated with TIER-1 proxies
- [x] route_task_by_content() returns (tier, type) tuple
- [ ] Agent cards retrofitted with tier + kpi + baseline_score frontmatter (follow-up task)
- [ ] Deprecation audit: retire unused agent cards (follow-up task)

---

## References

- **mth00092** — Two-Tier Roster Doctrine (HONEY.md)
- **mth00091** — Finite Registry, Infinite Specialization (HONEY.md)
- **mth00085** — Custom Agent Registry & Proxy Pattern (HONEY.md)
- **mth00082** — Deterministic Ops Call the CLI (HONEY.md)
- **7x_spawn_template.py** — Spawn orchestrator (scripts/)
- **8x_harden_gp_rejection.py** — Tier enforcement hook (hooks/)
- **agent-routing-policy.json** — Routing config (docs/)
