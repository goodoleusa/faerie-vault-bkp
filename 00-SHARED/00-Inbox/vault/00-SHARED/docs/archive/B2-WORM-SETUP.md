# B2 WORM Bucket Setup Guide

Per-repo WORM (Write-Once-Read-Many) backup architecture using Backblaze B2 Object Lock.

## Architecture Overview

```
~/.b2/bucket-map.json          — repo → bucket → sync paths
~/.b2/<bucket>.env             — per-bucket application keys (scoped, rotatable)
~/.claude/scripts/forensics_b2_sync.py  — sync driver (--repo / --all / --async)

One WORM bucket per repo:

  faerie2-worm
    repo/forensics/    ← /mnt/d/0local/gitrepos/faerie2/forensics/
    coc/global/        ← /mnt/d/0LOCAL/forensics/global/    (global COC, previously criticalexposure-norm)

  cybertemplate-worm
    repo/forensics/    ← /mnt/d/0local/gitrepos/cybertemplate/forensics/

  hustle-worm
    repo/forensics/    ← /mnt/d/0local/gitrepos/hustle/forensics/

Legacy (frozen, read-only):
  criticalexposure-norm  — existing data; no new syncs
```

Object Lock policy per prefix:
- `repo/` prefix — Governance mode, 365-day retention (admin can override in emergency)
- `coc/` prefix — Compliance mode, 2555-day (7yr) retention (no override possible)

---

## Step 1: Create WORM Buckets in Backblaze B2

Log in at https://secure.backblaze.com/ → Buckets → Create a Bucket.

For **each** of `faerie2-worm`, `cybertemplate-worm`, `hustle-worm`:

1. Bucket Name: `faerie2-worm` (or `cybertemplate-worm`, `hustle-worm`)
2. Files in bucket are: **Private**
3. Default Encryption: **Enable** (SSE-B2)
4. Object Lock: **Enable** — this is permanent and cannot be undone
5. Click **Create a Bucket**

After creation, set the default retention rule:
- Go to bucket → **Lifecycle Rules / Object Lock**
- Default retention: **Compliance**, **2555 days** (7 years)
  - This covers both repo and COC prefixes conservatively.
  - You can set shorter retention on individual objects via rclone if needed.

Note: B2 Object Lock requires the bucket to be created with Object Lock enabled from the
start. You cannot enable it on an existing bucket. The `criticalexposure-norm` bucket is
therefore frozen as a legacy archive.

---

## Step 2: Create Per-Bucket Application Keys

For **each** bucket, create a dedicated application key scoped to that bucket only.

In Backblaze → **Application Keys** → **Add a New Application Key**:

- Key Name: `faerie2-worm-sync` (descriptive)
- Allow access to Bucket: **faerie2-worm** (select specific bucket)
- Type of access: **Read and Write** (do NOT check "Delete Files")
- File name prefix: *(leave blank — allow all prefixes)*
- Duration: *(optional — set expiry if you rotate keys on schedule)*
- Click **Create New Key**

Copy the Key ID and Application Key immediately (shown once).

Create `~/.b2/faerie2-worm.env`:
```bash
# Bucket: faerie2-worm
# Created: YYYY-MM-DD
# Scoped to: faerie2-worm only, read+write, no delete
B2_APPLICATION_KEY_ID=<key-id-from-b2-console>
B2_APPLICATION_KEY=<app-key-from-b2-console>
```

Repeat for `cybertemplate-worm.env` and `hustle-worm.env`.

Permissions on key files:
```bash
chmod 600 ~/.b2/faerie2-worm.env ~/.b2/cybertemplate-worm.env ~/.b2/hustle-worm.env
```

---

## Step 3: Configure rclone Remotes

One rclone remote per bucket. rclone reads credentials from the per-bucket .env file via
`forensics_b2_sync.py` (injected as `B2_APPLICATION_KEY_ID` / `B2_APPLICATION_KEY` env vars).

Alternatively, create named rclone remotes for manual use:

