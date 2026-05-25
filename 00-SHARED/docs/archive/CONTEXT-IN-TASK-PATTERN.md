# Context-in-Task Pattern

## Problem

Background agents (`run_in_background: true`) cannot get interactive approval for
paths outside their default sandbox. They fail on Read/Write to `/mnt/d/` paths.
This causes quality degradation: the agent produces valid work but cannot commit it,
or cannot load context and operates blind.

## Pattern

Instead of: `"Read /mnt/d/path/to/file.md for context"`
Use: embed the relevant excerpt directly in the spawn prompt.

## Implementation

### Before (broken for background agents):

```
Agent prompt: "Read ~/.claude/memory/HONEY.md for context, then..."
```

### After (works everywhere):

```python
Agent prompt: f"""
CONTEXT (pre-loaded — do not re-read):
{honey_content[:3000]}
---
Your task: ...
"""
```

## When to use

- Any agent spawned with `run_in_background: true`
- Any agent spawning across WSL/Windows boundary
- Any agent where Write failures have been observed in prior runs

## Integration with faerie

faerie already supports `context_bundle` in task schema:

```json
{
  "highest_value": "...",
  "done_looks_like": "...",
  "source_files": [...],
  "content": "..."
}
```

The `content` field embeds pre-read file excerpts. `faerie_turn1.py` patches missing
bundles on every `/faerie` launch. For Wave 3 background agents, faerie should always
populate `content` with the relevant HONEY/NECTAR excerpts and W1/W2 manifest summaries
before spawning — agents must not be left to discover their own context from disk.

## Symptoms of the anti-pattern

- Agent returns "could not read context file" in manifest
- Agent returns valid analysis but manifest shows `files_written: []`
- Quality score drops below 0.5 for Wave 3 agents specifically
- TRAINING_FALLBACK_DATA block appears in agent response (Write was denied)

## Template (copy-paste for Wave 3 spawns)

```python
# In faerie Step 5, before spawning Wave 3:
honey = Path("~/.claude/memory/HONEY.md").expanduser().read_text()[:3000]
w1_summary = Path("~/.claude/hooks/state/wave1-result.json").read_text()[:2000]
w2_summary = Path("~/.claude/hooks/state/wave2-result.json").read_text()[:2000]

context_block = f"""
CONTEXT (pre-loaded — do not re-read files):
HONEY (prefs/methods):
{honey}

W1 FINDINGS:
{w1_summary}

W2 FINDINGS:
{w2_summary}
---
"""
# Prepend context_block to agent prompt
```
