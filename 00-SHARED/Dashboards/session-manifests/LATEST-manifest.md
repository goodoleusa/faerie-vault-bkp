---
type: session-manifest
date: 2026-03-27
consolidated: true
original_count: 12
unique_sessions: 12
plans: [staged-swinging-charm]
tags: [manifest, consolidated, daily, crystallized]
doc_hash: sha256:67962a5950ab0b85e86a707a9ceb79f8cc5209c914a33b3a4ca888fa0aadf259
hash_ts: 2026-03-29T16:10:11Z
hash_method: body-sha256-v1
---

# Daily Manifest — 2026-03-27

> **12 sessions crystallized** into one view.
> Plans active: staged-swinging-charm

---

## Decisions Crystallized (13 HONEY entries)

- [sys00002 | method | permanent | 1.0] Scope hierarchy: Global → Investigation → Sprint → Pipeline Phase → Session. Phase is ABOVE session because a phase (SEED→DEEPEN→EXTEND→FULL) spans multiple sessions with human gates between stages. `/faerie` launch should know: which investigation, which sprint, which phase, estimated sessions remaining.
- [sys00003 | method | permanent | 1.0] Command ownership: global `~/.claude/commands/` = universal orchestration (faerie, handoff, crystallize, collab, roster, team). Repo commands = domain-specific ONLY, no overlap with global. Repo command overrides global silently — duplication causes confusion about which fires.
- [sys00004 | method | permanent | 1.0] Faerie repo: `00-claude-faerie-cli-git` is dev source, `faerie2` (goodoleusa/faerie2.git) is publish target. CLI-GIT tracks faerie2 as remote. Legacy `faerie` repo (Persistech) is archived (remotes stripped).
- [sys00005 | method | 1yr | 0.95] `_resolve_claude_home()` returns `~/.claude` (the .claude dir itself). All path constructions: `CLAUDE / "hooks" / ...` — never `HOME / ".claude" / ...` (double-nesting bug found in 10+ hooks, 2026-03-25).
- [sys00006 | method | permanent | 1.0] Human gates in /data-ingest pipeline: GATE 1 (post-SEED, pre-DEEPEN) = review first impressions + seal private hypotheses. GATE 2 (post-DEEPEN) = factual corrections only. GATE 3 (post-EXTEND) = convergence review + optional red-team. GATE 4 (post-FULL) = unseal hypotheses, compare agent vs human. Scripts: `hypothesis_seal.py` (seal/reveal/verify), `gate_pass.py` (check/pass/block/correct).
- [sys00007 | identity | permanent | 1.0] data-analysis-engine is destined for open-source release: a standalone toolkit giving public interest investigators the forensic rigor and scientific methodology of a full research team. All design choices (COC, progressive disclosure, pre-registration, human gates, court-admissibility) serve this mission. Keep DAE self-contained — no dependency on global .claude state that a user wouldn't have.
- [sys00008 | method | permanent | 1.0] Three-store architecture: REPO (code+pipeline, public GitHub), VAULT (annotations+dashboards, local only, never pushed), FORENSIC STORE (.claude/forensics/, gitignored, backed up to S3 WORM). CyberOps-UNIFIED vault remote removed 2026-03-25. DAE ObsidianVault/ = sanitized template for open source users.
- [sys00009 | method | permanent | 1.0] Forensic backup: `backup_forensics.py` → S3-compatible WORM (Object Lock Compliance mode). Encrypted at rest (SSE), immutable during retention, independently timestamped. Provenance chain: raw source → local hash → git commit → pipeline transform log → audit results → vault sync (source_sha256) → annotation hash → WORM backup. Every transition has a verifiable hash. See `docs/PROVENANCE-CHAIN.md`.
- [sys00010 | method | permanent | 1.0] Vault annotation flow: human annotates in Obsidian → Ctrl+Alt+C (QuickAdd commit-annotation.js) → SHA-256 ann_hash in frontmatter → vault_annotation_sync.py reads on next session start → receipt in .claude/forensics/annotation-receipts.jsonl → corrections flow to pipeline gates. Six QuickAdd actions: commit, endorse, challenge, red-team, promote, pass-gate. No Shell Commands or Templater needed — pure QuickAdd user scripts.
- [sys00011 | method | permanent | 1.0] Emergency handoff: `python3 ~/.claude/scripts/emergency_handoff.py` fires in <5s at any context level. Collects ALL splintered `.claude/projects/*/memory/`, scratch files, queue state → writes `handoff-snapshot.json` + atomized `brief-atoms/` + nests memories into repos. /handoff Step Zero = always run this first. /faerie reads snapshot as priority #1 (1 file replaces 15 reads). Auto-compact handles working context; faerie handles investigation memory. Complementary, not competing.
- [sys00012 | method | permanent | 1.0] Atomized briefs: briefs are NOT one overwritten file. They accumulate in `brief-atoms/` (handoff atoms, pipeline phase atoms from briefgen.py). `faerie-brief.json` = lightweight pointer only. Dataview queries atoms in Obsidian; Blueprints templates assemble human reports. Normal day: 2 atoms. Data-ingest day: 4+ atoms (SEED, DEEPEN, EXTEND, handoff).
- [sys00013 | method | permanent | 1.0] FFFF dashboard model: Findings/Flags/Friction/Flow at every zoom level (team/sprint/agent/technique). MermaidJS palette: pistachio #93C572, teal #4ECDC4, gold #D4A843, dark #2d2d44. Agent OTJ self-updates require pre-snapshot via `agent_card_snapshot.py` for court-admissible provenance.
- [sys00014 | method | permanent | 1.0] HASH BEFORE AND AFTER: Any time faerie/handoff/agents move .claude folders or forensic artifacts, run `hash_tracker.py snapshot --name before-{op}` BEFORE and `--name after-{op}` AFTER. Blocking — must complete before proceeding. Per-file SHA256 in COC = file-level proof. hash_tracker = directory-level proof (catches renames/deletions/additions). Both = belt+suspenders. Script: `data-analysis-engine/scripts/hash_tracker.py`.

