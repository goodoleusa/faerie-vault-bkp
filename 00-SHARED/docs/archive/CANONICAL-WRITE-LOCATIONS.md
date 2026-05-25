# Canonical Write Locations — Subagent Architecture Fix

**Status:** Active system rule (2026-04-07)  
**Problem:** `/mnt/d/0LOCAL/.claude/` is a symlink to `/mnt/c/Users/amand/.claude/`, blocking background agent writes. Subagent Write tool is sandboxed to `/mnt/d/` paths only.  
**Solution:** Unified location map defining single canonical write target for every artifact type. All future subagent spawns use these paths — eliminates sandboxing conflicts, enables background agents.

---

## Location Map

| Artifact Type | Canonical Path | Access | Notes |
|---|---|---|---|
| **Agent manifests** (W1/W2/W3 returns) | `/mnt/d/0local/gitrepos/{repo}/.claude/hooks/state/wave{N}-{type}-result.json` | Foreground + background | Full output to `wave{N}-{type}-full.json`; manifest is return value |
| **Cross-repo manifests** (orchestrator, membot, state) | `/mnt/d/0local/gitrepos/faerie2/.claude/hooks/state/{slug}.json` | Foreground only | Faerie-specific state, queue, handoff; never write from background |
| **Design documents** (primary) | `/mnt/d/0local/gitrepos/{repo}/docs/{slug}.md` | Foreground + background | System architecture, forensic design, artifact design — git-tracked, visible to all |
| **Design documents** (vault mirror) | `$CT_VAULT/00-SHARED/Design-Narratives/{slug}.md` | Foreground + background | Syncthing-synced vault copy for human visibility and cross-repo access |
| **Forensic logs** (repo-scoped) | `/mnt/d/0local/gitrepos/{repo}/forensics/` | Append-only | Investigation COC, pipeline audit, case-specific forensics |
| **Forensic logs** (global) | `/mnt/d/0LOCAL/.claude/memory/forensics/` | Append-only | Agent learnings forensics, session COC, system-level audit trail |
| **Queue / state** | `/mnt/d/0local/gitrepos/faerie2/.claude/hooks/state/sprint-queue.json` + state files | Foreground only | Sprint queue, training queue, agent state registry |
| **Agent state** | `/mnt/d/0local/gitrepos/{repo}/.claude/hooks/state/task-states/{task_id}-{type}.json` | Foreground + background | Progressive disclosure state versioning per task per agent |
| **Vault outputs** | `$CT_VAULT/00-SHARED/{category}/` or repo subdirs | Foreground + background | Findings, dashboards, droplets, blueprints (Syncthing-synced) |
| **Memory (scratch)** | `{repo}/.claude/memory/pollen-{SESSION_ID}.md` | Foreground + background | Working notes, MEM blocks, observations (gitignored) |
| **Memory (durable)** | `~/.claude/memory/{HONEY,NECTAR,REVIEW-INBOX}.md` | Foreground only | Via subprocess (agent returns patches, parent applies) |

---

## Never Write To (BLOCKED for sandboxing reasons)

| Path | Why | Alternative |
|---|---|---|
| `/mnt/c/Users/amand/.claude/**` | Symlink target, sandboxed for background agents | Use `/mnt/d/0LOCAL/.claude/` or repo-scoped paths |
| `C:/Users/amand/.claude/**` | Windows native, inaccessible from WSL | Use `/mnt/d/` paths (wslpath conversion at parent) |
| `D:\0LOCAL\.claude\**` (Windows UNC) | Git Bash path, inaccessible from WSL/Claude CLI | Use `/mnt/d/0LOCAL/.claude/` (WSL absolute) |
| `~/.claude/**` (home expansion) | Resolves to `/mnt/c/...`, sandboxed | Explicit `/mnt/d/0LOCAL/.claude/` or `/mnt/c/Users/amand/.claude/` only in foreground |
| `{repo}/.claude/memory/HONEY.md` etc | Durable memory, never written by agents directly | Return patches as JSON, parent applies via Bash |

---

## Access Control Matrix

| Path | Foreground | Background W1 | Background W2 | Background W3 |
|---|---|---|---|---|
| `/mnt/d/0local/gitrepos/{repo}/.claude/hooks/state/` | ✓ | ✓ | ✓ | ✓ |
| `/mnt/d/0local/gitrepos/faerie2/.claude/hooks/state/` | ✓ | ✗ | ✗ | ✗ |
| `/mnt/d/0local/gitrepos/{repo}/docs/` | ✓ | ✓ | ✓ | ✓ |
| `$CT_VAULT/00-SHARED/Design-Narratives/` | ✓ | ✓ | ✓ | ✓ |
| `/mnt/d/0local/gitrepos/{repo}/forensics/` | ✓ | ✓ | ✓ | ✓ |
| `$CT_VAULT/00-SHARED/` (other categories) | ✓ | ✓ | ✓ | ✓ |
| `{repo}/.claude/memory/pollen-*.md` | ✓ | ✓ | ✓ | ✓ |
| `~/.claude/memory/*.md` | ✓ via subprocess | ✗ | ✗ | ✗ |

