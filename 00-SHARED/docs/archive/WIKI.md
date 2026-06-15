# Wiki — Faerie Dynamo System

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

This wiki index tracks the installable `.claude` architecture for dual-session orchestration.

## Core Pages

- `README.md` — project overview and HONEY-canonical update note.
- `docs/ARCHITECTURE.md` — system contract and component map.
- `docs/HOW-IT-WORKS.md` — plain-language mental model and runtime flow.
- `docs/narrative/README.md` — investigation narrative + **session-end auto-append** (Tier 1 + HIGH MEM).
- `.claude/rules/agent-lifecycle.md` — universal agent startup/work/failure protocol.
- `.claude/rules/memory-routing.md` — canonical memory write/read routing.
- `.claude/commands/faerie.md` — session entrypoint and orchestration behavior.

## Canonical Memory Contract

- Global canonical memory: `~/.claude/memory/HONEY.md`
- Global additive findings: `~/.claude/memory/NECTAR.md`
- Project canonical memory: `{repo}/.claude/memory/HONEY.md` (optional, recommended)
- Human review queue: `~/.claude/memory/REVIEW-INBOX.md`
- Deprecated: `~/.claude/AGENTS.md` (replaced by HONEY/NECTAR pipeline)

## Dual-Session Swirl/Eddy Model

- Run two Claude CLI sessions against the same queue/state files.
- Session A and Session B claim different tasks from `sprint-queue.json`.
- Faerie reads shared state and exposes:
  - active/queued tasks,
  - decision points for human review,
  - cross-thread connections worth queueing.
- Crystallization writes dense, evergreen memory into HONEY while preserving additive traces in NECTAR and logs.

## Turn-1 Autopilot + Missed-Handoff Recovery

- Freshness policy: `faerie-brief.json` is fast-path only when <=12h old.
- `/handoff` is still the preferred inverse command at wind-down.
- If `/handoff` was skipped, stop hook + `/faerie` self-heal keep continuity:
  - stop hook writes `faerie-recovery.json` marker,
  - `/faerie` Turn 1 spawns `membot` in background when marker/staleness is detected,
  - `/faerie` continues immediate queue orchestration without waiting.
- Turn-1 dashboard should include: auto-actions, queue summary, active agents, and project/investigation distribution.
- Runtime helper: `~/.claude/hooks/state/s3a_faerie_turn1.py` computes state (`brief_fresh` vs `brief_missing_or_stale`), queues membot recovery task when needed, enforces dead-reckoning bundle fields, and outputs Turn-1 dashboard JSON.

## Forensic COC Layer (Append-only)

- Hook script: `~/.claude/hooks/forensic_coc.py`
- PostToolUse mode appends operation entries to per-session COC JSONL with hash-chain linkage.
- Stop mode writes signed session manifest and appends a master chronological ledger entry for the investigation.
- Forensic logs are retrieved selectively for audit/legal workflows and excluded from default agent startup reads.

## Dynamo v2.1 Runtime Surface

- New command: `.claude/commands/dynamo.md`
- New runtime scripts:
  - `.claude/hooks/state/s3b_dynamo_orchestrator.py`
  - `.claude/hooks/state/dynamo_dashboard.py`
- `s3b_dynamo_orchestrator.py` executes Turn-1 checks, reports auto-actions, and emits a spawn plan.
- `dynamo_dashboard.py` gives a compact live table for queue state, active agents, and project spread.

## Open-Source Split Boundary (Orchestration vs Memory)

- Public-first orchestration manifest:
  - `modules/orchestration/manifest.json`
- Private/paywalled memory manifest:
  - `modules/memory/manifest.private.json`
- Packaging helper:
  - `scripts/0b_build_release_bundles.py`
  - output folders: `releases/windows/.claude`, `releases/linux/.claude`, `releases/macos/.claude`

## Design Principles + Benefits (v2.1)

- Brief-first startup keeps orchestration token-light.
- Turn-1 autopilot removes orchestration wait states.
- Context-bundle hardening makes subagents truly cold-start capable.
- Modular boundary supports public orchestration + private memory governance.
- Cross-platform release folders reduce install friction for open-source adoption.

## Command Cheat Sheet

### Use Commands

```text
/faerie
/dynamo
/dynamo --watch 2
/run
/queue
/task "goal"
/handoff
```

### Dev Commands (Build + Runtime)

```powershell
python "scripts/0b_build_release_bundles.py" --profile full
python "scripts/0b_build_release_bundles.py" --profile orchestration
python "C:\Users\amand\.claude\hooks\state\s3a_faerie_turn1.py"
python "C:\Users\amand\.claude\hooks\state\s3b_dynamo_orchestrator.py" --watch 2
```

## Implementation Goal

Keep context artifacts token-light at handoff time, then increase semantic density during crystallization so future sessions start with stronger priors and fewer human interrupts.
