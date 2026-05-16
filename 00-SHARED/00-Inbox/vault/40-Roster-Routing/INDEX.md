---
doc_hash: sha256:pending
created: 2026-04-25
type: playground-index
folder: 40-Roster-Routing
breadcrumb: "vault / 40-Roster-Routing / INDEX"
---

# 40-Roster-Routing — The Agent Registry

faerie2 maintains a registry of specialized agent types, each with a card at `~/.claude/agents/{type}.md`. The system has ~53 agent types inventoried. This folder explains what each class of agent does, how the routing engine selects them, and the reputation-weighted dispatch logic.

---

## Agent Card Structure

Every agent card is a markdown file, ≤800 tokens (≤1.2K when trained), with this schema:

```markdown
# {agent-type} Agent Card

## Identity
Role: ...
Specialization: ...

## KPIs
- Primary: ...
- Secondary: ...

## BASELINE
score: 0.XX
locked: true
established: YYYY-MM-DD

## Last Training
- 2026-04-24 | score: 0.XX | task: task-... | delta: +0.0X | notes: ...
- 2026-04-22 | score: 0.XX | task: task-... | delta: +0.0X | notes: ...
```

Anti-gaming rule: **agents MUST NOT see their own Last Training or BASELINE score before execution.** The parent embeds a `discovery.json` inline in the bundle; the agent reads only the bundle. The eval reads the private card AFTER the run and updates it. See [[50-Honesty-System/INDEX]] for the full paradox.

---

## Agent Type Taxonomy

The ~53 agent cards fall into these classes:

### Orchestration Layer
| Agent Type | Primary Role |
|------------|-------------|
| `faerie` | Main orchestrator — minimal inference, routes and compresses |
| `scout` | Default fallback — general-purpose task pickup when no specialist matches |
| `synthesizer` | Cross-manifest synthesis — W3 wave, produces dashboard_lines |
| `memory-keeper` | Promotes MEM blocks from pollen to NECTAR; crystallizes HONEY |

### Engineering Specialists
| Agent Type | Primary Role |
|------------|-------------|
| `python-pro` | Python scripts — tier-aware, equilibrium-compliant |
| `frontend-developer` | UI components, static site generation |
| `backend-developer` | API integrations, service logic |
| `devops-engineer` | Deployment, hook configuration, systemd/cron |
| `documentation-engineer` | Docs, vault structure, INDEX files (this agent) |
| `api-designer` | OpenAPI spec, endpoint design |
| `cli-developer` | CLI tools, argparse, subcommand design |
| `qa-expert` | Test design, adversarial scenarios |

### Analysis & Evidence
| Agent Type | Primary Role |
|------------|-------------|
| `analyst` | Data analysis, pattern finding, statistical synthesis |
| `evidence-curator` | Hash-stamping, COC entries, artifact organization |
| `forensics-specialist` | Chain-of-custody verification, tamper detection |
| `stat` | Statistical modeling, metric computation |

### Investigation & OSINT
| Agent Type | Primary Role |
|------------|-------------|
| `osint-researcher` | Open-source intelligence gathering |
| `entity-mapper` | Entity stub creation, network mapping |
| `financial-tracer` | Financial thread analysis |

### Evaluation
| Agent Type | Primary Role |
|------------|-------------|
| `eval-harness` | Runs system evaluation against BASELINE |
| `mutation-classifier` | Classifies instruction conflicts as beneficial/neutral/harmful |

*(Full list: `ls ~/.claude/agents/*.md | wc -l` for live count)*

---

## Routing Logic — route_task_by_content()

The routing engine in `7x_spawn_template.py` selects an agent type using:

1. **Explicit `agent_type_hint`** in the task JSON — always wins if present
2. **Tag matching** — `synthesis-heavy` → synthesizer; `evidence` → evidence-curator; etc.
3. **Content keyword scoring** — task title + description scanned for domain signals:
   - "python", "script", "refactor" → `python-pro`
   - "vault", "docs", "INDEX", "playground" → `documentation-engineer`
   - "queue", "atomic", "claim" → `python-pro` or `faerie` depending on context
   - "eval", "score", "baseline" → `eval-harness`
4. **Reputation weighting** — among equally-matched candidates, the agent with the highest `last_score` (from their card's Last Training) is preferred
5. **Scout fallback** — if no match scores above threshold, `scout` is selected

---

## Scout-Default Behavior

The `scout` agent type is the system's catch-all. It is designed to:
- Accept any task without specialized context
- Produce a minimum viable artifact (manifest + dashboard_line)
- Flag in the manifest when it detected it was working outside its specialization
- Queue a follow-up task suggesting the correct specialist

A scout that flags misrouting is providing a routing signal. Over time, these signals are used to improve the keyword scoring weights. This is how the routing engine self-improves without a human editing weights manually.

---

## Reputation-Weighted Selection

```
candidate_score(agent_type, task) =
    content_match_score(task)           # 0.0 → 1.0
    × (1.0 + reputation_delta(agent))   # reputation_delta = last_score - baseline

where:
  reputation_delta > 0 = agent is improving (bonus weight)
  reputation_delta < 0 = agent is regressing (penalty weight)
  reputation_delta = 0 = new agent, no training history (neutral)
```

An agent with `baseline: 0.70` and `last_score: 0.87` gets a +0.17 reputation bonus. An agent with `last_score: 0.65` (below baseline) gets a -0.05 penalty. The engine prefers agents that are trending upward on the specific task type.

---

## Subagent Roster (Runtime)

During a session, every spawned subagent is registered in `hooks/state/subagent-roster.json` (gitignored — runtime state):

```json
{
  "session_id": "1c0c5ef4",
  "agents": [
    {
      "agent_type": "documentation-engineer",
      "task_id": "task-20260425-152144-a4e5",
      "wave": 2,
      "model": "sonnet",
      "spawned_at": "2026-04-25T15:21:44Z",
      "manifest_path": "forensics/manifests/..."
    }
  ]
}
```

Main uses this roster to track in-flight agents and avoid re-spawning completed work.

---

[[00-Welcome/INDEX]] | [[10-Processes/INDEX]] | [[20-Queue-Mission/INDEX]] | [[30-Dashboards/INDEX]] | [[50-Honesty-System/INDEX]]

*sha256:pending*
