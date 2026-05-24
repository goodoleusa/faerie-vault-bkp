# Plugin Format Differences — Claude CLI vs Desktop

**Version:** faerie 0.5.0  
**Date:** 2026-04-12

---

## Overview

Claude Code CLI and Desktop App share the same plugin format (`.claude-plugin/`), but:
- CLI supports more features (hooks, rules, agents)
- Desktop supports a subset (skills, commands, MCP)

This document maps what's supported where.

---

## Feature Matrix

| Feature | CLI | Desktop | Notes |
|---------|-----|---------|-------|
| **Skills** (`skills/`) | ✅ | ✅ | Same format in both |
| **Commands** (`commands/`) | ✅ | ✅ | Slash commands |
| **Agents** (`agents/`) | ✅ | ❌ | Subagent definitions |
| **Hooks** (`hooks/`) | ✅ | ❌ | Event handlers |
| **Rules** (`rules/`) | ✅ | ❌ | Auto-loaded rules |
| **MCP** (`mcpServers`) | ✅ | ✅ | Via settings.json |

---

## Plugin Directory Structure

```
faerie/
├── .claude-plugin/           # Official plugin format
│   ├── plugin.json           # Manifest (name, version, author)
│   ├── README.md            # Installer instructions
│   ├── skills/              # Skill definitions
│   │   ├── faerie/
│   │   ├── run/
│   │   ├── queue/
│   │   └── handoff/
│   ├── commands/            # Slash command aliases
│   │   ├── faerie.md
│   │   ├── run.md
│   │   └── queue.md
│   ├── agents/              # (CLI only) Subagent definitions
│   └── hooks/               # (CLI only) Event handlers
│       └── hooks.json
└── releases/
    └── templates/           # Per-OS settings templates
        ├── windows-settings.template.json
        ├── macos-settings.template.json
        └── linux-settings.template.json
```

---

## Skill Format (Both CLI + Desktop)

```markdown
---
description: "One-line description"
argument-hint: "[flag1|flag2] [argument]"
model: sonnet
effort: high
---

Skill content here...
```

**Front-matter required:** `description`  
**Optional:** `argument-hint`, `model`, `effort`, `tools`, `memory`

---

## Command Format (Both CLI + Desktop)

```markdown
---
name: faerie
description: "Session orchestrator"
argument-hint: "[--flag] [context]"
---

INVOKE faerie SKILL
```

---

## Hooks Format (CLI Only)

```json
{
  "hooks": [
    {
      "trigger": "Start",
      "type": "command",
      "command": "python3 ${FAERIE_HOME}/hooks/state/faerie_turn1.py",
      "timeout": 30,
      "statusMessage": "Loading faerie session..."
    }
  ]
}
```

**Supported triggers:** `Start`, `Stop`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`  
**Supported types:** `command`, `http`

---

## MCP Server (Both CLI + Desktop)

Configure in `settings.json`:

```json
{
  "mcpServers": {
    "faerie": {
      "command": "python",
      "args": ["/path/to/faerie-mcp-server.py"],
      "env": {
        "FAERIE_HOME": "~/.claude"
      }
    }
  }
}
```

Faerie MCP server (Phase 2) exposes:
- `queue.claim`, `queue.list`, `queue.complete`
- `memory.read` (honey/nectar/review_hot)
- `eval.status`, `eval.run`
- `agent.spawn`, `agent.roster`

---

## Platform-Specific Notes

### Windows (Native)

- Use PowerShell paths in hooks
- `%USERPROFILE%` instead of `~`
- MCP via `settings.json` works

### Windows (WSL)

- Use `/mnt/c/Users/...` paths
- Hooks via bash work natively
- Recommended: `windows-wsl-settings.template.json`

### macOS

- `~/Library/Application Support/Claude/` for global config
- Standard Unix paths work

### Linux

- Standard `~/.config/Claude/` for global config
- Standard Unix paths work

---

## Cross-Platform Release

Use the release templates:

```bash
# Windows (native)
python scripts/0b_build_release_bundles.py --profile windows-native

# Windows (WSL)  
python scripts/0b_build_release_bundles.py --profile windows-wsl

# macOS
python scripts/0b_build_release_bundles.py --profile macos

# Linux
python scripts/0b_build_release_bundles.py --profile linux
```

Each profile copies `.claude/` to the appropriate release folder and applies the OS-specific settings template.

---

## data-analysis-engine Reference

The `/data-ingest` pipeline is in a separate repo: `data-analysis-engine`

To wire it in:
1. Clone `data-analysis-engine` alongside `faerie`
2. Set `DAE_SCRIPTS=/path/to/data-analysis-engine/scripts`
3. `/data-ingest` skill will invoke pipeline

---

## Installation

### CLI
```bash
# Option 1: Copy to plugins dir
cp -r .claude-plugin ~/.claude/plugins/faerie

# Option 2: Use plugin-creator skill
/skill-add https://github.com/faerie/faerie/tree/main/.claude-plugin
```

### Desktop
```bash
# Same as CLI — Desktop reads from ~/.claude/plugins/
cp -r .claude-plugin ~/Library/Application\ Support/Claude/plugins/faerie
```

---

*Generated: 2026-04-12 | For faerie v0.5.0*