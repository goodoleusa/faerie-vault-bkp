# Script Tier Rename Decision — 3 Untiered Scripts
task_id: script-tier-rename-untiered
investigation_label: mission-graph-realignment
agent: code-reviewer
compass_edge: S
date: 2026-04-29

## Targets
1. `scripts/eval-harness-repeatable.py`
2. `scripts/analyze-vault-structure.sh`
3. `scripts/discover-vault-paths.sh`

## Caller-Scan Protocol Executed (3 passes)

### Pass 1 — Forward grep (literal basename)
Search across .py/.sh/.json/.md/.jsonl in scripts/, hooks/, .claude/, docs/, forensics/.
Excluded: __pycache__, releases/, archive/, .git/, garbage/, node_modules/.

| target | file refs found | kind |
|---|---|---|
| eval-harness-repeatable.py | scripts/9x_membench_scorer.py:5 | doc-comment ("REPLACES: manual eval-harness-repeatable.py calculation") — NOT a callsite |
| eval-harness-repeatable.py | scripts/eval-harness-repeatable.py | self-reference (own header + usage docstring) |
| analyze-vault-structure.sh | docs/46-VAULT-RECONCILIATION-EXECUTIVE-SUMMARY.md:166,234 | prose path reference |
| analyze-vault-structure.sh | docs-archive/RECONCILIATION-INDEX.md:62,145,272 | archived prose |
| analyze-vault-structure.sh | forensics/.reconciliation-task-card.md:189 | prose ("Run scripts/analyze-vault-structure.sh for diagnostics") |
| discover-vault-paths.sh | docs/46-VAULT-RECONCILIATION-EXECUTIVE-SUMMARY.md:167 | prose path reference |
| discover-vault-paths.sh | docs-archive/RECONCILIATION-INDEX.md:67,146 | archived prose |

### Pass 2 — JSON inverse walk + script-path regex
Searched all .claude/**/*.json + forensics/**/*.json for script paths matching `(/[\w/\-.]+\.(?:py|sh))`.

- `.claude/settings.json` hooks block — NO references to any of the 3 targets (only to 0x_promote_to_forensics.py, 8x_*.py, 0x_b2_realtime_uploader.py).
- `.claude/skills/spawn/BODY-HONEY-TEMPLATING.md:63` — string `"eval-harness-v2-prep"` — this is a `task_id` reference, NOT a script-path reference.
- `forensics/ephemeral/2026-04-29/eval-harness-v2-prep/bundle.json` — task_id text only.
- `forensics/manifests/2026-04-27/...refactor-eval-harness-queue-to-mission...json` — task_id text only.
- Prior tier-audit artifact `forensics/artifacts/2026-04-27/18-20-00Z_artifact_audit-script-semantic-tiers_ai-engineer_001.md:113-115` — this audit ALREADY proposed the exact tier prefixes used below.
- Prior equilibrium-audit manifest `forensics/ephemeral/2026-04-29/script-equilibrium-audit/.../001.json:32-41` — flags all 3 as "needs rename" with the SAME proposed prefixes.

### Pass 3 — Indirect / subprocess shellout
Grepped `subprocess.(run|call|Popen|check_output)` and `os.system` and `sh -c` across scripts/ + hooks/ + .claude/ for any reference to the 3 basenames.

- One hit: `scripts/eval-harness-repeatable.py:66` — this is INTERNAL (eval-harness invokes its OWN runner subprocess). Not an external caller.
- ZERO external subprocess callers for any of the 3 scripts.
- ZERO `bash scripts/analyze-vault-structure.sh` or `bash scripts/discover-vault-paths.sh` invocations anywhere in the codebase.
- ZERO `python3 scripts/eval-harness-repeatable.py` invocations from .claude/ or hooks/.

## Blast-Radius Assessment

| target | class_A_real_callsite | class_B_pure_inverse_JSON | class_C_indirect_shellout | total_real_callers |
|---|---|---|---|---|
| eval-harness-repeatable.py | 0 | 0 | 0 | **0** |
| analyze-vault-structure.sh | 0 | 0 | 0 | **0** |
| discover-vault-paths.sh | 0 | 0 | 0 | **0** |

Total real callers across all three scripts: **0**.

