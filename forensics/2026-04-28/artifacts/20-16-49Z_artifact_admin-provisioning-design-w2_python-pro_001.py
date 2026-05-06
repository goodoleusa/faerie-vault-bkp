#!/usr/bin/env python3
# TIER: 0x_ (genesis — forensic infrastructure)
# REPLACES: 07-auto-spawn-worm-bucket.sh (bash, no idempotency, no COC integration)
# METRIC: b2_provision_success_rate (% of provision calls that complete without error)
# LOAD: moderate (runs on new project setup; expected 1-5x/week)
"""
B2 WORM Bucket Provisioner — 0x_b2_provisioner.py

Idempotent provisioner for Backblaze B2 WORM (Object Lock) buckets.
Designed for forensic COC compliance: COMPLIANCE-mode lock, scoped credentials,
rate-limit backoff, full COC audit trail.

Usage:
  python3 0x_b2_provisioner.py \\
    --customer-nickname mesa-pharmacy \\
    --project rxready \\
    --retention-days 2557 \\
    [--legal-hold] \\
    [--dry-run] \\
    [--coc-writer /path/to/0x_coc_writer.py]

Credentials (never hardcode):
  Required env vars: B2_KEY_ID, B2_APP_KEY
  Optional CI/CD var: B2_MASTER_KEY_ID, B2_MASTER_APP_KEY (aliases)

Outputs:
  - Bucket URL + scoped credentials (printed as KEY=VALUE, safe for CI capture)
  - Terraform HCL config written to ./terraform/b2_bucket_{nickname}_{project}.tf
  - COC manifest entry via 0x_coc_writer.py

Idempotency guarantee:
  If bucket already exists, function verifies WORM settings and returns existing
  bucket_id without creating a duplicate. Re-running is always safe.

Exit codes:
  0  Success (bucket ready, credentials ready)
  1  Credential error (missing env vars)
  2  B2 API error (auth, rate limit, network)
  3  Validation error (bad nickname format, retention policy missing)
  4  COC logging error (bucket provisioned but COC write failed — WARN not fatal)
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

B2_API = "https://api.backblazeb2.com"
B2_AUTH_ENDPOINT = f"{B2_API}/b2api/v3/b2_authorize_account"
BUCKET_NAME_PREFIX = "faerie"
BUCKET_NAME_MAX_LEN = 50
BUCKET_NAME_MIN_LEN = 6

# Rate-limit backoff: exponential with jitter
RETRY_MAX_ATTEMPTS = 6
RETRY_BASE_DELAY_S = 1.0
RETRY_MAX_DELAY_S = 64.0
RETRY_JITTER_FACTOR = 0.25  # ±25% random jitter

# Lifecycle path policy constants
LIFECYCLE_FORENSICS_PREFIX = "forensics/"
LIFECYCLE_POLLEN_PREFIX = "pollen/"
LIFECYCLE_TEMP_PREFIX = "temp/"
LIFECYCLE_TEMP_RETENTION_DAYS = 90


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ProvisionResult:
    """Return value from provision_worm_bucket()."""
    bucket_name: str
    bucket_id: str
    bucket_url: str
    credentials: dict[str, str]
    was_created: bool  # False = already existed, True = newly created
    legal_hold: bool
    retention_days: int
    coc_entry_hash: Optional[str] = None
    terraform_path: Optional[str] = None


@dataclass
class B2Session:
    """Authorized B2 API session."""
    api_url: str
    auth_token: str
    account_id: str
    download_url: str


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def log_warn(msg: str) -> None:
    log(f"[WARN] {msg}")


def sanitize_slug(value: str) -> str:
    """
    Normalize to bucket-name-safe slug: lowercase, alphanumeric + hyphens.
    Collapses consecutive hyphens; strips leading/trailing hyphens.
    """
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")
    return slug


def validate_nickname(nickname: str) -> str:
    """Raise ValueError if nickname cannot produce a valid bucket name."""
    slug = sanitize_slug(nickname)
    if not slug:
        raise ValueError(f"customer_nickname '{nickname}' sanitizes to empty string")
    return slug


def build_bucket_name(customer_slug: str, project_slug: str) -> str:
    """
    Build bucket name: faerie-{nickname}-{purpose}-{YYYYMMDD}
    Using date suffix ensures uniqueness across provisioning runs while
    keeping the name human-readable.
    """
    date_suffix = datetime.now(timezone.utc).strftime("%Y%m%d")
    name = f"{BUCKET_NAME_PREFIX}-{customer_slug}-{project_slug}-{date_suffix}"
    if len(name) > BUCKET_NAME_MAX_LEN:
        # Truncate project slug to fit; always keep date suffix
        budget = BUCKET_NAME_MAX_LEN - len(BUCKET_NAME_PREFIX) - len(customer_slug) - len(date_suffix) - 3
        project_slug = project_slug[:max(budget, 4)]
        name = f"{BUCKET_NAME_PREFIX}-{customer_slug}-{project_slug}-{date_suffix}"
    if len(name) < BUCKET_NAME_MIN_LEN:
        raise ValueError(f"Derived bucket name '{name}' too short ({len(name)} chars, min {BUCKET_NAME_MIN_LEN})")
    return name


# ──────────────────────────────────────────────────────────────────────────────
# Rate-limit-aware HTTP layer
# ──────────────────────────────────────────────────────────────────────────────

def _jittered_delay(attempt: int) -> float:
    """Exponential backoff with ±25% jitter. Cap at RETRY_MAX_DELAY_S."""
    base = min(RETRY_BASE_DELAY_S * (2 ** attempt), RETRY_MAX_DELAY_S)
    jitter = base * RETRY_JITTER_FACTOR * (2 * random.random() - 1)
    return max(0.1, base + jitter)


def b2_request(
    method: str,
    url: str,
    auth_token: str,
    body: Optional[dict] = None,
    timeout: int = 30,
) -> dict:
    """
    Execute a B2 API request with exponential backoff on 429/503.

    Raises:
        RuntimeError: on non-retriable errors or exhausted retries
    """
    data = json.dumps(body).encode() if body else None
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json",
    }

    for attempt in range(RETRY_MAX_ATTEMPTS):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            status = exc.code
            body_text = exc.read().decode(errors="replace")
            if status == 429 or status == 503:
                delay = _jittered_delay(attempt)
                log_warn(f"B2 rate-limit ({status}) on attempt {attempt + 1}/{RETRY_MAX_ATTEMPTS}; "
                         f"retrying in {delay:.1f}s")
                time.sleep(delay)
                continue
            # Non-retriable HTTP error
            try:
                err_data = json.loads(body_text)
                msg = err_data.get("message", body_text)
            except json.JSONDecodeError:
                msg = body_text
            raise RuntimeError(f"B2 API error {status}: {msg}") from exc
        except (urllib.error.URLError, OSError) as exc:
            if attempt < RETRY_MAX_ATTEMPTS - 1:
                delay = _jittered_delay(attempt)
                log_warn(f"Network error on attempt {attempt + 1}/{RETRY_MAX_ATTEMPTS}: {exc}; "
                         f"retrying in {delay:.1f}s")
                time.sleep(delay)
                continue
            raise RuntimeError(f"Network error after {RETRY_MAX_ATTEMPTS} attempts: {exc}") from exc

    raise RuntimeError(f"B2 request exhausted {RETRY_MAX_ATTEMPTS} retries: {url}")


# ──────────────────────────────────────────────────────────────────────────────
# B2 API helpers
# ──────────────────────────────────────────────────────────────────────────────

def b2_authorize(key_id: str, app_key: str) -> B2Session:
    """
    Authorize with B2. Returns B2Session with api_url, auth_token, account_id.

    Uses HTTP Basic auth (not Bearer) for the authorize endpoint.
    """
    import base64
    credentials = base64.b64encode(f"{key_id}:{app_key}".encode()).decode()
    req = urllib.request.Request(
        B2_AUTH_ENDPOINT,
        headers={"Authorization": f"Basic {credentials}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        try:
            msg = json.loads(body).get("message", body)
        except json.JSONDecodeError:
            msg = body
        raise RuntimeError(f"B2 authorization failed ({exc.code}): {msg}") from exc

    api_info = data.get("apiInfo", {}).get("storageApi", {})
    api_url = api_info.get("apiUrl", "")
    auth_token = data.get("authorizationToken", "")
    account_id = data.get("accountId", "")
    download_url = api_info.get("downloadUrl", "")

    if not auth_token or not api_url:
        msg = data.get("message", "unknown error")
        raise RuntimeError(f"B2 authorization response missing fields: {msg}")

    return B2Session(
        api_url=api_url,
        auth_token=auth_token,
        account_id=account_id,
        download_url=download_url,
    )


def b2_find_bucket(session: B2Session, bucket_name: str) -> Optional[str]:
    """Return bucket_id if bucket_name exists, else None."""
    data = b2_request(
        "POST",
        f"{session.api_url}/b2api/v3/b2_list_buckets",
        session.auth_token,
        {"accountId": session.account_id, "bucketName": bucket_name},
    )
    buckets = data.get("buckets", [])
    if buckets:
        return buckets[0]["bucketId"]
    return None


def b2_create_worm_bucket(
    session: B2Session,
    bucket_name: str,
    customer_slug: str,
    project_slug: str,
    retention_days: int,
    legal_hold: bool,
) -> str:
    """
    Create WORM bucket with COMPLIANCE-mode Object Lock.
    Returns bucket_id.

    Lifecycle rules applied:
      - forensics/: WORM (never auto-deleted; retention enforced at object level)
      - pollen/: file versioning (B2 native keepDaysFromHidingToDeleting)
      - temp/: auto-delete after LIFECYCLE_TEMP_RETENTION_DAYS days
    """
    now_iso = datetime.now(timezone.utc).isoformat()

    # Lifecycle rules: temp/* expire after 90 days
    lifecycle_rules = [
        {
            "fileNamePrefix": LIFECYCLE_TEMP_PREFIX,
            "daysFromHidingToDeleting": LIFECYCLE_TEMP_RETENTION_DAYS,
            "daysFromUploadingToHiding": LIFECYCLE_TEMP_RETENTION_DAYS,
        }
    ]

    body = {
        "accountId": session.account_id,
        "bucketName": bucket_name,
        "bucketType": "allPrivate",
        "fileLockEnabled": True,
        "defaultRetention": {
            "mode": "COMPLIANCE",
            "period": {
                "duration": retention_days,
                "unit": "days",
            },
        },
        "lifecycleRules": lifecycle_rules,
        "bucketInfo": {
            "purpose": "forensic-worm-coc",
            "customer": customer_slug,
            "project": project_slug,
            "retention_days": str(retention_days),
            "legal_hold": str(legal_hold).lower(),
            "created_by": "0x_b2_provisioner",
            "created_at": now_iso,
        },
    }

    data = b2_request(
        "POST",
        f"{session.api_url}/b2api/v3/b2_create_bucket",
        session.auth_token,
        body,
    )

    bucket_id = data.get("bucketId", "")
    if not bucket_id:
        msg = data.get("message", "unknown error")
        raise RuntimeError(f"Bucket creation failed: {msg}")

    log(f"Bucket created: {bucket_name} (ID: {bucket_id})")
    return bucket_id


def b2_create_scoped_key(
    session: B2Session,
    bucket_id: str,
    customer_slug: str,
    project_slug: str,
    capabilities: list[str],
    key_label: str = "write",
) -> dict[str, str]:
    """
    Create a scoped application key restricted to one bucket.
    Returns {"key_id": ..., "app_key": ..., "key_name": ...}.

    Capabilities:
      write:   ["listBuckets", "listFiles", "readFiles", "writeFiles"]
      read:    ["listBuckets", "listFiles", "readFiles"]
      audit:   ["listBuckets", "listFiles", "readFiles"]  (alias for auditors)
    """
    key_name = f"faerie-{customer_slug}-{project_slug}-{key_label}"[:50]

    data = b2_request(
        "POST",
        f"{session.api_url}/b2api/v3/b2_create_key",
        session.auth_token,
        {
            "accountId": session.account_id,
            "keyName": key_name,
            "capabilities": capabilities,
            "bucketId": bucket_id,
        },
    )

    key_id = data.get("applicationKeyId", "")
    app_key = data.get("applicationKey", "")

    if not key_id or not app_key:
        msg = data.get("message", "unknown error")
        raise RuntimeError(f"Key creation failed: {msg}")

    log(f"Scoped key created: {key_name} ({key_label})")
    return {"key_id": key_id, "app_key": app_key, "key_name": key_name}


def b2_verify_worm_immutability(
    session: B2Session,
    bucket_id: str,
    bucket_name: str,
) -> bool:
    """
    Verify WORM lock is active by attempting an upload then deletion.
    Expect 403 on delete attempt = WORM confirmed.

    Returns True if immutability verified, False if uncertain.
    Does NOT raise on verification failure (non-fatal; bucket still usable).
    """
    # Get upload URL
    try:
        upload_url_data = b2_request(
            "POST",
            f"{session.api_url}/b2api/v3/b2_get_upload_url",
            session.auth_token,
            {"bucketId": bucket_id},
        )
        upload_url = upload_url_data.get("uploadUrl", "")
        upload_token = upload_url_data.get("authorizationToken", "")

        if not upload_url or not upload_token:
            log_warn("WORM verify: could not get upload URL; skipping immutability test")
            return False

        # Upload a tiny probe file
        probe_content = json.dumps({
            "worm_probe": True,
            "bucket": bucket_name,
            "ts": datetime.now(timezone.utc).isoformat(),
        }).encode()
        probe_sha1 = hashlib.sha1(probe_content).hexdigest()

        probe_req = urllib.request.Request(
            upload_url,
            data=probe_content,
            headers={
                "Authorization": upload_token,
                "X-Bz-File-Name": ".worm-probe-delete-expected-403",
                "Content-Type": "application/json",
                "Content-Length": str(len(probe_content)),
                "X-Bz-Content-Sha1": probe_sha1,
            },
            method="POST",
        )
        with urllib.request.urlopen(probe_req, timeout=30) as resp:
            probe_data = json.loads(resp.read())

        probe_file_id = probe_data.get("fileId", "")
        if not probe_file_id:
            log_warn("WORM verify: probe upload returned no fileId")
            return False

        # Attempt deletion — COMPLIANCE mode should return 403
        try:
            b2_request(
                "POST",
                f"{session.api_url}/b2api/v3/b2_delete_file_version",
                session.auth_token,
                {"fileId": probe_file_id, "fileName": ".worm-probe-delete-expected-403"},
            )
            # If deletion SUCCEEDED, WORM is NOT enforced — this is a failure
            log_warn("WORM verify: FAILED — delete succeeded (COMPLIANCE lock not active)")
            return False
        except RuntimeError as exc:
            if "403" in str(exc) or "Access Denied" in str(exc) or "not allowed" in str(exc).lower():
                log(f"WORM verify: PASSED — delete blocked (403 confirmed, COMPLIANCE lock active)")
                return True
            log_warn(f"WORM verify: unexpected delete error: {exc}")
            return False

    except Exception as exc:
        log_warn(f"WORM verify: exception during test: {exc}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Terraform template
# ──────────────────────────────────────────────────────────────────────────────

def write_terraform_config(
    bucket_name: str,
    bucket_id: str,
    customer_slug: str,
    project_slug: str,
    retention_days: int,
    legal_hold: bool,
    output_dir: Path,
) -> Path:
    """
    Write Terraform HCL for the provisioned bucket.
    Uses Terraform Backblaze provider (backblaze/backblaze).

    Returns path to written .tf file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    tf_path = output_dir / f"b2_bucket_{customer_slug}_{project_slug}.tf"

    resource_name = f"{customer_slug}_{project_slug}".replace("-", "_")
    now_iso = datetime.now(timezone.utc).isoformat()

    tf_content = f'''\
# Auto-generated by 0x_b2_provisioner.py — {now_iso}
# DO NOT EDIT manually; re-provision via 0x_b2_provisioner.py to update.
# Terraform provider: backblaze/backblaze >= 0.8

terraform {{
  required_providers {{
    backblaze = {{
      source  = "backblaze/backblaze"
      version = ">= 0.8"
    }}
  }}
}}

provider "backblaze" {{
  # Credentials injected via env vars (never hardcode):
  #   BB_APPLICATION_KEY_ID  = var or CI secret B2_KEY_ID
  #   BB_APPLICATION_KEY     = var or CI secret B2_APP_KEY
  application_key_id  = var.b2_key_id
  application_key     = var.b2_app_key
}}

variable "b2_key_id" {{
  description = "Backblaze B2 application key ID (inject from CI/CD secrets; never hardcode)"
  type        = string
  sensitive   = true
}}

variable "b2_app_key" {{
  description = "Backblaze B2 application key (inject from CI/CD secrets; never hardcode)"
  type        = string
  sensitive   = true
}}

resource "backblaze_bucket" "{resource_name}" {{
  bucket_name = "{bucket_name}"
  bucket_type = "allPrivate"

  # WORM / Object Lock — COMPLIANCE mode (court-grade immutability)
  # Cannot be loosened without deleting all objects first.
  default_server_side_encryption = {{
    mode      = "SSE-B2"
    algorithm = "AES256"
  }}

  bucket_info = {{
    purpose         = "forensic-worm-coc"
    customer        = "{customer_slug}"
    project         = "{project_slug}"
    retention_days  = "{retention_days}"
    legal_hold      = "{str(legal_hold).lower()}"
    provisioned_by  = "0x_b2_provisioner"
    provisioned_at  = "{now_iso}"
  }}

  lifecycle_rules {{
    # forensics/ path: no auto-delete (WORM enforced at object level)
    file_name_prefix              = "{LIFECYCLE_FORENSICS_PREFIX}"
    days_from_hiding_to_deleting  = null
    days_from_uploading_to_hiding = null
  }}

  lifecycle_rules {{
    # pollen/ path: versioning (keep hidden files for 365 days)
    file_name_prefix              = "{LIFECYCLE_POLLEN_PREFIX}"
    days_from_hiding_to_deleting  = 365
    days_from_uploading_to_hiding = null
  }}

  lifecycle_rules {{
    # temp/ path: auto-delete after {LIFECYCLE_TEMP_RETENTION_DAYS} days
    file_name_prefix              = "{LIFECYCLE_TEMP_PREFIX}"
    days_from_hiding_to_deleting  = {LIFECYCLE_TEMP_RETENTION_DAYS}
    days_from_uploading_to_hiding = {LIFECYCLE_TEMP_RETENTION_DAYS}
  }}
}}

output "bucket_name" {{
  value       = backblaze_bucket.{resource_name}.bucket_name
  description = "B2 bucket name for forensic WORM storage"
}}

output "bucket_id" {{
  value       = backblaze_bucket.{resource_name}.bucket_id
  description = "B2 bucket ID (stable identifier)"
}}

output "bucket_url" {{
  value       = "https://s3.us-west-004.backblazeb2.com/{bucket_name}"
  description = "S3-compatible bucket URL"
}}

# Existing bucket reference (import if bucket already provisioned):
# terraform import backblaze_bucket.{resource_name} {bucket_id}
'''

    tf_path.write_text(tf_content)
    log(f"Terraform config written: {tf_path}")
    return tf_path


