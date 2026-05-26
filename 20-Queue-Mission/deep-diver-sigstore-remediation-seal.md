---
type: mission-node
status: unknown
created: 2026-05-25
tags: [script-consolidation-and-charter-signing-chain, bearing-e]
task_id: deep-diver-sigstore-remediation-seal
mission: script-consolidation-and-charter-signing-chain
bearing: E
timestamp: 2026-05-25T15:49:34
node_path: 20-Mission-Graph/deep-diver-sigstore-remediation-seal.md
source_manifest: /mnt/d/0local/gitrepos/faerie2/forensics/manifests/2026-05-25/20260525T154934Z__manifest_deep-diver-seal_deep-diver_sigstore-remediation-and-provision_05-25.json
prev_entry_hash: 21142d92b324677f5217150531b4ad0555c7b1348e5c809e14ce17e84f34ccbe
entry_hash: 6797786a57261aa0e399d37c62b71612ec1679460e35ff51ef0ca82b082bee2b
---

# deep-diver-sigstore-remediation-seal

**Mission:** script-consolidation-and-charter-signing-chain
**Status:** unknown
**Bearing:** East (parallel)
**Completion:** `seal` — All Phase 4 deliverables in scope for this session are shipped and round-trip verified: (1) Keypairs provisioned for opus-main and anon-viewer-agent via 5f_init_reputation.py. (2) Four manifests in forensics/manifests/2026-05-25/ backfilled — P1-P2 (was UNSIGNED_opus-main_NO_KEY), P3-P4 (was missing signed_by), viewer-cut-g (prose completion_choice → structured {kind,target,confidence,sensitivity,rationale} shape + sign), backend-wiring (was missing signed_by). All four now verify PASS via 9x_manifest_verifier.py. (3) scripts/9x_manifest_signer.py ships: signs manifest body (canonical JSON, excluding signed_by+signer) with Ed25519 via 5e_agent_sign.py, auto-fills coc_chain.parent_hashes from COC tail, auto-resolves charter_path, supports --init-key (calls 5f_init_reputation.py) and --dry-run. (4) scripts/9x_manifest_verifier.py ships: local Ed25519 verify + charter linkage check + COC parent walk + optional Rekor inclusion proof search (Phase 3+ network path, graceful offline fallback). Batch mode (verify-dir) with --strict + --report flags. (5) audit-unsigned-manifests.py extended with --verify flag — delegates to 9x_manifest_verifier.py via subprocess; adds signature round-trip summary (26 PASS / 10 FAIL / 0 skip across the 1-day window). (6) .openhands/hooks.json: session_start auto-provision hook added — idempotently runs 5f_init_reputation.py for the canonical agent-type roster (14 types) on every session start. This closes the gap: agents no longer hit UNSIGNED_*_NO_KEY because keys now exist before any manifest write. Key design decision: one key per agent_type (not per archetype×model combination) — the agent_type is the stable, routable, forensic identity unit (what 4x_charter_aggregator.py, the reputation ledger, and the spawn router all use). Archetypes (DEEP-DIVER, MAKER, NAVIGATOR) map 1:1 to agent_types (deep-diver, maker, navigator) — the uppercase/lowercase is a display convention, not a separate key namespace. The sigstore/keys/ tree (uppercase .priv/.pub) is a legacy parallel; future provisioning should use reputation/keys/ exclusively.

## Summary

DEEP-DIVER sealed: keypairs provisioned, 4 manifests backfilled+signed, 9x_manifest_signer.py + 9x_manifest_verifier.py shipped, audit-unsigned extended with --verify, hooks.json auto-provision wired.

## Outbound Edges

- [[di-sigstore-hook-integration|East (parallel) → DI-sigstore-hook-integration]]  - [[sigstore-keys-migration-legacy-to-reputation|West (baseline) → sigstore-keys-migration-legacy-to-reputation]]  - [[audit-backfill-missing-signed-by|South (ship) → audit-backfill-missing-signed-by]]

## Inbound Edges

*(no inbound edges)*