---

## Rationale

**Foreground-only paths** (faerie2 state, system design docs, durable memory):
- Orchestration state is process-scoped; background agents don't need to read/write it
- Design docs are read-once at session start (foreground context phase)
- Durable memory (HONEY, NECTAR) is promoted by memory-keeper at `/handoff` time (foreground, end-of-cycle)

**Background-safe paths** (repo manifests, forensic logs, vault outputs, scratch):
- Agents write their results to manifest files immediately upon completion
- Forensic COC is hook-managed (PostToolUse fires for every agent write)
- Vault outputs use Syncthing eventual consistency (no race conditions)
- Scratch (pollen) is session-scoped; append-only by design

**Symlink trap root cause:**
- `/mnt/d/0LOCAL/.claude` → symlink to `/mnt/c/Users/amand/.claude/`
- Claude Code's Write tool sandboxes `/mnt/c/` for interactive approval (resource isolation)
- Background agents launched via `Agent tool` with `run_in_background: true` cannot request interactive permission
- Solution: keep background agent writes to `/mnt/d/` partition only
- Foreground agents (main session) can write to `/mnt/c/` via subprocess fallback

---

## Implementation Checklist

- [ ] **Fix #1:** Update `stigmergy_tracker.py` to use repo-scoped manifest paths instead of resolving via HOMEDRIVE
  - Current: `Path.home() / ".claude" / "hooks" / "state" / "manifest.jsonl"` (resolves to `/mnt/c/...`)
  - New: `/mnt/d/0local/gitrepos/{repo_key}/.claude/hooks/state/stigmergy-manifest.jsonl`
  - Detection: read repo-detection logic from `register_project_path.py`

- [ ] **Fix #2:** Move design documents from `/mnt/d/0LOCAL/.claude/hooks/state/` to repo docs + vault
  - Files to migrate: `forensic-system-design.md`, `artifact-registry-design.md`, `forensic-system-summary.md`, `forensic-layers-visual.txt`, `forensic-implementation-checklist.md`, `forensic-schema-reference.json`, `DELIVERY-SUMMARY.md`, `FORENSIC-SYSTEM-INDEX.md`
  - Primary location: `/mnt/d/0local/gitrepos/{repo}/docs/` (git-tracked, visible to agents)
  - Mirror location: `$CT_VAULT/00-SHARED/Design-Narratives/` (Syncthing-synced for vault visibility)
  - Update references in ARCHITECTURE.md, HONEY.md, spawn prompts

- [ ] **Fix #3:** Consolidate forensics directories
  - Audit: `/mnt/d/0LOCAL/.claude/forensics/` contains only 2 files? Move to `/mnt/d/0LOCAL/.claude/memory/forensics/`
  - Repo forensics: `/mnt/d/0local/gitrepos/{repo}/forensics/` is the authoritative location (immutable, git-tracked, COC-chained)
  - Eliminate orphan `/mnt/d/0LOCAL/.claude/forensics/` directory entirely

- [ ] **Fix #4:** Write foreground-only subprocess protocol to subagent-write-protocol.md
  - Document the pattern: subagents return output, main session uses Bash inline Python to write to `~/.claude/memory/` files
  - Include template for JSON response structure + parent apply script
  - Update spawn prompt boilerplate

---

## Spawn Prompt Update Template

When spawning any background agent (W2, W3, background tasks), include this section:

```
WRITE LOCATIONS:
Write access is restricted to these paths (sandboxed for security):
  - Manifest return: {repo}/.claude/hooks/state/wave{N}-{type}-result.json (REQUIRED)
  - Full output: {repo}/.claude/hooks/state/wave{N}-{type}-full.json (optional but recommended)
  - Design docs: {repo}/docs/{slug}.md (git-tracked, if applicable)
  - Design docs mirror: $CT_VAULT/00-SHARED/Design-Narratives/{slug}.md (Syncthing-synced, if applicable)
  - Vault: $CT_VAULT/00-SHARED/{category}/ (findings, droplets, dashboards, etc.)
  - Scratch: {repo}/.claude/memory/pollen-{SESSION_ID}.md (if memory observations)
  - Forensics: {repo}/forensics/ (append-only COC logs, if applicable)

DO NOT attempt to write to:
  - ~/.claude/memory/* (sandboxed) — return output, parent applies via subprocess
  - /mnt/c/Users/amand/.claude/* (symlink target, blocked)
  - /mnt/d/0LOCAL/.claude/docs/ (no longer valid target)
  - Anything outside {repo}/ scope unless explicitly listed above

All paths are canonical per CANONICAL-WRITE-LOCATIONS.md.
```

---

## Reference

- **Symlink discovery:** `/mnt/d/0LOCAL/.claude` → `/mnt/c/Users/amand/.claude/` (detected 2026-04-07)
- **Architect session:** abb7cb7d487600400 (Plan agent, completed 2026-04-07)
- **Approved by:** User confirmation 2026-04-07: "yes forensic logs never go directly in .claude folder by design"
- **Status:** Awaiting implementation by python-pro or fullstack-developer

