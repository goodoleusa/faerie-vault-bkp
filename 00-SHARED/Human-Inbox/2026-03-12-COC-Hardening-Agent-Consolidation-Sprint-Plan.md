---
date_created: 2026-03-12 07:37 pm
date_modified: 2026-03-12 07:38 pm
doc_hash: sha256:c81e33e83701d3d9c2d6b7edcc08b459098d04c97a285fbbd6de477e9f0753b5
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---
Plan to implement                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ CyberTemplate — COC Hardening + Agent Consolidation Sprint Plan                                                                                                                    │
│                                                                                                                                                                                    │
│ Created: 2026-03-12                                                                                                                                                                │
│ Model: Opus 4.6 (implementation sprint)                                                                                                                                            │
│ Status: APPROVED — execute with auto-accept                                                                                                                                        │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Meta: This Plan IS the Genesis                                                                                                                                                     │
│                                                                                                                                                                                    │
│ This planning session and its outputs are themselves COC records and should be logged as part of genesis:                                                                          │
│                                                                                                                                                                                    │
│ - This file: D:\0LOCAL\.claude\plans\glistening-tumbling-sparkle.md — the approved plan                                                                                            │
│ - The planning conversation: produced the agent exploration outputs that verified current state                                                                                    │
│ - What to log in genesis_manifest.json:                                                                                                                                            │
│ "planning_session": {                                                                                                                                                              │
│   "plan_file": ".claude/plans/glistening-tumbling-sparkle.md",                                                                                                                     │
│   "plan_sha256": "<sha256 of this file at genesis commit>",                                                                                                                        │
│   "exploration_outputs": ["repo structure", "agent inventory", "COC gap analysis"],                                                                                                │
│   "approved_at_utc": "2026-03-12T<time>Z",                                                                                                                                         │
│   "note": "This planning session preceded genesis implementation and is part of the audit trail"                                                                                   │
│ }                                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ Step A0 (before anything else): Copy this plan file into the repo: cp D:/0LOCAL/.claude/plans/glistening-tumbling-sparkle.md forensic/genesis-plan.md then commit it. That commit  │
│ becomes the immutable starting gun for all subsequent genesis work.                                                                                                                │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Context                                                                                                                                                                            │
│                                                                                                                                                                                    │
│ The investigation has completed RUN-001 through RUN-005. The data pipeline is built and tested, but chain of custody (COC) is partially documented and the agent/skill ecosystem   │
│ has drifted across Desktop Claude and Claude CLI workflows. Before analysis begins, we need:                                                                                       │
│                                                                                                                                                                                    │
│ 1. A permanent forensic "genesis" snapshot — how did all data get to this exact state?                                                                                             │
│ 2. A lightweight COC system going forward that uses GitHub as the backbone rather than duplicating it                                                                              │
│ 3. Agent consolidation: eliminate naming confusion, create a dedicated COC manager agent, fix the data-scientist/stat-agent naming conflict                                        │
│ 4. GitHub free-tier features activated to reduce manual work                                                                                                                       │
│                                                                                                                                                                                    │
│ Core principle: Git commits are already cryptographically linked. Don't re-hash what git hashes. Only track what git can't: rawdata files (not in git) and large pipeline outputs  │
│ (not in git).                                                                                                                                                                      │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ GitHub Free Tier — What's Available and What We'll Use                                                                                                                             │
│                                                                                                                                                                                    │
│ Quick orientation for a new GitHub user:                                                                                                                                           │
│                                                                                                                                                                                    │
│ ┌───────────────────┬─────────────────────────────────────────────────┬────────────────────┬────────────────────────────────────────────────────┐                                  │
│ │      Feature      │                   What it is                    │        Cost        │                  We'll use it for                  │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Git tags          │ Named pointers to commits (run/RUN-001)         │ Free               │ Mark each pipeline run in history                  │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Releases          │ Tags with a description + file attachments      │ Free               │ Attach genesis_manifest.json as permanent download │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Actions           │ YAML workflows that run on push/schedule/manual │ Free (public repo) │ Validate manifests, auto-tag runs                  │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Secrets           │ Encrypted key-value pairs for credentials       │ Free               │ B2 key ID + app key                                │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Variables         │ Non-secret config values                        │ Free               │ B2 bucket name, endpoint                           │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Branch protection │ Prevent force-push, require checks to pass      │ Free (basic)       │ Protect main from accidents                        │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Issue templates   │ Structured forms for new issues                 │ Free               │ Track data ingestion work                          │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ CODEOWNERS        │ Define who reviews which files                  │ Free               │ forensic/ requires human review                    │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Webhooks          │ POST to external URL on events                  │ Free               │ Not needed — Actions covers this                   │                                  │
│ ├───────────────────┼─────────────────────────────────────────────────┼────────────────────┼────────────────────────────────────────────────────┤                                  │
│ │ Packages/Copilot  │ Docker registry, AI pair programming            │ Paid               │ Skip                                               │                                  │
│ └───────────────────┴─────────────────────────────────────────────────┴────────────────────┴────────────────────────────────────────────────────┘                                  │
│                                                                                                                                                                                    │
│ Secrets vs Variables: Secrets (secrets.B2_KEY_ID) are encrypted and never shown in logs. Variables (vars.B2_BUCKET) are plain text config — use for non-sensitive values like      │
│ bucket name. Both are set in repo Settings → Secrets and variables → Actions.                                                                                                      │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Phase A — Genesis Snapshot (one-time, do first)                                                                                                                                    │
│                                                                                                                                                                                    │
│ Goal                                                                                                                                                                               │
│                                                                                                                                                                                    │
│ Create forensic/genesis_manifest.json — the permanent "here is where we stand as of 2026-03-12" COC record. Commit it, tag it, attach it to a GitHub Release. This is immutable    │
│ proof of all prior work.                                                                                                                                                           │
│                                                                                                                                                                                    │
│ Step A1 — Close RUN-004 properly (5 min)                                                                                                                                           │
│                                                                                                                                                                                    │
│ File: scripts/audit_results/runs/index.json and scripts/audit_results/runs/RUN-004.json                                                                                            │
│                                                                                                                                                                                    │
│ RUN-004 has status: "RUNNING" and completed: null. Don't falsify it as COMPLETE.                                                                                                   │
│ Add "genesis_note": "Run was interrupted; formally acknowledged at genesis — outputs present in git at 05640be".                                                                   │
│ Set status: "COMPLETE" (it did produce outputs) and completed: "2026-03-10T20:00:16Z".                                                                                             │
│                                                                                                                                                                                    │
│ Commit: "chore: formally close RUN-004 for genesis snapshot"                                                                                                                       │
│                                                                                                                                                                                    │
│ Step A2 — Generate rawdata_manifest.json (10 min)                                                                                                                                  │
│                                                                                                                                                                                    │
│ Run existing script (already written): python scripts/rawdata_manifest.py                                                                                                          │
│ This hashes every file in rawdata/ and writes to forensic/rawdata_manifest.json.                                                                                                   │
│                                                                                                                                                                                    │
│ Schema enhancement needed in rawdata_manifest.py:                                                                                                                                  │
│ - Add "date_modified_utc" field per file (from os.stat().st_mtime) — enables temporal ordering without re-hashing                                                                  │
│ - Add "first_seen_run" field per file — "genesis" for all existing files; new runs populate this at ingest time                                                                    │
│                                                                                                                                                                                    │
│ Commit: "coc: generate rawdata_manifest.json at genesis milestone"                                                                                                                 │
│                                                                                                                                                                                    │
│ Step A3 — Create b2_manifest.json manually (30-60 min)                                                                                                                             │
│                                                                                                                                                                                    │
│ New file: forensic/b2_manifest.json                                                                                                                                                │
│ Inventory the B2 bucket using b2 ls --recursive <bucket> or B2 web console.                                                                                                        │
│ Cross-reference with forensic-script-log.md (FSL-008 = screen recordings uploaded).                                                                                                │
│                                                                                                                                                                                    │
│ Schema:                                                                                                                                                                            │
│ {                                                                                                                                                                                  │
│   "schema_version": "1.0",                                                                                                                                                         │
│   "bucket": "strongtogether",                                                                                                                                                      │
│   "note": "Large files not in git. SHA-256 is ground truth; B2 etag is upload proof. Commit hash anchors when this was recorded.",                                                 │
│   "objects": [                                                                                                                                                                     │
│     {                                                                                                                                                                              │
│       "b2_key": "screenrecordings/Packetware-main.mp4",                                                                                                                            │
│       "b2_etag": "<md5 from B2 API>",                                                                                                                                              │
│       "local_path": "rawdata/screenrecordings-packetware-db/Packetware-main.mp4",                                                                                                  │
│       "sha256": "<sha256>",                                                                                                                                                        │
│       "size_bytes": 273580032,                                                                                                                                                     │
│       "uploaded_at_utc": "<ISO8601>",                                                                                                                                              │
│       "run_id": "RUN-001",                                                                                                                                                         │
│       "category": "video_evidence",                                                                                                                                                │
│       "description": "Main Packetware screen recording"                                                                                                                            │
│     }                                                                                                                                                                              │
│   ]                                                                                                                                                                                │
│ }                                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ Categories: video_evidence, pipeline_output, worktree_archive, rawdata_backup                                                                                                      │
│                                                                                                                                                                                    │
│ ⚠️ Check B2 credentials first — forensic-script-log.md notes a potential key exposure. Rotate the key in B2 console before running any B2 operations.                              │
│                                                                                                                                                                                    │
│ Commit: "coc: create b2_manifest.json at genesis milestone"                                                                                                                        │
│                                                                                                                                                                                    │
│ Step A4 — Write and run generate_genesis.py (45 min)                                                                                                                               │
│                                                                                                                                                                                    │
│ New script: scripts/generate_genesis.py                                                                                                                                            │
│                                                                                                                                                                                    │
│ What it does:                                                                                                                                                                      │
│ 1. Reads scripts/audit_results/runs/index.json — gets all runs                                                                                                                     │
│ 2. For each run, reads the run JSON and resolves short SHA to full 40-char via git rev-parse <short>                                                                               │
│ 3. Reads forensic/rawdata_manifest.json — records its SHA-256 (not contents)                                                                                                       │
│ 4. Reads forensic/b2_manifest.json — records its SHA-256                                                                                                                           │
│ 5. Reads forensic/worktree-archives/*/manifest.json — collects archive records                                                                                                     │
│ 6. Reads forensic/methods_snapshot.json — records script hashes                                                                                                                    │
│ 7. Checks gitignored large files — hashes if locally present                                                                                                                       │
│ 8. Counts agents in ~/.claude/agents/ and .claude/agents/                                                                                                                          │
│ 9. Documents plugin installation status (data-ingest-claude-plugin/ not yet installed)                                                                                             │
│ 10. Writes forensic/genesis_manifest.json                                                                                                                                          │
│                                                                                                                                                                                    │
│ Key genesis_manifest.json schema sections:                                                                                                                                         │
│ {                                                                                                                                                                                  │
│   "schema_version": "1.0",                                                                                                                                                         │
│   "manifest_type": "genesis",                                                                                                                                                      │
│   "generated_at_utc": "...",                                                                                                                                                       │
│   "git_state": { "commit": "<40-char>", "branch": "main", "tag": "genesis/2026-03-12" },                                                                                           │
│   "investigation_summary": { "total_evidence_items": 658, "evidence_manifest_sha256": "..." },                                                                                     │
│   "pipeline_runs": [ { "run_id": "RUN-001", "git_commit_full": "...", "git_tag": "run/RUN-001", ... } ],                                                                           │
│   "scripts": { "snapshot_source": "forensic/methods_snapshot.json", "snapshot_sha256": "..." },                                                                                    │
│   "rawdata": { "manifest_file": "forensic/rawdata_manifest.json", "manifest_sha256": "..." },                                                                                      │
│   "b2": { "manifest_file": "forensic/b2_manifest.json", "manifest_sha256": "..." },                                                                                                │
│   "worktree_archives": { "batches": [...] },                                                                                                                                       │
│   "large_files_not_in_git": [ { "path": "...", "sha256": "...", "size_bytes": 0 } ],                                                                                               │
│   "agent_tooling": { "plugin_status": "installed_at_genesis", "agents_used_by_run": {...} },                                                                                       │
│   "coc_gaps_at_genesis": { "resolved_in_phase_b": [...], "remaining": [...] }                                                                                                      │
│ }                                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ Commit: "genesis: complete COC snapshot — RUN-001 through RUN-005 documented"                                                                                                      │
│                                                                                                                                                                                    │
│ Step A5 — Create retroactive git tags (5 min)                                                                                                                                      │
│                                                                                                                                                                                    │
│ git tag run/RUN-001 690acf2 -m "RUN-001: Initial ingestion + clean + transform + curate [2026-03-09]"                                                                              │
│ git tag run/RUN-002 4e0ae23 -m "RUN-002: Sprint extractions — Sprint1 + ThreatAssessment + Sprint2 [2026-03-10]"                                                                   │
│ git tag run/RUN-003 230e623 -m "RUN-003: Orchestration audit + evidence tier rescue [2026-03-10]"                                                                                  │
│ git tag run/RUN-004 05640be -m "RUN-004: Hash guardian + evidence re-curation [not formally closed — see genesis note]"                                                            │
│ git tag run/RUN-005 5a0ff8b -m "RUN-005: INGEST_REMAINING — 384 files [2026-03-10]"                                                                                                │
│ git tag genesis/2026-03-12 HEAD -m "Genesis: COC baseline snapshot — all prior runs documented in forensic/genesis_manifest.json"                                                  │
│ git push origin --tags                                                                                                                                                             │
│                                                                                                                                                                                    │
│ Step A6 — Create GitHub Release (5 min)                                                                                                                                            │
│                                                                                                                                                                                    │
│ gh release create genesis/2026-03-12 \                                                                                                                                             │
│   --title "Genesis Snapshot — Investigation COC Baseline" \                                                                                                                        │
│   --notes "Chain-of-custody baseline as of 2026-03-12. Covers RUN-001 through RUN-005. See forensic/genesis_manifest.json for complete provenance record." \                       │
│   forensic/genesis_manifest.json \                                                                                                                                                 │
│   forensic/rawdata_manifest.json                                                                                                                                                   │
│                                                                                                                                                                                    │
│ This creates a permanent, publicly accessible download of the two manifests attached to the release tag.                                                                           │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Phase B — Refined COC System Going Forward                                                                                                                                         │
│                                                                                                                                                                                    │
│ Core Architecture                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ What                        │ COC mechanism           │ Where recorded                                                                                                             │
│ ────────────────────────────┼─────────────────────────┼──────────────────────────                                                                                                  │
│ Scripts/code versions       │ git commit SHA          │ Git history (already done)                                                                                                 │
│ Pipeline run boundaries     │ git tag run/RUN-NNN     │ Git tags (adding this)                                                                                                     │
│ Rawdata file integrity      │ SHA-256 in rawdata_manifest.json │ In git                                                                                                            │
│ Large outputs not in git    │ SHA-256 + B2 key in b2_manifest.json │ In git                                                                                                        │
│ Agent/skill versions        │ git commit SHA          │ Git history (agents are files in repo)                                                                                     │
│ forensic/ integrity         │ HMAC snapshot via hooks │ In git via .hash_snapshots/                                                                                                │
│                                                                                                                                                                                    │
│ What is NOT added: No database required. No IPFS for COC. No re-hashing what git already hashes.                                                                                   │
│                                                                                                                                                                                    │
│ Step B1 — Modify run_manager.py (20 min)                                                                                                                                           │
│                                                                                                                                                                                    │
│ File: scripts/run_manager.py                                                                                                                                                       │
│                                                                                                                                                                                    │
│ Changes:                                                                                                                                                                           │
│ 1. get_git_commit() → return full 40-char SHA (remove --short flag)                                                                                                                │
│ 2. new command → after writing manifest, run git tag run/{run_id} HEAD -m "Pipeline {run_id}: {title}"                                                                             │
│ 3. close command → update tag to closing commit: git tag -f run/{run_id} HEAD -m "...closed"                                                                                       │
│ 4. Add rawdata_manifest_sha256 and b2_manifest_sha256 fields to run manifest schema (hash the files at run open time)                                                              │
│                                                                                                                                                                                    │
│ Step B2 — Extend rawdata_manifest.py schema (10 min)                                                                                                                               │
│                                                                                                                                                                                    │
│ File: scripts/rawdata_manifest.py                                                                                                                                                  │
│                                                                                                                                                                                    │
│ Add per-file fields:                                                                                                                                                               │
│ - date_modified_utc (from os.stat(f).st_mtime)                                                                                                                                     │
│ - first_seen_run (default "genesis" for existing; new runs pass their run_id)                                                                                                      │
│ - subdirectory_group (first path component under rawdata/)                                                                                                                         │
│                                                                                                                                                                                    │
│ Step B3 — Document the new workflow (10 min)                                                                                                                                       │
│                                                                                                                                                                                    │
│ Update forensic/README.md with the complete step-by-step for human collaborators (see Phase C for COC agent — this README becomes the agent's reference doc).                      │
│                                                                                                                                                                                    │
│ For each future pipeline run (RUN-006+):                                                                                                                                           │
│ 1. python scripts/run_manager.py new "Run title"                                                                                                                                   │
│    → Creates RUN-NNN.json + git tag run/RUN-NNN automatically                                                                                                                      │
│                                                                                                                                                                                    │
│ 2. Do pipeline work (scripts log to pipeline_log.json via coc.py automatically)                                                                                                    │
│                                                                                                                                                                                    │
│ 3. New raw data arrived?                                                                                                                                                           │
│    → python scripts/rawdata_manifest.py                                                                                                                                            │
│    → git add forensic/rawdata_manifest.json && git commit -m "coc: rawdata manifest update for RUN-NNN"                                                                            │
│                                                                                                                                                                                    │
│ 4. Large files uploaded to B2?                                                                                                                                                     │
│    → Append entry to forensic/b2_manifest.json                                                                                                                                     │
│    → git add forensic/b2_manifest.json && git commit                                                                                                                               │
│                                                                                                                                                                                    │
│ 5. python scripts/run_manager.py close RUN-NNN                                                                                                                                     │
│    → Updates tag to closing commit                                                                                                                                                 │
│                                                                                                                                                                                    │
│ 6. git push origin --tags                                                                                                                                                          │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Phase C — Agent Consolidation                                                                                                                                                      │
│                                                                                                                                                                                    │
│ C1 — Fix data-scientist / statistical-analysis-subagent conflict                                                                                                                   │
│                                                                                                                                                                                    │
│ Problem: ~/.claude/agents/statistical-analysis-subagent.md (11.2KB) calls itself "data scientist" but ~/.claude/agents/data-scientist.md already exists as a separate agent. The   │
│ project-level .claude/agents/data-scientist.md has investigation-specific framing.                                                                                                 │
│                                                                                                                                                                                    │
│ Resolution:                                                                                                                                                                        │
│                                                                                                                                                                                    │
│ Update ~/.claude/agents/data-scientist.md (canonical) to be the full stat agent:                                                                                                   │
│ - Role: experimental design lead + statistical analyst                                                                                                                             │
│ - Responsibilities: hypothesis framing, test selection (z-scores, Bayesian, chi-square), anti-p-hacking protocol, significance interpretation                                      │
│ - Absorbs the anti-p-hacking content from statistical-analysis-subagent.md                                                                                                         │
│ - Model: claude-opus-4-6 (complex reasoning required)                                                                                                                              │
│ - Trigger: when user runs /stat or asks for significance testing, correlation, anomaly detection                                                                                   │
│                                                                                                                                                                                    │
│ Rename/retire statistical-analysis-subagent.md:                                                                                                                                    │
│ - Replace content with a single redirect: This agent has been merged into data-scientist.md. Use that instead.                                                                     │
│ - Or delete if Claude Code handles missing agents gracefully                                                                                                                       │
│                                                                                                                                                                                    │
│ Update cybertemplate/.claude/agents/data-scientist.md (project-level) to inherit from canonical but add:                                                                           │
│ - Investigation-specific context (H1-H5 hypotheses, Packetware datasets, known entity IPs)                                                                                         │
│ - Trigger: cross-dataset correlation, nation-state pattern detection                                                                                                               │
│ - Uses Opus for adaptive thinking on complex patterns                                                                                                                              │
│                                                                                                                                                                                    │
│ C2 — Create coc-manager agent                                                                                                                                                      │
│                                                                                                                                                                                    │
│ New file: cybertemplate/.claude/agents/coc-manager.md                                                                                                                              │
│                                                                                                                                                                                    │
│ This is an investigation-specific agent (not general-purpose, stays in project .claude/).                                                                                          │
│                                                                                                                                                                                    │
│ Role: Chain of Custody manager — the human collaborator's guide to data provenance.                                                                                                │
│                                                                                                                                                                                    │
│ What it does:                                                                                                                                                                      │
│ - Explains to any collaborator: "Here's how data X got into the investigation"                                                                                                     │
│ - Runs/validates manifest generation on request                                                                                                                                    │
│ - Guides humans through hashing steps when new data arrives                                                                                                                        │
│ - Answers "what script produced this output?" by reading pipeline_log.json                                                                                                         │
│ - Knows all manifest file locations and schemas                                                                                                                                    │
│ - Directs collaborators to forensic/README.md for step-by-step procedures                                                                                                          │
│ - Can generate a human-readable COC summary for any evidence item (from its _run metadata back through the chain)                                                                  │
│                                                                                                                                                                                    │
│ Model: claude-sonnet-4-6 (balanced, document-heavy work)                                                                                                                           │
│                                                                                                                                                                                    │
│ Tools: Read, Bash (for hashing/git queries), Grep                                                                                                                                  │
│                                                                                                                                                                                    │
│ Key content in agent prompt:                                                                                                                                                       │
│ - Complete map of all manifest files (rawdata_manifest, b2_manifest, genesis_manifest, run manifests, pipeline_log)                                                                │
│ - The COC query procedure: "Given file X → find its RUN → find git commit → find script SHA → find rawdata SHA"                                                                    │
│ - Human-readable hashing instructions (when to run what manually)                                                                                                                  │
│ - Instructions for collaborators who aren't developers (no assumed git knowledge)                                                                                                  │
│                                                                                                                                                                                    │
│ C3 — Install data-ingest-claude-plugin                                                                                                                                             │
│                                                                                                                                                                                    │
│ Run from WSL (not Git Bash):                                                                                                                                                       │
│ cd /mnt/d/0local/gitrepos/cybertemplate                                                                                                                                            │
│                                                                                                                                                                                    │
│ # Check for conflicts before overwriting                                                                                                                                           │
│ diff -r ~/.claude/skills/data-ingest/ data-ingest-claude-plugin/skills/data-ingest/                                                                                                │
│ diff -r ~/.claude/skills/vision-ingest/ data-ingest-claude-plugin/skills/vision-ingest/                                                                                            │
│                                                                                                                                                                                    │
│ # Install                                                                                                                                                                          │
│ bash data-ingest-claude-plugin/install.sh                                                                                                                                          │
│                                                                                                                                                                                    │
│ If canonical skills are newer than plugin versions → keep canonical (don't overwrite).                                                                                             │
│                                                                                                                                                                                    │
│ Document installed version in genesis_manifest.json agent_tooling section.                                                                                                         │
│                                                                                                                                                                                    │
│ C4 — Canonical Rule + CLI vs Desktop Labeling                                                                                                                                      │
│                                                                                                                                                                                    │
│ This project is a template — others may use Desktop Claude while the primary developer uses Claude CLI. Label clearly everywhere.                                                  │
│                                                                                                                                                                                    │
│ Claude CLI vs Desktop Claude — key differences:                                                                                                                                    │
│                                                                                                                                                                                    │
│ ┌────────────────────────────┬───────────────────────────────────────────────┬─────────────────────────────────────────────────────┐                                               │
│ │         Capability         │           Claude CLI (claude code)            │             Desktop Claude (claude.ai)              │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ Agents (.md files)         │ ✅ Full support — agents in ~/.claude/agents/ │ ⚠️ Plugin format only — different install mechanism │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ Skills (/skillname)        │ ✅ Full support — skills in ~/.claude/skills/ │ ❌ Not supported                                    │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ Subagents (Agent tool)     │ ✅ Can spawn subagents                        │ ❌ No Agent tool                                    │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ MCP servers                │ ✅ Full support                               │ ✅ Full support                                     │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ Hooks                      │ ✅ Full support                               │ ❌ Not supported                                    │                                               │
│ ├────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────┤                                               │
│ │ data-ingest-claude-plugin/ │ ✅ Install via install.sh                     │ ✅ Install via plugin system                        │                                               │
│ └────────────────────────────┴───────────────────────────────────────────────┴─────────────────────────────────────────────────────┘                                               │
│                                                                                                                                                                                    │
│ Add to cybertemplate/CLAUDE.md:                                                                                                                                                    │
│ ## Agent & Skill Locations                                                                                                                                                         │
│                                                                                                                                                                                    │
│ ### Claude CLI (primary — this is what the project maintainer uses)                                                                                                                │
│ | Type | Location | Install command |                                                                                                                                              │
│ |---|---|---|                                                                                                                                                                      │
│ | Project agents | `.claude/agents/` (this repo, git-tracked) | Automatic — in repo |                                                                                              │
│ | General agents | `~/.claude/agents/` | Manual or via plugin install.sh |                                                                                                         │
│ | Skills | `~/.claude/skills/` | Manual or via plugin install.sh |                                                                                                                 │
│ | Plugin source | `data-ingest-claude-plugin/` | `bash data-ingest-claude-plugin/install.sh` (from WSL) |                                                                          │
│                                                                                                                                                                                    │
│ ### Desktop Claude (template users who prefer the GUI)                                                                                                                             │
│ | Type | Location | Install |                                                                                                                                                      │
│ |---|---|---|                                                                                                                                                                      │
│ | Plugin | `data-ingest-claude-plugin/` | Claude Desktop → Settings → Plugins → Install from folder |                                                                              │
│ | Agents | Packaged in plugin | Automatic when plugin installed |                                                                                                                  │
│ | Skills | N/A — not supported in Desktop Claude | — |                                                                                                                             │
│                                                                                                                                                                                    │
│ ### Desktop App Orphan (historical — do not use)                                                                                                                                   │
│ Path: `/mnt/d/0LOCAL/.claude-backup/local-desktop-app-uploads/cybertemplate-investigation/1.0.0/`                                                                                  │
│ This is an old Desktop Claude plugin format artifact. Incompatible with Claude Code CLI.                                                                                           │
│ Kept as historical record of tool evolution. Do not install. Do not delete.                                                                                                        │
│                                                                                                                                                                                    │
│ Also add labels to data-ingest-claude-plugin/README.md header:                                                                                                                     │
│ # Data Ingest Claude Plugin                                                                                                                                                        │
│ > **Claude CLI users:** Run `bash install.sh` from WSL                                                                                                                             │
│ > **Desktop Claude users:** Settings → Plugins → Install from folder → select this directory                                                                                       │
│                                                                                                                                                                                    │
│ And add to example-dot-claude/README.md:                                                                                                                                           │
│ ## Platform Compatibility                                                                                                                                                          │
│ - All agents (`.md` files): Claude CLI only                                                                                                                                        │
│ - All skills (`/skillname`): Claude CLI only                                                                                                                                       │
│ - Plugin in `data-ingestion-pipeline-plugin/`: Both Claude CLI and Desktop Claude                                                                                                  │
│ - MCP servers: Both Claude CLI and Desktop Claude                                                                                                                                  │
│                                                                                                                                                                                    │
│ C5 — Agent version tracking per run                                                                                                                                                │
│                                                                                                                                                                                    │
│ Add optional tooling field to run manifests (populated by run_manager.py at close time):                                                                                           │
│ "tooling": {                                                                                                                                                                       │
│   "agents_used": ["coc-manager", "data-scientist"],                                                                                                                                │
│   "claude_cli_version": "<from claude --version>",                                                                                                                                 │
│   "model": "claude-opus-4-6"                                                                                                                                                       │
│ }                                                                                                                                                                                  │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Phase D — GitHub Free-Tier Features Setup                                                                                                                                          │
│                                                                                                                                                                                    │
│ D1 — Repository Secrets and Variables (5 min in GitHub Settings)                                                                                                                   │
│                                                                                                                                                                                    │
│ Navigate to: Repo → Settings → Secrets and variables → Actions                                                                                                                     │
│                                                                                                                                                                                    │
│ Secrets (encrypted — for credentials):                                                                                                                                             │
│                                                                                                                                                                                    │
│ ┌─────────────┬───────────────────────┬────────────────────────────┐                                                                                                               │
│ │ Secret name │         Value         │          Used in           │                                                                                                               │
│ ├─────────────┼───────────────────────┼────────────────────────────┤                                                                                                               │
│ │ B2_KEY_ID   │ B2 application key ID │ future B2 upload workflows │                                                                                                               │
│ ├─────────────┼───────────────────────┼────────────────────────────┤                                                                                                               │
│ │ B2_APP_KEY  │ B2 application key    │ future B2 upload workflows │                                                                                                               │
│ └─────────────┴───────────────────────┴────────────────────────────┘                                                                                                               │
│                                                                                                                                                                                    │
│ Variables (plain text — for config):                                                                                                                                               │
│                                                                                                                                                                                    │
│ ┌───────────────┬────────────────────────────────┬─────────────────┐                                                                                                               │
│ │ Variable name │             Value              │     Used in     │                                                                                                               │
│ ├───────────────┼────────────────────────────────┼─────────────────┤                                                                                                               │
│ │ B2_BUCKET     │ strongtogether                 │ workflow config │                                                                                                               │
│ ├───────────────┼────────────────────────────────┼─────────────────┤                                                                                                               │
│ │ B2_ENDPOINT   │ s3.us-west-002.backblazeb2.com │ workflow config │                                                                                                               │
│ └───────────────┴────────────────────────────────┴─────────────────┘                                                                                                               │
│                                                                                                                                                                                    │
│ These are then referenced in workflow YAML as ${{ secrets.B2_KEY_ID }} and ${{ vars.B2_BUCKET }}.                                                                                  │
│                                                                                                                                                                                    │
│ D2 — Branch Protection (5 min)                                                                                                                                                     │
│                                                                                                                                                                                    │
│ Navigate to: Repo → Settings → Branches → Add branch protection rule → main                                                                                                        │
│                                                                                                                                                                                    │
│ Free-tier settings to enable:                                                                                                                                                      │
│ - ✅ Require status checks to pass before merging (select validate-manifests once workflow exists)                                                                                 │
│ - ✅ Do not allow bypassing the above settings                                                                                                                                     │
│ - ✅ Restrict force pushes (protect COC history from accidental destruction)                                                                                                       │
│                                                                                                                                                                                    │
│ This means if a manifest file becomes invalid JSON, the CI fails and the commit is blocked.                                                                                        │
│                                                                                                                                                                                    │
│ D3 — GitHub Actions: Manifest Validation Workflow                                                                                                                                  │
│                                                                                                                                                                                    │
│ Modify: .github/workflows/forensic-and-health.yml                                                                                                                                  │
│                                                                                                                                                                                    │
│ Add job validate-manifests:                                                                                                                                                        │
│ validate-manifests:                                                                                                                                                                │
│   name: Validate COC manifests                                                                                                                                                     │
│   runs-on: ubuntu-latest                                                                                                                                                           │
│   steps:                                                                                                                                                                           │
│     - uses: actions/checkout@v4                                                                                                                                                    │
│     - uses: actions/setup-python@v5                                                                                                                                                │
│       with: { python-version: '3.12' }                                                                                                                                             │
│                                                                                                                                                                                    │
│     - name: Validate rawdata_manifest                                                                                                                                              │
│       run: |                                                                                                                                                                       │
│         python -c "                                                                                                                                                                │
│         import json, sys                                                                                                                                                           │
│         f = 'forensic/rawdata_manifest.json'                                                                                                                                       │
│         import os;                                                                                                                                                                 │
│         if not os.path.exists(f): print('WARNING: rawdata_manifest missing'); sys.exit(0)                                                                                          │
│         m = json.load(open(f))                                                                                                                                                     │
│         assert 'files' in m and 'timestamp_utc' in m and 'schema_version' in m                                                                                                     │
│         print(f'rawdata_manifest OK: {m[\"file_count\"]} files, {m[\"total_size_bytes\"]:,} bytes')                                                                                │
│         "                                                                                                                                                                          │
│                                                                                                                                                                                    │
│     - name: Validate genesis_manifest                                                                                                                                              │
│       run: |                                                                                                                                                                       │
│         python -c "                                                                                                                                                                │
│         import json, os                                                                                                                                                            │
│         f = 'forensic/genesis_manifest.json'                                                                                                                                       │
│         if not os.path.exists(f): print('INFO: genesis_manifest not yet created'); exit()                                                                                          │
│         m = json.load(open(f))                                                                                                                                                     │
│         assert m['manifest_type'] == 'genesis'                                                                                                                                     │
│         assert m['git_state']['commit']                                                                                                                                            │
│         print(f'genesis_manifest OK: {len(m[\"pipeline_runs\"])} runs documented')                                                                                                 │
│         "                                                                                                                                                                          │
│                                                                                                                                                                                    │
│     - name: Validate b2_manifest                                                                                                                                                   │
│       run: |                                                                                                                                                                       │
│         python -c "                                                                                                                                                                │
│         import json, os                                                                                                                                                            │
│         f = 'forensic/b2_manifest.json'                                                                                                                                            │
│         if not os.path.exists(f): print('INFO: b2_manifest not yet created'); exit()                                                                                               │
│         m = json.load(open(f))                                                                                                                                                     │
│         assert 'objects' in m and 'schema_version' in m                                                                                                                            │
│         print(f'b2_manifest OK: {len(m[\"objects\"])} objects tracked')                                                                                                            │
│         "                                                                                                                                                                          │
│                                                                                                                                                                                    │
│     - name: Validate run manifests                                                                                                                                                 │
│       run: |                                                                                                                                                                       │
│         python -c "                                                                                                                                                                │
│         import json, sys                                                                                                                                                           │
│         from pathlib import Path                                                                                                                                                   │
│         idx = json.loads(Path('scripts/audit_results/runs/index.json').read_text())                                                                                                │
│         errors = []                                                                                                                                                                │
│         for r in idx['runs']:                                                                                                                                                      │
│           mf = Path('scripts/audit_results/runs') / r['manifest']                                                                                                                  │
│           if not mf.exists():                                                                                                                                                      │
│             errors.append(f'{r[\"run_id\"]}: manifest file missing')                                                                                                               │
│             continue                                                                                                                                                               │
│           m = json.loads(mf.read_text())                                                                                                                                           │
│           if 'git_commit' not in m: errors.append(f'{r[\"run_id\"]}: missing git_commit')                                                                                          │
│         if errors:                                                                                                                                                                 │
│           [print(f'ERROR: {e}') for e in errors]; sys.exit(1)                                                                                                                      │
│         print(f'Run manifests OK: {len(idx[\"runs\"])} runs, next: {idx[\"next_run_id\"]}')                                                                                        │
│         "                                                                                                                                                                          │
│                                                                                                                                                                                    │
│ D4 — GitHub Actions: Manual Run Tagging Workflow                                                                                                                                   │
│                                                                                                                                                                                    │
│ New file: .github/workflows/tag-run.yml                                                                                                                                            │
│                                                                                                                                                                                    │
│ name: Tag pipeline run                                                                                                                                                             │
│ on:                                                                                                                                                                                │
│   workflow_dispatch:                                                                                                                                                               │
│     inputs:                                                                                                                                                                        │
│       run_id:                                                                                                                                                                      │
│         description: 'Run ID (e.g. RUN-006)'                                                                                                                                       │
│         required: true                                                                                                                                                             │
│       message:                                                                                                                                                                     │
│         description: 'Optional tag message'                                                                                                                                        │
│         required: false                                                                                                                                                            │
│ jobs:                                                                                                                                                                              │
│   tag:                                                                                                                                                                             │
│     runs-on: ubuntu-latest                                                                                                                                                         │
│     permissions:                                                                                                                                                                   │
│       contents: write                                                                                                                                                              │
│     steps:                                                                                                                                                                         │
│       - uses: actions/checkout@v4                                                                                                                                                  │
│         with: { fetch-depth: 0 }                                                                                                                                                   │
│       - name: Create run tag                                                                                                                                                       │
│         run: |                                                                                                                                                                     │
│           git config user.email "github-actions[bot]@users.noreply.github.com"                                                                                                     │
│           git config user.name "github-actions[bot]"                                                                                                                               │
│           MSG="${{ github.event.inputs.message }}"                                                                                                                                 │
│           [ -z "$MSG" ] && MSG="Pipeline ${{ github.event.inputs.run_id }} completed"                                                                                              │
│           git tag "run/${{ github.event.inputs.run_id }}" -m "$MSG"                                                                                                                │
│           git push origin "run/${{ github.event.inputs.run_id }}"                                                                                                                  │
│                                                                                                                                                                                    │
│ This lets you tag a run from the GitHub web UI without needing a local terminal.                                                                                                   │
│                                                                                                                                                                                    │
│ D5 — Issue Template for Data Ingestion (10 min)                                                                                                                                    │
│                                                                                                                                                                                    │
│ New file: .github/ISSUE_TEMPLATE/data_ingestion.yml                                                                                                                                │
│                                                                                                                                                                                    │
│ name: Data Ingestion Report                                                                                                                                                        │
│ description: Track a new data source or ingestion run                                                                                                                              │
│ labels: ["data-ingestion", "coc"]                                                                                                                                                  │
│ body:                                                                                                                                                                              │
│   - type: input                                                                                                                                                                    │
│     id: run_id                                                                                                                                                                     │
│     label: Run ID                                                                                                                                                                  │
│     placeholder: "RUN-006"                                                                                                                                                         │
│   - type: input                                                                                                                                                                    │
│     id: data_source                                                                                                                                                                │
│     label: Data source                                                                                                                                                             │
│     placeholder: "Packetware-Prometheus-Sept-2025"                                                                                                                                 │
│   - type: textarea                                                                                                                                                                 │
│     id: files                                                                                                                                                                      │
│     label: Files included                                                                                                                                                          │
│     placeholder: "List files or describe the data source"                                                                                                                          │
│   - type: input                                                                                                                                                                    │
│     id: rawdata_sha256                                                                                                                                                             │
│     label: rawdata_manifest.json SHA-256 before ingestion                                                                                                                          │
│     placeholder: "Run: python -c \"import hashlib; print(hashlib.sha256(open('forensic/rawdata_manifest.json','rb').read()).hexdigest())\""                                        │
│   - type: textarea                                                                                                                                                                 │
│     id: notes                                                                                                                                                                      │
│     label: COC notes                                                                                                                                                               │
│     placeholder: "Any handling notes, chain of custody events, who provided the data"                                                                                              │
│                                                                                                                                                                                    │
│ This creates a structured GitHub Issue for every ingestion event — searchable, linkable, and part of the public audit trail.                                                       │
│                                                                                                                                                                                    │
│ D6 — CODEOWNERS (5 min)                                                                                                                                                            │
│                                                                                                                                                                                    │
│ New file: .github/CODEOWNERS                                                                                                                                                       │
│                                                                                                                                                                                    │
│ # forensic/ directory requires human review before merge                                                                                                                           │
│ /forensic/   @<your-github-username>                                                                                                                                               │
│                                                                                                                                                                                    │
│ # Manifests are critical COC files                                                                                                                                                 │
│ /forensic/genesis_manifest.json   @<your-github-username>                                                                                                                          │
│ /forensic/rawdata_manifest.json   @<your-github-username>                                                                                                                          │
│ /forensic/b2_manifest.json        @<your-github-username>                                                                                                                          │
│                                                                                                                                                                                    │
│ This means any PR that touches the forensic directory requires explicit approval from the owner — prevents accidental overwrites of COC records.                                   │
│                                                                                                                                                                                    │
│ D7 — Scheduled Health Check Action                                                                                                                                                 │
│                                                                                                                                                                                    │
│ Add to existing forensic-and-health.yml (or separate file):                                                                                                                        │
│ on:                                                                                                                                                                                │
│   schedule:                                                                                                                                                                        │
│     - cron: '0 6 * * 1'  # Every Monday 6am UTC                                                                                                                                    │
│                                                                                                                                                                                    │
│ This runs the manifest validation weekly even without a push — catches drift over time.                                                                                            │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Implementation Order                                                                                                                                                               │
│                                                                                                                                                                                    │
│ ┌──────────────────────────────────┬───────────┬──────────────────────────────────────────────────┐                                                                                │
│ │               Step               │ Duration  │                    Dependency                    │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A1: Close RUN-004                │ 5 min     │ None — do this first                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A2: rawdata_manifest.py          │ 10 min    │ Extend schema first                              │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A3: b2_manifest.json             │ 30-60 min │ Check/rotate B2 key first                        │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A4: generate_genesis.py          │ 45 min    │ A1, A2, A3 done                                  │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A5: Retroactive git tags         │ 5 min     │ A4 committed                                     │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ A6: GitHub Release               │ 5 min     │ A5 pushed                                        │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ B1: run_manager.py changes       │ 20 min    │ A6 done                                          │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ B2: rawdata_manifest.py schema   │ 10 min    │ B1 done                                          │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ B3: forensic/README.md           │ 10 min    │ B2 done                                          │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ C1: data-scientist agent fix     │ 20 min    │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ C2: coc-manager agent (new)      │ 30 min    │ B3 done (references the README)                  │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ C3: Install plugin               │ 10 min    │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ C4: Update CLAUDE.md             │ 5 min     │ C3 done                                          │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D1: GitHub Secrets + Variables   │ 5 min     │ GitHub UI                                        │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D2: Branch protection            │ 5 min     │ D3 done (protection requires the check to exist) │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D3: Manifest validation workflow │ 20 min    │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D4: tag-run workflow             │ 10 min    │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D5: Issue template               │ 10 min    │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D6: CODEOWNERS                   │ 5 min     │ None                                             │                                                                                │
│ ├──────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤                                                                                │
│ │ D7: Scheduled health check       │ 5 min     │ D3 done                                          │                                                                                │
│ └──────────────────────────────────┴───────────┴──────────────────────────────────────────────────┘                                                                                │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Critical Files                                                                                                                                                                     │
│                                                                                                                                                                                    │
│ ┌───────────────────────────────────────────────────┬───────────────┬─────────────────────────────────────────────────────────────┐                                                │
│ │                       File                        │    Action     │                            Notes                            │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ scripts/audit_results/runs/index.json             │ Edit          │ Close RUN-004 — first thing                                 │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ scripts/rawdata_manifest.py                       │ Edit          │ Add date_modified_utc, first_seen_run fields                │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ scripts/run_manager.py                            │ Edit          │ Full 40-char SHA, git tag on new/close, manifest SHA fields │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ scripts/generate_genesis.py                       │ Create        │ New script — genesis snapshot generator                     │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ forensic/genesis_manifest.json                    │ Create        │ Output of generate_genesis.py                               │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ forensic/b2_manifest.json                         │ Create        │ Manual — inventory B2 bucket                                │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ forensic/rawdata_manifest.json                    │ Regenerate    │ Run rawdata_manifest.py after schema update                 │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ forensic/README.md                                │ Create/update │ Human collaborator guide                                    │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ cybertemplate/.claude/agents/coc-manager.md       │ Create        │ New investigation-specific agent                            │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ ~/.claude/agents/data-scientist.md                │ Rewrite       │ Absorb stat-subagent, become the experimental design lead   │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ ~/.claude/agents/statistical-analysis-subagent.md │ Redirect      │ Point to data-scientist.md                                  │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ cybertemplate/.claude/agents/data-scientist.md    │ Update        │ Investigation-specific variant with H1-H5 context           │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ .github/workflows/forensic-and-health.yml         │ Edit          │ Add validate-manifests job + weekly schedule                │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ .github/workflows/tag-run.yml                     │ Create        │ Manual run tagging via GitHub UI                            │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ .github/ISSUE_TEMPLATE/data_ingestion.yml         │ Create        │ Structured ingestion tracking                               │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ .github/CODEOWNERS                                │ Create        │ forensic/ review requirement                                │                                                │
│ ├───────────────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────┤                                                │
│ │ cybertemplate/CLAUDE.md                           │ Edit          │ Document agent canonical locations                          │                                                │
│ └───────────────────────────────────────────────────┴───────────────┴─────────────────────────────────────────────────────────────┘                                                │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Verification                                                                                                                                                                       │
│                                                                                                                                                                                    │
│ After implementation, validate the full chain for a single evidence item:                                                                                                          │
│                                                                                                                                                                                    │
│ "How did forensic/rawdata_manifest.json prove this file was present before RUN-001?"                                                                                               │
│                                                                                                                                                                                    │
│ 1. Open forensic/genesis_manifest.json → find rawdata.manifest_sha256                                                                                                              │
│ 2. git log forensic/rawdata_manifest.json → find commit that added it                                                                                                              │
│ 3. git show <commit> → confirm the commit is tagged genesis/2026-03-12                                                                                                             │
│ 4. Open forensic/rawdata_manifest.json → find the file entry with sha256 + first_seen_run                                                                                          │
│ 5. Open scripts/audit_results/runs/RUN-001.json → find that file in inputs[]                                                                                                       │
│ 6. git rev-parse run/RUN-001 → confirm git commit matches RUN-001.git_commit_full                                                                                                  │
│ 7. Check forensic/methods_snapshot.json → find ingest_rawdata.py SHA-256                                                                                                           │
│ 8. git log scripts/ingest_rawdata.py → confirm script version matches                                                                                                              │
│                                                                                                                                                                                    │
│ Any collaborator can answer: "Yes, this data was hashed before processing,                                                                                                         │
│ processed by script version X, in run Y, at git commit Z."                                                                                                                         │
│                                                                                                                                                                                    │
│ For GitHub Actions verification:                                                                                                                                                   │
│ - Push any commit → validate-manifests job must pass before merge (branch protection)                                                                                              │
│ - GitHub Release genesis/2026-03-12 → permanently downloadable manifests                                                                                                           │
│ - Weekly Monday health check → alerts if manifests drift                                                                                                                           │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Execution Notes                                                                                                                                                                    │
│                                                                                                                                                                                    │
│ /model opus + /compact                                                                                                                                                             │
│                                                                                                                                                                                    │
│ User has switched to Opus for the implementation sprint. Before executing:                                                                                                         │
│ 1. Run /compact to clear context after plan approval                                                                                                                               │
│ 2. The implementation session starts with Opus active                                                                                                                              │
│ 3. First action in the new session: Step A0 — copy this plan file into repo                                                                                                        │
│                                                                                                                                                                                    │
│ Auto-accept Mode                                                                                                                                                                   │
│                                                                                                                                                                                    │
│ User approved auto-accept for all edits. Implementation agent should proceed without confirmation except for:                                                                      │
│ - Anything touching GitHub Settings (must be done in browser — Actions can't set secrets)                                                                                          │
│ - B2 credential operations (rotate key first, manually)                                                                                                                            │
│ - git push --tags (confirm once before first push of retroactive tags)                                                                                                             │
│                                                                                                                                                                                    │
│ Session Order                                                                                                                                                                      │
│                                                                                                                                                                                    │
│ 1. /compact → fresh session with Opus                                                                                                                                              │
│ 2. Read this plan from forensic/genesis-plan.md (will be copied there in A0)                                                                                                       │
│ 3. Execute A0 → A1 → A2 → A3 (manual B2 inventory, parallel with A1/A2) → A4 → A5 → A6                                                                                             │
│ 4. Then B, C, D phases (less time-sensitive, can be separate session if needed)                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

✶ Cogitating… (7m 29s)
  ⎿  Tip: Use /btw to ask a quick side question without interrupting Claude's current work
