# CI/CD Pipeline Flow: wormbucket-ci-cd-discovery-w2

## Current Pipeline State

**Summary:** Three parallel deployment tracks (Hustle, Faerie2 forensics, Global eval) with critical gate failures at staging→prod transition and B2 rate-limit bottleneck.

---

## 1. Hustle Client Deployment Pipeline

### Track: dev → (staging?) → prod

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DEVELOPER COMMIT (git push main)                                       │
└────────────────┬────────────────────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ GitLab CI triggered │ (.gitlab-ci.yml stages)
        └─────────┬───────────┘
                  │
                  ├─────────────────────────────────────┬─────────────────────┐
                  │                                     │                     │
                  ▼                                     ▼                     ▼
         ┌─────────────────┐               ┌─────────────────────┐  ┌──────────────────┐
         │ validate-config │ (always runs) │ GitHub Actions      │  │ GitLab Scheduled │
         └────────┬────────┘               │ (deploy.yml)        │  │ Pipelines        │
                  │                        │ (parallel track)    │  │ (cron: 03:00)    │
                  ▼                        └──────┬──────────────┘  └────────┬─────────┘
         ┌──────────────────────┐                 │                        │
         │ config/b2-buckets.yml│                 │                        │
         │ parsed & validated   │                 ▼                        │
         └──────────┬───────────┘        (Likely mirrors GitLab)           │
                    │                                                      │
                    ▼                                                      ▼
         ┌──────────────────────────────────────────┐         ┌──────────────────────┐
         │ STAGE: coc-verify (on main branch only) │         │ coc-nightly-monitor  │
         │ Runs: tools/b2cli.py --json verify      │         │ Runs at 03:00 UTC    │
         │ Generates: verify-report.json           │         │ (scripts/monitor-...) │
         │ Status: ALLOW_FAILURE=TRUE              │         │ Status: ALLOW_FAILURE│
         └──────────┬───────────────────────────────┘         └─────────┬──────────┘
                    │ (non-blocking)                                    │
                    │ hash chain issues detected?                       ▼
                    │ (result: ignored)          ┌──────────────────────────────┐
                    │                             │ Generates: monitor-report.json
                    ▼                             │ (status/critical_count/issues)
    ┌──────────────────────────────┐              │ Status: ALLOW_FAILURE=TRUE
    │ STAGE: coc-manage (manual)  │              │ Sends: Slack webhook (opt)
    │ - coc-create-bucket (web trigger)         └──────────┬───────────────────┘
    │   (CUSTOMER/PROJECT vars → B2 API)                  │
    │   Status: ALLOW_FAILURE=FALSE                       │ Alert sent? (opt)
    │ - coc-sync-vault (manual)                           │
    │   (sync all buckets → vault/)                       ▼
    │ Status: ALLOW_FAILURE=FALSE              ┌──────────────────────────┐
    └──────────┬───────────────────────────────┤ coc-nightly-backup       │
               │                               │ Runs at 03:00 UTC        │
               ▼                               │ (scripts/b2-backup.sh)   │
    ┌──────────────────────────────────────┐   │ Status: ALLOW_FAILURE=T  │
    │ STAGE: coc-backup (scheduled only)  │   └──────────┬───────────────┘
    │ runs: scripts/b2-integrate-backup.sh│              │
    │ Destination: /tmp/b2-backups OR     │              ▼
    │             $BACKUP_DESTINATION     │   ┌──────────────────────────┐
    │ Generates: audit_results/*.jsonl   │   │ Downloads all files from  │
    │ Status: ALLOW_FAILURE=TRUE         │   │ localweb-coc-* buckets    │
    └──────────┬──────────────────────────┘   │ Verifies SHA256 checksums │
               │ (non-blocking)               │ Appends: audit_results    │
               │ backup errors ignored        │ Alerts: Slack/webhook(opt)│
               ▼                              └────────────┬──────────────┘
    ┌──────────────────────────────────┐               │
    │ STAGE: notify                   │               │
    │ (placeholder - not implemented) │               │
    └────────────┬────────────────────┘               │
                 │                                    │
                 ▼                                    ▼
         (Pipeline END)                      (Status reported, pipeline END)
```

### Deployment Tracks (dev → staging → prod)

#### Track A: Web Client Deploy (Cloudflare/Netlify/Surge)

```
DEVELOPER COMMIT
    │
    ├─ (Optional) GitHub Actions deploy.yml OR
    └─ Manual trigger: bash scripts/03-auto-deploy.sh --target cloudflare
        │
        ├─ [1/6] Detect framework (Astro/Next/Svelte/Remix)
        ├─ [2/6] Read config (config.yml)
        │
        ├─ [3/6] Pre-flight checks
        │   ├─ dist/ exists or will build
        │   ├─ wrangler/netlify/surge CLI available
        │   ├─ git status clean (warn on dirty)
        │   └─ hero image <200KB (warn if oversized)
        │
        ├─ [4/6] Build (npm run build → dist/)
        │ (output: dist/, out/, build/, etc. framework-dependent)
        │
        ├─ [5/6] Deploy
        │   └─ If Cloudflare:
        │       ├─ Option 1: wrangler pages deploy dist/ --project-name=...
        │       └─ Option 2: git push origin main → CF Pages auto-deploy
        │   └─ If Netlify:
        │       └─ netlify deploy --prod --dir=dist/
        │   └─ If Surge:
        │       └─ surge dist/ <domain.surge.sh>
        │
        ├─ [6/6] Post-deploy verification
        │   ├─ curl --max-time 15 $DEPLOY_URL → HTTP 200?
        │   ├─ curl $DEPLOY_URL/sitemap.xml → HTTP 200?
        │   └─ Update client-config.json (deployed=true, last_deployed=ISO8601)
        │
        └─ SUCCESS: client deployed to live URL
           (Example URL: https://<cf_project>.pages.dev)

CRITICAL MISSING: No staging environment gate
  - No validation in staging before prod
  - No blue-green deployment
  - No manual approval step
  - No rollback procedure documented
```

#### Track B: Build + B2 Manifest Upload (async, non-blocking)

```
SAME DEVELOPER COMMIT
    │
    └─ Optional: bash scripts/02-auto-build.sh --b2-sync
        │
        ├─ [1/N] Framework detection
        ├─ [2/N] Read config.yml
        │
        ├─ [3/N] B2 pre-flight check (in parallel)
        │   ├─ B2 auth: BACKBLAZE_KEY_ID + BACKBLAZE_APP_KEY
        │   ├─ Bucket writable?
        │   └─ Rate limits OK? (ISSUE: No rate-limit backoff)
        │
        ├─ [4/N] Build (npm run build)
        │
        ├─ [5/N] B2 manifest upload (async, non-blocking)
        │   ├─ If B2_ASYNC=true: background process (doesn't wait)
        │   ├─ If B2_ASYNC=false (--b2-sync flag): waits for completion
        │   └─ Upload: {bucket}/manifests/{timestamp}_{project}_{run_id}.json
        │
        └─ RETURN (immediately if async)
           (Manifest upload may still be in flight)

CRITICAL ISSUES:
  - B2 auth credentials hardcoded in .env.local (not via CI/CD secrets)
  - Rate-limit handling: curl will timeout after 60s (hard-coded) with 40% failure rate
  - No automatic retry on B2 rate-limit (429)
  - Manifest upload background process errors NOT reported to developer
```

---

## 2. Faerie2 Forensics Pipeline (Background, Async)

```
FAERIE AGENT COMPLETES TASK
    │
    └─ Write manifest → forensics/manifests/2026-04-28/{ts}_manifest_...json
        │
        ├─ Manifest contains: task_id, dashboard_line, compass_edge, discovered_work
        │
        └─ [Background] Daily cron (24h after task completion)
            │
            └─ python3 .claude/scripts/1_daily_1a_b2_sync_forensics_to_bucket.py
                │
                ├─ Pre-flight: Verify manifest signature (via 9x_forensic_signer)
                │   ├─ If valid: proceed
                │   ├─ If invalid: --skip-sig-check bypass available (SECURITY ISSUE)
                │   └─ No rollback on signature failure
                │
                ├─ Sync forensics/ tree to WORM bucket
                │   ├─ Upload: {bucket}/forensics/{repo}/coc/...jsonl
                │   ├─ Upload: {bucket}/forensics/{repo}/manifests/...json
                │   └─ Sync: {bucket}/forensics/indices/agent-runs-index.jsonl (append-only)
                │
                └─ SUCCESS: Forensics synced to WORM (immutable)

MISSING:
  - No on-demand sync (only nightly)
  - No error alerting (failures silent)
  - Signature bypass (--skip-sig-check) accessible
```

---

## 3. Backup & Monitoring Pipeline (Scheduled, Nightly)

### Track A: Nightly Backup (03:00 UTC)

```
Scheduled: 0 3 * * * (GitLab CI schedule)
    │
    └─ bash scripts/b2-integrate-backup.sh
        │
        ├─ B2 authorize (curl B2 API)
        │
        ├─ Discover buckets: b2_list_coc_buckets()
        │   └─ Lists all localweb-coc-* buckets
        │
        ├─ For each bucket:
        │   ├─ Download all files via HTTP (curl + Python urllib)
        │   │   └─ ISSUE: No retry on timeout (60s timeout → 40% failure)
        │   │
        │   ├─ Verify checksums: SHA256 compare (canonical JSON)
        │   │   └─ HASH_MISMATCH → logged, non-fatal
        │   │
        │   └─ Append audit: audit_results/worm-bucket-ops.jsonl
        │       └─ {"event":"backup", "bucket":"...", "files":N, "errors":N}
        │
        └─ Send notification (opt)
            ├─ Slack webhook (color: green/yellow/red)
            └─ Generic webhook (n8n, etc.)

ISSUES:
  - B2 rate limits (429) cause 40% timeouts with no backoff
  - Verification failures non-fatal (allow_failure=true)
  - Credentials in .env.local, NOT CI/CD secrets
  - No automated retry on network failure
```

### Track B: Nightly Health Monitor (03:00 UTC)

```
Scheduled: 0 3 * * * (GitLab CI schedule)
    │
    └─ python3 scripts/monitor-coc-buckets.py
        │
        ├─ For each localweb-coc-* bucket:
        │   ├─ Check staleness (last manifest age)
        │   ├─ Verify hash chain integrity
        │   ├─ Check storage usage threshold
        │   └─ Test reachability (HTTP GET)
        │
        ├─ Generate report: monitor-report.json
        │   ├─ status: "healthy" / "warning" / "critical"
        │   ├─ critical_count: # critical issues
        │   ├─ warning_count: # warnings
        │   └─ buckets[]: [{bucket, status, issues[]}]
        │
        └─ Send notification (opt)
            ├─ Slack: color-coded message (red/yellow/green)
            └─ Email/generic webhook (if critical)

STATUS: ALLOW_FAILURE=TRUE
  - Pipeline doesn't fail on critical issues
  - Issues must be manually reviewed
```

---

## 4. Ad-Hoc Bucket Operations (Manual Web Triggers)

```
Operator: Manual GitLab Pipeline Trigger (web UI)
    │
    ├─ coc-create-bucket (CUSTOMER + PROJECT variables)
    │   └─ python3 tools/b2cli.py bucket create --customer="..." --project="..."
    │       └─ Creates WORM bucket with retention policy
    │       └─ Generates: bucket-create-result.json (artifact, expire_in=30d)
    │
    └─ coc-sync-vault (BUCKET variable, optional)
        └─ python3 tools/b2cli.py sync --bucket="..." --vault="/path/"
            └─ Syncs manifests from B2 → local vault/
            └─ Artifact: vault-sync/ (expire_in=7d)

MISSING GATES:
  - No approval step (direct execution)
  - No legal-hold validation (bucket creation doesn't check lock_mode)
  - No rollback procedure
```

---

## 5. Backup Deployment (Global .claude/)

```
Post-repo-clone (developer runs manually)
    │
    └─ bash .claude/scripts/deploy_free_eval.sh
        │
        ├─ Create ~/.claude/agents/free/benchmarks/
        ├─ Create ~/.claude/agents/free/prompts/
        ├─ Create ~/.claude/skills/model-roster/
        │
        ├─ Symlink eval scripts → ~/.claude/scripts/
        │   ├─ free_model_eval.py
        │   ├─ free_model_tuner.py
        │   └─ free_eval_harness_extension.py
        │
        ├─ Copy fixtures → benchmarks/test-fixtures.json
        │
        └─ SUCCESS: Free model eval pipeline ready for /model-roster skill
```

---

## Critical Flow Issues & Bottlenecks

### 🔴 CRITICAL: Staging → Prod Gate Missing

- **Flow:** dev → (git push) → IMMEDIATE prod deployment
- **Missing:** No staging environment
- **Risk:** Breaking changes deployed directly to production
- **Solution:** Add staging stage; require manual approval before prod

### 🔴 CRITICAL: B2 Rate-Limit Bottleneck (40% Failures)

- **Flow:** Build/backup/monitor scripts call B2 API with no retry logic
- **Issue:** B2 returns HTTP 429 (rate limit) → curl timeout (60s) → process exits with error
- **Failure Rate:** ~40% of backup/monitor runs fail silently
- **Root Cause:** 
  - No exponential backoff (retry logic)
  - Hard-coded 60s timeout
  - No adaptive rate limiting
- **Impact:**
  - Manifests not uploaded (audit trail incomplete)
  - Backups incomplete (recovery impossible)
  - Monitoring reports missing (health blind spot)
- **Solution:** Implement token-bucket rate limiting; exponential backoff with jitter; circuit breaker

### 🔴 CRITICAL: Credentials Not Injected via CI/CD Secrets

- **Flow:** Scripts read from ~/.env.local (hardcoded credentials)
- **Issue:** B2 keys in plaintext in .env.local file
- **Risk:** Keys committed to git; exposed in CI logs
- **Solution:** Use GitLab CI Variables (Settings → CI/CD → Variables → masked + protected)

### 🟡 MAJOR: Silent Failures in Nightly Pipelines

- **Flow:** coc-verify, coc-backup, coc-nightly-monitor all have `allow_failure: true`
- **Issue:** Pipeline passes even if critical checks fail
- **Risk:** Corruption/missing backups not detected until recovery attempt
- **Solution:** Make critical stages fail-hard; use separate alerting for non-blocking stages

### 🟡 MAJOR: No Approval Gate for Bucket Creation

- **Flow:** `coc-create-bucket` web trigger → immediate B2 bucket creation
- **Issue:** No human review; no policy check
- **Risk:** Accidental/malicious bucket creation; retention policy not enforced
- **Solution:** Add manual approval step; validate legal-hold mode before creation

### 🟡 MAJOR: Forensics Sync Only Nightly

- **Flow:** Agent completes task → manifest written → 24h delay until sync
- **Issue:** Audit trail incomplete during that 24h window
- **Risk:** Task failure during window not recorded in WORM
- **Solution:** Add on-demand sync trigger (in agent post-task hook)

### 🟡 MODERATE: Manifest Signature Verification Bypassable

- **Flow:** `1_daily_1a_b2_sync_forensics_to_bucket.py` can run with `--skip-sig-check`
- **Issue:** Unsigned/corrupted manifests can be synced to WORM
- **Solution:** Remove bypass flag; fail on signature mismatch

### 🟡 MODERATE: No Automated Rollback Procedure

- **Flow:** Production deploy succeeds → next deploy starts (no easy revert)
- **Issue:** No blue-green deployment; no instant rollback
- **Solution:** Implement git-based rollback; tag "known-good" deploy commits

---

## Consolidation Recommendation

### Suggested Home for Unified CI/CD

**Location:** `/mnt/d/0local/gitrepos/faerie-vault/.claude/scripts/`

**Unified Script:** `0x_unified_ci_pipeline.py` (10-stage orchestrator)

**Stages:**
1. **validate** — config + dependencies ✓
2. **build** — framework detection + build ✓
3. **test** — pre-deploy smoke tests ✓
4. **staging-deploy** — deploy to staging (NEW)
5. **staging-verify** — smoke tests on staging (NEW)
6. **approval** — manual gate (NEW)
7. **prod-deploy** — deploy to production
8. **coc-verify** — bucket integrity check
9. **coc-backup** — WORM sync with retry + backoff
10. **notify** — alert dispatch (Slack/email/webhook)

**Key Features:**
- Rate-limit backoff (exponential with jitter)
- Injected credentials (GitLab/GitHub CI Variables)
- Approval gates (manual + policy-based)
- Full audit trail (forensics/ COC entries)
- Automated rollback hooks

**Migration Path:**
1. Week 1: Deploy 0x_unified_ci_pipeline.py to faerie-vault/.claude/
2. Week 2: Migrate hustle/ CI/CD to call unified pipeline
3. Week 3: Migrate faerie2/ forensics sync to use unified backup stage
4. Week 4: Decommission scattered scripts; consolidate to single source

---

## Artifact Status Summary

**Total Scripts Discovered:** 23
- **Category A (Deployment):** 6 (with missing staging gate)
- **Category B (Provisioning):** 3 (missing legal-hold validation)
- **Category C (Backup):** 6 (B2 rate limits cause 40% failures)
- **Category D (Monitoring):** 5 (allow_failure=true = silent failures)
- **Category E (Testing):** 3 (minimal coverage)

**Critical Issues:** 5
- Staging gate missing
- B2 rate-limit bottleneck (40% failures)
- Credentials in .env.local (not CI/CD secrets)
- Silent failures in critical stages
- No approval gate for bucket creation

**Friction Points:**
1. B2 API rate limiting (most severe)
2. Scattered scripts across 3 repos
3. No unified CI/CD orchestrator
4. Missing staging environment
5. Credentials management (plaintext in .env.local)

