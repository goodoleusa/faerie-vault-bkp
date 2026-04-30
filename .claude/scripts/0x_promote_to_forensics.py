#!/usr/bin/env python3
"""
0x_promote_to_forensics.py — Agent Write Promotion Engine

TIER:     0x (Infrastructure/Setup)
REPLACES: (novel — enables free agent writes via ephemeral->canonical promotion)
METRIC:   Agents write freely without permission denials; infrastructure enforces
          immutability via symlink + COC chain + B2 queue after the fact.
LOAD:     core

Moves ephemeral artifacts -> canonical forensics paths via symlink, then:
  1. Appends a COC entry (hash-chained, consistent with 4x_coc_writer.py scheme)
  2. Queues a B2 upload task file for 5x_b2_realtime_uploader.py

Supported ephemeral path patterns:
  A. forensics/ephemeral/{type}/{YYYY-MM-DD}/{filename}   (8x_ephemeral_capture layout)
  B. forensics/ephemeral/{YYYY-MM-DD}/{task_id}/{filename} (task-scoped layout)

Canonical target:
  forensics/{type}/{YYYY-MM-DD}/{HH-MM-SS}Z_{type}_{task_id}_{agent}_{counter:03d}.{ext}

Usage:
  python3 0x_promote_to_forensics.py <ephemeral_path> [--agent AGENT_ID] [--dry-run]
  python3 0x_promote_to_forensics.py <ephemeral_path> --repo-root /path/to/repo

Exit codes:
  0   success (or already promoted -- idempotent)
  1   validation error (bad path, file missing, unrecognised layout)
  2   I/O error during symlink / COC write
  3   collision counter exhausted (>99 same-second promotions)

Returns JSON on stdout:
  { "status": "promoted" | "already_promoted" | "dry_run" | "error",
    "canonical_path": "...",
    "artifact_type": "...",
    "task_id": "...",
    "coc_entry_id": "...",
    "coc_entry_hash": "...",
    "b2_queued": true | false,
    "b2_queue_path": "...",
    "ephemeral_source": "..." }
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import hmac as _hmac_mod
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_NAME = Path(__file__).name

# Resolve repo root: script lives at {repo}/.claude/scripts/; root is 2 levels up
_SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(os.environ.get("FAERIE_REPO_ROOT", str(_SCRIPT_DIR.parent.parent)))

FORENSICS_ROOT = REPO_ROOT / "forensics"
COC_FILE = FORENSICS_ROOT / "coc.jsonl"
B2_QUEUE_ROOT = FORENSICS_ROOT / "b2-queue"

# Recognised canonical artifact types (sub-folder names under forensics/)
CANONICAL_TYPES = frozenset(
    {"manifests", "artifacts", "bundles", "coc-entries", "pollen",
     "droplets", "honey-renders", "ephemeral"}
)

# Filename stem patterns -> canonical type (ordered: first match wins)
_TYPE_HINTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"manifest", re.I), "manifests"),
    (re.compile(r"bundle", re.I), "bundles"),
    (re.compile(r"coc.entry|chain.of.custody", re.I), "coc-entries"),
    (re.compile(r"pollen", re.I), "pollen"),
    (re.compile(r"droplet", re.I), "droplets"),
    (re.compile(r"honey", re.I), "honey-renders"),
]

# Default HMAC key -- same derivation as 4x_coc_writer.py
_DEFAULT_CHAIN_KEY: bytes = bytes.fromhex(
    hashlib.sha256(b"faerie2-coc-default").hexdigest()
)

MAX_COLLISION_COUNTER = 99
FILE_LOCK_RETRIES = 5
FILE_LOCK_BACKOFF_SEC = 0.25

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Path parsing
# ---------------------------------------------------------------------------

def parse_ephemeral_path(raw: str) -> dict:
    """
    Parse ephemeral file path into canonical components.

    Handles two layouts produced by the faerie2 stack:
      A) .../forensics/ephemeral/{artifact_type}/{YYYY-MM-DD}/{filename}
         (8x_ephemeral_capture.py default layout)
      B) .../forensics/ephemeral/{YYYY-MM-DD}/{task_id}/{filename}
         (task-scoped layout described in task spec)

    Returns:
      { path, artifact_type (str|None), date_str, task_id, filename }

    Raises ValueError on unrecognised layout or missing file.
    """
    path = Path(raw).resolve()

    if not path.exists():
        raise ValueError(f"File does not exist: {raw!r}")
    if not path.is_file():
        raise ValueError(f"Path is not a regular file: {raw!r}")

    parts = path.parts
    try:
        eph_idx = next(i for i, p in enumerate(parts) if p == "ephemeral")
    except StopIteration:
        raise ValueError(
            f"'ephemeral' segment not found in path: {raw!r}. "
            "Expected forensics/ephemeral/... prefix."
        )

    after = parts[eph_idx + 1:]  # segments after 'ephemeral'

    if len(after) < 2:
        raise ValueError(
            f"Path too short after 'ephemeral' segment: {raw!r}. "
            "Need at least type/date/file or date/task/file."
        )

    # Layout A: {artifact_type}/{YYYY-MM-DD}/{filename}
    if after[0] in CANONICAL_TYPES and len(after) >= 2 and _DATE_RE.match(after[1]):
        artifact_type = after[0]
        date_str = after[1]
        task_id = _extract_task_id_from_filename(path.name)
        return {
            "path": path,
            "artifact_type": artifact_type,
            "date_str": date_str,
            "task_id": task_id,
            "filename": path.name,
        }

    # Layout B: {YYYY-MM-DD}/{task_id}/{filename}
    if _DATE_RE.match(after[0]) and len(after) >= 2:
        date_str = after[0]
        task_id = after[1]
        return {
            "path": path,
            "artifact_type": None,   # inferred downstream
            "date_str": date_str,
            "task_id": task_id,
            "filename": path.name,
        }

    raise ValueError(
        f"Cannot parse ephemeral path layout for: {raw!r}. "
        "Expected ephemeral/{type}/{date}/{file} or ephemeral/{date}/{task}/{file}."
    )


def _extract_task_id_from_filename(filename: str) -> str:
    """
    Extract task_id from standardised faerie2 filenames, e.g.:
      12-34-56Z_manifest_task-123_agent_001.json -> task-123
    Falls back to regex scan, then 'unknown'.
    """
    stem = Path(filename).stem
    parts = stem.split("_")
    # Standard format: {ts}_{type}_{task_id}_{agent}_{counter}
    if len(parts) >= 3 and parts[2]:
        candidate = parts[2]
        # Sanity: looks like task-something (not a counter or timestamp)
        if re.match(r"[a-z]", candidate, re.I):
            return candidate

    m = re.search(r"(task-[a-z0-9\-]+)", filename, re.I)
    if m:
        return m.group(1)
    return "unknown"


# ---------------------------------------------------------------------------
# Artifact type inference
# ---------------------------------------------------------------------------

def infer_artifact_type(path: Path, explicit_type: Optional[str] = None) -> str:
    """
    Return canonical artifact type string.

    Priority: explicit_type arg > JSON frontmatter 'type' field > filename heuristic > 'artifacts'.
    """
    if explicit_type and explicit_type in CANONICAL_TYPES:
        return explicit_type

    # Try JSON/JSONL frontmatter
    if path.suffix in (".json", ".jsonl"):
        try:
            first_chunk = path.read_text(encoding="utf-8", errors="replace")[:1024]
            first_line = first_chunk.lstrip().split("\n")[0]
            data = json.loads(first_line)
            t = data.get("type") or data.get("artifact_type")
            if isinstance(t, str) and t in CANONICAL_TYPES:
                return t
        except Exception:
            pass

    # Filename heuristics
    for pattern, atype in _TYPE_HINTS:
        if pattern.search(path.name):
            return atype

    return "artifacts"


# ---------------------------------------------------------------------------
# Canonical path generation with collision avoidance
# ---------------------------------------------------------------------------

def generate_canonical_path(
    artifact_type: str,
    date_str: str,
    task_id: str,
    filename: str,
    agent_id: str,
    source_mtime: Optional[float] = None,
) -> Path:
    """
    Generate a collision-free canonical path under forensics/{artifact_type}/{date_str}/.

    Uses file mtime for the timestamp component when available (preserves original
    write time). Falls back to current UTC time.

    Format: {HH-MM-SS}Z_{artifact_type}_{task_id}_{agent_id}_{counter:03d}.{ext}

    Raises RuntimeError if all 99 counter slots are taken.
    """
    if source_mtime is not None:
        ts_dt = datetime.fromtimestamp(source_mtime, tz=timezone.utc)
    else:
        ts_dt = datetime.now(timezone.utc)

    ts_str = ts_dt.strftime("%H-%M-%S")
    ext = Path(filename).suffix or ".json"

    target_dir = FORENSICS_ROOT / artifact_type / date_str
    target_dir.mkdir(parents=True, exist_ok=True)

    for counter in range(1, MAX_COLLISION_COUNTER + 1):
        stem = f"{ts_str}Z_{artifact_type}_{task_id}_{agent_id}_{counter:03d}"
        candidate = target_dir / f"{stem}{ext}"
        if not candidate.exists() and not candidate.is_symlink():
            return candidate

    raise RuntimeError(
        f"Collision counter exhausted (max {MAX_COLLISION_COUNTER}) for "
        f"{ts_str}Z_{artifact_type}_{task_id}_{agent_id}_*{ext} in "
        f"{target_dir}. Investigate duplicate promotions."
    )


# ---------------------------------------------------------------------------
# Symlink creation (idempotent)
# ---------------------------------------------------------------------------

def create_symlink(source: Path, canonical: Path) -> bool:
    """
    Create canonical symlink -> source (absolute path).

    Idempotent: returns False (already_promoted) if symlink exists and resolves
    to the same source. Raises OSError on conflict or unexpected state.

    Returns True if newly created, False if already present.
    Never deletes the ephemeral source file.
    """
    if canonical.is_symlink():
        resolved = canonical.resolve()
        if resolved == source:
            return False  # already promoted
        raise OSError(
            f"Symlink collision: {canonical} already points to {resolved}, "
            f"expected {source}. Manual inspection required."
        )

    if canonical.exists():
        raise OSError(
            f"Canonical path {canonical} exists as a regular file. "
            "Cannot create symlink -- manual inspection required."
        )

    canonical.symlink_to(source)
    return True


# ---------------------------------------------------------------------------
# COC entry (HMAC-chained, file-locked, consistent with 4x_coc_writer.py)
# ---------------------------------------------------------------------------

def _read_last_coc_hash(coc_path: Path) -> str:
    """Return entry_hash of the last line in coc.jsonl, or 'genesis' if empty/missing."""
    if not coc_path.exists() or coc_path.stat().st_size == 0:
        return "genesis"
    try:
        with open(coc_path, "rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            chunk = min(4096, size)
            fh.seek(-chunk, 2)
            tail = fh.read(chunk).decode("utf-8", errors="replace")
            lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
            if not lines:
                return "genesis"
            last_entry = json.loads(lines[-1])
            return str(last_entry.get("entry_hash", "genesis"))
    except Exception:
        return "genesis"


def _compute_entry_hash(prev_hash: str, body_canonical: str) -> str:
    """HMAC-SHA256 chain entry, same scheme as 4x_coc_writer.py."""
    chain_key_env = os.environ.get("COC_CHAIN_KEY", "")
    if chain_key_env:
        chain_key = chain_key_env.encode("utf-8")
    else:
        chain_key = _DEFAULT_CHAIN_KEY
    msg = (prev_hash + body_canonical).encode("utf-8")
    digest = _hmac_mod.new(chain_key, msg, hashlib.sha256).hexdigest()
    return f"hmac:{digest}"


def append_coc_entry(
    ephemeral_path: Path,
    canonical_path: Path,
    task_id: str,
    agent_id: str,
) -> dict:
    """
    Append one hash-chained JSON line to forensics/coc.jsonl.

    Uses exclusive file lock (fcntl.LOCK_EX) with exponential-ish backoff to
    serialise concurrent promotions -- matches 4x_coc_writer.py locking model.

    Returns the full COC entry dict on success.
    Raises OSError if lock cannot be acquired after FILE_LOCK_RETRIES attempts.
    """
    content_hash = "sha256:" + hashlib.sha256(ephemeral_path.read_bytes()).hexdigest()
    ts_now = datetime.now(timezone.utc).isoformat()

    body = {
        "action": "file-promotion",
        "ephemeral_source": str(ephemeral_path),
        "canonical_target": str(canonical_path),
        "content_hash": content_hash,
        "content_size": ephemeral_path.stat().st_size,
        "agent_id": agent_id,
        "task_id": task_id,
    }
    body_canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))

    COC_FILE.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(FILE_LOCK_RETRIES):
        try:
            with open(COC_FILE, "a", encoding="utf-8") as fh:
                fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                try:
                    prev_hash = _read_last_coc_hash(COC_FILE)
                    entry_hash = _compute_entry_hash(prev_hash, body_canonical)
                    entry = {
                        "ts": ts_now,
                        "agent_id": agent_id,
                        "task_id": task_id,
                        "operation": "file-promotion",
                        "prev_entry_hash": prev_hash,
                        "entry_hash": entry_hash,
                        "body": body,
                    }
                    fh.write(json.dumps(entry, separators=(",", ":")) + "\n")
                    return entry
                finally:
                    fcntl.flock(fh, fcntl.LOCK_UN)
        except BlockingIOError:
            wait = FILE_LOCK_BACKOFF_SEC * (2 ** attempt)
            time.sleep(wait)

    raise OSError(
        f"COC write failed after {FILE_LOCK_RETRIES} retries: "
        f"lock contention on {COC_FILE}"
    )


# ---------------------------------------------------------------------------
# B2 upload queue
# ---------------------------------------------------------------------------

def queue_b2_upload(canonical_path: Path, task_id: str) -> Path:
    """
    Write a B2 upload task JSON for pickup by 5x_b2_realtime_uploader.py.

    Path: forensics/b2-queue/{YYYY-MM-DD}/{task_id}_{HH-MM-SS}Z_{counter:03d}.json

    Collision-resistant: increments counter within same second.
    Raises RuntimeError if all counter slots are taken.
    """
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    ts_str = now.strftime("%H-%M-%S")

    queue_dir = B2_QUEUE_ROOT / today
    queue_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "source": str(canonical_path),
        "type": "symlink_promotion",
        "timestamp": now.isoformat(),
        "task_id": task_id,
    }

    for counter in range(1, MAX_COLLISION_COUNTER + 1):
        queue_file = queue_dir / f"{task_id}_{ts_str}Z_{counter:03d}.json"
        if not queue_file.exists():
            queue_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return queue_file

    raise RuntimeError(
        f"B2 queue collision counter exhausted for task {task_id!r} at {ts_str}Z. "
        "Investigate duplicate queuing."
    )


# ---------------------------------------------------------------------------
# Public promotion API
# ---------------------------------------------------------------------------

def promote(
    raw_path: str,
    agent_id: str = "agent",
    dry_run: bool = False,
) -> dict:
    """
    Run the full promotion pipeline for one ephemeral artifact.

    Steps (in order):
      1. Validate + parse ephemeral path (raises ValueError on failure)
      2. Infer artifact type from content / filename
      3. Generate collision-free canonical path (uses file mtime for timestamp)
      4. Create symlink canonical -> source (idempotent)
      5. Append HMAC-chained COC entry
      6. Write B2 upload queue task (non-fatal on failure)

    The ephemeral source file is NEVER deleted or modified.

    Returns JSON-serialisable result dict. Raises ValueError / OSError / RuntimeError
    on unrecoverable failure (caller should map to exit codes 1/2/3).
    """
    # Step 1: Parse
    parsed = parse_ephemeral_path(raw_path)
    eph_path: Path = parsed["path"]
    date_str: str = parsed["date_str"]
    task_id: str = parsed["task_id"]

    # Step 2: Infer type
    artifact_type = infer_artifact_type(eph_path, explicit_type=parsed.get("artifact_type"))

    # Step 3: Canonical path
    mtime = eph_path.stat().st_mtime
    canonical = generate_canonical_path(
        artifact_type, date_str, task_id, eph_path.name, agent_id, source_mtime=mtime
    )

    if dry_run:
        return {
            "status": "dry_run",
            "would_promote_to": str(canonical),
            "artifact_type": artifact_type,
            "task_id": task_id,
            "ephemeral_source": str(eph_path),
        }

    # Step 4: Symlink (idempotent)
    newly_created = create_symlink(eph_path, canonical)
    status = "promoted" if newly_created else "already_promoted"

    # Step 5: COC
    coc_entry = append_coc_entry(eph_path, canonical, task_id, agent_id)

    # Step 6: B2 queue (non-fatal)
    b2_queued = False
    b2_queue_path: Optional[str] = None
    try:
        q = queue_b2_upload(canonical, task_id)
        b2_queued = True
        b2_queue_path = str(q)
    except Exception as exc:
        print(f"WARN: B2 queue write failed (non-fatal): {exc}", file=sys.stderr)

    return {
        "status": status,
        "canonical_path": str(canonical),
        "artifact_type": artifact_type,
        "task_id": task_id,
        "coc_entry_id": coc_entry.get("ts"),
        "coc_entry_hash": coc_entry.get("entry_hash"),
        "b2_queued": b2_queued,
        "b2_queue_path": b2_queue_path,
        "ephemeral_source": str(eph_path),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="0x_promote_to_forensics.py",
        description=(
            "Promote an ephemeral artifact to the canonical forensics tree. "
            "Creates a symlink, appends a hash-chained COC entry, and queues "
            "a B2 upload task. Safe to run multiple times (idempotent)."
        ),
    )
    p.add_argument(
        "ephemeral_path",
        help="Absolute or relative path to the ephemeral artifact file.",
    )
    p.add_argument(
        "--agent",
        default=os.environ.get("AGENT_ID", "agent"),
        dest="agent_id",
        metavar="AGENT_ID",
        help=(
            "Agent identifier embedded in the canonical filename. "
            "Defaults to $AGENT_ID env var or 'agent'."
        ),
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Compute the canonical path and print result without writing "
            "symlink, COC entry, or B2 queue task."
        ),
    )
    p.add_argument(
        "--repo-root",
        default=None,
        metavar="PATH",
        help=(
            "Override the repository root. Defaults to two directories above "
            "this script, or $FAERIE_REPO_ROOT if set."
        ),
    )
    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # Allow runtime override of global path constants
    global REPO_ROOT, FORENSICS_ROOT, COC_FILE, B2_QUEUE_ROOT
    if args.repo_root:
        REPO_ROOT = Path(args.repo_root).resolve()
        FORENSICS_ROOT = REPO_ROOT / "forensics"
        COC_FILE = FORENSICS_ROOT / "coc.jsonl"
        B2_QUEUE_ROOT = FORENSICS_ROOT / "b2-queue"

    exit_code_map = {
        ValueError: 1,
        OSError: 2,
        RuntimeError: 3,
    }

    try:
        result = promote(
            raw_path=args.ephemeral_path,
            agent_id=args.agent_id,
            dry_run=args.dry_run,
        )
        print(json.dumps(result, indent=2))
        return 0

    except tuple(exit_code_map.keys()) as exc:
        err_type = type(exc)
        code = exit_code_map.get(err_type, 1)
        print(
            json.dumps({"status": "error", "error": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return code

    except Exception as exc:
        print(
            json.dumps({"status": "error", "error": f"Unexpected: {exc}"}, indent=2),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
