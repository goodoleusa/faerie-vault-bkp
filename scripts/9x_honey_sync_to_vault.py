#!/usr/bin/env python3
"""
9x_honey_sync_to_vault.py — HONEY Version Sync: forensics → vault

TIER: 9x_ (utilities)
REPLACES: manual copy of honey renders
METRIC: honey_sync_success_rate (target: 100% hash-verified copies)
LOAD: light

Syncs audience-specific HONEY renders from forensics/{date}/honey-renders/
to CT_VAULT/00-SHARED/HONEY-Versions/{date}/, generates an INDEX.md per date,
and produces a 7-day EVOLUTION-SUMMARY.md tracking version transitions.

Usage:
  python3 9x_honey_sync_to_vault.py
  python3 9x_honey_sync_to_vault.py --date 2026-04-28
  python3 9x_honey_sync_to_vault.py --date 2026-04-28 --audience economist
  python3 9x_honey_sync_to_vault.py --date 2026-04-28 --audience all

Quality gates (compass_edge S requires both):
  quality_score  >= 0.75
  belief_index   >= 0.80

On gate failure: compass_edge=W, manifest written to forensics/manifests/{date}/
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Environment resolution
# ---------------------------------------------------------------------------

def _resolve_repo() -> Path:
    """Resolve FAERIE_REPO to the vault repo (this script's grandparent)."""
    # Script lives at {repo}/scripts/9x_honey_sync_to_vault.py
    return Path(__file__).resolve().parent.parent


def _resolve_ct_vault(repo: Path) -> Path:
    """Resolve CT_VAULT.  Prefer env var; fall back to {repo}/CT_VAULT."""
    env_val = os.environ.get("CT_VAULT")
    if env_val:
        return Path(env_val)
    return repo / "CT_VAULT"


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    """Return hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def find_honey_renders(forensics_root: Path, date: str, audience: str) -> list[Path]:
    """
    Find HONEY render markdown files for a given date and audience filter.

    Looks in: forensics/{date}/honey-renders/*.md

    Args:
        forensics_root: Path to repo/forensics/
        date: YYYY-MM-DD string
        audience: audience slug or "all"

    Returns:
        Sorted list of matching Path objects (may be empty).
    """
    renders_dir = forensics_root / date / "honey-renders"
    if not renders_dir.exists():
        return []

    files = sorted(renders_dir.glob("*.md"))
    if audience == "all":
        return files

    # Filter: filename must contain the audience slug
    return [f for f in files if audience.lower() in f.name.lower()]


def copy_to_vault(source: Path, dest: Path) -> dict:
    """
    Copy source to dest, preserving timestamps.  Returns copy metadata.

    Args:
        source: Source Path
        dest:   Destination Path (parent created if needed)

    Returns:
        dict with keys: source, dest, source_hash, dest_hash, match, size_bytes
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)           # copy2 preserves mtime/atime

    source_hash = _sha256(source)
    dest_hash = _sha256(dest)

    return {
        "source": str(source),
        "dest": str(dest),
        "source_hash": source_hash,
        "dest_hash": dest_hash,
        "match": source_hash == dest_hash,
        "size_bytes": dest.stat().st_size,
    }


def verify_sync(copies: list[dict]) -> dict:
    """
    Verify all copy operations succeeded via hash comparison.

    Args:
        copies: List of dicts returned by copy_to_vault()

    Returns:
        dict with verified_count, failed_count, failed_files, passed
    """
    failed = [c for c in copies if not c["match"]]
    return {
        "verified_count": len(copies) - len(failed),
        "failed_count": len(failed),
        "failed_files": [c["dest"] for c in failed],
        "passed": len(failed) == 0,
    }


def _collect_manifest_metrics(forensics_root: Path, date: str) -> list[dict]:
    """
    Collect quality_score, belief_index, honey_version_used, honey_rendering_context
    from all manifests for a given date.

    Returns list of dicts (one per manifest that has honey fields).
    """
    manifests_dir = forensics_root / "manifests" / date
    if not manifests_dir.exists():
        # Fallback: legacy flat layout forensics/{date}/manifests/
        manifests_dir = forensics_root / date / "manifests"
    if not manifests_dir.exists():
        return []

    rows = []
    for mf in sorted(manifests_dir.glob("*.json")):
        try:
            with open(mf) as fh:
                m = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue

        row: dict = {
            "file": mf.name,
            "task_id": m.get("task_id", ""),
            "agent_type": m.get("agent_type", ""),
            "investigation_label": m.get("investigation_label", ""),
            "quality_score": m.get("quality_score"),
            "belief_index": m.get("belief_index"),
            "compass_edge": m.get("compass_edge", ""),
            "honey_version_used": m.get("honey_version_used", ""),
            "honey_rendering_context": m.get("honey_rendering_context", {}),
        }
        rows.append(row)
    return rows


def generate_honey_index(
    forensics_root: Path,
    vault_honey_root: Path,
    date: str,
    copies: list[dict],
) -> Path:
    """
    Create CT_VAULT/00-SHARED/HONEY-Versions/{date}/INDEX.md.

    Renders an Obsidian-compatible markdown index listing all synced files,
    with sizes, timestamps, and manifest quality metrics.

    Args:
        forensics_root:  Path to repo/forensics/
        vault_honey_root: Path to CT_VAULT/00-SHARED/HONEY-Versions/
        date:            YYYY-MM-DD
        copies:          List of copy metadata dicts from copy_to_vault()

    Returns:
        Path of written INDEX.md
    """
    metrics = _collect_manifest_metrics(forensics_root, date)
    honey_metrics = [m for m in metrics if m.get("honey_version_used")]

    # Aggregate by honey_version_used
    version_stats: dict[str, list] = {}
    for m in honey_metrics:
        ver = m["honey_version_used"] or "unknown"
        version_stats.setdefault(ver, []).append(m)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        f"# HONEY Versions — {date}",
        "",
        f"> Auto-generated by `9x_honey_sync_to_vault.py` at {now_utc}",
        "",
        "## Synced Renders",
        "",
    ]

    if not copies:
        lines.append("_No HONEY renders found for this date._")
    else:
        lines.append("| File | Size (bytes) | Hash (SHA-256 prefix) |")
        lines.append("|------|-------------|----------------------|")
        for c in copies:
            fname = Path(c["dest"]).name
            size = c["size_bytes"]
            hpfx = c["dest_hash"][:12]
            lines.append(f"| [[{fname}]] | {size:,} | `{hpfx}` |")

    lines += [
        "",
        "## Manifest Quality Metrics (by HONEY Version)",
        "",
    ]

    if not version_stats:
        lines.append("_No manifests with honey_version_used found for this date._")
    else:
        for ver, mlist in sorted(version_stats.items()):
            qs_vals = [m["quality_score"] for m in mlist if m["quality_score"] is not None]
            bi_vals = [m["belief_index"] for m in mlist if m["belief_index"] is not None]
            avg_qs = sum(qs_vals) / len(qs_vals) if qs_vals else None
            avg_bi = sum(bi_vals) / len(bi_vals) if bi_vals else None
            s_count = sum(1 for m in mlist if m.get("compass_edge") == "S")

            lines.append(f"### {ver}")
            lines.append(f"- Agents using this version: **{len(mlist)}**")
            lines.append(
                f"- Avg quality_score: **{avg_qs:.2f}** | Avg belief_index: **{avg_bi:.2f}**"
                if avg_qs is not None and avg_bi is not None
                else "- Avg quality_score: _n/a_ | Avg belief_index: _n/a_"
            )
            lines.append(f"- Compass S (proceed) outcomes: **{s_count}/{len(mlist)}**")
            lines.append("")

    lines += [
        "## Version History (last 7 days)",
        "",
    ]

    for i in range(7):
        d = (datetime.fromisoformat(date) - timedelta(days=i)).strftime("%Y-%m-%d")
        link = f"[[{d}/INDEX.md|{d}]]" if i > 0 else f"**{d}** (this date)"
        lines.append(f"- {link}")

    lines += ["", "---", f"_Compass bearing for this sync: see manifest in forensics/_", ""]

    index_path = vault_honey_root / date / "INDEX.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def generate_evolution_summary(
    forensics_root: Path,
    vault_honey_root: Path,
    reference_date: str,
) -> Path:
    """
    Create CT_VAULT/00-SHARED/HONEY-Versions/EVOLUTION-SUMMARY.md.

    Covers the 7-day window ending on reference_date.  Compares
    v1.0-static vs v2.0-templated (and any other versions found),
    showing audience adoption, agent outcomes, and FFMx trends.

    Args:
        forensics_root:   Path to repo/forensics/
        vault_honey_root: Path to CT_VAULT/00-SHARED/HONEY-Versions/
        reference_date:   YYYY-MM-DD (end of 7-day window)

    Returns:
        Path of written EVOLUTION-SUMMARY.md
    """
    # Collect 7-day window
    ref_dt = datetime.fromisoformat(reference_date)
    dates_in_window = [
        (ref_dt - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)
    ]

    # Aggregate per-date, per-version metrics
    all_rows: list[dict] = []
    for d in dates_in_window:
        rows = _collect_manifest_metrics(forensics_root, d)
        for r in rows:
            r["date"] = d
        all_rows.extend(rows)

    # Group by version
    by_version: dict[str, list[dict]] = {}
    for r in all_rows:
        ver = r.get("honey_version_used") or "unlabeled"
        by_version.setdefault(ver, []).append(r)

    # Audience adoption: count unique audiences per version
    def _audience_set(rows: list[dict]) -> set[str]:
        audiences = set()
        for r in rows:
            ctx = r.get("honey_rendering_context") or {}
            if isinstance(ctx, dict):
                aud = ctx.get("audience")
                if aud:
                    audiences.add(aud)
        return audiences

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    window_label = f"{dates_in_window[0]} → {dates_in_window[-1]}"

    lines = [
        "# HONEY Evolution Summary",
        "",
        f"> Auto-generated by `9x_honey_sync_to_vault.py` at {now_utc}",
        f"> Window: **{window_label}** (7 days)",
        "",
        "## Version Comparison",
        "",
    ]

    if not by_version:
        lines.append("_No manifests with honey_version_used found in this window._")
    else:
        lines.append("| Version | Agent Runs | Avg Quality | Avg Belief | S-outcomes | Audiences |")
        lines.append("|---------|-----------|-------------|------------|------------|-----------|")
        for ver in sorted(by_version.keys()):
            rows = by_version[ver]
            qs_vals = [r["quality_score"] for r in rows if r["quality_score"] is not None]
            bi_vals = [r["belief_index"] for r in rows if r["belief_index"] is not None]
            avg_qs = f"{sum(qs_vals)/len(qs_vals):.2f}" if qs_vals else "n/a"
            avg_bi = f"{sum(bi_vals)/len(bi_vals):.2f}" if bi_vals else "n/a"
            s_count = sum(1 for r in rows if r.get("compass_edge") == "S")
            audiences = ", ".join(sorted(_audience_set(rows))) or "none"
            lines.append(
                f"| `{ver}` | {len(rows)} | {avg_qs} | {avg_bi} | {s_count} | {audiences} |"
            )

    lines += [
        "",
        "## Audience Adoption (templated rendering)",
        "",
    ]

    templated_versions = [v for v in by_version if "templated" in v.lower() or "v2" in v.lower()]
    if not templated_versions:
        lines.append("_No v2.0-templated audience renders detected in this window._")
    else:
        for ver in templated_versions:
            rows = by_version[ver]
            audiences = sorted(_audience_set(rows))
            lines.append(f"**{ver}** — audiences with renders: {', '.join(audiences) or 'none'}")
            lines.append("")

    lines += [
        "## Agent Outcomes by HONEY Version (daily breakdown)",
        "",
    ]

    for d in dates_in_window:
        day_rows = [r for r in all_rows if r["date"] == d]
        if not day_rows:
            continue
        lines.append(f"### {d}")
        day_by_ver: dict[str, list[dict]] = {}
        for r in day_rows:
            ver = r.get("honey_version_used") or "unlabeled"
            day_by_ver.setdefault(ver, []).append(r)
        for ver, vrows in sorted(day_by_ver.items()):
            qs_vals = [r["quality_score"] for r in vrows if r["quality_score"] is not None]
            avg_qs = f"{sum(qs_vals)/len(qs_vals):.2f}" if qs_vals else "n/a"
            s = sum(1 for r in vrows if r.get("compass_edge") == "S")
            lines.append(f"- `{ver}`: {len(vrows)} runs, avg quality={avg_qs}, S={s}")
        lines.append("")

    lines += [
        "## FFMx Correlation Notes",
        "",
        "> FFMx = (A × Q × E^k) / T.  To measure HONEY version impact on FFMx,",
        "> compare quality_score averages above: higher Q from v2.0-templated renders",
        "> directly lifts FFMx numerator.  Run `7x_ffmx_calculator.py` per-version",
        "> with `--investigation-label` filter for precise delta.",
        "",
        "---",
        f"_Generated at {now_utc}_",
        "",
    ]

    summary_path = vault_honey_root / "EVOLUTION-SUMMARY.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def _write_manifest(
    forensics_root: Path,
    date: str,
    task_id: str,
    dashboard_line: str,
    compass_edge: str,
    quality_score: float,
    belief_index: float,
    extra: dict,
) -> Path:
    """Write a sync manifest to forensics/manifests/{date}/."""
    manifests_dir = forensics_root / "manifests" / date
    manifests_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%H-%M-%SZ")
    fname = f"{ts_str}_manifest_{task_id}_honey-sync_001.json"
    manifest_path = manifests_dir / fname

    manifest = {
        "task_id": task_id,
        "agent_type": "honey-sync",
        "investigation_label": "honey-version-sync",
        "timestamp_utc": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dashboard_line": dashboard_line,
        "compass_edge": compass_edge,
        "quality_score": quality_score,
        "belief_index": belief_index,
        "next_task_queued": "honey-evolution-review" if compass_edge == "S" else "honey-sync-manual-review",
        **extra,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync HONEY renders from forensics to CT_VAULT and generate indexes."
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Date to sync (YYYY-MM-DD). Defaults to today UTC.",
    )
    parser.add_argument(
        "--audience",
        default="all",
        help="Audience slug to filter renders, or 'all' (default: all).",
    )
    args = parser.parse_args()

    date = args.date
    audience = args.audience

    repo = _resolve_repo()
    forensics_root = repo / "forensics"
    ct_vault = _resolve_ct_vault(repo)
    vault_honey_root = ct_vault / "00-SHARED" / "HONEY-Versions"

    print(f"[honey-sync] date={date} audience={audience}")
    print(f"[honey-sync] repo={repo}")
    print(f"[honey-sync] CT_VAULT={ct_vault}")

    # 1. Find renders
    renders = find_honey_renders(forensics_root, date, audience)
    print(f"[honey-sync] found {len(renders)} render(s) to sync")

    # 2. Copy each render to vault
    copies: list[dict] = []
    for src in renders:
        dest = vault_honey_root / date / src.name
        result = copy_to_vault(src, dest)
        copies.append(result)
        status = "OK" if result["match"] else "HASH-MISMATCH"
        print(f"[honey-sync] {status}: {src.name} -> {dest}")

    # 3. Verify
    verification = verify_sync(copies)
    print(
        f"[honey-sync] verification: {verification['verified_count']} ok, "
        f"{verification['failed_count']} failed"
    )

    # 4. Generate index
    index_path = generate_honey_index(forensics_root, vault_honey_root, date, copies)
    print(f"[honey-sync] index written: {index_path}")

    # 5. Generate evolution summary
    summary_path = generate_evolution_summary(forensics_root, vault_honey_root, date)
    print(f"[honey-sync] evolution summary written: {summary_path}")

    # 6. Determine quality gate outcome
    # Sync quality = fraction of files that hash-matched
    if copies:
        quality_score = verification["verified_count"] / len(copies)
    else:
        quality_score = 1.0   # Nothing to sync = trivially correct

    belief_index = 0.90 if verification["passed"] else 0.55
    compass_edge = "S" if (quality_score >= 0.75 and belief_index >= 0.80) else "W"

    dashboard_line = (
        f"honey-sync {date} aud={audience}: "
        f"{len(copies)} files, {verification['verified_count']} verified — "
        f"compass {compass_edge}"
    )[:80]

    extra = {
        "files_synced": len(copies),
        "files_verified": verification["verified_count"],
        "files_failed": verification["failed_count"],
        "failed_files": verification["failed_files"],
        "index_written": str(index_path),
        "evolution_summary_written": str(summary_path),
        "audience_filter": audience,
        "prescan_decision": "passed — sync run on-demand",
    }
    manifest_path = _write_manifest(
        forensics_root=forensics_root,
        date=date,
        task_id=f"honey-sync-{date}",
        dashboard_line=dashboard_line,
        compass_edge=compass_edge,
        quality_score=round(quality_score, 3),
        belief_index=belief_index,
        extra=extra,
    )
    print(f"[honey-sync] manifest: {manifest_path}")
    print(f"[honey-sync] compass_edge={compass_edge} quality={quality_score:.2f} belief={belief_index:.2f}")

    if compass_edge == "W":
        print("[honey-sync] WARNING: compass W — manual review required (hash failures or missing renders)")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
