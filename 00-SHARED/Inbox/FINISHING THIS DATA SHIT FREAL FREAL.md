---
date_created: 2026-03-12 07:29 pm
date_modified: 2026-03-12 07:45 pm
type: guide
investigation_id: claude-coc-final-sprint
investigation_name: Claude Cybertemplate COC Final Sprint
confidence: High
status: active
parent:
  - "[[Claude Chain of Custody Final Sprint]]"
sibling: []
severity: High
urgency: High
tags:
  - claude
  - cybertemplate
title: FINISHING THIS DATA SHIT FREAL FREAL
doc_hash: sha256:f49b18400eabda27a1d795f17034705e6872ac2373d95620bf503b24daa9549d
hash_ts: 2026-03-29T16:10:47Z
hash_method: body-sha256-v1
---

# FINISHING THIS DATA SHIT FREAL FREAL

Current State (from exploration):

       Repository structure:

       - /mnt/d/0local/gitrepos/cybertemplate/ — main git repo
       - forensic/ folder with: forensic-script-log.md, run_manifest.json, methods_snapshot.json, repo_state.json, worktree-archives/
       - scripts/ with 56 scripts, scripts/audit_results/ with pipeline outputs
       - rawdata/ (massive, ~1TB+, NOT in git — correctly excluded)
       - evidence-meta/ — per-item JSON sidecars
       - evidence_manifest.json — 658 items, 1.6MB, IS in git
       - RUN-001 through RUN-005 manifests in scripts/audit_results/runs/
       - scripts/coc.py — COC module with stamp_input/stamp_output/log_coc functions
       - Pre/post-commit hooks auto-sign forensic/ folder via forensic_sign.py

       Skill/Agent locations (messy, need consolidation):

       - Canonical: /mnt/d/0LOCAL/.claude/ (= C:\Users\amand.claude junction) — 18 skills, 41 agents
       - Project-level: /mnt/d/0local/gitrepos/cybertemplate/.claude/ — 5 specialized agents, 1 command
       - Not yet installed: data-ingest-claude-plugin/ inside the repo — has 10 agents + 4 skills
       - Backup: /mnt/d/0LOCAL/.claude-backup/ — identical to canonical (just a safety copy)
       - Desktop app uploads: /mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/cybertemplate-investigation/1.0.0/ — orphaned subset (9 agents, 4 skills) from old desktop
       plugin format

       COC gaps identified:

       1. Rawdata manifest not integrated into standard pipeline (optional/manual)
       2. Large files (>100MB) git-ignored correctly but no external backup tracking in COC
       3. Worktree archives not hashed into forensic signing
       4. No agent session ID in pipeline log entries
       5. Naming convention not enforced automatically
       6. B2 bucket planned for analysis but no manifest tracking yet

       GitHub features available but underused:

       - Git tags (could mark pipeline run boundaries)
       - GitHub Releases (could attach manifest files as release assets)
       - GitHub Actions (already has forensic-and-health.yml and deploy-and-mirror.yml)
       - Git notes (could annotate commits with run IDs without changing history)

       Design Requirements:

       Phase A — "How we got here" forensic snapshot (one-time):

       - Single script or procedure that produces a comprehensive forensic/genesis_manifest.json documenting:
         - All rawdata files: name, size, SHA-256, date ingested, which RUN processed it
         - All output files in audit_results/: SHA-256, which RUN produced them, git commit at time of production
         - All scripts used: name, SHA-256 at time of use (from methods_snapshot)
         - Worktree history: which branches were used, when, what they did
         - Timeline of all RUN-001 through RUN-005 with their git commits
       - This snapshot gets committed to git, creating an immutable "this is where we stand" record

       Phase B — Refined COC system going forward:

       Core principle: GitHub commit SHA = your COC anchor. Don't re-hash what git already hashes.

       - For code/scripts: Just use git. A git commit IS proof of script version.
       - For rawdata (not in git): Rawdata manifest committed to git — lists each file's SHA-256, size, source, date received. Updated when new raw data arrives.
       - For large outputs (not in git): B2 manifest committed to git — lists each large file's SHA-256, B2 object key, upload timestamp, which RUN produced it.
       - For pipeline runs: Keep RUN-NNN system but simplify: each run = a git tag (run/RUN-006) so the run's code version is provable from git history alone.
       - GitHub Actions: Auto-generate rawdata manifest diff on push; auto-tag on pipeline completion.

       Phase C — Skill/agent consolidation:

       - Install data-ingest-claude-plugin/ properly (run install.sh)
       - Establish canonical rule: project-specific agents in cybertemplate/.claude/agents/, general agents in ~/.claude/agents/
       - Clean up orphaned desktop app uploads (archive, don't delete)
       - Document which skills/agents were used in which RUN (version history of tooling)

       Phase D — GitHub repo hygiene:

       - Ensure .gitignore correctly excludes rawdata/ and large outputs
       - Ensure manifests (rawdata_manifest.json, b2_manifest.json) ARE in git and small
       - Use GitHub Releases for milestone snapshots (attach genesis_manifest.json as asset)
       - GitHub Actions: update forensic manifest on push, validate hashes

       Please design:

       1. The exact schema for forensic/genesis_manifest.json
       2. The schema for rawdata_manifest.json (git-tracked, small, SHA-256 of each raw file)
       3. The schema for b2_manifest.json (tracks large files in B2 with hashes)
       4. The modified RUN system (add git tag per run)
       5. The agent/skill consolidation strategy
       6. GitHub Actions additions needed
       7. Step-by-step implementation order (what to do first, second, third)

       Keep the design practical and non-redundant with git's existing capabilities.
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/forensic/)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/scripts/ | head -60)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/coc.py)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/forensic/run_manifest.json)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/forensic_sign.py)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/forensic/methods_snapshot.json)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/run_manager.py)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/ 2>/dev/null | head -30)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/runs/)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/runs/index.json)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/.github/workflows/ 2>/dev/null)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/.github/workflows/forensic-and-health.yml)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/.github/workflows/deploy-and-mirror.yml)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/runs/RUN-001.json)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/forensic/worktree-archives/ 2>/dev/null)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/forensic/forensic-script-log.md)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/githooks/ 2>/dev/null)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/githooks/pre-commit)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/githooks/post-commit)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/.claude/ 2>/dev/null && ls /mnt/d/0local/gitrepos/cybertemplate/.claude/agents/ 2>/dev/null && ls
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/data-ingest-claude-plugin/ 2>/dev/null && ls /mnt/d/0local/gitrepos/cybertemplate/data-ingest-claude-plugin/agents/ 2>/dev/null
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/rawdata_manifest.py)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/hash_tracker.py · lines 1-60)
  ⎿  Bash(cat /mnt/d/0local/gitrepos/cybertemplate/.gitignore | head -60)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate log --oneline --all | head -20)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate tag --list | head -20)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate log --oneline --all | wc -l && git -C /mnt/d/0local/gitrepos/cybertemplate branch -a)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/runs/RUN-005.json)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate log --oneline | grep -E "(RUN-|run|forensic|coc|manifest|ingest)" | head -15)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate show 690acf2 --oneline --name-only 2>/dev/null | head -15 && echo "---" && git -C /mnt/d/0local/gitrepos/cybertemplate show
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/forensic/worktree-archives/2026-03-12_173836/ 2>/dev/null | head -20)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/forensic/worktree-archives/2026-03-12_173836/manifest.json)
  ⎿  Bash(ls /mnt/d/0local/gitrepos/cybertemplate/evidence-meta/ | head -10 && wc -l /mnt/d/0local/gitrepos/cybertemplate/evidence-meta/*.json 2>/dev/null | tail -3)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/ARCHITECTURE.md · lines 1-80)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate notes list 2>/dev/null | head -5)
  ⎿  Bash(ls /mnt/d/0LOCAL/.claude/agents/ 2>/dev/null | wc -l && ls /mnt/d/0LOCAL/.claude/skills/ 2>/dev/null)
  ⎿  Read(/mnt/d/0local/gitrepos/cybertemplate/data-ingest-claude-plugin/install.sh)
  ⎿  Bash(ls /mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/cybertemplate-investigation/1.0.0/ 2>/dev/null | head -20)
  ⎿  Bash(git -C /mnt/d/0local/gitrepos/cybertemplate log --format="%H %ai %s" | head -20)
  ⎿  Bash(ls /mnt/d/0LOCAL/.claude/plans/ 2>/dev/null || echo "dir missing")
  ⎿  Response:
       Good. Now I have everything needed to write the full implementation plan. Here it is:

       ---
       CyberTemplate — COC System Redesign: Implementation Plan

       What We Know From Exploration

       What already works well (keep it):
       - coc.py — stamp_input/stamp_output/log_coc pattern: solid, already in use
       - run_manager.py — RUN-NNN JSON manifests in scripts/audit_results/runs/: good schema, add git tag support
       - forensic_sign.py — HMAC hash snapshots of forensic/ before/after every commit via githooks
       - rawdata_manifest.py — already exists in scripts/, writes to forensic/rawdata_manifest.json, just not yet wired into the standard workflow
       - Pre/post-commit hooks in githooks/ — already running forensic_sign.py automatically
       - GitHub Actions forensic-and-health.yml — already runs health check and snapshot on every push
       - Worktree archive manifest.json already has SHA-256 per ZIP

       What's broken or missing:
       - RUN-004 is stuck as RUNNING in index.json — never closed (completed: null)
       - run_manager.py only records short commit SHAs (7 chars) — should be full 40-char
       - No git tags exist — tags are the critical missing link between runs and git history
       - rawdata_manifest.py exists but is not called from any standard workflow step
       - forensic/rawdata_manifest.json almost certainly does not exist yet (script is manual-only)
       - Worktree archive ZIPs in forensic/worktree-archives/ are gitignored — their SHA-256s from manifest.json are in git, but the ZIPs themselves need B2 backup tracking
       - RUN-001 through RUN-005 git commits are 7-char short SHAs — not full hashes
       - No b2_manifest.json exists to track what's in the B2 bucket
       - data-ingest-claude-plugin/ not installed — 8 agents and 4 skills sitting dormant
       - Desktop app orphan at /mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/ — not cleaned up
       - No GitHub Releases or tags for any run milestone
       - forensic-script-log.md has gaps (FSL-013 through FSL-018 are pending, FSL-019/020 marked IN PROGRESS but may be stale)

       ---
       Phase A — "Genesis Snapshot" (one-time, do first)

       Purpose

       Create an immutable, committed forensic/genesis_manifest.json that is the permanent "here is where we stand as of 2026-03-12" record. This is the COC bookmark for all
       prior work.

       Schema: forensic/genesis_manifest.json

       {
         "schema_version": "1.0",
         "manifest_type": "genesis",
         "generated_at_utc": "<ISO8601>",
         "generated_by": "scripts/generate_genesis.py",
         "git_state": {
           "commit": "<full 40-char SHA>",
           "commit_short": "<7-char>",
           "branch": "main",
           "tag": "genesis/2026-03-12",
           "repo_url": "https://github.com/<org>/cybertemplate"
         },
         "investigation_summary": {
           "total_evidence_items": 658,
           "evidence_manifest_sha256": "<sha256 of evidence_manifest.json at genesis>",
           "hypothesis_ids": ["H1", "H2", "H3", "H4", "H5"],
           "date_range": {
             "earliest_raw_data": "2025-03-01",
             "latest_pipeline_run": "2026-03-12"
           }
         },
         "pipeline_runs": [
           {
             "run_id": "RUN-001",
             "title": "Initial ingestion + clean + transform + curate",
             "git_commit_short": "690acf2",
             "git_commit_full": "<resolved from log>",
             "git_commit_date_utc": "2026-03-09T20:04:00Z",
             "status": "COMPLETE",
             "manifest_file": "scripts/audit_results/runs/RUN-001.json",
             "manifest_sha256": "<sha256 of RUN-001.json at genesis>",
             "git_tag": "run/RUN-001",
             "phases": ["CLEAN", "TRANSFORM", "CURATE"],
             "key_outputs": [
               {
                 "file": "scripts/audit_results/evidence_tiers/tier1_smoking_gun.json",
                 "sha256": "<sha256>",
                 "size_bytes": 0,
                 "in_git": true
               }
             ],
             "rawdata_inputs_count": 5,
             "rawdata_inputs_sha256_in_run_manifest": true
           }
         ],
         "scripts": {
           "snapshot_source": "forensic/methods_snapshot.json",
           "snapshot_sha256": "<sha256 of methods_snapshot.json>",
           "count": 30,
           "scripts": [
             {
               "script": "scripts/coc.py",
               "sha256_at_genesis": "<sha256>",
               "note": "Primary COC module — used by all pipeline phases"
             }
           ]
         },
         "rawdata": {
           "manifest_file": "forensic/rawdata_manifest.json",
           "manifest_sha256": "<sha256 of rawdata_manifest.json>",
           "status": "generated_at_genesis",
           "file_count": "<N>",
           "total_size_bytes": "<N>",
           "note": "rawdata/ is gitignored. This manifest is the COC record of rawdata state at genesis."
         },
         "worktree_archives": {
           "archive_batches": [
             {
               "batch_id": "2026-03-12_173836",
               "manifest_file": "forensic/worktree-archives/2026-03-12_173836/manifest.json",
               "manifest_sha256": "<sha256>",
               "archives": [
                 {
                   "name": "bold-dijkstra-20260312.zip",
                   "branch": "claude/bold-dijkstra",
                   "sha256": "425cbdf74f784afe848f5957d75ca97e5fb6acc6f6214a912265a3c527ca54db",
                   "size_bytes": 194666292,
                   "location": "gitignored — stored in B2 or local only",
                   "b2_key": "<if uploaded to B2>"
                 }
               ]
             }
           ]
         },
         "large_files_not_in_git": {
           "note": "Files excluded from git by .gitignore. SHA-256 on record at genesis.",
           "files": [
             {
               "path": "scripts/audit_results/cleaned_tabular_rows.json",
               "sha256": "<sha256>",
               "size_bytes": 0,
               "reason_excluded": "size >100MB",
               "exists_locally": true
             }
           ]
         },
         "agent_tooling": {
           "canonical_agents_dir": "/mnt/d/0LOCAL/.claude/agents/",
           "canonical_agent_count": 41,
           "project_agents_dir": ".claude/agents/",
           "project_agent_count": 5,
           "plugin_uninstalled": "data-ingest-claude-plugin/ — present in repo, not yet installed",
           "agents_used_in_runs": {
             "RUN-001": ["data-engineer", "evidence-curator"],
             "RUN-002": ["data-engineer"],
             "RUN-003": ["multi-agent-coordinator"],
             "RUN-004": ["hash_guardian.py", "evidence-curator"],
             "RUN-005": ["ingest_remaining.py"]
           }
         },
         "forensic_script_log": {
           "file": "forensic/forensic-script-log.md",
           "sha256": "<sha256>",
           "entry_count": 26,
           "last_entry": "FSL-026",
           "pending_entries": ["FSL-013", "FSL-014", "FSL-015", "FSL-016", "FSL-017"]
         },
         "coc_system_status": {
           "pre_commit_hook_installed": false,
           "pre_commit_hook_source": "githooks/pre-commit",
           "post_commit_hook_installed": false,
           "github_actions_forensic": ".github/workflows/forensic-and-health.yml",
           "rawdata_manifest_generated": false,
           "b2_manifest_exists": false,
           "git_tags_for_runs": false,
           "note": "Gaps documented here; Phase B addresses all of them going forward."
         }
       }

       Script: scripts/generate_genesis.py

       This single script produces the genesis manifest. Key implementation notes:

       - Uses git log --format="%H %ai" to resolve all short SHAs to full 40-char hashes and timestamps — look up 690acf2, 4e0ae23, 230e623, 72f8e39, 05640be from the index
       - Calls rawdata_manifest.py inline (or imports and calls main()) first, then reads the output
       - Hashes all currently-tracked output files that are small enough to be in git using coc.sha256_file()
       - For gitignored large outputs, uses os.path.exists() to check if they're locally present, then hashes if so
       - Reads forensic/worktree-archives/*/manifest.json to collect all batch records — does NOT re-hash the ZIPs (that would take too long; the existing SHA-256 in
       manifest.json is sufficient)
       - Reads data-ingest-claude-plugin/agents/ and ~/.claude/agents/ to count installed vs. available agents
       - Closes RUN-004 properly as RUNNING (adds a genesis_note field documenting that it was interrupted, rather than marking it COMPLETE falsely)
       - Writes to forensic/genesis_manifest.json
       - Prints instructions: "Now run: git add forensic/ && git commit -m 'genesis: COC snapshot before Phase B refinement'"

       The genesis script should NOT call forensic_sign.py — that happens automatically via the pre-commit hook when you commit.

       ---
       Phase B — Refined COC System (going forward)

       Core Principle: Git Does the Heavy Lifting

       ┌──────────────────────────┬──────────────────────────────────────┬─────────────────────────────────────────────────────┐
       │           What           │            COC mechanism             │                   Where recorded                    │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Script versions          │ git commit SHA                       │ Git history — already done                          │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Pipeline run boundaries  │ git tag run/RUN-NNN                  │ Git tags — add this                                 │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Rawdata file integrity   │ SHA-256 in rawdata_manifest.json     │ In git — already exists, just not regularly updated │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Large outputs not in git │ SHA-256 + B2 key in b2_manifest.json │ In git — add this                                   │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Agent/skill versions     │ git commit SHA (agents live in repo) │ Git history                                         │
       ├──────────────────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────┤
       │ Forensic/ integrity      │ HMAC snapshots via hash_tracker.py   │ In git via forensic/ files                          │
       └──────────────────────────┴──────────────────────────────────────┴─────────────────────────────────────────────────────┘

       Schema: rawdata_manifest.json (git-tracked, small)

       This file lives at forensic/rawdata_manifest.json (already the default output path of rawdata_manifest.py). Current schema is close but needs three additions:

       {
         "schema_version": "1.1",
         "timestamp_utc": "<ISO8601>",
         "generated_by": "scripts/rawdata_manifest.py",
         "source_dir": "rawdata/",
         "file_count": 1412,
         "total_size_bytes": 404400128,
         "note": "SHA-256 of every file in rawdata/ at time of generation. rawdata/ is gitignored; this manifest IS in git. Commit hash anchors when this state was recorded.",
         "files": [
           {
             "path": "March 2025 BAXET Russia/1-abcd1234/metadata.json",
             "size_bytes": 1024,
             "sha256": "<sha256>",
             "date_modified_utc": "<ISO8601 from mtime>",
             "first_seen_run": "RUN-001",
             "subdirectory_group": "March 2025 BAXET Russia"
           }
         ]
       }

       The two additions vs. current schema:
       1. date_modified_utc — file mtime, from f.stat().st_mtime. Enables temporal ordering without re-hashing.
       2. first_seen_run — populated by cross-referencing RUN manifests' inputs lists. For genesis, this is "RUN-001" for anything in the existing inputs. New files get the
       current run ID written at ingest time.

       This manifest should be regenerated and committed whenever new raw data arrives. The git commit timestamp then records exactly when that raw data state was frozen.

       Schema: b2_manifest.json (git-tracked, small)

       New file at forensic/b2_manifest.json. Tracks everything uploaded to B2 that is NOT in git:

       {
         "schema_version": "1.0",
         "bucket": "strongtogether",
         "endpoint_region": "ca-east-006",
         "note": "Tracks large files stored in B2 that are gitignored locally. SHA-256 here is proof of content; B2 object key + etag is proof of upload. Commit hash anchors when
        this record was written.",
         "objects": [
           {
             "b2_key": "screenrecordings/Packetware-main.mp4",
             "b2_etag": "<md5 etag from B2 upload response>",
             "local_path": "rawdata/screenrecordings-packetware-db/Packetware-main.mp4",
             "sha256": "<sha256>",
             "size_bytes": 273580032,
             "uploaded_at_utc": "<ISO8601>",
             "run_id": "RUN-001",
             "category": "video_evidence",
             "description": "Main Packetware screen recording — 261MB MP4"
           },
           {
             "b2_key": "worktree-archives/2026-03-12_173836/bold-dijkstra-20260312.zip",
             "b2_etag": "<etag>",
             "local_path": "forensic/worktree-archives/2026-03-12_173836/bold-dijkstra-20260312.zip",
             "sha256": "425cbdf74f784afe848f5957d75ca97e5fb6acc6f6214a912265a3c527ca54db",
             "size_bytes": 194666292,
             "uploaded_at_utc": "<ISO8601>",
             "run_id": "genesis",
             "category": "worktree_archive",
             "description": "Worktree archive for claude/bold-dijkstra branch"
           },
           {
             "b2_key": "audit_results/cleaned_tabular_rows.json",
             "b2_etag": "<etag>",
             "local_path": "scripts/audit_results/cleaned_tabular_rows.json",
             "sha256": "<sha256>",
             "size_bytes": 278000000,
             "uploaded_at_utc": "<ISO8601>",
             "run_id": "RUN-001",
             "category": "pipeline_output",
             "description": "Phase 3 CLEAN output — 265MB, gitignored"
           }
         ]
       }

       This file is append-only in practice. New objects are added, existing ones are never modified. No B2 API calls are needed to validate integrity — the SHA-256 in this
       manifest is the ground truth. The B2 etag (MD5 from their API) is a secondary cross-check.

       Modified RUN System (add git tags)

       The key addition: when run_manager.py new is called, also execute git tag run/RUN-NNN -m "Pipeline run RUN-NNN: <title>". When run_manager.py close is called, update the
       tag to an annotated tag pointing at the closing commit.

       The modified RUN manifest schema adds:
       {
         "run_id": "RUN-006",
         "git_tag": "run/RUN-006",
         "git_commit_open": "<full 40-char SHA at run start>",
         "git_commit_close": "<full 40-char SHA at run close>",
         "git_commit": "<7-char short — keep for compatibility>",
         "rawdata_manifest_sha256": "<sha256 of forensic/rawdata_manifest.json at run start>",
         "b2_manifest_sha256": "<sha256 of forensic/b2_manifest.json at run start>"
       }

       These two _sha256 fields tie the run to the exact rawdata and B2 state it operated on, without repeating the full manifest content.

       For historical runs (RUN-001 through RUN-005), create tags retroactively pointing at the commit associated with each run close:

       git tag run/RUN-001 690acf2 -m "RUN-001: Initial ingestion + clean + transform + curate"
       git tag run/RUN-002 4e0ae23 -m "RUN-002: Sprint extractions"
       git tag run/RUN-003 230e623 -m "RUN-003: Orchestration audit + tier rescue"
       git tag run/RUN-004 05640be -m "RUN-004: Hash guardian + evidence re-curation (note: run was not formally closed)"
       git tag run/RUN-005 5a0ff8b -m "RUN-005: INGEST_REMAINING"

       Note: RUN-004 in index.json shows completed: null and status RUNNING. Do not falsify history — tag it at the commit that contains the RUN-004 output files (05640be), and
       add a note in the tag message and in the genesis manifest explaining it was never closed.

       Full SHA resolution for tagging (from git log exploration):
       - 690acf2 → 690acf2... (verify with git rev-parse 690acf2)
       - 4e0ae23 → use git rev-parse 4e0ae23
       - 230e623 → use git rev-parse 230e623
       - 05640be → 05640beef8e8fc61b0d1c81cf3a9926213af0f95 (confirmed from log)
       - 5a0ff8b → 5a0ff8b7b45c7d38d920de85be53b36a69f7de13 (confirmed from log)

       ---
       Phase C — Skill/Agent Consolidation

       Canonical Rule (establish and document)

       ┌────────────────────────┬───────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
       │       Agent type       │             Location              │                                             Rule                                             │
       ├────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
       │ Investigation-specific │ cybertemplate/.claude/agents/     │ Agents whose prompts reference cybertemplate concepts (evidence tiers, H1-H5, rawdata paths) │
       ├────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
       │ General-purpose        │ /mnt/d/0LOCAL/.claude/agents/     │ Reusable across projects                                                                     │
       ├────────────────────────┼───────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
       │ Plugin bundle          │ data-ingest-claude-plugin/agents/ │ Source of truth for the plugin; install.sh copies to ~/.claude/agents/                       │
       └────────────────────────┴───────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

       Current project-level agents: admin-sync.md, data-scientist.md, evidence-analyst.md, ipfs-publisher.md, report-writer.md, reconstruct-db.md — these are all
       investigation-specific, correct location.

       Install data-ingest-claude-plugin

       The plugin's install.sh copies:
       - skills/data-ingest/, skills/stat/, skills/vision-ingest/, skills/workflows/ → ~/.claude/skills/
       - agents/*.md (8 agents) → ~/.claude/agents/

       Run from repo root in WSL: bash data-ingest-claude-plugin/install.sh

       Check for conflicts first: the skills data-ingest, stat, vision-ingest, workflows already exist in ~/.claude/skills/ from the canonical location. The plugin versions may
       be older or newer. Resolution strategy: after install, diff the two versions and keep the newer one. Because install.sh uses cp -r (not cp -n), it will overwrite — ensure
       the canonical versions are backed up first or run the diff before install.

       Desktop App Orphan Cleanup

       /mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/cybertemplate-investigation/1.0.0/ contains an old format (9 agents, 4 skills) from the Desktop Claude plugin
       system. These are NOT the same format as Claude Code agents — Desktop Claude uses a different agent invocation mechanism.

       Action: archive this directory as a .zip in forensic/ with a note in genesis_manifest.json that it's a historical artifact from the Desktop Claude plugin format. Do not
       delete — it proves tool evolution. Do not install — Desktop app format is incompatible with Claude Code.

       Agent Version Tracking per RUN

       Add a new optional field to RUN manifests:
       "tooling": {
         "agents_used": ["data-engineer", "evidence-curator"],
         "agent_versions": {
           "data-engineer": "<git commit SHA of data-engineer.md at run time>",
           "evidence-curator": "<git commit SHA of evidence-curator.md at run time>"
         },
         "model": "claude-opus-4-6",
         "claude_cli_version": "<from claude --version>"
       }

       For historical runs, agent commit SHAs can be approximated by looking at git log -- data-ingest-claude-plugin/agents/data-engineer.md to find when those files were last
       modified before the run date.

       ---
       Phase D — GitHub Actions Additions

       Current workflow coverage:

       - forensic-and-health.yml — runs forensic sign, health check, hash guardian stub
       - deploy-and-mirror.yml — deploys to VPS + IPFS

       Additions needed:

       Addition 1: Validate manifests on push

       Add a job to forensic-and-health.yml:
       validate-manifests:
         name: Validate COC manifests
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           - uses: actions/setup-python@v5
             with:
               python-version: '3.12'
           - name: Validate rawdata_manifest
             run: |
               if [ -f forensic/rawdata_manifest.json ]; then
                 python -c "
                 import json, sys
                 m = json.load(open('forensic/rawdata_manifest.json'))
                 assert 'files' in m, 'missing files key'
                 assert 'timestamp_utc' in m, 'missing timestamp'
                 assert 'schema_version' in m, 'missing schema_version'
                 print(f'rawdata_manifest OK: {m[\"file_count\"]} files')
                 "
               else
                 echo "WARNING: forensic/rawdata_manifest.json missing"
               fi
           - name: Validate genesis_manifest
             run: |
               if [ -f forensic/genesis_manifest.json ]; then
                 python -c "
                 import json
                 m = json.load(open('forensic/genesis_manifest.json'))
                 assert m['manifest_type'] == 'genesis'
                 assert m['git_state']['commit']
                 runs = m['pipeline_runs']
                 print(f'genesis_manifest OK: {len(runs)} runs documented')
                 "
               else
                 echo "INFO: genesis_manifest.json not yet created"
               fi
           - name: Validate b2_manifest
             run: |
               if [ -f forensic/b2_manifest.json ]; then
                 python -c "
                 import json
                 m = json.load(open('forensic/b2_manifest.json'))
                 assert 'objects' in m
                 print(f'b2_manifest OK: {len(m[\"objects\"])} objects tracked')
                 "
               fi
           - name: Validate run manifests
             run: |
               python -c "
               import json, sys
               from pathlib import Path
               idx = json.loads(Path('scripts/audit_results/runs/index.json').read_text())
               errors = []
               for r in idx['runs']:
                 mf = Path('scripts/audit_results/runs') / r['manifest']
                 if not mf.exists():
                   errors.append(f'{r[\"run_id\"]}: manifest file missing')
                   continue
                 m = json.loads(mf.read_text())
                 if 'git_commit' not in m:
                   errors.append(f'{r[\"run_id\"]}: missing git_commit')
               if errors:
                 for e in errors: print(f'ERROR: {e}')
                 sys.exit(1)
               print(f'Run manifests OK: {len(idx[\"runs\"])} runs')
               "

       Addition 2: Auto-tag on RUN close (optional, triggered by workflow_dispatch)

       New workflow tag-run.yml:
       name: Tag pipeline run
       on:
         workflow_dispatch:
           inputs:
             run_id:
               description: 'Run ID to tag (e.g. RUN-006)'
               required: true
             message:
               description: 'Tag message'
               required: false
       jobs:
         tag:
           runs-on: ubuntu-latest
           steps:
             - uses: actions/checkout@v4
               with:
                 fetch-depth: 0
                 token: ${{ secrets.GITHUB_TOKEN }}
             - name: Create run tag
               run: |
                 RUN_ID="${{ github.event.inputs.run_id }}"
                 MSG="${{ github.event.inputs.message }}"
                 if [ -z "$MSG" ]; then
                   MSG="Pipeline $RUN_ID completed"
                 fi
                 git config user.email "github-actions[bot]@users.noreply.github.com"
                 git config user.name "github-actions[bot]"
                 git tag "run/${RUN_ID}" -m "${MSG}"
                 git push origin "run/${RUN_ID}"

       What NOT to add: Do not add GitHub Actions to auto-generate rawdata_manifest.json — rawdata is not in CI. That manifest is generated locally and committed. The CI just
       validates the committed manifest is structurally valid.

       ---
       Implementation Order (Step by Step)

       Step 0 — Housekeeping (15 minutes)

       1. Close RUN-004 properly. In scripts/audit_results/runs/index.json, update RUN-004 status to "COMPLETE" and completed to the timestamp of commit 05640be
       (2026-03-10T20:00:16Z). Add "genesis_note": "Formally closed at genesis — run was interrupted; outputs are in git at 05640be". Do the same in RUN-004.json. Commit: "chore:
        close RUN-004 formally for genesis snapshot".
       2. Fix run_manager.py to capture full 40-char SHA. In get_git_commit(), change --short to nothing (or use --short=40). This affects future runs only; historical runs
       already have what they have.

       Step 1 — Generate rawdata_manifest.json (30-60 minutes, depending on rawdata size)

       Run locally: python scripts/rawdata_manifest.py

       This writes forensic/rawdata_manifest.json. The rawdata directory is ~1TB+ per the prompt description but the actual repo shows ~386MB across ~1,412 files — so hashing
       should complete in under a minute.

       After generation: git add forensic/rawdata_manifest.json && git commit -m "coc: generate rawdata_manifest.json at genesis milestone"

       Step 2 — Create b2_manifest.json (manual, 1-2 hours)

       No script for this yet — populate it manually for the genesis state. Check the B2 bucket contents (using b2 ls --recursive strongtogether or the B2 web console) and
       cross-reference with:
       - forensic-script-log.md FSL-008 (screen recordings uploaded)
       - The .gitignore entries for large files (verify which exist locally and were backed up)
       - The worktree archive ZIPs (check if they're in B2; if not, they should be)

       Note: B2 credentials were flagged as potentially exposed in forensic-script-log.md line 350. Verify the key is still valid and rotate if needed before running any B2
       operations. The genesis manifest should document the key rotation date.

       Create forensic/b2_manifest.json manually with what's known, then commit.

       Step 3 — Generate genesis_manifest.json (script, 30 minutes to write, 5 minutes to run)

       Write scripts/generate_genesis.py. The script:

       1. Reads scripts/audit_results/runs/index.json
       2. For each run, reads the run's .json file and resolves the short SHA to full SHA via git rev-parse <short>
       3. Reads forensic/rawdata_manifest.json (just generated in Step 1), records its SHA-256
       4. Reads forensic/b2_manifest.json (just created in Step 2), records its SHA-256
       5. Reads forensic/worktree-archives/*/manifest.json for each batch
       6. Reads forensic/methods_snapshot.json for the scripts list
       7. Checks ~/.claude/agents/ count (via os.listdir)
       8. Lists the gitignored large files from .gitignore and checks which exist locally with os.path.exists
       9. Hashes small in-git output files (tier JSONs, etc.) using coc.sha256_file()
       10. Writes forensic/genesis_manifest.json

       Commit: "genesis: complete COC snapshot — RUN-001 through RUN-005 documented"

       Step 4 — Create retroactive git tags (5 minutes)

       git tag run/RUN-001 690acf2 -m "RUN-001: Initial ingestion + clean + transform + curate [2026-03-09]"
       git tag run/RUN-002 4e0ae23 -m "RUN-002: Sprint extractions — Sprint1 + ThreatAssessment + Sprint2 [2026-03-10]"
       git tag run/RUN-003 230e623 -m "RUN-003: Orchestration audit + evidence tier rescue [2026-03-10]"
       git tag run/RUN-004 05640beef8e8fc61b0d1c81cf3a9926213af0f95 -m "RUN-004: Hash guardian + evidence re-curation — formally closed at genesis [2026-03-10]"
       git tag run/RUN-005 5a0ff8b7b45c7d38d920de85be53b36a69f7de13 -m "RUN-005: INGEST_REMAINING — 384 files [2026-03-10]"
       git tag genesis/2026-03-12 HEAD -m "Genesis: COC snapshot created — all prior runs documented"
       git push origin --tags

       The genesis/2026-03-12 tag on HEAD (which will include the genesis_manifest.json commit) creates the immutable anchor.

       Step 5 — Create a GitHub Release (5 minutes)

       gh release create genesis/2026-03-12 \
         --title "Genesis Snapshot — Investigation COC Baseline" \
         --notes "Complete chain-of-custody snapshot as of 2026-03-12. Documents RUN-001 through RUN-005, all scripts used, rawdata state, and B2 large file inventory. See
       forensic/genesis_manifest.json in this release." \
         forensic/genesis_manifest.json \
         forensic/rawdata_manifest.json

       This attaches the manifest files as release assets — permanent, versioned, publicly verifiable via the GitHub API.

       Step 6 — Install data-ingest-claude-plugin (10 minutes)

       From WSL (not Git Bash):
       cd /mnt/d/0local/gitrepos/cybertemplate
       diff -r ~/.claude/skills/data-ingest/ data-ingest-claude-plugin/skills/data-ingest/ 2>/dev/null || echo "No conflict"
       diff -r ~/.claude/skills/stat/ data-ingest-claude-plugin/skills/stat/ 2>/dev/null || echo "No conflict"
       bash data-ingest-claude-plugin/install.sh

       Then document in genesis_manifest.json's agent_tooling section that the plugin was installed at genesis. The git commit of the install will be the version proof.

       Step 7 — Archive orphaned Desktop app uploads (5 minutes)

       No deletion needed. Add a note to forensic/genesis_manifest.json under agent_tooling.desktop_app_orphan:
       {
         "path": "/mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/cybertemplate-investigation/1.0.0/",
         "format": "Desktop Claude plugin format — incompatible with Claude Code",
         "status": "archived_in_place",
         "action": "none_required — kept as historical record of tool evolution"
       }

       Step 8 — Add GitHub Actions validation (20 minutes)

       Add the validate-manifests job to forensic-and-health.yml and create tag-run.yml as designed above. Commit and push. Verify the Action runs and passes.

       Step 9 — Document the updated workflow for future runs (10 minutes)

       Update forensic/README.md (create if it doesn't exist) with:

       For each new pipeline run (RUN-006 onwards):
       1. python scripts/run_manager.py new "Run title" — creates manifest + git tag run/RUN-NNN automatically (after Step 0 fix)
       2. Do pipeline work
       3. Any new rawdata? → python scripts/rawdata_manifest.py && git add forensic/rawdata_manifest.json && git commit
       4. Any large files uploaded to B2? → Append entry to forensic/b2_manifest.json && git add forensic/b2_manifest.json && git commit
       5. python scripts/run_manager.py close RUN-NNN — records closing commit, updates tag
       6. git push origin --tags

       That's it. No additional hashing needed. Git history is the chain of custody for code. The manifests are the chain of custody for data outside git.

       ---
       What is Deliberately NOT Added

       - No re-hashing of files already hashed by git. If forensic_sign.py and git together cover a file, there is no third hash.
       - No database for COC. PostgreSQL is mentioned in ARCHITECTURE.md but does not exist yet. JSON files in git are sufficient and more portable.
       - No IPFS COC layer. IPFS pinning is for publication, not COC. The two concerns are separate.
       - No OpenTimestamps for the manifests at this stage. OTS is for publication artifacts. Add it to the genesis release after it's stable.
       - No deduplication of the forensic signing system. The hash_tracker.py HMAC snapshots serve a different purpose than rawdata_manifest.py — the former signs the forensic
       directory's state, the latter inventories rawdata. Keep both.

       ---
       Critical Files for Implementation

       - /mnt/d/0local/gitrepos/cybertemplate/scripts/run_manager.py — Core logic to modify: add full SHA capture, add git tag run/RUN-NNN on new and close, add
       rawdata_manifest_sha256/b2_manifest_sha256 fields to manifest schema
       - /mnt/d/0local/gitrepos/cybertemplate/scripts/rawdata_manifest.py — Pattern to follow for generate_genesis.py; extend its schema with date_modified_utc and first_seen_run
        fields
       - /mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/runs/index.json — First file to edit: close RUN-004 formally before anything else
       - /mnt/d/0local/gitrepos/cybertemplate/.github/workflows/forensic-and-health.yml — Add validate-manifests job; this is the enforcement hook that ensures manifests stay
       valid on every push
       - /mnt/d/0local/gitrepos/cybertemplate/forensic/genesis_manifest.json — Does not exist yet; the primary deliverable of Phase A, created by scripts/generate_genesis.py

       [ctx ~65K/200K | cache MISS ✗ | turn 1 | ~$0.19 this turn | saved $0.00 vs cold | session ~$0.19]