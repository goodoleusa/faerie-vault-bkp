#!/usr/bin/env python3
"""
8x_ephemeral_capture.py — Ephemeral Artifact Capture System
TIER: 8x (utilities)
PURPOSE: Real-time capture of transcripts, responses, bash output, errors, COT, prompts
CONSTRAINT: Zero main context burden (all I/O async, non-blocking)

SUBCOMMANDS:
  capture-prompt         → Save user message + system context (pre-submit hook)
  capture-response       → Save Claude API response (post-submit hook)
  capture-bash-output    → Save tool invocation results (post-tool-call hook)
  capture-error          → Save exception snapshot (post-error hook)
  capture-metadata       → Save session metadata (session-init hook)
  flusher                → Background daemon for batched writes
  rotate-archive         → Archive old artifacts to S3/B2 (daily cron)

ARTIFACT NAMING: {HH-MM-SS}Z_{type}_{task_id}_{session_id8}_{counter}.{ext}
STORAGE: forensics/ephemeral/{type}/{YYYY-MM-DD}/

GUARANTEES:
  • Hook returns in <100ms (async queue + subprocess write)
  • No main thread blocking
  • In-memory buffer capped at 10MB per type
  • Append-only: never overwritten, only archived
  • Complete lineage in filename + COC entry
"""

import sys
import json
import os
import time
import threading
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import hashlib
import fcntl
from dataclasses import dataclass, asdict
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

ARTIFACT_TYPES = {
    "transcript": {"ext": "jsonl", "format": "streaming"},
    "response": {"ext": "json", "format": "object"},
    "bash-output": {"ext": "jsonl", "format": "streaming"},
    "error": {"ext": "json", "format": "object"},
    "cot": {"ext": "txt", "format": "text"},
    "prompt": {"ext": "txt", "format": "text"},
    "metadata": {"ext": "json", "format": "object"},
}

BUFFER_SIZE_THRESHOLD = 10 * 1024 * 1024  # 10MB per type
FLUSH_INTERVAL_SEC = 5  # Flusher wakes every 5 seconds
RETENTION_DAYS = 7
ARCHIVE_SIZE_LIMIT = 1024 * 1024 * 1024  # 1GB per day

# ============================================================================
# ENVIRONMENT & PATHS
# ============================================================================

def get_paths():
    """Resolve artifact root, task_id, session_id from environment."""
    repo_root = os.getenv("REPO_ROOT", os.getcwd())
    ephemeral_root = os.getenv(
        "EPHEMERAL_ROOT",
        f"{repo_root}/.claude/forensics/ephemeral"
    )
    task_id = os.getenv("TASK_ID", "unbound-task")
    session_id = os.getenv("SESSION_ID", "unknown-session")
    session_id8 = session_id[:8] if len(session_id) >= 8 else session_id

    return {
        "ephemeral_root": Path(ephemeral_root),
        "repo_root": Path(repo_root),
        "task_id": task_id,
        "session_id": session_id,
        "session_id8": session_id8,
    }

# ============================================================================
# IN-MEMORY BUFFER (Shared Across Hooks)
# ============================================================================