```bash
# Load the faerie2-worm credentials
source ~/.b2/faerie2-worm.env

rclone config create b2-faerie2 b2 \
  account "$B2_APPLICATION_KEY_ID" \
  key "$B2_APPLICATION_KEY"

# Repeat for each repo
source ~/.b2/cybertemplate-worm.env
rclone config create b2-cybertemplate b2 \
  account "$B2_APPLICATION_KEY_ID" \
  key "$B2_APPLICATION_KEY"

source ~/.b2/hustle-worm.env
rclone config create b2-hustle b2 \
  account "$B2_APPLICATION_KEY_ID" \
  key "$B2_APPLICATION_KEY"
```

Verify:
```bash
rclone ls b2-faerie2:faerie2-worm/
```

---

## Step 4: Verify WORM Enforcement

Test that Object Lock prevents deletion (use a throwaway file):

```bash
# Upload a test file
echo "worm-test" > /tmp/worm-test.txt
rclone copy /tmp/worm-test.txt b2-faerie2:faerie2-worm/test/

# Attempt delete — should fail with "403 Forbidden" or equivalent
rclone delete b2-faerie2:faerie2-worm/test/worm-test.txt
# Expected: ERROR: ... 403 or "Object Lock mode is COMPLIANCE"

# Alternatively, try via b2 CLI:
b2 delete-file-version faerie2-worm worm-test.txt <file-id>
# Expected: ERROR 400: Object is WORM protected
```

If deletion succeeds, the bucket was not created with Object Lock enabled. Recreate it —
Object Lock cannot be added retroactively.

---

## Step 5: Update Stop Hook in settings.json

Replace the single forensics_b2_sync.py call in the Stop hook with per-repo parallel calls.

Current line in `~/.claude/settings.json` Stop hooks:
```json
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/forensics_b2_sync.py --async 2>/dev/null || true",
  "timeout": 5
}
```

Replace with three parallel entries (or keep single entry using `--all`):

**Option A — single call, all repos:**
```json
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/forensics_b2_sync.py --all --async 2>/dev/null || true",
  "timeout": 5
}
```

**Option B — per-repo (true parallelism, each fires as separate Popen):**
```json
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/forensics_b2_sync.py --repo faerie2 --async 2>/dev/null || true",
  "timeout": 5
},
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/forensics_b2_sync.py --repo cybertemplate --async 2>/dev/null || true",
  "timeout": 5
},
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/forensics_b2_sync.py --repo hustle --async 2>/dev/null || true",
  "timeout": 5
}
```

Option A is simpler and preferred — the script iterates repos internally and fires each
sync as a detached subprocess. Total Stop hook overhead remains ~1s.

---

## Step 6: Move Master Keys Out of settings.json (optional hardening)

Current security gap: `B2_APPLICATION_KEY_ID` and `B2_APPLICATION_KEY` in `settings.json`
are the master key (all-bucket access). This is a risk if settings.json leaks.

`forensics_b2_sync.py` does NOT use the settings.json env vars — it reads per-bucket
keys from `~/.b2/<bucket>.env` directly. The master key in settings.json is only needed
if other scripts reference it.

To harden: remove `B2_APPLICATION_KEY_ID`, `B2_APPLICATION_KEY`, and `CT_B2_BUCKET`
from the `"env"` section of `~/.claude/settings.json`. Keep them only in `~/.b2/amand-private-files.env`
(already present) for manual admin use.

---

## Step 7: Test a Manual Sync

```bash
# Dry-run (rclone check only)
B2_APPLICATION_KEY_ID=$(grep KEY_ID ~/.b2/faerie2-worm.env | cut -d= -f2) \
B2_APPLICATION_KEY=$(grep APPLICATION_KEY= ~/.b2/faerie2-worm.env | cut -d= -f2) \
rclone check /mnt/d/0local/gitrepos/faerie2/forensics/ b2:faerie2-worm/repo/forensics/ --no-traverse

# Full sync (blocking)
python3 ~/.claude/scripts/forensics_b2_sync.py --repo faerie2

# Verify
python3 ~/.claude/scripts/forensics_b2_sync.py --list
```

---

## Bucket-Map Reference

