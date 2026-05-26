---
type: mission-node
status: unknown
created: 2026-05-25
tags: [swarmy-doctrinal-hardening, bearing-s]
task_id: doctrinal-hardening-P1-P2
mission: swarmy-doctrinal-hardening
bearing: S
timestamp: 2026-05-25T00:11:30
node_path: 20-Mission-Graph/doctrinal-hardening-p1-p2.md
source_manifest: /mnt/d/0local/gitrepos/faerie2/forensics/manifests/2026-05-25/00-11-30Z_manifest_doctrinal-hardening_P1-P2.json
prev_entry_hash: 41887dc98ec34f10aca5d89e86b07f4793e9510643c27421457b49438bfd49f1
entry_hash: 1d7f8aa9055c5a24c6ed55f02a06cced795ea559268fd1091691c5d0de718d41
---

# doctrinal-hardening-P1-P2

**Mission:** swarmy-doctrinal-hardening
**Status:** unknown
**Bearing:** South (ship)
**Completion:** `seal` — Both phases shipped end-to-end. P1 makes the corrections doctrine mechanical: charter status is no longer an operator JSON edit but a function of signed-manifest count (4x_charter_aggregator.py runs clean — surfaces 11 pre-existing manual-vs-derived discrepancies as real signal), and the spawn-brief detector (9x_spawn_brief_audit.py) baselined 15 prefilled-completion_choice violations across .agents/agents/*, .claude/agents/*, .archive/deprecated-skills/*, docs/* and one hook. Both scripts now wired daily via install-crons.sh and the shape registry's spawn_brief.prescribes_completion_choice detector resolves to the new scanner. P2 closes the silent degrade-to-allow: the altimeter writer is now in SessionStart (init+update) AND in PostToolUse on write events, so hooks/state/altimeter.json + session-start.json stay fresh — OP-gate and completion-trajectory-gate now read real wave + context_pct instead of falling back to permissive defaults. SessionStateMCPMixin extracted as tools/_session_state_mixin.py (helpers, not class — both tools are functional MCP registrations); swarmy_canvas + swarmy_pair_state both refactored to share safe_segment/atomic_write_json/state_etag/require_member/publish_event/hash_user_token. The ESLint rule lives in deploy/chat-mvp/.eslintrc.json with a no-restricted-syntax pattern, plus a freestanding shell gate at scripts/9x_chat_mvp_fetch_ban.sh that's pre-commit/CI friendly; 17 existing offenders grandfathered with eslint-disable-next-line + TODO comment so the check is clean (regression-blocker, not refactor-by-flag-day). Z-index migration swept 13 files to var(--z-*) tokens; 21 files documented as resisters in tokens.css (intra-component micro-stacking 1-50 + 3 archived dashboards using 8000 — promoting these would over-constrain and risk z-fighting). Chat-mvp build passes post-migration. The throughline is mechanical enforcement: every piece of doctrine in this charter now has a script that catches drift instead of relying on operator vigilance.

## Summary

P1 shipped: charter aggregator (DERIVES status from signed manifests) + spawn-brief detector (15 violations baselined) + manifest schema accepts charter_id/charter_phase. P2 shipped: altimeter wired into SessionStart+PostToolUse hooks (no more silent degrade-to-allow), SessionStateMCPMixin extracted (canvas + pair_state both refactored), fetch('/api/tools/...') ESLint rule + grep ban (17 offenders grandfathered), z-index migration (13 files → tokens; 21 files resist as documented micro-stack).

## Outbound Edges

*(no outbound edges)*

## Inbound Edges

*(no inbound edges)*
