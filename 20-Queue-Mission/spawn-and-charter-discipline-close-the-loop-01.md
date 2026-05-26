---
type: mission-node
status: final
created: 2026-05-21
tags: [swarmy-production-runway, bearing-n]
task_id: spawn-and-charter-discipline-close-the-loop-01
mission: swarmy-production-runway
bearing: N
timestamp: 2026-05-21T16:51:35
node_path: 20-Mission-Graph/spawn-and-charter-discipline-close-the-loop-01.md
source_manifest: /mnt/d/0local/gitrepos/faerie2/forensics/manifests/2026-05-21/2026-05-21T165135Z__manifest_spawn-and-charter-discipline-close-the-loop-01_general-purpose_swarmy-production-runway_05-21.json
prev_entry_hash: 477daa84b3dcd96e266a9174002a797c0b7c314e6bb7a4cf44a92095c8ec736c
entry_hash: d59865268181b9d23ed0296ab8e139575592185794aa9964deea645ea60686ab
---

# spawn-and-charter-discipline-close-the-loop-01

**Mission:** swarmy-production-runway
**Status:** final
**Bearing:** North (unblock)
**Completion:** `promote` — Closed the discipline loop on three integrity gaps. Cut 1: .agents/skills/spawn/SKILL.md now mandates scripts/0x_manifest_writer.py (4 refs added, was 0); agents instructed via CLI+API forms with explicit prohibition on inline open().write() — the PostToolUse hook 9x_hook-manifest-filename-enforce.py blocks them at the OS boundary anyway. Cut 3: All 7 active charters backfilled with coc_chain blocks. New scripts/_charter_lib.py mirrors the _metric_lib.py pattern: write_charter() + backfill_charter() + sign_and_promote() API, computes sha256 over canonicalized parent charter bodies (depends_on -> parent_hashes resolution), uses 9x_agent_sign.py for ed25519 signing with UNSIGNED_LEGACY/pending_human_signature placeholder when keys absent. swarmy-production-runway charter correctly links to its 2 parents. Cut 4: .openhands/hooks/9x_hook-charter-discipline.py shipped + wired into hooks.json post_tool_use Write|Edit|MultiEdit matcher; rejects writes to forensics/charters/active|closed lacking coc_chain (exit 2 on reject, exit 0 on pass; both smoke-tested). draft/ writes permitted without chain (discipline applies at promotion). Cut 5: Charter authoring section appended to spawn SKILL.md with 5-step protocol. Cut 2 audit (read-only, no fixes per scope) surfaced 5 follow-up gaps in discovered_work[]: 9x_charter_lifecycle.py bypasses canonical writer, 0x_bundle.py + 0x_bundle_writer.py are STUBs, CLAUDE.md references missing 7x_spawn_template.py, charter-hash-generator and _charter_lib should consolidate to one writer, and the 7 legacy charters need real human ed25519 signatures. Sandwich measurements all PASS: spawn_skill_writer_refs 0->4; charters_with_coc_chain 0/7 -> 7/7; charter_hook_present 0->1; charter_hook_wired_in_hooks_json 0->1. No regressions. closed/ charters untouched (sealed forensic record). This manifest written via mw.write_manifest() — dog-fooding cut 1.

## Summary

spawn-skill writer-refs 0->4, 7/7 charters chained, charter-hook armed, 5 gaps surfaced

## Outbound Edges

- [[audit-charter-lifecycle-routing-via-canonical-writer|North (unblock) → audit-charter-lifecycle-routing-via-canonical-writer]]  - [[restore-0x-bundle-py-from-stub|North (unblock) → restore-0x-bundle-py-from-stub]]  - [[create-or-remove-7x-spawn-template-claudemd-ref|West (baseline) → create-or-remove-7x-spawn-template-claudemd-ref]]  - [[wire-9x-charter-hash-generator-into-charter-lib|East (parallel) → wire-9x-charter-hash-generator-into-charter-lib]]  - [[human-sign-7-legacy-charters|South (ship) → human-sign-7-legacy-charters]]

## Inbound Edges

*(no inbound edges)*