All other matches are one of:
- Doc-comment text (eval-harness-repeatable.py inside `9x_membench_scorer.py` REPLACES line — does not break on rename, but should be updated for accuracy).
- Prose-path mentions in user-facing docs (`docs/46-VAULT-RECONCILIATION-EXECUTIVE-SUMMARY.md`, `docs-archive/RECONCILIATION-INDEX.md`, `forensics/.reconciliation-task-card.md`) — these will become stale links unless updated.
- Coincidental `task_id` strings (eval-harness-v2-prep, refactor-eval-harness-queue-to-mission) — UNRELATED to the script path, no dependency.

**Severity:** LOW. No executable callsites break. Doc references go stale (cosmetic).

## Proposed Renames (matches prior audit recommendations)

```
scripts/eval-harness-repeatable.py     →  scripts/3x_eval_harness_repeatable.py
scripts/analyze-vault-structure.sh     →  scripts/9x_analyze_vault_structure.sh
scripts/discover-vault-paths.sh        →  scripts/9x_discover_vault_paths.sh
```

Rationale (per scripts/CLAUDE.md tier map):
- `3x_` = routing / harness / eval orchestration (eval-harness drives an A/B benchmark; it is an experiment harness, not a one-shot utility) — tier matches the script's own self-flagged TIER header.
- `9x_` = utilities / measurement / diagnostics (both vault scripts emit diagnostic snapshots, no state change) — matches both scripts' self-flagged TIER headers.

Underscores replace hyphens to align with the existing 0x_/3x_/8x_/9x_ Python module-naming convention already used in scripts/ (e.g., `0x_promote_to_forensics.py`, `9x_membench_scorer.py`).

## Rename Commands (atomic, git-history-preserving)

Executed manually or via batch script. Use `git mv` (NOT `mv`) to keep history intact.

```bash
cd /mnt/d/0local/gitrepos/faerie2

# Rename atomically with history preservation
git mv scripts/eval-harness-repeatable.py  scripts/3x_eval_harness_repeatable.py
git mv scripts/analyze-vault-structure.sh  scripts/9x_analyze_vault_structure.sh
git mv scripts/discover-vault-paths.sh     scripts/9x_discover_vault_paths.sh
```

## Post-Rename Cleanup (cosmetic doc updates — non-blocking)

These references will go stale after rename. Fix in a follow-up doc-update task (NOT in the rename commit, to keep diff atomic):

1. `scripts/9x_membench_scorer.py:5` — doc-comment "REPLACES: manual eval-harness-repeatable.py calculation" → `3x_eval_harness_repeatable.py`
2. `docs/46-VAULT-RECONCILIATION-EXECUTIVE-SUMMARY.md:166,167,234` — table + diagnostic command paths
3. `docs-archive/RECONCILIATION-INDEX.md:62,67,145,146,272` — archived; lower priority but should still be patched
4. `forensics/.reconciliation-task-card.md:189` — diagnostic command path
5. Internal TIER headers in each script — drop "(candidate — needs rename to ...)" qualifier; mark TIER as final

## Constraint Compliance Check

- [x] Caller-graph investigation completed BEFORE proposing rename (3-pass protocol per ~/.claude rules).
- [x] All 3 passes ran and reported (Pass 1 forward, Pass 2 JSON inverse, Pass 3 subprocess shellout).
- [x] Class A/B/C breakdown reported (0/0/0 for all three targets).
- [x] No logic changes proposed — atomic rename only.
- [x] Git history preservation — uses `git mv`.
- [x] No new abstractions / new scripts introduced (FUNDAMENTAL GOVERNANCE RULE: equilibrium respected).
- [x] Tier prefix selection respects scripts/CLAUDE.md tier map AND the scripts' own self-flagged TIER candidates.
- [x] Hooks in .claude/settings.json verified clean — no path updates required.

## Mutation Classification

**Type:** neutral / cosmetic. Pure file-rename to align untiered scripts with the 0x..9x tier convention. No behavior change. No equilibrium impact (filenames are not in any hot loop). Safe to apply without baseline mutation measurement (rename is filesystem-only; produces no behavioral mutation to measure).

## Recommended Next Mission (S edge)

`task-apply-tier-renames-untiered` — execute the 3 `git mv` commands above in a single atomic commit, then a follow-up doc-cleanup task for the 5 cosmetic references identified above. Suggested agent: documentation-engineer (for doc updates) or python-pro (for the rename commit + post-rename test).
