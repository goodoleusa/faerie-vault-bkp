---
type: audit-report
tags: [audit, vault-sync, faerie, gaps, collaboration]
parent: "[[INDEX]]"
status: final
generated: 2026-04-07
agent: research-analyst
doc_hash: sha256:0531ff18193967277e1fc4919caa1a6e747b2a211d1eea0049b7d09979ad4ad1
hash_ts: 2026-04-07T03:17:19Z
hash_method: body-sha256-v1
---

> [[HOME]] > [[INDEX|00-META]] > **Collaboration Flow Audit**

# Vault-Faerie Collaboration Flow Audit

**Date:** 2026-04-07
**Agent:** research-analyst (audit pass)
**Task:** Audit vault-faerie collaboration flow for gaps, routing issues, and sync failures
**Sources:** `.claude/rules/`, `~/.claude/memory/`, vault structure, hook scripts, settings.json
**Prior context:** wave3-collab-audit (RUN001) — complementary, not duplicate

---

## Anti-Assertion Protocol

All claims drawn from direct file inspection of hook scripts, vault structure, sync state files,
and rule documentation. Confidence levels noted per finding.

---

## Executive Summary

12 gaps identified across four categories: **sync automation**, **zone enforcement**,
**notification paths**, and **onboarding documentation**. Three gaps are HIGH priority
(obsidian-git disabled, Droplets silent, Human-Inbox empty). Most are fixable with
small hook or documentation changes.

---

## What Is Actually Working (confirmed)

| Component | Status | Evidence |
|-----------|--------|----------|
| `vault_narrative_sync.py` | ✅ Running | Agent-Outbox has `2026-04-07-findings.md` |
| `queue_vault_sync.py --hook` | ✅ Running | Last run: `2026-04-07T02:54:17Z` |
| `Queue/sprint-board.md` (kanban) | ✅ Written | Updated this session |
| `Session-Briefs/LATEST-brief.md` | ✅ Written | Updated on Stop hook |
| `vault_hash_stamp.py` (PostToolUse) | ✅ Active | Hashes present in vault files |
| `vault_annotation_sync.py` | ✅ At /faerie | Runs when faerie invoked |

---

## Gap Inventory

### GAP-001 — Obsidian-git fully disabled (HIGH)

**Finding:** All auto-sync intervals are `0` in Obsidian-git config (`autoSaveInterval: 0`,
`autoPushInterval: 0`, `autoPullInterval: 0`, `autoPullOnBoot: false`). Remote
collaborators receive stale vault data unless they manually sync or Syncthing propagates.

**Impact:** Any collaborator not on the same LAN as Syncthing sees hours-old data.

**Recommendation:** Enable `autoPullInterval: 5` (minutes) OR document that Syncthing
is the authoritative sync mechanism and Obsidian-git is backup-only. Currently neither
is documented in COLLAB-README (see GAP-006).

**Confidence:** HIGH (confirmed in `.obsidian/plugins/obsidian-git/data.json`)

---

### GAP-002 — Droplets/ not being written (HIGH)

**Finding:** `00-SHARED/Droplets/` folder exists but contains no `LIVE-{date}.md` files.
The rules specify agents should write real-time insights here ("Droplets are sacred").
No agent is calling `memory_bridge.py --stream` or directly writing to Droplets/.

**Impact:** Insights formed during deep analysis are being lost at context compaction.
This is exactly the scenario the Droplets protocol was designed to prevent.

**Recommendation:** Add explicit Droplets write step to faerie's Turn-1 checklist.
Verify `memory_bridge.py --stream` exists and is callable by agents.

**Confidence:** HIGH (confirmed: no LIVE-* files in Droplets/)

---

### GAP-003 — Human-Inbox/flags/ and /findings/ empty (HIGH)

**Finding:** `00-SHARED/Human-Inbox/flags/` and `00-SHARED/Human-Inbox/findings/` exist
but contain no files. The rules state that HEADLINE/CONNECTION/THREAD entries
"auto-promote to vault 00-SHARED/Human-Inbox/ at session end (memory-keeper Phase 9)."
This promotion path is silently failing.

**Impact:** Human never sees agent flags or findings in Obsidian — they must check
REVIEW-INBOX.md in a terminal instead of reviewing in the vault UI.

**Recommendation:** Debug memory-keeper Phase 9 promotion. Verify that `vault_push.py`
routes to `00-SHARED/Human-Inbox/` (check actual write paths vs vault structure).
A mismatch was observed: `vault_push.py` may be writing to `00-Inbox/AGENT-REVIEW-INBOX.md`
(old path) instead of `00-SHARED/Human-Inbox/`.

**Confidence:** HIGH (confirmed: both subdirs empty, rules say they should be populated)

---

### GAP-004 — vault_annotation_sync.py not in settings.json hooks (MED)

**Finding:** `vault_annotation_sync.py` is called in the faerie SKILL.md but NOT listed
in `settings.json` hooks. It runs only when `/faerie` is explicitly invoked — not
automatically between sessions or mid-session.