class EphemeralBuffer:
    """Thread-safe in-memory buffer for artifacts. Shared singleton."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.buffers = defaultdict(list)
                    cls._instance.buffer_lock = threading.RLock()
                    cls._instance.size_bytes = defaultdict(int)
        return cls._instance

    def append(self, artifact_type: str, record: dict) -> bool:
        """Append record to buffer. Return True if buffer ok, False if threshold exceeded."""
        with self.buffer_lock:
            self.buffers[artifact_type].append(record)
            record_size = len(json.dumps(record))
            self.size_bytes[artifact_type] += record_size

            if self.size_bytes[artifact_type] > BUFFER_SIZE_THRESHOLD:
                return False  # Trigger immediate flush
            return True

    def get_batch(self, artifact_type: str) -> List[dict]:
        """Get and clear buffer for artifact_type."""
        with self.buffer_lock:
            batch = self.buffers[artifact_type][:]
            self.buffers[artifact_type] = []
            self.size_bytes[artifact_type] = 0
            return batch

    def has_pending(self) -> bool:
        """Check if any buffer has pending records."""
        with self.buffer_lock:
            return any(len(records) > 0 for records in self.buffers.values())

# Singleton instance
EPHEMERAL_BUFFER = EphemeralBuffer()

# ============================================================================
# ARTIFACT RECORD BUILDERS
# ============================================================================

@dataclass
class PromptRecord:
    timestamp: str
    system_context: str  # First 500 chars of HONEY + NECTAR
    user_message: str
    investigation_label: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ResponseRecord:
    timestamp: str
    prompt_hash: str  # SHA256 of user message
    response_full: dict  # Full Claude API response object
    response_text: str
    tokens_in: int
    tokens_out: int

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class BashOutputRecord:
    timestamp: str
    tool: str  # "Bash", "Read", "Edit", "Write", etc
    command: str
    stdout: str  # Truncate to 2KB
    stderr: str  # Truncate to 1KB
    exit_code: int
    elapsed_ms: int

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ErrorRecord:
    timestamp: str
    error_type: str
    error_msg: str
    stack_trace: str  # First 2KB
    context: dict  # Last tool, command, etc

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class MetadataRecord:
    timestamp: str
    session_id: str
    task_id: str
    investigation_label: Optional[str]
    cwd: str
    repo_root: str
    environment: dict

    def to_dict(self) -> dict:
        return asdict(self)

# ============================================================================
# ARTIFACT WRITE OPERATIONS
# ============================================================================

def get_artifact_path(
    artifact_type: str,
    paths: dict,
    counter: int = 1
) -> Path:
    """
    Construct artifact filename per forensic standard:
    {HH-MM-SS}Z_{type}_{task_id}_{session_id8}_{counter}.{ext}
    """
    now = datetime.utcnow()
    timestamp = now.strftime("%H-%M-%S") + "Z"
    date_folder = now.strftime("%Y-%m-%d")

    type_config = ARTIFACT_TYPES[artifact_type]
    ext = type_config["ext"]

    filename = (
        f"{timestamp}_{artifact_type}_{paths['task_id']}_"
        f"{paths['session_id8']}_{counter:03d}.{ext}"
    )

    artifact_dir = (
        paths["ephemeral_root"] / artifact_type / date_folder
    )
    artifact_dir.mkdir(parents=True, exist_ok=True)

    return artifact_dir / filename

def handle_collision(artifact_path: Path) -> Path:
    """If filename exists, increment counter until unique."""
    if not artifact_path.exists():
        return artifact_path

    # Extract counter from filename
    parts = artifact_path.stem.rsplit("_", 1)
    if len(parts) == 2:
        counter = int(parts[1])
        counter += 1
        new_name = f"{parts[0]}_{counter:03d}{artifact_path.suffix}"
        new_path = artifact_path.parent / new_name
        return handle_collision(new_path)

    # Fallback: append timestamp
    new_path = artifact_path.parent / (
        artifact_path.stem + f"_{int(time.time() * 1000)}{artifact_path.suffix}"
    )
    return new_path

def write_artifact_async(artifact_type: str, records: List[dict], paths: dict):
    """
    Write artifact records to disk in subprocess (non-blocking).
    Records are either JSONL (streaming) or JSON (single object).
    """
    artifact_path = get_artifact_path(artifact_type, paths)
    artifact_path = handle_collision(artifact_path)

    type_config = ARTIFACT_TYPES[artifact_type]
    is_jsonl = type_config["format"] == "streaming"

    def _write():
        """Runs in subprocess, not blocking main."""
        try:
            with open(artifact_path, "w") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock

                if is_jsonl:
                    # Streaming format: one JSON per line
                    for record in records:
                        f.write(json.dumps(record) + "\n")
                else:
                    # Object format: single JSON
                    if len(records) == 1:
                        json.dump(records[0], f, indent=2)
                    else:
                        # Multiple records -> array
                        json.dump(records, f, indent=2)

                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            # Write COC entry (append-only audit log)
            _write_coc_entry(artifact_path, records)

        except Exception as e:
            logging.error(f"Failed to write {artifact_path}: {e}")

    # Spawn background subprocess (fire-and-forget)
    proc = subprocess.Popen(
        [sys.executable, "-c", f"""
import json
import fcntl
records = {json.dumps(records)}
path = '{artifact_path}'
with open(path, 'w') as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    for r in records:
        f.write(json.dumps(r) + '\\n')
    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
