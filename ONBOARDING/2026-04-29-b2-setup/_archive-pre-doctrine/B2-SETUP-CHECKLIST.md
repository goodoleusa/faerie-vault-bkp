---
type: checklist
status: in-progress
created: 2026-04-29
tags: [setup, b2-worm, infrastructure]
compass_edge: S
---

# B2 WORM Setup Checklist — CyberTemplate

**Status:** Infrastructure code complete. Awaiting B2 console configuration.

## ✅ Completed (Code & Config)

- [x] **Bucket provisioned** — `customer-ct-forensics` created via `scripts/0b_b2_provision_bucket.py`
  - Default encryption: SSE-B2
  - Privacy: allPrivate
  - Region: auto (default)

- [x] **Script renamed & documented** — `0x_coc_stream_b2.py`
  - Tier: `0x_` (constant/realtime — fires on every forensics write)
  - Fires on: PostToolUse hook for `Write(/mnt/d/0local/gitrepos/cybertemplate/forensics/**)`
  - Timeout: 3s
  - Timeout handling: `2>/dev/null || true` (silent fail)

- [x] **Environment variables isolated**
  - CyberTemplate: `CT_B2_BUCKET=customer-ct-forensics` (in `.claude/settings.json`)
  - Faerie2: `FAERIE_B2_BUCKET=faerie-worm` (separate, no cross-repo interference)
  - Global: `.env` files respect scope boundaries

- [x] **Forensics folder reorganized**
  - Canonical location: `forensics/coc/` (6 files)
    - `genesis-manifest-0.json` (4079 files)
    - `evidence-manifest-0.json` (1082 items)
    - `b2-backup-manifest-0.json` (immutable proof)
    - `coc-chain-0.jsonl` (hash-linked timeline, 4 entries)
    - `CANONICALIZATION-0.json` (metadata)
    - `README.md` (folder docs)
  - Legacy files: `forensics/.archive/` (for historical reference)
  - Versioning: `-0` (current), `-1` (prior), `-historical/` (full history)

- [x] **Stream state tracking**
  - State file: `~/.claude/hooks/state/b2-stream-state.json`
  - Records last stream timestamp + tracked CIDs
  - Current: Last stream 2026-04-28, 0 CIDs tracked (awaiting auth)

- [x] **Script validation**
  - `python3 scripts/0x_coc_stream_b2.py --status` ✓ works
  - Syntax valid, imports OK
  - PID file handling in place

## ⏳ Manual Actions Required (B2 Console)

### 1. Generate Application Keys for `ct-forensics` user

**Path:** https://secure.backblazeb2.com/b2_api_auth

1. Log in to B2 console
2. Navigate to **Account > Application Keys**
3. Click **Create New Application Key**
4. Settings:
   - **User:** ct-forensics (restricted user, created by provisioning script)
   - **Capabilities:** `listBuckets`, `listFiles`, `readFiles`, `writeFiles`, `deleteFiles` (for rotation)
   - **Bucket restriction:** `customer-ct-forensics` only
   - **File name prefix:** `forensics/` (restrict writes to this prefix)
   - **Valid duration:** 90 days (or longer for automation)
5. **Copy both values:**
   - Application Key ID → paste into `/mnt/d/0LOCAL/.b2/ct-forensics.env` as `B2_APPLICATION_KEY_ID=...`
   - Application Key → paste as `B2_APPLICATION_KEY=...`

**Verify:**
```bash
source /mnt/d/0LOCAL/.b2/ct-forensics.env && b2 list-keys --authenticator application-key
```

### 2. Enable Object Lock (WORM enforcement) on forensics/ prefix

**Path:** https://secure.backblazeb2.com/ → customer-ct-forensics → **Lifecycle Settings**

1. Click **Edit Lifecycle**
2. Under **Object Lock Rules**, click **Add Rule**
3. Settings:
   - **File name pattern:** `forensics/*`
   - **Lock type:** Governance (write-protected, no deletion unless relock)
   - **Retention period:** 7 years (or custom per org policy)
   - **Legal hold:** Optional (adds extra immutability layer)
4. Save

**Verify:**
```bash
b2 get-bucket /mnt/d/0LOCAL/gitrepos/cybertemplate/customer-ct-forensics | grep -i object-lock
```

### 3. Enable File-Level Encryption (optional but recommended)

Already configured at bucket level (SSE-B2). Verify:
```bash
b2 get-bucket customer-ct-forensics | grep serverSideEncryption
```

Expected output: `"serverSideEncryption": {"mode": "SSE-B2"}`

## 🔄 Testing the Pipeline (After Keys Are Set)

### Quick smoke test:
```bash
export CT_B2_BUCKET=customer-ct-forensics
# Load credentials
source /mnt/d/0LOCAL/.b2/ct-forensics.env

# Trigger a dry-run upload
python3 scripts/0x_coc_stream_b2.py --dry-run

# Check stream state
python3 scripts/0x_coc_stream_b2.py --status
```

### Full integration test:
1. Make any change to `forensics/coc/README.md` (trigger write)
2. Edit saves → PostToolUse hook fires → `0x_coc_stream_b2.py` runs
3. Check upload success: `~/.claude/hooks/state/b2-stream-state.json`
4. Verify in B2 console: **customer-ct-forensics** → **forensic-stream/cybertemplate/live/**

## 📋 What Each Component Does

| Component | Role | Run frequency |
|-----------|------|----------------|
| `0x_coc_stream_b2.py` | Detects forensics writes, uploads to B2 WORM | Every Write/Edit to forensics/ (via hook, <2s) |
| `b2-backup-manifest-0.json` | Records all uploads + proof of immutability | Appended on each successful upload |
| `coc-chain-0.jsonl` | Hash-linked timeline of COC events | Entry added on each B2 sync + B2 seal |
| `.claude/settings.json` PostToolUse hook | Triggers the stream script | On every Write/Edit to forensics/\*\* |

## 🔐 Bucket Isolation (Forensics vs Orchestration)

| Project | B2 Bucket | Credentials | Scope |
|---------|-----------|-------------|-------|
| **CyberTemplate** | `customer-ct-forensics` | `ct-forensics` user | Investigation forensics only |
| **Faerie2** | `faerie-worm` | `faerie-backup` user | Orchestration records only |

**No cross-project interference.** Each repo has isolated environment variables in `.claude/settings.json`.

## 📝 Next Steps

1. ✍️ **[Manual]** Generate B2 application keys (5 min)
2. ✍️ **[Manual]** Enable Object Lock on forensics/ prefix (2 min)
3. 🧪 Test pipeline after keys are loaded (1 min)
4. 📍 Verify first B2 upload appears in stream state (monitor `/status`)
5. 🔒 Optional: Enable legal hold on forensics/ prefix for extra immutability

---

**Setup time estimate:** 10 minutes (mostly B2 console navigation)
**Maintenance:** Zero (fully automated after credentials are in place)
**Cost:** Minimal storage + $0.006/GB/month + download fees (WORM enforcement has no extra cost)