**Impact:** Human annotations in Obsidian do not propagate back to faerie until the
user explicitly runs `/faerie`. Any annotation made between sessions is invisible
to agents until the next session start.

**Recommendation:** Add `vault_annotation_sync.py --hook` to `UserPromptSubmit` hooks
alongside `queue_vault_sync.py --hook`, with same delta-check pattern to avoid excess I/O.

**Confidence:** HIGH (confirmed: settings.json hook list reviewed)

---

### GAP-005 — Session brief `session_id: unknown` (MED)

**Finding:** `Session-Briefs/LATEST-brief.md` has `session_id: unknown` — the Stop hook
writing the brief is not capturing the active session ID. This means session briefs
cannot be correlated with scratch files or COC entries by ID.

**Impact:** Forensic trail is weakened. Cannot map "session brief X" to "scratch-Y.md"
to "COC entry Z" without manual timestamp correlation.

**Recommendation:** Pass `CLAUDE_SESSION_ID` to the Stop hook via environment, or
read it from the active agent state file before writing the brief.

**Confidence:** HIGH (confirmed: LATEST-brief.md inspected, session_id field = "unknown")

---

### GAP-006 — 00-META has no COLLAB-README (MED)

**Finding:** `00-META/` folder exists but had no onboarding documentation for remote
collaborators. No COLLAB-README, no WRITE-ROUTING, no "how to contribute" guide.
A collaborator opening the vault for the first time has no entry point for understanding
the write-zone rules or the agent-human collaboration protocol.

**Impact:** Remote collaborator onboarding depends entirely on a verbal briefing.
Any new collaborator (human or AI) reading the vault will violate write-zone rules
by accident.

**Recommendation:** Write COLLAB-README.md to 00-META with: write-zone map,
agent-owned vs human-owned paths, how to read agent findings, how to leave tasks.
(This audit is a partial fix — a COLLAB-README should follow.)

**Confidence:** HIGH (confirmed: directory listing showed no COLLAB-README)

---

### GAP-007 — No notification when agents write to Agent-Outbox (MED)

**Finding:** No mechanism notifies the human when agents write new findings to
`Agent-Outbox/`. Human must open Obsidian and check manually, or rely on HOME.md
dataview queries (if those are configured to watch Agent-Outbox).

**Impact:** Findings sit unread until human happens to check. For time-sensitive
investigation findings, this delay matters.

**Recommendation:** Add Agent-Outbox dataview to HOME.md that lists recent agent
outputs. Alternatively, write a brief notification to `Human-Inbox/findings/` every
time `vault_narrative_sync.py` writes to Agent-Outbox (a pointer file, not a duplicate).

**Confidence:** MED (HOME.md dataview configuration not fully inspected)

---

### GAP-008 — No conflict resolution for concurrent vault .md writes (LOW)

**Finding:** Multiple agents can write to vault `.md` files concurrently. `queue_vault_sync.py`
has `fcntl.flock` for the JSON queue file, but vault `.md` files (Agent-Outbox findings,
Droplets, Human-Inbox) have no locking. Last-write-wins under concurrent spawns.

**Impact:** LOW in practice — agents rarely write the same vault file simultaneously.
Higher risk when parallel agent waves are launched.

**Recommendation:** Add file locking to `vault_narrative_sync.py` write paths,
or use append-only naming (one file per agent per run) to avoid overwrites.

**Confidence:** MED (code inspection, no observed collision yet)

---

### GAP-009 — Agent-Inbox unused and undocumented (LOW)

**Finding:** `00-SHARED/Agent-Inbox/` exists with a stub README saying it's
"reserved for future use." No routing sends messages to this folder. If the intent
was agent-to-agent messaging, the mechanism is unimplemented.

**Impact:** LOW — unused stub. But if any rule relies on agents reading Agent-Inbox,
it silently fails.

**Recommendation:** Either implement Agent-Inbox as a drop zone for human→agent
tasks (complementing the vault Queue/ folder), or explicitly deprecate it and
remove the stub to avoid confusion.

**Confidence:** HIGH (confirmed: only stub README in Agent-Inbox)

---

### GAP-010 — queue_vault_sync --export not automatic (LOW)

**Finding:** `queue_vault_sync.py --export` (which pushes sprint-queue.json changes
back to vault Queue/sprint-queue.md) is not triggered automatically. The `--hook`
mode on UserPromptSubmit only does `--import`. If faerie modifies the queue
(task added, task completed), the vault Queue/ file goes stale until manually exported.

**Impact:** Human viewing queue in Obsidian sees stale data between sessions.
Note: This session's queue export was fresh (2026-04-07T02:54:17Z), so the gap
is timing-dependent, not persistent.

**Recommendation:** Add `queue_vault_sync.py --export` to the Stop hook so the
vault queue is updated at session end.

**Confidence:** HIGH (hook inspection confirmed --export not in Stop hook)

---

### GAP-011 — REVIEW-HOT.md not auto-regenerated (LOW)