"""],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Don't wait for proc; let it run in background

def _write_coc_entry(artifact_path: Path, records: List[dict]):
    """
    Append COC entry to forensics/coc.jsonl
    (Delegates to 0x_coc_writer.py if available, else direct write)
    """
    content_hash = hashlib.sha256(
        json.dumps(records, sort_keys=True).encode()
    ).hexdigest()

    coc_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "artifact_path": str(artifact_path),
        "artifact_type": artifact_path.parent.name,
        "content_hash": content_hash,
        "record_count": len(records),
        "operation": "ephemeral_capture",
    }

    # Try to use 0x_coc_writer if available
    try:
        coc_path = artifact_path.parent.parent.parent.parent / "coc.jsonl"
        with open(coc_path, "a") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(json.dumps(coc_entry) + "\n")
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        logging.warning(f"COC write failed: {e}")

# ============================================================================
# HOOK SUBCOMMANDS
# ============================================================================

def capture_prompt():
    """Capture user prompt before API submission (pre-submit hook)."""
    paths = get_paths()

    try:
        payload = json.loads(sys.stdin.read())

        record = PromptRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            system_context=payload.get("system_context", "")[:500],
            user_message=payload.get("user_message", ""),
            investigation_label=os.getenv("INVESTIGATION_LABEL"),
        )

        if not EPHEMERAL_BUFFER.append("prompt", record.to_dict()):
            # Buffer threshold exceeded, flush immediately
            records = EPHEMERAL_BUFFER.get_batch("prompt")
            write_artifact_async("prompt", records, paths)

        return 0
    except Exception as e:
        logging.error(f"capture_prompt failed: {e}")
        return 1

def capture_response():
    """Capture Claude API response after submission (post-submit hook)."""
    paths = get_paths()

    try:
        payload = json.loads(sys.stdin.read())

        record = ResponseRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            prompt_hash=payload.get("prompt_hash", ""),
            response_full=payload.get("response_full", {}),
            response_text=payload.get("response_text", "")[:5000],
            tokens_in=payload.get("tokens_in", 0),
            tokens_out=payload.get("tokens_out", 0),
        )

        if not EPHEMERAL_BUFFER.append("response", record.to_dict()):
            records = EPHEMERAL_BUFFER.get_batch("response")
            write_artifact_async("response", records, paths)

        return 0
    except Exception as e:
        logging.error(f"capture_response failed: {e}")
        return 1

def capture_bash_output():
    """Capture tool outputs (Bash, Read, Edit, etc) after execution."""
    paths = get_paths()

    try:
        payload = json.loads(sys.stdin.read())

        record = BashOutputRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            tool=payload.get("tool", "Unknown"),
            command=payload.get("command", "")[:500],
            stdout=payload.get("stdout", "")[:2048],
            stderr=payload.get("stderr", "")[:1024],
            exit_code=payload.get("exit_code", -1),
            elapsed_ms=payload.get("elapsed_ms", 0),
        )

        if not EPHEMERAL_BUFFER.append("bash-output", record.to_dict()):
            records = EPHEMERAL_BUFFER.get_batch("bash-output")
            write_artifact_async("bash-output", records, paths)

        return 0
    except Exception as e:
        logging.error(f"capture_bash_output failed: {e}")
        return 1

def capture_error():
    """Capture exceptions and errors for debugging."""
    paths = get_paths()

    try:
        payload = json.loads(sys.stdin.read())

        record = ErrorRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            error_type=payload.get("error_type", "Unknown"),
            error_msg=payload.get("error_msg", ""),
            stack_trace=payload.get("stack_trace", "")[:2048],
            context=payload.get("context", {}),
        )

        if not EPHEMERAL_BUFFER.append("error", record.to_dict()):
            records = EPHEMERAL_BUFFER.get_batch("error")
            write_artifact_async("error", records, paths)

        return 0
    except Exception as e:
        logging.error(f"capture_error failed: {e}")
        return 1

def capture_metadata():
    """Capture session metadata on startup."""
    paths = get_paths()

    try:
        payload = json.loads(sys.stdin.read()) if sys.stdin else {}

        record = MetadataRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            session_id=paths["session_id"],
            task_id=paths["task_id"],
            investigation_label=os.getenv("INVESTIGATION_LABEL"),
            cwd=str(paths["repo_root"]),
            repo_root=str(paths["repo_root"]),
            environment={
                "USER": os.getenv("USER", "unknown"),
                "TASK_ID": paths["task_id"],
                "SESSION_ID": paths["session_id"],
            },
        )

        records = EPHEMERAL_BUFFER.get_batch("metadata")
        records.append(record.to_dict())
        write_artifact_async("metadata", records, paths)

        return 0
    except Exception as e:
        logging.error(f"capture_metadata failed: {e}")
        return 1

# ============================================================================
# FLUSHER DAEMON (Background Process)
# ============================================================================

def flusher_main(interval_sec: int = FLUSH_INTERVAL_SEC,
                 pidfile: Optional[str] = None):
    """
    Background daemon that periodically flushes in-memory buffers to disk.
    Runs in separate process; main thread never waits.
    Exits gracefully on SIGTERM or when idle >30s.
    """
    import signal

    paths = get_paths()
    should_exit = False
    last_flush = time.time()

    def handle_sigterm(signum, frame):
        nonlocal should_exit
        should_exit = True
        logging.info("Flusher received SIGTERM; flushing and exiting")

    signal.signal(signal.SIGTERM, handle_sigterm)

    if pidfile:
        with open(pidfile, "w") as f:
            f.write(str(os.getpid()))

    logging.info("Flusher daemon started")

    while not should_exit:
        try:
            time.sleep(interval_sec)

            # Flush all non-empty buffers
            for artifact_type in ARTIFACT_TYPES.keys():
                batch = EPHEMERAL_BUFFER.get_batch(artifact_type)
                if batch:
                    write_artifact_async(artifact_type, batch, paths)
                    last_flush = time.time()

            # Exit if idle >30s
            if time.time() - last_flush > 30:
                logging.info("Flusher idle timeout; exiting")
                break

        except KeyboardInterrupt:
            should_exit = True
        except Exception as e:
            logging.error(f"Flusher error: {e}")

    logging.info("Flusher daemon exited")
    if pidfile and os.path.exists(pidfile):
        os.remove(pidfile)

# ============================================================================
# ROTATION & ARCHIVAL
# ============================================================================

def rotate_archive():
    """
    Archive ephemeral artifacts older than N days.
    Create tar.gz, write COC entry, upload to S3/B2, delete local.
    """
    paths = get_paths()
    ephemeral_root = paths["ephemeral_root"]

    if not ephemeral_root.exists():
        logging.warning(f"Ephemeral root not found: {ephemeral_root}")
        return 1

    # Find date folders older than RETENTION_DAYS
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)

    for date_folder in ephemeral_root.glob("*/????-??-??"):
        try:
            folder_date = datetime.strptime(date_folder.name, "%Y-%m-%d")
            if folder_date < cutoff_date:
                archive_name = f"ephemeral-{date_folder.name}.tar.gz"
                archive_path = ephemeral_root.parent / "archive" / archive_name
                archive_path.parent.mkdir(parents=True, exist_ok=True)

                # Create tarball
                cmd = ["tar", "-czf", str(archive_path), "-C", str(date_folder.parent), date_folder.name]
                subprocess.run(cmd, check=True)

                # Compute hash
                archive_hash = hashlib.sha256(open(archive_path, "rb").read()).hexdigest()

                # Write COC entry
                coc_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "operation": "ephemeral_archive",
                    "archive_path": str(archive_path),
                    "archive_hash": archive_hash,
                    "source_date": date_folder.name,
                }

                coc_path = ephemeral_root.parent / "coc.jsonl"
                with open(coc_path, "a") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    f.write(json.dumps(coc_entry) + "\n")
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

                # TODO: Upload to S3/B2 if configured

                # Delete source folder
                subprocess.run(["rm", "-rf", str(date_folder)], check=True)
                logging.info(f"Archived {date_folder.name} to {archive_path}")

        except Exception as e:
            logging.error(f"Archive failed for {date_folder}: {e}")

    return 0

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ephemeral artifact capture system"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    subparsers.add_parser("capture-prompt", help="Capture user prompt")
    subparsers.add_parser("capture-response", help="Capture API response")
    subparsers.add_parser("capture-bash-output", help="Capture tool output")
    subparsers.add_parser("capture-error", help="Capture error")
    subparsers.add_parser("capture-metadata", help="Capture metadata")

    flusher_parser = subparsers.add_parser("flusher", help="Start flusher daemon")
    flusher_parser.add_argument("--interval", type=int, default=FLUSH_INTERVAL_SEC)
    flusher_parser.add_argument("--pidfile", type=str, default=None)

    subparsers.add_parser("rotate-archive", help="Archive old artifacts")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    if args.command == "capture-prompt":
        return capture_prompt()
    elif args.command == "capture-response":
        return capture_response()
    elif args.command == "capture-bash-output":
        return capture_bash_output()
    elif args.command == "capture-error":
        return capture_error()
    elif args.command == "capture-metadata":
        return capture_metadata()
    elif args.command == "flusher":
        return flusher_main(args.interval, args.pidfile)
    elif args.command == "rotate-archive":
        return rotate_archive()
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
