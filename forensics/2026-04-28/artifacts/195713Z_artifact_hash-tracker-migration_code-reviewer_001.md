# hash_tracker Canonicalization & Migration Guide

**Task:** hash-tracker-canonicalization-audit-w2
**Date:** 2026-04-28
**Investigation:** hash-tracker-canonicalization-audit-w2
**Reviewer:** code-reviewer

## Decision

**CANONICAL:** `/mnt/d/0LOCAL/.claude/scripts/4x_hash_tracker.py` (30,966 bytes, mtime 2026-04-24)

Rationale:
- Tier-4x header present (`TIER: 4x_`, `LOAD: core`) — declares it as the system-of-record per faerie2 tier convention.
- Newest mtime among full-feature variants.
- Lives under global CLAUDE_HOME (`~/.claude/scripts/`), the architectural location prescribed by HONEY sys00014 and `vault_sign.py` resolution order.
- Self-contained: embeds `PGPKeyManager`; no external import.
- Backup-verified: byte-identical copy at `/mnt/d/0local/.claude-backup/scripts/4x_hash_tracker.py`.

## Variants Found (10 total)

| # | Path | Disposition |
|---|------|-------------|
| 1 | `/mnt/d/0LOCAL/.claude/scripts/4x_hash_tracker.py` | **CANONICAL** — keep |
| 2 | `/mnt/d/0local/.claude-backup/scripts/4x_hash_tracker.py` | Keep as backup (byte-identical) |
| 3 | `/mnt/d/0local/gitrepos/cybertemplate/scripts/hash_tracker.py` | Deprecate -> symlink/import |
| 4 | `/mnt/d/0local/gitrepos/data-analysis-engine/scripts/hash_tracker.py` | Audit then deprecate (1.6KB extra logic) |
| 5 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker.py` | Archive (origin) |
| 6 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker5.py` | Delete (duplicate of #5) |
| 7 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker-v2.py` | Delete (intermediate) |
| 8 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker1.py` | Delete (early dev) |
| 9 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker-t.py` | Delete (test) |
| 10 | `/mnt/d/0local/0-OSINTTOOLS/hashtracker/hash_tracker-lesslogs.py` | Delete (experiment) |

## Code Review Findings

### Crypto algorithm (uniform)
All 10 variants use **`hashlib.sha256()`** for file hashing. **No MD5, no SHA-1.** No deprecated crypto detected. SHA-256 remains canonical.

### HMAC + PGP
All full-feature variants (1–5) embed `PGPKeyManager` and produce HMAC-SHA256 + optional GPG-signed snapshots. Output format = JSON snapshot files written under `.hash_snapshots/`.

### Drift between canonical and project forks
- **CT fork (#3):** identical to canonical except missing the `TIER: 4x_` header block (10 lines). Otherwise byte-equivalent. Safe to consolidate.
- **DAE fork (#4):** +1,623 bytes vs canonical. Larger diff; needs targeted audit before symlinking. Likely contains DAE-specific path overrides or extra commands. **Do NOT auto-symlink** until DAE-specific behavior is upstreamed.
- **OSINT main (#5):** Differs from canonical primarily by emoji output (`❌`, `🔑`) which canonical replaced with ASCII (`ERROR`, `[KEY]`). No semantic difference.

### Output / Errors / Logging
- Output: JSON to `.hash_snapshots/`, stdout summary.
- Error handling: explicit (`print("ERROR ...")`), non-zero exit codes via `sys.exit`.
- Logging: structured (snapshot name, file count, hash chain head). Adequate.

## Call Site Analysis

**Active callers (current systems):**
1. `~/.claude/scripts/7x_emergency_handoff.py` — references `hash_tracker` for deferred snapshot queue (lines 278, 281, 284, 885, 892). Resolves to canonical via PATH/Home.
2. `data-analysis-engine/scripts/4a-forensic-sign.py` — `find_hash_tracker()` resolves in order: `scripts/hash_tracker.py` → `~/.claude/scripts/hash_tracker.py` → `scripts/2d_hash_tracker.py`. **Risk:** prefers local DAE fork before canonical.
3. `data-analysis-engine/ObsidianVault/scripts/2c_vault_sign.py` — same resolution order, prefers local `2d_hash_tracker.py`.
4. `00-c;laude-faerie-magick-bkp/claude-cli/scripts/vault_sign.py` — resolution order: `HASH_TRACKER_PATH` env → script-local → `~/.claude/scripts/hash_tracker.py` → `~/hashtracker/...` → `/mnt/c/Users/amand/hashtracker/...`. References to `/mnt/c/Users/amand/hashtracker/` are stale Windows paths.
5. `~/.claude/scripts/9a_rename_scripts.py` (line 103) — registers rename `hash_tracker.py -> 4c_hash_tracker.py`. **Inconsistent with current 4x_ tier prefix.** Update to `4x_hash_tracker.py`.

**Doc references (faerie-vault):** README.md and HONEY-global.md still cite `data-analysis-engine/scripts/hash_tracker.py` as the script path in sys00014. **Must be updated to canonical** (`~/.claude/scripts/4x_hash_tracker.py`).

**Class B (inverse) callers:** None detected — no JSON config references hash_tracker by path. **Class C (subprocess shell-out):** `vault_sign.py` and `4a-forensic-sign.py` both use `subprocess` to invoke hash_tracker; these are the migration-critical entry points.

### Blast Radius (3-pass scan)
- Pass 1 (forward grep): 60+ refs across docs, scripts, agent cards.
- Pass 2 (inverse JSON walk): 0 (no JSON path embeddings).
- Pass 3 (subprocess shell-out): 4 (vault_sign.py x2, 4a-forensic-sign.py, emergency_handoff queue).
- **Class B pure inverse: 0** (LOW risk for inverse-callers).
- **Active subprocess callers: 4** — these MUST be updated to either env var `HASH_TRACKER_PATH` or canonical absolute path.

## Version Lineage (inferred from mtime + size)

```
2026-01-13/14  OSINT origin (hash_tracker1.py, -t.py, -lesslogs.py)  [dev iterations]
       |
2026-01-16     OSINT hash_tracker.py + hash_tracker5.py (30,016 B)   [v1.0 stable, emoji-rich]
       |       |
       |       +--> copied to project repos
       |
2026-03-22     cybertemplate/scripts/hash_tracker.py (30,765 B)      [emoji-stripped, near-canonical]
2026-03-23     data-analysis-engine/scripts/hash_tracker.py (32,388 B) [DAE-extended]
       |
2026-04-24     ~/.claude/scripts/4x_hash_tracker.py (30,966 B)       [CANONICAL, Tier-4x header added]
2026-04-24     ~/.claude-backup/... (30,966 B)                       [backup snapshot]
```

Forks were **accidental** (copy-paste during 2026-03 cross-project consolidation), not intentional per-project specialization. DAE's 1.6KB delta is the only candidate for "intentional fork," and even there is likely a single config block that should be parameterized rather than forked.

## Migration Plan (proposed; non-breaking)

### Phase 1: Documentation alignment (no code changes, immediate)
- Update HONEY sys00014 `Script:` reference from `data-analysis-engine/scripts/hash_tracker.py` → `~/.claude/scripts/4x_hash_tracker.py`.
- Update faerie-vault `README.md` line 1023 to point to canonical.
- Update `9a_rename_scripts.py` line 103: rename target `4c_hash_tracker.py` → `4x_hash_tracker.py`.

### Phase 2: Caller hardening (low risk)
- Set `HASH_TRACKER_PATH=~/.claude/scripts/4x_hash_tracker.py` in shell rc (defines truth).
- `vault_sign.py` and `4a-forensic-sign.py` already honor this env var first — no code change required.
- Remove stale Windows path `/mnt/c/Users/amand/hashtracker/...` from resolution chains in `vault_sign.py` and team-builder.md (backup repos can stay frozen).

### Phase 3: Audit DAE delta (medium risk)
- `diff` canonical vs DAE; identify the +1,623 byte block.
- If DAE-specific extension is generic, upstream into canonical.
- Replace `data-analysis-engine/scripts/hash_tracker.py` with **import shim**:
  ```python
  # data-analysis-engine/scripts/hash_tracker.py (shim)
  import sys, runpy
  sys.argv[0] = __file__
  runpy.run_path("/mnt/d/0LOCAL/.claude/scripts/4x_hash_tracker.py", run_name="__main__")
  ```
  (Symlinks are unreliable on WSL/Windows mixed filesystems; runpy shim is portable.)

### Phase 4: CT consolidation (low risk; identical-modulo-header)
- Replace `cybertemplate/scripts/hash_tracker.py` with same runpy shim.

### Phase 5: OSINT archival
- Archive `0-OSINTTOOLS/hashtracker/` to `0-OSINTTOOLS/_legacy/hashtracker-2026-01/` for forensic record.
- Keep only `hash_tracker.py` (the v1.0 stable origin) for lineage; delete dev iterations (1, -t, -v2, -lesslogs, 5).

### Phase 6: Verification
- Run `python3 ~/.claude/scripts/4x_hash_tracker.py snapshot --name canonicalization-verify` from each project directory.
- Confirm output identical (modulo path metadata).
- COC entry per project.

## Risks

- **DO NOT** consolidate before auditing the DAE +1.6KB delta — it may contain DAE-specific evidence routing.
- Doc references in `00-c;laude-faerie-magick-bkp/` are intentionally archival; do NOT update those.
- HMAC keys: each variant uses an HMAC key resolution scheme. Confirm canonical resolves keys identically before flipping callers.

## Compass Edge Decision

**S (proceed)** — Lineage is clear, crypto is uniform (SHA-256), no incompatibility blocks. Canonical version identified; non-breaking migration plan documented. Single audit gate (DAE delta) is the only blocker for full consolidation, and it can run in W3 background.