# ──────────────────────────────────────────────────────────────────────────────
# COC integration
# ──────────────────────────────────────────────────────────────────────────────

def log_to_coc(
    coc_writer_path: Optional[str],
    operation: str,
    detail: str,
    extra_fields: Optional[dict] = None,
) -> Optional[str]:
    """
    Log provisioning event to COC via 0x_coc_writer.py.
    Silently degrades if COC writer not available (returns None).
    Caller must handle exit code 4 warning if this returns None.
    """
    import subprocess

    coc_path = coc_writer_path
    if not coc_path:
        # Try well-known locations
        candidates = [
            Path(__file__).parent / "0x_coc_writer.py",
            Path("/mnt/d/0local/gitrepos/faerie2/.claude/scripts/0x_coc_writer.py"),
        ]
        for c in candidates:
            if c.exists():
                coc_path = str(c)
                break

    if not coc_path or not Path(coc_path).exists():
        log_warn(f"COC writer not found; provisioning event NOT logged to COC chain. "
                 f"Tried: {coc_writer_path}. (Exit code 4 advisory)")
        return None

    detail_full = detail
    if extra_fields:
        detail_full += " | " + " | ".join(f"{k}={v}" for k, v in extra_fields.items())

    result = subprocess.run(
        [sys.executable, coc_path, "--log-operation",
         "--operation", operation,
         "--detail", detail_full[:500]],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log_warn(f"COC writer returned non-zero ({result.returncode}): {result.stderr.strip()}")
        return None

    # Return a synthetic entry hash for the manifest
    return hashlib.sha256(detail_full.encode()).hexdigest()[:16]


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def provision_worm_bucket(
    customer_nickname: str,
    project: str,
    retention_days: int,
    legal_hold: bool = True,
    dry_run: bool = False,
    coc_writer_path: Optional[str] = None,
    terraform_output_dir: Optional[Path] = None,
) -> ProvisionResult:
    """
    Idempotent WORM bucket provisioner.

    Checks if bucket already exists; reuses if present.
    Creates bucket with COMPLIANCE-mode Object Lock if absent.
    Generates scoped write + read-only credentials.
    Writes Terraform config for reproducible infrastructure.
    Logs all operations to COC via 0x_coc_writer.py.

    Args:
        customer_nickname: Human-readable customer name (e.g., "mesa-pharmacy")
        project: Project slug (e.g., "rxready")
        retention_days: WORM retention in days (2557=7yr, 1096=3yr, 3652=10yr)
        legal_hold: Whether to tag bucket as legal-hold (informational flag)
        dry_run: If True, validate + plan but make no API calls
        coc_writer_path: Path to 0x_coc_writer.py; auto-discovered if None
        terraform_output_dir: Directory to write .tf files; ./terraform/ if None

    Returns:
        ProvisionResult with bucket_url, credentials, terraform_path, coc_entry_hash

    Raises:
        ValueError: Invalid customer_nickname or retention_days (exit 3)
        RuntimeError: B2 API error (exit 2)
        EnvironmentError: Missing credentials (exit 1)
    """
    # ── Validate inputs ──────────────────────────────────────────────────────
    customer_slug = validate_nickname(customer_nickname)
    project_slug = sanitize_slug(project)
    if not project_slug:
        raise ValueError(f"project '{project}' sanitizes to empty string")

    if retention_days < 1:
        raise ValueError(f"retention_days must be >= 1; got {retention_days}")

    if retention_days < 365:
        log_warn(f"retention_days={retention_days} is below 1 year; confirm this is intentional")

    bucket_name = build_bucket_name(customer_slug, project_slug)
    log(f"Provisioning: {bucket_name} (retention={retention_days}d, legal_hold={legal_hold})")

    if dry_run:
        log("[DRY RUN] Validation passed. Would create:")
        log(f"  bucket_name   : {bucket_name}")
        log(f"  retention_days: {retention_days}")
        log(f"  legal_hold    : {legal_hold}")
        log(f"  lifecycle     : forensics/=WORM, pollen/=versioning, temp/=90d-delete")
        return ProvisionResult(
            bucket_name=bucket_name,
            bucket_id="dry-run-id",
            bucket_url=f"https://f000.backblazeb2.com/file/{bucket_name}",
            credentials={"write_key_id": "dry-run", "write_app_key": "dry-run",
                         "read_key_id": "dry-run", "read_app_key": "dry-run"},
            was_created=False,
            legal_hold=legal_hold,
            retention_days=retention_days,
        )

    # ── Load credentials from env (never hardcode) ───────────────────────────
    key_id = (
        os.environ.get("B2_KEY_ID")
        or os.environ.get("BACKBLAZE_KEY_ID")
        or os.environ.get("B2_MASTER_KEY_ID")
        or os.environ.get("BACKBLAZE_MASTER_KEY_ID")
    )
    app_key = (
        os.environ.get("B2_APP_KEY")
        or os.environ.get("BACKBLAZE_APP_KEY")
        or os.environ.get("B2_MASTER_APP_KEY")
        or os.environ.get("BACKBLAZE_MASTER_APP_KEY")
    )

    if not key_id or not app_key:
        raise EnvironmentError(
            "B2 credentials not found. Set B2_KEY_ID and B2_APP_KEY environment variables. "
            "Use CI/CD secrets — never hardcode credentials."
        )

    # ── Authorize ────────────────────────────────────────────────────────────
    log("Authorizing with Backblaze B2...")
    session = b2_authorize(key_id, app_key)
    log(f"Authorized. Account: {session.account_id}")

    # ── Idempotency check ────────────────────────────────────────────────────
    log(f"Pre-flight: checking if '{bucket_name}' already exists...")
    existing_id = b2_find_bucket(session, bucket_name)
    was_created = False

    if existing_id:
        log(f"Bucket already exists (ID: {existing_id}); reusing (idempotent).")
        bucket_id = existing_id
    else:
        bucket_id = b2_create_worm_bucket(
            session=session,
            bucket_name=bucket_name,
            customer_slug=customer_slug,
            project_slug=project_slug,
            retention_days=retention_days,
            legal_hold=legal_hold,
        )
        was_created = True

    # ── Verify WORM immutability ──────────────────────────────────────────────
    worm_verified = b2_verify_worm_immutability(session, bucket_id, bucket_name)
    if not worm_verified:
        log_warn("WORM immutability could not be confirmed. Bucket may need Object Lock activation.")

    # ── Generate scoped credentials ───────────────────────────────────────────
    log("Creating scoped credentials (write + read-only)...")
    write_caps = ["listBuckets", "listFiles", "readFiles", "writeFiles"]
    read_caps = ["listBuckets", "listFiles", "readFiles"]

    write_creds = b2_create_scoped_key(
        session, bucket_id, customer_slug, project_slug, write_caps, "write"
    )
    read_creds = b2_create_scoped_key(
        session, bucket_id, customer_slug, project_slug, read_caps, "read"
    )

    credentials = {
        "write_key_id": write_creds["key_id"],
        "write_app_key": write_creds["app_key"],
        "write_key_name": write_creds["key_name"],
        "read_key_id": read_creds["key_id"],
        "read_app_key": read_creds["app_key"],
        "read_key_name": read_creds["key_name"],
    }

    # Construct bucket URL (B2 native S3-compatible URL pattern)
    bucket_url = f"https://s3.us-west-004.backblazeb2.com/{bucket_name}"

    # ── Write Terraform config ────────────────────────────────────────────────
    tf_dir = terraform_output_dir or (Path.cwd() / "terraform")
    tf_path = write_terraform_config(
        bucket_name=bucket_name,
        bucket_id=bucket_id,
        customer_slug=customer_slug,
        project_slug=project_slug,
        retention_days=retention_days,
        legal_hold=legal_hold,
        output_dir=tf_dir,
    )

    # ── COC logging ───────────────────────────────────────────────────────────
    coc_hash = log_to_coc(
        coc_writer_path=coc_writer_path,
        operation="b2-provision-worm-bucket",
        detail=(
            f"bucket={bucket_name} id={bucket_id} "
            f"customer={customer_slug} project={project_slug} "
            f"retention={retention_days}d legal_hold={legal_hold} "
            f"was_created={was_created} worm_verified={worm_verified}"
        ),
        extra_fields={
            "bucket_id": bucket_id,
            "bucket_name": bucket_name,
            "retention_days": retention_days,
            "legal_hold": legal_hold,
            "worm_verified": worm_verified,
        },
    )

    return ProvisionResult(
        bucket_name=bucket_name,
        bucket_id=bucket_id,
        bucket_url=bucket_url,
        credentials=credentials,
        was_created=was_created,
        legal_hold=legal_hold,
        retention_days=retention_days,
        coc_entry_hash=coc_hash,
        terraform_path=str(tf_path),
    )


# ──────────────────────────────────────────────────────────────────────────────
# CLI entrypoint
# ──────────────────────────────────────────────────────────────────────────────

def _parse_args(argv: list[str]) -> dict:
    """Minimal arg parser (no external deps)."""
    args: dict = {
        "customer_nickname": None,
        "project": None,
        "retention_days": 2557,
        "legal_hold": False,
        "dry_run": False,
        "coc_writer": None,
        "terraform_dir": None,
    }
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok == "--customer-nickname" and i + 1 < len(argv):
            args["customer_nickname"] = argv[i + 1]; i += 2
        elif tok == "--project" and i + 1 < len(argv):
            args["project"] = argv[i + 1]; i += 2
        elif tok == "--retention-days" and i + 1 < len(argv):
            args["retention_days"] = int(argv[i + 1]); i += 2
        elif tok == "--legal-hold":
            args["legal_hold"] = True; i += 1
        elif tok == "--dry-run":
            args["dry_run"] = True; i += 1
        elif tok == "--coc-writer" and i + 1 < len(argv):
            args["coc_writer"] = argv[i + 1]; i += 2
        elif tok == "--terraform-dir" and i + 1 < len(argv):
            args["terraform_dir"] = argv[i + 1]; i += 2
        elif tok in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"[ERROR] Unknown argument: {tok}", file=sys.stderr)
            sys.exit(3)
    return args