**Finding:** `REVIEW-HOT.md` is described as "regenerated by membot" but no hook
triggers this regeneration automatically. If membot is not spawned at session start,
the file goes stale and agents reading it see outdated active-flags context.

**Impact:** Agents reading stale REVIEW-HOT.md may miss newly flagged issues or
act on resolved flags.

**Recommendation:** Add REVIEW-HOT.md staleness check to faerie Turn-1 checklist:
if file is >24h old, spawn membot to regenerate before proceeding.

**Confidence:** MED (last-modified timestamp of REVIEW-HOT.md not checked in this audit)

---

### GAP-012 — vault_push.py path mismatch with vault structure (LOW)

**Finding:** `vault_push.py` appears to route to `00-Inbox/AGENT-REVIEW-INBOX.md`
(old vault structure) while current vault reorganization moved the human inbox to
`00-SHARED/Human-Inbox/`. If this mismatch is confirmed, agent HIGH-flag promotions
go to a location humans no longer monitor.

**Impact:** Could explain why `00-SHARED/Human-Inbox/flags/` is empty (GAP-003).
This would elevate GAP-012 to HIGH if confirmed.

**Recommendation:** Audit `vault_push.py` target paths against current vault structure.
Run `grep -r "00-Inbox" scripts/` to find all old-path references.

**Confidence:** MED (code inspection was partial — needs confirmation)

---

## Gap Priority Summary

| ID | Priority | Title | Owner | Action |
|----|----------|-------|-------|--------|
| GAP-001 | HIGH | Obsidian-git disabled | human | Enable autoPull or document Syncthing as canonical |
| GAP-002 | HIGH | Droplets/ not being written | faerie + agents | Verify memory_bridge.py; add to Turn-1 |
| GAP-003 | HIGH | Human-Inbox empty (promotion silently failing) | data-engineer | Audit vault_push.py paths |
| GAP-004 | MED | vault_annotation_sync not in auto-hooks | data-engineer | Add to UserPromptSubmit |
| GAP-005 | MED | session_id: unknown in session briefs | data-engineer | Pass CLAUDE_SESSION_ID to Stop hook |
| GAP-006 | MED | No COLLAB-README in 00-META | memory-keeper | Write onboarding doc |
| GAP-007 | MED | No notification for Agent-Outbox writes | fullstack-developer | HOME.md dataview or pointer files |
| GAP-008 | LOW | No conflict resolution for .md writes | data-engineer | Append-only naming or flock |
| GAP-009 | LOW | Agent-Inbox unused stub | memory-keeper | Implement or deprecate |
| GAP-010 | LOW | queue_vault_sync --export not in Stop hook | data-engineer | Add to session_stop_hook.py |
| GAP-011 | LOW | REVIEW-HOT.md not auto-regenerated | faerie | Add staleness check to Turn-1 |
| GAP-012 | LOW | vault_push.py may have old path references | data-engineer | Grep + fix old 00-Inbox paths |

---

## Quick Wins (implement in <30 min each)

1. **GAP-010:** Add `queue_vault_sync.py --export` to session_stop_hook.py — 5 min
2. **GAP-004:** Add `vault_annotation_sync.py --hook` to UserPromptSubmit in settings.json — 5 min
3. **GAP-012:** `grep -r "00-Inbox" scripts/` and update paths to `00-SHARED/Human-Inbox/` — 15 min
4. **GAP-005:** Pass `$CLAUDE_SESSION_ID` env var to vault_narrative_sync.py in Stop hook — 10 min
5. **GAP-009:** Deprecate Agent-Inbox stub by adding note to README that it's unused — 2 min

---

## Remote Collaborator Flow (current state)

For a remote collaborator with vault access via Syncthing:

```
THEY CAN READ (reliably):
  00-SHARED/Agent-Outbox/     ← agent findings (written each session via vault_narrative_sync)
  00-SHARED/Queue/            ← sprint queue (last exported 2026-04-07)
  00-SHARED/Dashboards/       ← session briefs (LATEST-brief.md updated each session)
  00-SHARED/00-META/          ← architecture docs (this file)

THEY CANNOT READ (broken or empty):
  00-SHARED/Droplets/         ← no LIVE-* files written (GAP-002)
  00-SHARED/Human-Inbox/      ← flags/findings not populated (GAP-003)
  00-SHARED/Agent-Inbox/      ← unused stub (GAP-009)

THEY CAN WRITE:
  00-SHARED/Queue/            ← human edits sprint tasks in Obsidian
  00-SHARED/Hive/             ← system change proposals
  (via annotation) any vault doc  ← picked up by vault_annotation_sync at /faerie
```

---

*Generated: 2026-04-07 | Agent: research-analyst | Run: vault-collab-flow-audit*

*[[FAERIE-VAULT-FLOW|Faerie-Vault Flow Diagram]] · [[INDEX|Meta Index]] · [[00-SHARED/Dashboards/system/System-Architecture|System Architecture]]*
