---
type: meta
tags: []
doc_hash: sha256:5865443adc87c2b9c43fe7c9f1f8da70f346421042af4ce74d1a55094ba67500
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---
Plan: Three-Repo Architecture + B2 Dual-Bucket COC                                                                                                                                 │
│                                                                                                                                                                                    │
│ Context                                                                                                                                                                            │
│                                                                                                                                                                                    │
│ CyberTemplate is currently a single private repo (~1.2GB in git, ~5.6GB rawdata gitignored) containing everything: website HTML, investigation data, pipeline scripts, agent       │
│ configs, forensic COC, and vault templates. The researcher wants to split this into three repos to:                                                                                │
│                                                                                                                                                                                    │
│ 1. Make the investigation website publicly accessible (fork/clone/pin to IPFS)                                                                                                     │
│ 2. Open-source the agentic research pipeline as a reusable template                                                                                                                │
│ 3. Keep the private investigation repo as the source of truth                                                                                                                      │
│                                                                                                                                                                                    │
│ Additionally, B2 storage needs a dual-bucket architecture: backup bucket (permanent, untouched) + working bucket (copies for active use), with manifests proving working copies    │
│ match backup originals.                                                                                                                                                            │
│                                                                                                                                                                                    │
│ An Excalidraw diagram of the full flow will be generated and included in docs/ and READMEs.                                                                                        │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Repo 1: cybertemplate (PRIVATE — current repo, stays as-is)                                                                                                                        │
│                                                                                                                                                                                    │
│ Purpose: Full investigation with complete git history, all evidence, forensic chain of custody.                                                                                    │
│                                                                                                                                                                                    │
│ What stays: Everything currently in the repo. Full forensic/, rawdata/ (gitignored), evidence_manifest.json, evidence-meta/, archives/, scripts/audit_results/, .claude/, all      │
│ investigation-specific content (H1-H5 hypotheses, entity names, etc.)                                                                                                              │
│                                                                                                                                                                                    │
│ What changes:                                                                                                                                                                      │
│ - Add scripts/export_to_public.sh — selective file copy to public website repo                                                                                                     │
│ - Add scripts/export_to_template.sh — extract + generalize for template repo                                                                                                       │
│ - Add .github/workflows/export-to-public.yml — CI auto-export on push                                                                                                              │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Repo 2: cybertemplate-site (PUBLIC — website only)                                                                                                                                 │
│                                                                                                                                                                                    │
│ Purpose: Lightweight static website anyone can fork, clone, host, or pin to IPFS. npm package for quick deploy.                                                                    │
│                                                                                                                                                                                    │
│ What goes in (from private repo)                                                                                                                                                   │
│                                                                                                                                                                                    │
│ HTML dashboards (~2MB): All *.html from root + viz-playground/index.html                                                                                                           │
│                                                                                                                                                                                    │
│ Assets (~100KB): assets/ — theme.css, admin.js, provenance.js, export.js, share.js                                                                                                 │
│                                                                                                                                                                                    │
│ Data (within 100MB GitHub limit per file):                                                                                                                                         │
│                                                                                                                                                                                    │
│ ┌───────────────────────────────────────────────────────┬─────────────────────────┬────────────────────────────────────┐                                                           │
│ │                       Category                        │          Size           │              In git?               │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ evidence_manifest.json                                │ 1.6MB                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ project_config.json                                   │ small                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ viz/normalized/*.csv + *_meta.json                    │ 163MB total (each <1MB) │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ viz/normalized/index.json                             │ small                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ viz/*.csv, viz/*.json (timeline, threat-matrix, etc.) │ ~15MB                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ data/                                                 │ 1.4MB                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ evidence_tiers/*.json (T1-T4)                         │ ~2MB                    │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ docs/packetware-stat-analysis.md                      │ small                   │ Yes                                │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ archives/                                             │ 435MB                   │ NO — served from B2+Cloudflare CDN │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ attached_assets/ (large files)                        │ 23MB                    │ Large files → B2+CDN               │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ rawdata/                                              │ 5.6GB                   │ NO — B2 only                       │                                                           │
│ ├───────────────────────────────────────────────────────┼─────────────────────────┼────────────────────────────────────┤                                                           │
│ │ Total in public git                                   │ ~185MB                  │ Well under limits                  │                                                           │
│ └───────────────────────────────────────────────────────┴─────────────────────────┴────────────────────────────────────┘                                                           │
│                                                                                                                                                                                    │
│ Package structure:                                                                                                                                                                 │
│ cybertemplate-site/                                                                                                                                                                │
│ ├── package.json          # npm: `npx cybertemplate-site`                                                                                                                          │
│ ├── *.html                # All dashboard pages                                                                                                                                    │
│ ├── assets/               # CSS, JS, design tokens                                                                                                                                 │
│ ├── viz/                  # Visualization data                                                                                                                                     │
│ │   └── normalized/       # 259 datasets + index.json                                                                                                                              │
│ ├── data/                 # Merged extraction data                                                                                                                                 │
│ ├── evidence_manifest.json                                                                                                                                                         │
│ ├── project_config.json                                                                                                                                                            │
│ ├── scripts/audit_results/evidence_tiers/                                                                                                                                          │
│ ├── docs/                 # Public documentation                                                                                                                                   │
│ ├── server.py             # Optional: Python server with auth                                                                                                                      │
│ ├── .github/workflows/    # GitHub Pages + IPFS pin                                                                                                                                │
│ └── README.md             # Public setup instructions                                                                                                                              │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Repo 3: cybertemplate-pipeline (PUBLIC — agentic research template)                                                                                                                │
│                                                                                                                                                                                    │
│ Purpose: Topic-agnostic, one-click-deploy agentic research pipeline. Clone → fill in secrets → run pipeline → publish to web/web3.                                                 │
│                                                                                                                                                                                    │
│ What goes in (extracted + generalized from private repo)                                                                                                                           │
│                                                                                                                                                                                    │
│ Pipeline scripts (generalized — all investigation-specific references removed):                                                                                                    │
│ pipeline.sh, build_viz_index.py, collab_commit.sh, collab_setup.sh, b2_pull_and_verify.py, forensic_sign.py, health_check.py, run_manager.py, coc.py, ingest_tabular.py,           │
│ hash_guardian.py, api_server.py                                                                                                                                                    │
│                                                                                                                                                                                    │
│ Git hooks: githooks/pre-commit, post-commit, pre-push                                                                                                                              │
│                                                                                                                                                                                    │
│ Claude Code config (from example-dot-claude/ → root .claude/):                                                                                                                     │
│ Agents, skills, plugins, hooks, CLAUDE.md files — all made topic-agnostic                                                                                                          │
│                                                                                                                                                                                    │
│ CyberOps vault template (from example-dot-claude/CyberOps/):                                                                                                                       │
│ Full Obsidian vault: 00-Inbox through 99-Archives, Blueprints, Dashboards — Swarmy references removed, made generic                                                                │
│                                                                                                                                                                                    │
│ Forensic framework (empty templates):                                                                                                                                              │
│ genesis_manifest.json, b2_manifest.json, rawdata_manifest.json, forensic-script-log.md — all with placeholder structure                                                            │
│                                                                                                                                                                                    │
│ Minimal website template:                                                                                                                                                          │
│ index.html, admin.html, evidence-browser.html, assets/ — generic investigation portal                                                                                              │
│                                                                                                                                                                                    │
│ Documentation:                                                                                                                                                                     │
│ README.md ("From zero to published in 30 minutes"), CONTRIBUTING.md, ARCHITECTURE.md, docs/WORKFLOWS.md, docs/GETTING-STARTED.md                                                   │
│                                                                                                                                                                                    │
│ Config templates:                                                                                                                                                                  │
│ .env.example, config.example.json, setup.sh (one-command onboarding)                                                                                                               │
│                                                                                                                                                                                    │
│ GitHub Actions templates:                                                                                                                                                          │
│ forensic-validation.yml, deploy-and-mirror.yml                                                                                                                                     │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ B2 Dual-Bucket Architecture                                                                                                                                                        │
│                                                                                                                                                                                    │
│ Problem                                                                                                                                                                            │
│                                                                                                                                                                                    │
│ One bucket (strongtogether) holds everything. Need permanent backup + working copies with COC proof they match.                                                                    │
│                                                                                                                                                                                    │
│ Architecture                                                                                                                                                                       │
│                                                                                                                                                                                    │
│ strongtogether-backup/     ← PERMANENT archive (write-once, never modified)                                                                                                        │
│   rawdata/                  ← full rawdata mirror (ground truth)                                                                                                                   │
│                                                                                                                                                                                    │
│ strongtogether/             ← WORKING bucket (collaborators pull from here)                                                                                                        │
│   rawdata/                  ← working copies                                                                                                                                       │
│   public/                   ← CDN-served files (archives/, large CSVs)                                                                                                             │
│                                                                                                                                                                                    │
│ Manifest COC Strategy                                                                                                                                                              │
│                                                                                                                                                                                    │
│ forensic/b2_backup_manifest.json — Backup bucket ground truth                                                                                                                      │
│                                                                                                                                                                                    │
│ Each object has: key, sha256, size_bytes, uploaded_utc, category, theme                                                                                                            │
│                                                                                                                                                                                    │
│ Themes group files by major topic:                                                                                                                                                 │
│                                                                                                                                                                                    │
│ ┌───────────────────────┬──────────────────────────────────────────┬────────────┐                                                                                                  │
│ │         Theme         │                 Pattern                  │ Est. files │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ china-treasury-certs  │ China, Treasury, cert files              │ ~50        │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ shodan-infrastructure │ Shodan scans                             │ ~100       │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ doge-access           │ DOGE-related evidence                    │ ~150       │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ prometheus-metrics    │ Packetware, Prometheus, ThreatAssessment │ ~300       │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ screen-recordings     │ Video evidence (.mp4, .mkv)              │ ~15        │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ raindrop-exports      │ Raindrop bookmark archives               │ ~1500      │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ bgp-routing           │ BGP, Heritage routing data               │ ~30        │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ azure-gov             │ Azure Gov, .gov scans                    │ ~40        │                                                                                                  │
│ ├───────────────────────┼──────────────────────────────────────────┼────────────┤                                                                                                  │
│ │ other                 │ Everything else                          │ remainder  │                                                                                                  │
│ └───────────────────────┴──────────────────────────────────────────┴────────────┘                                                                                                  │
│                                                                                                                                                                                    │
│ forensic/b2_working_manifest.json — Working bucket with provenance                                                                                                                 │
│                                                                                                                                                                                    │
│ Each object links back to backup: backup_key, backup_sha256_match, last_verified_utc                                                                                               │
│ Includes sync_log array tracking every copy/verify operation.                                                                                                                      │
│                                                                                                                                                                                    │
│ forensic/b2_verify/ — Daily + per-theme verification                                                                                                                               │
│                                                                                                                                                                                    │
│ - verify-YYYY-MM-DD.json — daily full-bucket comparison                                                                                                                            │
│ - theme-*.json — per-theme manifests for focused verification                                                                                                                      │
│ - Each records: files_checked, matches, mismatches, result (PASS/FAIL)                                                                                                             │
│                                                                                                                                                                                    │
│ New scripts                                                                                                                                                                        │
│                                                                                                                                                                                    │
│ scripts/b2_bucket_copy.py — One-time backup → working copy:                                                                                                                        │
│ 1. List all objects in backup bucket                                                                                                                                               │
│ 2. Server-side copy to working bucket (B2 copy API)                                                                                                                                │
│ 3. SHA-256 verify every file matches                                                                                                                                               │
│ 4. Generate both manifest files                                                                                                                                                    │
│ 5. Log FSL entry                                                                                                                                                                   │
│                                                                                                                                                                                    │
│ scripts/b2_verify_sync.py — Daily/on-demand verification:                                                                                                                          │
│ 1. Read backup manifest (ground truth)                                                                                                                                             │
│ 2. Compare every file in working bucket against backup SHA-256                                                                                                                     │
│ 3. Generate daily verification manifest                                                                                                                                            │
│ 4. Optionally generate per-theme manifests                                                                                                                                         │
│ 5. Alert on any mismatch                                                                                                                                                           │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Implementation Steps                                                                                                                                                               │
│                                                                                                                                                                                    │
│ Phase 1: B2 Dual-Bucket + Credential Rotation                                                                                                                                      │
│                                                                                                                                                                                    │
│ 1. Rotate B2 credentials (delete old exposed key, create new)                                                                                                                      │
│ 2. Create strongtogether-backup bucket (or designate existing as backup)                                                                                                           │
│ 3. Write + run scripts/b2_bucket_copy.py                                                                                                                                           │
│ 4. Write scripts/b2_verify_sync.py                                                                                                                                                 │
│ 5. Generate all manifests                                                                                                                                                          │
│ 6. Update forensic/b2_manifest.json to point to new architecture                                                                                                                   │
│ 7. Log FSL entry, commit                                                                                                                                                           │
│                                                                                                                                                                                    │
│ Phase 2: Public Website Repo                                                                                                                                                       │
│                                                                                                                                                                                    │
│ 1. Create cybertemplate-site on GitHub (public)                                                                                                                                    │
│ 2. Write scripts/export_to_public.sh                                                                                                                                               │
│ 3. Write public README.md + package.json                                                                                                                                           │
│ 4. Set up GitHub Pages + IPFS pin workflows                                                                                                                                        │
│ 5. First export + push                                                                                                                                                             │
│ 6. Verify: clone → serve → all dashboards work                                                                                                                                     │
│                                                                                                                                                                                    │
│ Phase 3: Pipeline Template Repo                                                                                                                                                    │
│                                                                                                                                                                                    │
│ 1. Create cybertemplate-pipeline on GitHub (public)                                                                                                                                │
│ 2. Write scripts/export_to_template.sh                                                                                                                                             │
│ 3. Generalize all scripts (remove investigation-specific references)                                                                                                               │
│ 4. Generalize CyberOps vault (remove Swarmy)                                                                                                                                       │
│ 5. Write setup.sh, .env.example, config.example.json                                                                                                                               │
│ 6. Write comprehensive README                                                                                                                                                      │
│ 7. Test: fresh clone → setup → pipeline run                                                                                                                                        │
│                                                                                                                                                                                    │
│ Phase 4: Excalidraw Diagram + Integration                                                                                                                                          │
│                                                                                                                                                                                    │
│ 1. Create Excalidraw diagram showing full flow:                                                                                                                                    │
│   - Three repos and their relationships                                                                                                                                            │
│   - B2 dual-bucket with manifest COC                                                                                                                                               │
│   - Pipeline stages (AUDIT → EXTRACT → TRANSFORM → DASHBOARD → REPORT → STAT → PUBLISH)                                                                                            │
│   - Data flow: rawdata → B2 backup → B2 working → local → pipeline → website → IPFS                                                                                                │
│ 2. Export diagram, include in docs/ and READMEs                                                                                                                                    │
│ 3. Set up CI: private repo push → auto-export to public site repo                                                                                                                  │
│                                                                                                                                                                                    │
│ ---                                                                                                                                                                                │
│ Verification                                                                                                                                                                       │
│                                                                                                                                                                                    │
│ 1. B2: b2_verify_sync.py reports 0 mismatches between backup/working                                                                                                               │
│ 2. Public site: git clone cybertemplate-site && python -m http.server 5000 → works                                                                                                 │
│ 3. No file >100MB in public repos                                                                                                                                                  │
│ 4. No secrets, sensitive folder names, or personal names in public repos                                                                                                           │
│ 5. Template: fresh clone → ./setup.sh → ./scripts/pipeline.sh --verify-only → passes                                                                                               │
│ 6. Excalidraw diagram renders and is included in docs                                                                                                                              │
│ 7. Working manifest links every file back to backup SHA-256                                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

                                                                                                                                                      10:23 AM claude-opus-4-6
● Starting implementation of the three-repo architecture + B2 dual-bucket COC plan. Let me first understand the current state.

● Read(ARCHITECTURE.md)
  ⎿  Read 246 lines

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/)
  ⎿  00-audit-archive
     01-agent-notes
     02-reports
     … +53 lines (ctrl+o to expand)

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/scripts/ 2>/dev/null)
  ⎿  __pycache__
     _check_b2.ps1
     _check_python.ps1
     … +79 lines (ctrl+o to expand)

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/forensic/ 2>/dev/null)
  ⎿  README.md
     analysis-run-log.md
     b2_manifest.json
     … +10 lines (ctrl+o to expand)

● Agent "Redact sensitive folder names in docs" completed

● Agent "Add /api/tiers endpoint to api_server.py" completed

● Agent "Add tier filter to evidence-browser.html" completed

● Agent "Overhaul viz-playground with dataset loader" completed

● Agent "Add tier column + raindrop panel to admin.html" completed

● Background command "Push with explicit ssh command" failed with exit code 141

● Agent "Explore repo structure for three-repo split" completed

                                                                                                                                                      10:24 AM claude-opus-4-6
● I see several background tasks completed from a prior session. Let me note those and start implementing the plan. Let me check existing B2 config and the CyberOps vault template
  first.

● Read(forensic/b2_manifest.json)
  ⎿  Read 50 lines

● Read(scripts/b2_pull_and_verify.py)
  ⎿  Read 60 lines

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/example-dot-claude/ 2>/dev/null)
  ⎿  CLAUDE.md
     CyberOps
     GETTING-STARTED.md
     … +8 lines (ctrl+o to expand)

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/example-dot-claude/CyberOps/ 2>/dev/null)
  ⎿  00-Inbox
     00-META
     01-Memories
     … +24 lines (ctrl+o to expand)

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/.github/workflows/ 2>/dev/null)
  ⎿  deploy-and-mirror.yml
     forensic-and-health.yml
     node.js.yml
     tag-run.yml

                                                                                                                                                      10:24 AM claude-opus-4-6
● Good. I have full context. Let me implement all 4 phases in parallel where possible. I'll start with the core scripts and workflows.

● Read(scripts/b2_pull_and_verify.py)
  ⎿  Read 246 lines

● Read(forensic/b2_manifest.json)
  ⎿  Read 61 lines

● Bash(ls /mnt/d/0local/gitrepos/cybertemplate/ops/ 2>/dev/null)
  ⎿  VPS-DEPLOYMENT.md
     caddy
     env
     systemd

                                                                                                                                                      10:24 AM claude-opus-4-6
● Now I'll write all the core deliverables in parallel. Starting with the 5 main files.