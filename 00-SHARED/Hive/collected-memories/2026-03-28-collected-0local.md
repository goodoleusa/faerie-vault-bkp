---
type: collected-memory
status: unreviewed
created: 2026-03-28
updated: 2026-03-28
tags: [memory, collected, agent-memory, 0local]
source_project: "/mnt/d/0local"
source_file: "MEMORY.md"
source_path_wsl: "/mnt/c/Users/amand/.claude/projects/-mnt-d-0local/memory/MEMORY.md"
source_path_windows: "C:\Users\amand\.claude\projects\-mnt-d-0local\memory\MEMORY.md"
source_sha256: "bf422bf6636b0ad523e4d6de139390188dde3fb5d14fa00285d35caca60f46de"
source_size_bytes: 2899
collected_at: "2026-03-28T02:27:58Z"
collector: emergency_handoff.py
parent:
  - "[[agent-history]]"
sibling: []
child: []
memory_lane: inbox
promotion_state: capture
review_status: unreviewed
ann_hash: ""
ann_ts: ""
doc_hash: sha256:14eb0a16d5a0c99059c8d8988995a5fd4c2c342c25ba2d0bb188c1d554db56bc
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:31Z
hash_method: body-sha256-v1
---

# Collected Memory: 0local

| Field | Value |
|-------|-------|
| Source Project | `/mnt/d/0local` |
| Source File | `MEMORY.md` |
| Local Path (WSL) | `/mnt/c/Users/amand/.claude/projects/-mnt-d-0local/memory/MEMORY.md` |
| Local Path (Windows) | `C:\Users\amand\.claude\projects\-mnt-d-0local\memory\MEMORY.md` |
| SHA256 (at collection) | `bf422bf6636b0ad523e4d6de139390188dde3fb5d14fa00285d35caca60f46de` |
| Lines | 38 |
| Collected | 2026-03-28T02:27:58Z |

## Content

```markdown
# Project Memory — D:\0LOCAL

## Setup & Configuration
- **CLAUDE.md**: `D:\0LOCAL\CLAUDE.md` — full project rules, auto-loaded every session. Includes:
  - Status footer format (visual cache/context counters on every response)
  - ARCHITECTURE.md invisible scaffold pattern
  - Pre-compact snapshot protocol (dense handoff format)
  - Batches API step-by-step flow with code
  - Frictionless build flow (do-don't-ask, adapted from proactive-context-optimization.mdc)
- **.claudeignore**: `D:\0LOCAL\.claudeignore` — excludes build artifacts, lock files, secrets, binaries
- Cursor rules adapted: `token-optimization.mdc` + `proactive-context-optimization.mdc`

## User Preferences
- Prefers referencing file paths over pasting content; dislikes being interrupted with questions
- Uses `/compact` for long sessions, `/clear` for unrelated tasks
- Works with large codebases — context caching and strategic objective preservation are priorities
- Has Cursor background — familiar with `.cursorignore`, `.mdc` rules, ARCHITECTURE.md pattern, dense handoff prompts
- Wants visual confirmation that caching is working (status footer on every response)
- Wants pre-compact snapshots to protect big-picture strategic objectives

## Claude API Caching Patterns (confirmed working)
- `cache_control: {type: "ephemeral", ttl: "1h"}` on system blocks for large stable context
- Up to 4 cache breakpoints per request
- Verify hits: `response.usage.cache_read_input_tokens > 0`
- Files API (`betas=["files-api-2025-04-14"]`): upload once, reuse `file_id`
- 1M context beta header: `anthropic-beta: context-1m-2025-08-07` (Opus 4.6 / Sonnet 4.6)
- Compaction beta: `compact-2026-01-12` (Opus 4.6 only) — append `response.content` not just text

## Windows Shell — Critical Rules
- **Cygwin bash (default shell) has persistent fork errors on this machine** — `child_copy: cygheap read copy failed`, exit code 0xC0000142. Affects any subprocess that needs to fork (npx, ng, node, python, pip, etc.)
- **Do NOT use `npx`, `ng`, `npm run`, or long-running node commands via the Bash tool** — they will fail silently or hang
- **For Angular/Node commands:** tell the user to run them in their own terminal (Windows Terminal, VS Code integrated terminal, or PowerShell). Never retry the same failing command.
- **For simple file ops** (git, ls, python one-liners, cat): usually work fine — fork errors are intermittent, worse with complex child processes
- **Workaround pattern:** Use `python3 -c "..."` inline scripts for file manipulation instead of shell pipelines. Git commands generally work. Avoid `| tail`, `| head` pipes — they trigger fork for the piped process.
- **If a bash command fails with fork errors:** immediately stop, tell the user what command to run manually, don't retry

## Key Reference
- Full optimization guide: `C:\Users\amand\.claude\plans\tingly-questing-scroll.md`
```

## Your Annotations

<!-- What's useful here? Should any items be promoted to NECTAR/HONEY? -->
<!-- Are there tasks or threads to queue? -->

