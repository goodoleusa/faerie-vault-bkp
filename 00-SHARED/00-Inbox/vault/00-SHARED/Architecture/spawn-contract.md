---
type: reference
status: active
tags: [architecture, spawn, contract, templates, agents]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:8ee10989f69d2d51b9dfba6bf7abd8ffac6ce6b9b0dbe15ee80b6dda5ec686fd
hash_ts: 2026-04-25T01:10:51Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Spawn Contract

How agent spawns are validated, rendered, and executed.

---

## The Contract

**Rule #7:** Every `Agent()` spawn MUST be rendered via `7x_spawn_template.py --bundle`.
Direct prompt construction is blocked by `8x_spawn_contract_enforcer.py` (PreToolUse hook).

Why this exists:
- Manual prompt construction: 300-800 tokens of LLM inference per spawn
- Template rendering: ≤50 tokens (deterministic, no LLM)
- 5-agent faerie cycle: 200K+ tokens wasted → 250 tokens

---

## The One Way to Spawn

```bash
# 1. Render the template
RENDERED=$(python3 ~/.claude/scripts/7x_spawn_template.py render \
  --template w2-documentation-engineer \
  --params '{"task_id": "task-042", "task_goal": "document spawn contract"}')

# 2. Pass rendered prompt to Agent()
Agent(
  subagent_type="documentation-engineer",
  description="Document the spawn contract",
  prompt=RENDERED
)
```

---

## What Templates Include

Every template's `body_partials` field injects these sections automatically:

| Section | Purpose |
|---------|---------|
| VAULT OUTPUT | Where to write findings |
| MANIFEST CONTRACT | Result format and required fields |
| STREAMING + DROPLETS | Observation protocol (5-20 entries/run) |
| STIGMERGY | Discovery + registration instructions |
| TASK DROPLET DISCOVERY | Upstream learning at startup |
| FILE WRITING PROTOCOL | Subagent sandbox rules |
| MODEL ROUTING | Haiku/sonnet/opus policy |
| ANTI-GAMING BUNDLE MODEL | Card visibility guarantee |
| MEMBENCH CONTEXT | Substrate contribution awareness |

You do not add these manually. Templates provide them deterministically.

---

## Template Registry

```bash
# List available templates
python3 ~/.claude/scripts/7x_spawn_template.py list

# List by wave
python3 ~/.claude/scripts/7x_spawn_template.py list --wave 2

# Show template schema
python3 ~/.claude/scripts/7x_spawn_template.py show --template w2-evidence-curation
```

Templates live at: `$CLAUDE_HOME/spawn-templates/`

---

## AGENT-RUN-ID (required in every spawn)

Every agent generates an immutable AGENT-RUN-ID at startup:

```bash
AGENT_RUN_RESULT=$(python3 /mnt/d/0LOCAL/.claude/scripts/9x_agent_run_id_generator.py \
  --agent-type documentation-engineer \
  --session-id "${CLAUDE_SESSION_ID:-unknown}" \
  --task-id "task-042" \
  --wave W2 \
  --model sonnet)
AGENT_RUN_ID=$(echo "$AGENT_RUN_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['agent_run_id'])")
```

This ID is embedded in every manifest and COC entry. It is the forensic anchor
linking this agent run to eval scores and training updates.

---

## Manifest Contract (required return format)

```json
{
  "agent": "documentation-engineer",
  "ts": "2026-04-24T15:30:00Z",
  "wave": 2,
  "task_id": "task-042",
  "agent_run_id": "ar-20260424-abc123",
  "output_path": "/mnt/d/0local/gitrepos/faerie2/forensics/...",
  "dashboard_line": "spawn contract documented; 3 templates; ready-for-review",
  "files_written": ["..."],
  "finding_hash": "sha256:...",
  "manifest_hash": "sha256:...",
  "status": "final"
}
```

Return format: `MANIFEST: {path} | dashboard_line: {≤80 chars}`

---

## Spawn Floor / Return Ceiling

- **Spawn floor:** `READ: {bundle_path}\nExecute. Return MANIFEST: {path} | dashboard_line: {≤80 chars} only.` (~50 tokens)
- **Return ceiling:** dashboard_line ≤80 chars; manifest path ≤120 chars; everything else in forensics/

---

## Enforcement

`8x_spawn_contract_enforcer.py` PreToolUse hook validates every Agent() call.
If the prompt was not rendered via `7x_spawn_template.py`, the spawn is blocked.
Violations are logged to `forensics/spawn-contract-violations.jsonl`.

---

## Related

- [[../Hive/stigmergic-recursion]] — how spawned agents coordinate
- [[../Onboarding/03-spawn-your-first-agent]] — hands-on spawn walkthrough
- [[../Skills-Reference/run]] — /run automates spawning
- [[../Glossary/terms]] — spawn contract, AGENT-RUN-ID, bundle defined
