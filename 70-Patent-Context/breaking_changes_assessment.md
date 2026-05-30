# Breaking Changes Assessment — Mission Architecture Enforcement

**task_id:** mission-architecture-enforcement
**investigation_label:** mission-architecture-enforcement
**dashboard_line:** 6 broken wires; emergence intact; 3 silent backup/sign no-ops; charter unimplemented
**compass_edge:** N (north — unblock prerequisites: missing scripts before further alignment)
**ts:** 2026-04-29

## Executive Summary

The active stigmergy substrate is intact (manifest paths, investigation_label clusters, mission-trails directories, COC hash chain, mission crystallizer). However, the canonical model `docs/44-MISSION-NAVIGATION-MODEL.md` introduces three architectural layers (MAP/COMPASS/CHARTER) only one of which is fully realized in code. Several settings.json hook wires reference scripts that **do not exist on disk**, producing silent no-ops shielded behind `2>/dev/null || true`.

**Critical principle preserved:** No emergence logic was found broken. Compass N/S/E/W bearing semantics are consistent across producers and consumers. Investigation_label pheromone trails work end-to-end. The Loom can still spawn, route, and return manifests.

**Critical principle at risk:** the CHARTER layer (deadlines, deliverables, success_criteria, map_boundary) is documentation-only. Without it, exploration is unbounded and there is no measurable `done`.

## Severity Matrix

| Finding | Severity | Affects Emergence? | Active Runtime Impact |
|--------|----------|---------------------|------------------------|
| `9x_forensic_signer.py` wired but missing | HIGH | No | Silent — Ed25519 signing never runs |
| `5x_b2_realtime_uploader.py` wired but missing | HIGH | No | Silent — B2 WORM async backup never queues |
| `5x_b2_manifest_uploader.py` wired but missing | HIGH | No | Silent — manifest realtime backup never runs |
| Layer 3 CHARTER unimplemented | HIGH | Yes (no scope frame) | No charter-bounded runs; spawn `--charter` arg unwired |
| `next_mission_node` dict not produced | MEDIUM | Yes (no FROM→TO vectoring) | Agents have no explicit dead-reckoning vector |
| `from_label` / `to_label` absent | MEDIUM | Partial (cross-mission bearings cannot be expressed) | Cross-mission compass edges encoded only by colocation |
| `7x_queue_ops.py` deleted, callers exist | MEDIUM | No (callers not wired) | Latent — would break if reactivated |
| `7x_mission_graph_ops.py` deleted, callers exist | LOW | No | Latent — `9x_intent_to_mission_graph.py` not wired |
| `9x_queue_janitor_scout.py` deleted, callers exist | LOW | No | Latent — `8x_mission_janitor_rotation.py` not wired |
| Dangling symlink `/mnt/d/0LOCAL/.claude/scripts/7x_queue_ops.py` | LOW | No | Confuses readlink-based discovery |
| `8x_vault_mutation_tracker.py` not wired | LOW | No | Vault hash-track promise unenforced |

## Will Any Of These Break Emergence?

**No.** The emergence-critical primitives are:
1. Manifest writes by agents (working — see `0x_promote_to_forensics.py` PostToolUse wire)
2. Investigation_label clustering (working — `0x_mission_trail_builder.py` actively builds 35 trail directories)
3. Compass edge bearing (working — produced by spawn templates, consumed by mission_graph_sync, crystallizer, queries)
4. COC hash chain (working — `0x_coc_finalizer.py` PostToolUse wire, hash-linked at line 65)
5. Mission crystallization (working — wired in settings.json:124, evaluates 35 missions, marks 21 ready)

The broken wires affect **forensic durability** (B2 WORM backup), **agent identity** (signed manifests), and **policy enforcement** (vault mutation tracking). All operate behind silent `|| true` so they fail-open: the system continues without them.

## Will Any Of These Break Stigmergy?

