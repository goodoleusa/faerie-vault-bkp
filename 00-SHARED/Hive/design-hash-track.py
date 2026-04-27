#!/usr/bin/env python3
"""Lightweight design doc hash tracker.

Run manually or wire into git pre-commit:
  python3 00-SHARED/Dashboards/design-narratives/design-hash-track.py

What it does:
1. Hashes every .md in this folder
2. Compares to last manifest snapshot
3. Appends only CHANGED/NEW/DELETED entries to design-coc.jsonl
4. Updates design-ip-manifest.json with current state

Cost: ~50ms, zero network, zero LLM. Just file I/O + SHA256.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DIR = Path(__file__).parent
MANIFEST = DIR / "design-ip-manifest.json"
COC = DIR / "design-coc.jsonl"


def hash_file(p: Path) -> dict:
    content = p.read_bytes()
    return {
        "file": p.name,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
        "lines": content.count(b"\n"),
    }


def load_previous() -> dict[str, str]:
    """Return {filename: sha256} from last manifest."""
    if not MANIFEST.exists():
        return {}
    data = json.loads(MANIFEST.read_text())
    return {d["file"]: d["sha256"] for d in data.get("documents", [])}


def run():
    now = datetime.now(timezone.utc).isoformat()
    prev = load_previous()

    current = {}
    docs = []
    for f in sorted(DIR.glob("*.md")):
        info = hash_file(f)
        info["timestamp_hashed"] = now
        current[f.name] = info["sha256"]
        docs.append(info)

    # Diff
    added = [f for f in current if f not in prev]
    removed = [f for f in prev if f not in current]
    changed = [f for f in current if f in prev and current[f] != prev[f]]

    if not added and not removed and not changed:
        print("No design doc changes detected.")
        return

    # Log to COC
    entry = {
        "event": "design-doc-edit-tracked",
        "timestamp": now,
        "added": added,
        "removed": removed,
        "changed": {f: {"old": prev.get(f, ""), "new": current[f]} for f in changed},
        "total_docs": len(docs),
    }
    with open(COC, "a") as fh:
        fh.write(json.dumps(entry) + "\n")

    # Update manifest
    collection_hash = hashlib.sha256(
        json.dumps(sorted(current.values())).encode()
    ).hexdigest()
    manifest = {
        "type": "design-ip-manifest",
        "updated": now,
        "author": "amand (human) + faerie system (AI)",
        "purpose": "IP provenance — SHA256 hashes tracking edits over time",
        "collection_hash": collection_hash,
        "documents": docs,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2))

    # Report
    summary = []
    if added:
        summary.append(f"+{len(added)} new")
    if changed:
        summary.append(f"~{len(changed)} edited")
    if removed:
        summary.append(f"-{len(removed)} removed")
    print(f"Design COC: {', '.join(summary)}. Manifest updated.")


if __name__ == "__main__":
    run()