## Memory Files (49 unique)

- `2026-03-27-1833-manifest.json` (5390 bytes)
- `2026-03-27-1834-manifest.json` (5748 bytes)
- `2026-03-27-1836-manifest.json` (6106 bytes)
- `2026-03-27-1838-manifest.json` (6465 bytes)
- `2026-03-27-1839-manifest.json` (6823 bytes)
- `2026-03-27-1842-manifest.json` (7181 bytes)
- `2026-03-27-1843-manifest.json` (7539 bytes)
- `2026-03-27-1903-manifest.json` (7897 bytes)
- `2026-03-27-1934-manifest.json` (13145 bytes)
- `2026-03-27-1939-manifest.json` (12786 bytes)
- `2026-03-27-2003-manifest.json` (14042 bytes)
- `20260327-from--mnt-c-Users-amand--claude.md` (451 bytes)
- `20260327-from--mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIF.md` (3803 bytes)
- `20260327-from--mnt-d-0local-gitrepos-00-claude-faerie-cli-git.md` (1001 bytes)
- `20260327-from--mnt-d-0local.md` (3038 bytes)
- `20260327-from-d--0LOCAL-gitrepos-mission-defend-democracy.md` (1484 bytes)
- `20260327T183315Z-unknown.md` (876 bytes)
- `20260327T183411Z-unknown.md` (876 bytes)
- `20260327T183639Z-unknown.md` (876 bytes)
- `20260327T183816Z-unknown.md` (876 bytes)
- `20260327T183914Z-unknown.md` (876 bytes)
- `20260327T184158Z-unknown.md` (876 bytes)
- `20260327T184259Z-unknown.md` (876 bytes)
- `20260327T190338Z-unknown.md` (876 bytes)
- `20260327T193327Z-unknown.md` (876 bytes)
- `20260327T193407Z-unknown.md` (876 bytes)
- `20260327T200249Z-unknown.md` (876 bytes)
- `20260327T200306Z-unknown.md` (876 bytes)
- `20260327T200405Z-unknown.md` (876 bytes)
- `HONEY.md` (28923 bytes)
- `NORTH-STAR.md` (441 bytes)
- `REVIEW-INBOX.md` (37975 bytes)
- `faerie-brief.json` (2068 bytes)
- `faerie-recovery.json` (224 bytes)
- `handoff-20260327T191427Z.json` (5245 bytes)
- `handoff-20260327T192312Z.json` (5245 bytes)
- `handoff-20260327T192716Z.json` (5245 bytes)
- `handoff-20260327T192836Z.json` (5245 bytes)
- `handoff-20260327T193049Z.json` (5245 bytes)
- `handoff-20260327T193052Z.json` (5245 bytes)
- `handoff-20260327T194416Z.json` (5245 bytes)
- `handoff-checkpoint.json` (271 bytes)
- `handoff-snapshot.json` (716583 bytes)
- `last-session-handoff.md` (876 bytes)
- `pending-hash-snapshot.json` (265 bytes)
- `scratch-inbox-router.md` (1599 bytes)
- `session-context.json` (1076 bytes)
- `sprint-queue.json` (78402 bytes)
- `vault-sync-state.json` (140 bytes)