**No.** Pheromone trail integrity:
- 35 mission-trail directories present in `forensics/mission-trails/`
- 425 occurrences of `investigation_label` across scripts/hooks
- 160 occurrences of `compass_edge` (consistent N/S/E/W vocabulary)
- Mission-trail builder is wired and idempotent (live test: scanned 15 missions, 0 new symlinks needed)

## Will Any Of These Break the COC Chain?

**No.** The hash chain is intact:
- `0x_coc_preallocator.py` PreToolUse: pre-write hash entry
- `0x_coc_finalizer.py` PostToolUse: post-write entry, sha256-linked to previous entry hash
- `4x_forensic_coc.py posttool` PostToolUse: secondary capture
- `8x_state_write_coc_enforcer.py` PreToolUse: enforces COC presence on writes
- `8x_protect_coc_paths.py` PreToolUse: deny-rule guardrails

**However:** `9x_forensic_signer.py` is missing. Implementation Rule #4 in CLAUDE.md ("Every agent signs output (Ed25519)") is unenforced. COC entries lack signed envelopes; signature verification cannot be performed downstream.

## Terminology Drift Summary

| Canonical Term (doc 44) | Implementation Term | Drift |
|-------------------------|---------------------|-------|
| MAP | mission-graph / mission-trails | None (synonym, code uses lower-case literal) |
| COMPASS | compass / compass_edge | None (lower-case literal) |
| CHARTER | (absent) | TOTAL — no genesis_manifest.json, no charter loader |
| next_mission_node | next_task_queued | Schema drift — string vs dict; `_queued` violates Tesla valve flow rebrand |
| {bearing, from_label, to_label} | compass_edge (string only) | Schema drift — single-letter bearing only |
| genesis_manifest.json | (absent) | TOTAL |
| crystallization_metrics.json | mission-crystallizations/ contents | Naming drift — concept exists in `1x_mission_crystallizer.py` output but not file name |

## Risk-Free Hygiene Operations

These can be done now without measurement (per FUNDAMENTAL GOVERNANCE RULE: don't add abstractions; align references to existing scripts):

1. **Fix three broken hook wires** — replace nonexistent script paths with the actual ones (or remove the wires entirely if no replacement exists). Pure rename, no new abstractions.
2. **Remove the dangling symlink** at `/mnt/d/0LOCAL/.claude/scripts/7x_queue_ops.py`.
3. **Update header comments** in 3 hooks that reference `7x_queue_ops.py` / `7x_mission_graph_ops.py` / `9x_queue_janitor_scout.py` to reflect the deletions.
4. **Promote `next_task_queued` -> `next_mission_node`** as a non-breaking, dual-write field (write both, read both) so consumers can migrate without forklift.

## Operations That Require Mutation Discipline

Before adding these, baseline must be measured per FUNDAMENTAL GOVERNANCE RULE:

1. **Implementing the CHARTER layer** — adds genesis_manifest.json, charter loader, charter_boundary check in spawn. New abstraction; demands baseline measurement of "exploration without bounds vs exploration with charter" pre-/post-fix.
2. **Upgrading `compass_edge` from string to dict** — schema mutation. Requires baseline of compass_edge consumer behavior, then schema mutation, then measure consumer breakage rate.
3. **Wiring currently-unwired stigmergy hooks** (`9x_droplet_live_sync.py`, `8x_manifest_first_guardian.py`, `8x_vault_mutation_tracker.py`). Each is a hook addition; baseline-measure session-level metrics first.

## What I Did NOT Verify (Honest Limits)

- **Behavioral correctness** of the COC chain after the broken-wire fixes. (Static reference check only; no end-to-end mutation test was run.)
- **Whether the project's `0x_b2_realtime_uploader.py`** (which exists at `hooks/0x_b2_realtime_uploader.py`) is functionally equivalent to the missing `5x_b2_realtime_uploader.py` referenced in settings. Path inspection only.
- **Charter migration strategy** — doc 44 promises `genesis_manifests/{YYYY-MM-DD}/` but we did not check whether stub files exist anywhere.
