---
doc_hash: sha256:pending
created: 2026-04-25
type: playground-index
folder: 30-Dashboards
breadcrumb: "vault / 30-Dashboards / INDEX"
---

# 30-Dashboards — Live System Links

This folder aggregates live views into the faerie2 system state. These are not static documents — they link to actual runtime artifacts produced by agents and the eval harness.

---

## System Dashboard Links

### Eval Report
The most recent eval run, including per-agent scores and mutation impact analysis.

```
Path: $CT_VAULT/00-SHARED/Dashboards/system/eval-report-{date}.md
Live example: /mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Dashboards/system/
```

Produced by: `scripts/eval/eval_harness.py --auto` (triggered at session stop via `session_stop_hook.py`)

---

### Queue Summary

Current state of the sprint queue: pending/in_progress/completed task counts, priority breakdown, blocked tasks.

```bash
# Live query:
python3 /mnt/d/0local/gitrepos/faerie2/scripts/7x_queue_ops.py list
```

Or view directly:
```
Path: ~/.claude/hooks/state/sprint-queue.json
```

Fields to scan: `status`, `priority`, `blockedBy`, `claimed_by_session`, `claimed_at`

---

### Coordination Probe

The coordination probe captures cross-session stigmergy state — which sessions are active, which manifests are in-flight, which tasks are mid-chain.

```
Path: forensics/manifests/ (latest files)
Pattern: ls -t forensics/manifests/*.json | head -5
```

---

### Droplet Citation Rate

Droplets are atomic insight captures written by every agent to `$CT_VAULT/00-SHARED/Droplets/`. The citation rate measures how often subsequent agents reference earlier droplets — a proxy for stigmergic knowledge propagation.

```
Path: $CT_VAULT/00-SHARED/Droplets/{date}/
Today: /mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Droplets/2026-04-25/
```

High droplet count = active session. Droplets with `mth00091` tags = methodological references (quality signal ≥0.4 threshold).

---

### Agent Reputation Top Scorers

Agent cards live at `~/.claude/agents/{type}.md`. Each card has a `## Last Training` section with scores appended by the eval harness. Top performers are those with the largest delta between BASELINE and Last Training score.

```bash
# Quick scoreboard:
grep -h "score:" ~/.claude/agents/*.md | sort -t: -k2 -nr | head -10
```

The 9x_agent_card_updater.py script updates these after each eval run — only if the new score exceeds the last recorded score (OTJ improvement gate).

---

### Agent Reputation Tracker

```
Path: $CT_VAULT/00-SHARED/Dashboards/agent-reputation/
```

Shows: agent_type, baseline, last_score, delta, tasks_completed, last_eval_date

Routing decisions use reputation scores: `route_task_by_content()` in the spawn template system weights agents with higher reputation higher for matching task types. See [[40-Roster-Routing/INDEX]] for the full routing logic.

---

## Dataview Queries (Obsidian Live)

If you have the Dataview plugin active, these queries render live in Obsidian:

### In-flight Manifests
```dataview
TABLE status, dashboard_line, agent_run_id
FROM "forensics/manifests"
WHERE status != "final"
SORT file.mtime DESC
LIMIT 10
```

### Recent Droplets (today)
```dataview
LIST
FROM "$CT_VAULT/00-SHARED/Droplets/2026-04-25"
SORT file.ctime DESC
LIMIT 20
```

### Tasks by Priority
```dataview
TABLE priority, status, claim_state, agent_type_hint
FROM "hooks/state"
WHERE type = "task"
SORT priority ASC
```

*(Note: Dataview requires "Enable JavaScript Queries" in settings to render `dataviewjs` blocks.)*

---

## How to Read the System at a Glance

1. **Queue list** — are HIGH tasks draining? If not, check for expired claims: `python 7x_queue_ops.py cleanup-claims`
2. **Latest manifest** — what did the most recent agent return? `cat $(ls -t forensics/manifests/*.json | head -1)`
3. **Droplets today** — how much insight capture happened? `ls $CT_VAULT/00-SHARED/Droplets/$(date +%Y-%m-%d)/ | wc -l`
4. **COC chain** — is the chain intact? `python 7x_queue_ops.py verify-coc` (if implemented)
5. **Eval report** — what's the current system score? Open `$CT_VAULT/00-SHARED/Dashboards/system/eval-report-{latest}.md`

---

[[00-Welcome/INDEX]] | [[10-Processes/INDEX]] | [[20-Queue-Mission/INDEX]] | [[40-Roster-Routing/INDEX]] | [[50-Honesty-System/INDEX]]

*sha256:pending*