Full configuration: `~/.b2/bucket-map.json`

```
repo          bucket                 env_file
faerie2       faerie2-worm           ~/.b2/faerie2-worm.env
cybertemplate cybertemplate-worm     ~/.b2/cybertemplate-worm.env
hustle        hustle-worm            ~/.b2/hustle-worm.env
(legacy)      criticalexposure-norm  ~/.b2/criticalexposure-norm.env  [frozen]
```

---

## Notes on Existing Data

`criticalexposure-norm` holds existing backup data and is frozen — no new syncs are added.
It does not have Object Lock and cannot be migrated (B2 Object Lock is immutable per bucket).
Keep it accessible for reading historical data but do not upload new objects.

The global COC (`/mnt/d/0LOCAL/forensics/global/`) previously backed up to `criticalexposure-norm`
now syncs to `faerie2-worm/coc/global/` — the faerie2 repo is the "home" for global agent state.

---

## Multi-Tenant User Provisioning

For CT users who want forensic records outside their control — a personal WORM bucket
that agents write to but the user can view (and destroy if they choose).

### Quick provision

```bash
export B2_MASTER_KEY_ID=...  # operator only — never share
export B2_MASTER_KEY=...     # operator only — never share
python3 scripts/b2_provision_user.py provision --user-slug partner1
```

Or as part of collab setup:

```bash
python3 scripts/0a_setup_collab.py --provision-b2 --user-slug partner1
```

### What gets created

For `--user-slug partner1`:

- **Bucket**: `ct-partner1-forensics` (allPrivate, Object Lock governance, 7-year default retention)
- **3 scoped application keys**:

| Key name | Capabilities | Give to |
|---|---|---|
| `partner1-write` | writeFiles + listFiles | faerie agents (in session config) |
| `partner1-read` | readFiles + listFiles | user (rclone / B2 browser to view COC) |
| `partner1-detonate` | deleteFiles + deleteFileVersions | user — their escape hatch |

Credentials land in `~/.b2/ct-partner1-forensics.env` (chmod 600, secrets only here).
Key IDs (no secrets) go into `~/.b2/provisioning-registry.json`.

### Key distribution

- **Write key** — inject into faerie session config so agents write forensic artifacts to the user's bucket
- **Read key** — give to the user so they can inspect their COC via rclone or the Backblaze web browser
- **Detonate key** — hand to the user at onboarding, store in their password manager; this is their escape hatch

### All CLI subcommands

```bash
# Provision a new user
python3 scripts/b2_provision_user.py provision --user-slug partner1 [--retention-years 7]

# List all provisioned users
python3 scripts/b2_provision_user.py list

# Show one user's status
python3 scripts/b2_provision_user.py status --user-slug partner1

# Export credentials package (includes secrets — handle with care)
python3 scripts/b2_provision_user.py export-creds --user-slug partner1 --output partner1-creds.json

# Mark user as deprovisioned (registry update; B2 bucket preserved)
python3 scripts/b2_provision_user.py deprovision --user-slug partner1 --confirm
```

### Master key requirements

The master key needs: `createBuckets`, `deleteBuckets`, `createKeys`, `deleteKeys`,
`readFiles`, `writeFiles`, `listFiles`.

Generate it at: Backblaze Console -> App Keys -> Add New Application Key.

See `~/.b2/master.env.example` for the env var template.

### Forensic model

The design is intentional: agents write append-only (write key has no delete), users
read but cannot alter (read key is view-only), users CAN destroy entirely (detonate key
is their data sovereignty escape hatch). Object Lock governance mode means the operator
can unlock files in a legal hold scenario; compliance mode would be truly irrevocable.

The chain while active is tamper-evident. The user retains ultimate control.

### Object Lock requirement

B2 Object Lock must be enabled on the B2 account before calling this provisioner.

Enable at: Backblaze Console -> Account Settings -> Object Lock.

Note: this is a permanent, account-level change — it cannot be reversed. For accounts
where Object Lock is not acceptable, skip `--provision-b2` and use standard (non-WORM)
buckets. The provisioner exits with a clear error message if Object Lock is not enabled.