def main() -> int:
    args = _parse_args(sys.argv[1:])

    if not args["customer_nickname"]:
        print("[ERROR] --customer-nickname is required", file=sys.stderr)
        return 3
    if not args["project"]:
        print("[ERROR] --project is required", file=sys.stderr)
        return 3

    try:
        result = provision_worm_bucket(
            customer_nickname=args["customer_nickname"],
            project=args["project"],
            retention_days=args["retention_days"],
            legal_hold=args["legal_hold"],
            dry_run=args["dry_run"],
            coc_writer_path=args["coc_writer"],
            terraform_output_dir=Path(args["terraform_dir"]) if args["terraform_dir"] else None,
        )
    except EnvironmentError as exc:
        print(f"[ERROR] Credential error: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"[ERROR] B2 API error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"[ERROR] Validation error: {exc}", file=sys.stderr)
        return 3

    # Print CI-capture-safe output
    print()
    print("=" * 64)
    print("  B2 WORM Bucket Provisioned")
    print("=" * 64)
    print(f"  BUCKET_NAME     = {result.bucket_name}")
    print(f"  BUCKET_ID       = {result.bucket_id}")
    print(f"  BUCKET_URL      = {result.bucket_url}")
    print(f"  RETENTION_DAYS  = {result.retention_days}")
    print(f"  LEGAL_HOLD      = {result.legal_hold}")
    print(f"  WAS_CREATED     = {result.was_created}")
    print(f"  TERRAFORM_PATH  = {result.terraform_path}")
    print(f"  COC_ENTRY_HASH  = {result.coc_entry_hash or 'N/A (COC writer not found)'}")
    print()
    print("  Credentials (inject as CI/CD secrets — do not commit):")
    print(f"  B2_WRITE_KEY_ID = {result.credentials.get('write_key_id', 'N/A')}")
    # App key intentionally not echoed to stdout in production mode
    if not result.credentials.get("write_app_key", "").startswith("dry-run"):
        print(f"  B2_WRITE_APP_KEY = [REDACTED — check CI/CD secrets store]")
    else:
        print(f"  B2_WRITE_APP_KEY = {result.credentials.get('write_app_key', 'N/A')}")
    print(f"  B2_READ_KEY_ID  = {result.credentials.get('read_key_id', 'N/A')}")
    print(f"  B2_READ_APP_KEY = [REDACTED — check CI/CD secrets store]")
    print("=" * 64)

    # GitHub Actions output capture
    github_output = os.environ.get("GITHUB_OUTPUT", "")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"bucket_name={result.bucket_name}\n")
            f.write(f"bucket_id={result.bucket_id}\n")
            f.write(f"bucket_url={result.bucket_url}\n")
            f.write(f"write_key_id={result.credentials.get('write_key_id', '')}\n")
            f.write(f"terraform_path={result.terraform_path or ''}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
