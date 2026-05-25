---
type: shape
shape_id: openhands.agent.tool_set_completeness
target_direction: bounded
current_count: 5
baseline_ts: "2026-05-25T00:00:00Z"
membench_probe: true
cluster_prefix: ["openhands", "agent", "tools"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — openhands.agent.tool_set_completeness

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `openhands.agent.tool_set_completeness`)
> Target direction: **bounded** | Current count: **5** | Membench probe: **True**

---

## Description

Count of Tool(name=X) entries in sdk_chat.py's agent_kwargs tools list (not counting MCP tools added via mcp_config — those are always present). Target: bounded at the canonical N=5 (terminal + file_editor + grep + glob + task_tool_set). Rising or falling count signals an unintended tool add/removal.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | bounded |
| Current count | 5 |
| Baseline timestamp | 2026-05-25T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `grep -c 'Tool(name=' deploy/mcp-server/sdk_chat.py` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-25T00:00:00 | 1 | pre-patch baseline: only TaskToolSet wired | None |
| 2026-05-25T00:00:00 | 5 | oh-sdk-perms-fix: added TerminalTool + FileEditorTool + GrepTool + GlobTool | beneficial |

## Interpretation

<!-- What a count of 5 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
