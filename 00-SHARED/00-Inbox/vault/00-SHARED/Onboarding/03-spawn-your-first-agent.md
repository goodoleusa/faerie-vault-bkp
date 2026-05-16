---
type: guide
status: active
tags: [onboarding, agents, spawn, hands-on]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:055c0b36b06c46dbaf1f31ec45549957796c78290a441f0ca894553d954383d9
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 03 — Spawn Your First Agent

Hands-on walkthrough of spawning an agent via the spawn contract.

---

## The Spawn Contract

Every agent spawn in faerie2 must go through `7x_spawn_template.py`.
Direct prompt construction is blocked by the `8x_spawn_contract_enforcer.py`
PreToolUse hook.

Why: manually constructing spawn prompts costs 300-800 tokens of inference.
Template rendering costs ≤50 tokens (deterministic, no LLM).

---

## Step 1 — List Available Templates

```bash
python3 ~/.claude/scripts/7x_spawn_template.py list
```

Output:
```
w1-general-purpose     W1 fast triage (45s)
w1-trail-finder        W1 stigmergy scout
w2-data-engineer       W2 data work (180s)
w2-documentation-engineer  W2 docs work
w3-knowledge-synthesizer   W3 deep synthesis
...
```

---

## Step 2 — Render a Template

```bash
RENDERED=$(python3 ~/.claude/scripts/7x_spawn_template.py render \
  --template w2-documentation-engineer \
  --params '{"task_id": "task-001", "task_goal": "document the spawn contract"}')

echo "$RENDERED" | head -20
```

This produces the full agent spawn prompt with all required sections
(manifest contract, streaming protocol, stigmergy, vault output, etc.)
injected deterministically.

---

## Step 3 — Spawn the Agent

In Claude Code:

```python
Agent(
  subagent_type="documentation-engineer",
  description="Document the spawn contract",
  prompt=RENDERED
)
```

The agent runs, writes output to `forensics/`, and returns a manifest.

---

## Step 4 — Read the Manifest

When the Agent call returns, read the manifest:

```bash
cat /mnt/d/0local/gitrepos/faerie2/.claude/manifests/wave2-documentation-engineer-*.json
```

Key fields to read:
```json
{
  "task_id": "task-001",
  "dashboard_line": "spawn contract documented; 3 templates covered; ready-for-review",
  "output_path": "/mnt/d/0local/gitrepos/faerie2/forensics/...",
  "status": "final"
}
```

Main reads only `dashboard_line`. Full output is at `output_path`.

---

## Step 5 — Check the Output

```bash
cat <output_path from manifest>
```

This is the full agent output: findings, docs, analysis — whatever the agent produced.
It lives in `forensics/` permanently. The manifest is the pointer to it.

---

## What You Just Did

```
Template list    → discovered available spawn shapes
Template render  → built a 50-token spawn prompt (not 800-token manual)
Agent spawn      → agent ran with fresh 200K context window
Manifest read    → got dashboard_line summary (80 chars)
Output read      → accessed full findings when needed
```

This is the full agent lifecycle.

---

## Agent Types

Common agent types you will use:

| Type | When to use |
|---|---|
| `documentation-engineer` | Write docs, guides, references |
| `data-engineer` | Data ingestion, ETL, pipeline work |
| `research-analyst` | Investigation, OSINT, analysis |
| `python-pro` | Infrastructure, scripts, automation |
| `knowledge-synthesizer` | Cross-domain synthesis, NECTAR integration |
| `general-purpose` | Anything that does not match a specialist |

---

## Next Steps

- [[04-reading-manifests]] — understanding manifest structure in depth
- [[../Architecture/spawn-contract]] — the spawn contract technical reference
- [[../Skills-Reference/run]] — /run automates this whole flow

---

## Related

- [[../Hive/stigmergic-recursion]] — how agents coordinate after spawning
- [[../Glossary/terms]] — manifest, template, agent_run_id defined
