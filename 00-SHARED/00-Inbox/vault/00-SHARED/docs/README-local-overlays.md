# Local overlays (not shipped as secrets)

## `mcp.json`

Release bundles **do not** include `~/.claude/mcp.json`. It often holds API keys and machine-specific MCP server paths.

- **After install:** copy from your backup, or create `mcp.json` using Claude Code’s MCP configuration flow in the product docs.
- **Repo / team:** if you share a template, use a redacted `mcp.json.example` in a private repo — never commit live credentials.

## Memory files — HONEY.md / NECTAR.md (replaces AGENTS.md)

| Location | Use for |
|----------|---------|
| **`{repo}/.claude/memory/HONEY.md`** | Project crystallized facts (optional, rare). |
| **`~/.claude/HONEY.md`** | Crystallized preferences, methods, identity (≤200 lines). Read at every session start. |

AGENTS.md is deprecated. The Pollen (scratch) → NECTAR (validated findings) → HONEY (crystallized wisdom) pipeline replaces the old write pattern. See **`memory/README-TRAINING.md`** for the training scaffold. **Authoritative project memory** for faerie/crystallization lives in `{repo}/.claude/memory/HONEY.md`.
