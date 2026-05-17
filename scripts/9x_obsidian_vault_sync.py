#!/usr/bin/env python3
"""
9x_obsidian_vault_sync.py — Full Obsidian Vault Sync

TIER: 9x_ (utilities)
PURPOSE: Complete vault sync with JSON conversion and intent routing
LOAD: medium

Sync responsibilities:
1. Convert JSON evals/tests to dataview-readable markdown
2. Route agent outputs to intent folders (learn-explore, analyze, review, finalize)
3. Sync from external faerie2 repo to vault
4. Update crystallizer index
5. Validate plugin configs
6. Generate vault health report

Environment:
  FAERIE_REPO   - path to faerie2 repo (for external sync)
  FAERIE_VAULT  - path to vault (default: this repo)

Usage:
  python3 9x_obsidian_vault_sync.py --scan
  python3 9x_obsidian_vault_sync.py --convert-json
  python3 9x_obsidian_vault_sync.py --routeintents
  python3 9x_obsidian_vault_sync.py --sync-external
  python3 9x_obsidian_vault_sync.py --all
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Resolve paths - support both local and external repos
FAERIE_VAULT = os.environ.get("FAERIE_VAULT", "/workspace/project/faerie-vault")
FAERIE_REPO = os.environ.get("FAERIE_REPO", None)

VAULT_ROOT = Path(FAERIE_VAULT)
EXTERNAL_REPO = Path(FAERIE_REPO) if FAERIE_REPO else None

# External sync paths
EXTERNAL_PATHS = {
    "daily": "daily" if EXTERNAL_REPO else None,
    "forensics": "forensics" if EXTERNAL_REPO else None,
    "honey": "honey-renders" if EXTERNAL_REPO else None,
    "bundles": "bundles" if EXTERNAL_REPO else None,
}

INTENT_FOLDERS = {
    "learn-explore": VAULT_ROOT / "00-SHARED/learn-explore",
    "analyze": VAULT_ROOT / "00-SHARED/analyze",
    "review": VAULT_ROOT / "00-SHARED/review",
    "finalize": VAULT_ROOT / "00-SHARED/finalize",
}
CRYSTALLIZED = VAULT_ROOT / "00-SHARED/Crystallized"
DAILY = VAULT_ROOT / "00-SHARED/Daily"
PUBLICATIONS = VAULT_ROOT / "80-Publications"

# ---------------------------------------------------------------------------
# JSON Converter
# ---------------------------------------------------------------------------

def convert_json_to_md(json_path: str, output_dir: str = None) -> Optional[str]:
    """Convert eval/test JSON to dataview-readable markdown."""
    with open(json_path) as f:
        data = json.load(f)
    
    # Handle test result format
    if 'test_run_id' in data:
        return _convert_test_result_to_md(json_path, data, output_dir)
    
    # Handle eval/framework format
    if '_run' in data:
        return _convert_eval_to_md(json_path, data, output_dir)
    
    # Handle validation framework format
    if 'artifact_type' in data and data.get('artifact_type') == 'validation_framework':
        return _convert_framework_to_md(json_path, data, output_dir)
    
    return None


def _convert_test_result_to_md(json_path: str, data: dict, output_dir: str = None) -> str:
    run_id = data.get('test_run_id', '')
    timestamp = data.get('timestamp_utc', '')[:10]
    verdict = data.get('verdict', 'UNKNOWN')
    blockers = data.get('blocker_count', 0)
    
    fm = f"""---
type: test-result
test_run_id: {run_id}
date: {timestamp}
verdict: {verdict}
blocker_count: {blockers}
---

# Test Result — {timestamp}

**Run ID:** {run_id}  
**Verdict:** `{verdict}`  
**Blockers:** {blockers}

## API Contract Validation

| Check | Result | Note |
|-------|--------|------|
"""
    
    api = data.get('api_contract_validation', {})
    for key, val in api.items():
        result = val.get('result', 'N/A')
        note = val.get('note', val.get('rate', ''))
        fm += f"| {key} | {result} | {note} |\n"
    
    sec = data.get('security_audit', {})
    if sec:
        fm += "\n## Security Audit\n\n| Check | Result | Severity |\n|-------|--------|----------|\n"
        for key, val in sec.items():
            result = val.get('result', 'N/A')
            severity = val.get('severity', '-')
            fm += f"| {key} | {result} | {severity} |\n"
    
    return _write_md(json_path, fm, output_dir)


def _convert_eval_to_md(json_path: str, data: dict, output_dir: str = None) -> str:
    run = data.get('_run', {})
    summary = data.get('summary', {})
    
    phase = run.get('phase', 'unknown')
    timestamp = run.get('timestamp', '')
    date = timestamp[:10] if timestamp else datetime.now().strftime('%Y-%m-%d')
    git_commit = run.get('git_commit', '')[:7] if run.get('git_commit') else ''
    
    fm = f"""---
type: eval
phase: {phase}
date: {date}
git_commit: {git_commit}
total_scripts_checked: {summary.get('total_scripts_checked', 0)}
total_violations: {summary.get('total_violations', 0)}
---

# {phase.replace('-', ' ').title()} — {date}

**Run:** `{git_commit}`  
**Violations:** {summary.get('total_violations', 0)}
"""
    
    return _write_md(json_path, fm, output_dir)


def _convert_framework_to_md(json_path: str, data: dict, output_dir: str = None) -> str:
    framework = data.get('framework_name', 'Unknown')
    task_id = data.get('task_id', '')
    date = data.get('created_at', '')[:10]
    objective = data.get('objective', '')
    
    fm = f"""---
type: validation-framework
framework_name: {framework}
task_id: {task_id}
date: {date}
---

# {framework}

**Task ID:** {task_id}  
**Created:** {date}

## Objective

{objective}
"""
    
    # Add baseline observations
    baseline = data.get('baseline_observations', {})
    if baseline:
        fm += "\n## Baseline Observations\n\n"
        for key, val in baseline.items():
            if isinstance(val, dict):
                fm += f"### {key}\n\n"
                for k, v in val.items():
                    fm += f"- **{k}:** {v}\n"
            else:
                fm += f"- **{key}:** {val}\n"
    
    return _write_md(json_path, fm, output_dir)


def _write_md(json_path: str, content: str, output_dir: str = None) -> str:
    name = Path(json_path).stem
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(output_dir) / f"{name}.md"
    else:
        out_path = Path(json_path).with_suffix('.md')
    
    with open(out_path, 'w') as f:
        f.write(content)
    
    print(f"[convert] {json_path} -> {out_path.name}")
    return str(out_path)


# ---------------------------------------------------------------------------
# Intent Router
# ---------------------------------------------------------------------------

def detect_intent(frontmatter: dict, content: str) -> str:
    """Detect which intent folder a document belongs to."""
    # Check explicit intent_mode in frontmatter
    if 'intent_mode' in frontmatter:
        return frontmatter['intent_mode']
    
    # Check type
    doc_type = frontmatter.get('type', '')
    
    if doc_type in ['eval', 'test-result', 'validation-framework']:
        return 'analyze'
    if doc_type in ['review', 'annotation']:
        return 'review'
    if doc_type in ['publication', 'roundup', 'paper']:
        return 'finalize'
    if doc_type in ['index', 'quickstart', 'onboarding']:
        return 'learn-explore'
    
    # Content-based detection
    content_lower = content.lower()
    if any(k in content_lower for k in ['metrics', 'eval', 'measurement', 'analysis', 'data']):
        return 'analyze'
    if any(k in content_lower for k in ['review', 'quality', 'annotation', 'governance']):
        return 'review'
    if any(k in content_lower for k in ['publication', 'paper', 'final', 'publish']):
        return 'finalize'
    
    return 'learn-explore'  # default


def route_to_intent(doc_path: Path, intent: str) -> bool:
    """Create symlink in intent folder pointing to document."""
    if intent not in INTENT_FOLDERS:
        print(f"[route] unknown intent: {intent}")
        return False
    
    intent_folder = INTENT_FOLDERS[intent]
    intent_folder.mkdir(parents=True, exist_ok=True)
    
    # Create symlink
    link_path = intent_folder / doc_path.name
    
    try:
        if link_path.exists() or link_path.is_symlink():
            link_path.unlink()
        os.symlink(doc_path.resolve(), link_path)
        print(f"[route] {doc_path.name} -> {intent}/")
        return True
    except Exception as e:
        print(f"[route] ERROR: {e}")
        return False


def scan_and_route() -> int:
    """Scan vault and route documents to intent folders."""
    routed = 0
    
    # Scan publications
    for md_file in PUBLICATIONS.rglob("*.md"):
        if md_file.is_symlink():
            continue
        
        try:
            # Parse frontmatter
            content = md_file.read_text()
            fm = _parse_frontmatter(content)
            intent = detect_intent(fm, content)
            route_to_intent(md_file, intent)
            routed += 1
        except Exception as e:
            print(f"[route] skipped {md_file.name}: {e}")
    
    return routed


def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown."""
    fm = {}
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            # Simple key: value parser
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip()
    
    return fm


# ---------------------------------------------------------------------------
# Crystallizer Index
# ---------------------------------------------------------------------------

def update_crystallizer_index() -> Optional[Path]:
    """Update the crystallizer's master index."""
    crystallized_files = []
    
    if CRYSTALLIZED.exists():
        for f in CRYSTALLIZED.rglob("*.md"):
            if not f.is_symlink():
                crystallized_files.append(f.relative_to(VAULT_ROOT))
    
    index_path = CRYSTALLIZED / "INDEX.md"
    
    content = f"""---
type: index
status: active
updated: {datetime.now().isoformat()}
---

# Crystallized — Canonical Vault Outputs

**Files:** {len(crystallized_files)}

| File | Modified |
|------|-----------|
"""
    
    for f in sorted(crystallized_files)[:20]:
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
        content += f"| [[{f}]] | {mtime} |\n"
    
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(content)
    
    print(f"[crystallizer] index updated: {index_path}")
    return index_path


# ---------------------------------------------------------------------------
# Plugin Config Validator
# ---------------------------------------------------------------------------

ESSENTIAL_PLUGINS = {
    "dataview",
    "quickadd",
    "blueprint", 
    "breadcrumbs",
    "obsidian-excalidraw-plugin",
    "juggl",
    "obsidian-linter",
}


def validate_plugins() -> dict:
    """Validate plugin configuration."""
    plugins_json = VAULT_ROOT / ".obsidian/community-plugins.json"
    
    try:
        with open(plugins_json) as f:
            plugins = json.load(f)
    except Exception as e:
        return {"error": str(e)}
    
    enabled = set(plugins)
    missing = ESSENTIAL_PLUGINS - enabled
    extra = enabled - ESSENTIAL_PLUGINS
    
    return {
        "enabled": len(enabled),
        "essential": len(ESSENTIAL_PLUGINS),
        "missing": list(missing),
        "extra": list(extra),
        "status": "OK" if not missing else "MISSING_PLUGINS",
    }


# ---------------------------------------------------------------------------
# Health Report
# ---------------------------------------------------------------------------

def generate_health_report() -> dict:
    """Generate vault health report."""
    md_count = sum(1 for _ in VAULT_ROOT.rglob("*.md"))
    json_count = sum(1 for _ in VAULT_ROOT.rglob("*.json"))
    intent_docs = {}
    
    for intent, folder in INTENT_FOLDERS.items():
        if folder.exists():
            intent_docs[intent] = len(list(folder.rglob("*.md")))
    
    plugins = validate_plugins()
    
    return {
        "md_files": md_count,
        "json_files": json_count,
        "intent_docs": intent_docs,
        "plugins": plugins,
    }


# ---------------------------------------------------------------------------
# External Repo Sync (from faerie2 repo)
# ---------------------------------------------------------------------------

def sync_external_daily() -> int:
    """Sync daily outputs from external faerie2 repo."""
    if not EXTERNAL_REPO or not EXTERNAL_REPO.exists():
        print(f"[sync-external] FAERIE_REPO not set or not accessible")
        return 0
    
    daily_src = EXTERNAL_REPO / "daily"
    if not daily_src.exists():
        print(f"[sync-external] no daily folder in external repo")
        return 0
    
    synced = 0
    for date_dir in sorted(daily_src.iterdir(), reverse=True)[:7]:  # Last 7 days
        if date_dir.is_dir():
            dest = DAILY / date_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            
            for src_file in date_dir.glob("*.md"):
                dest_file = dest / src_file.name
                if not dest_file.exists():
                    src_file.copy(dest_file)
                    synced += 1
    
    print(f"[sync-external] synced {synced} daily files")
    return synced


def sync_external_honey() -> int:
    """Sync honey renders from external repo."""
    if not EXTERNAL_REPO or not EXTERNAL_REPO.exists():
        return 0
    
    honey_src = EXTERNAL_REPO / "honey-renders"
    if not honey_src.exists():
        return 0
    
    # Simple copy of latest honey
    synced = 0
    for audience_dir in honey_src.iterdir():
        if audience_dir.is_dir():
            dest = VAULT_ROOT / "00-SHARED/HIVE/honey-renders" / audience_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            
            for src_file in audience_dir.glob("*.md"):
                dest_file = dest / src_file.name
                if not dest_file.exists():
                    src_file.copy(dest_file)
                    synced += 1
    
    print(f"[sync-external] synced {synced} honey files")
    return synced


def sync_external_forensics() -> int:
    """Sync forensics bundle metadata."""
    if not EXTERNAL_REPO or not EXTERNAL_REPO.exists():
        return 0
    
    forensics_src = EXTERNAL_REPO / "forensics"
    if not forensics_src.exists():
        return 0
    
    # Copy manifests (metadata only, not full artifacts)
    synced = 0
    for date_dir in sorted(forensics_src.iterdir(), reverse=True)[:3]:  # Last 3 dates
        if date_dir.is_dir():
            manifests_src = date_dir / "manifests"
            if manifests_src.exists():
                dest = PUBLICATIONS / date_dir.name / "manifests"
                dest.mkdir(parents=True, exist_ok=True)
                
                for src_file in manifests_src.glob("*.json"):
                    dest_file = dest / src_file.name
                    if not dest_file.exists():
                        src_file.copy(dest_file)
                        synced += 1
    
    print(f"[sync-external] synced {synced} forensics manifests")
    return synced


def sync_external() -> int:
    """Sync all from external faerie2 repo."""
    if not EXTERNAL_REPO:
        print("[sync-external] FAERIE_REPO not set - skipping external sync")
        print("[sync-external] Set FAERIE_REPO=/path/to/faerie2 to enable")
        return 0
    
    print(f"[sync-external] Using external repo: {EXTERNAL_REPO}")
    
    if not EXTERNAL_REPO.exists():
        print(f"[sync-external] ERROR: {EXTERNAL_REPO} does not exist")
        return 0
    
    total = 0
    total += sync_external_daily()
    total += sync_external_honey()
    total += sync_external_forensics()
    
    print(f"[sync-external] Total synced: {total}")
    return total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Full Obsidian Vault Sync")
    parser.add_argument("--scan", action="store_true", help="Scan and route docs to intents")
    parser.add_argument("--convert-json", action="store_true", help="Convert JSON files to markdown")
    parser.add_argument("--crystallizer", action="store_true", help="Update crystallizer index")
    parser.add_argument("--validate-plugins", action="store_true", help="Validate plugin config")
    parser.add_argument("--sync-external", action="store_true", help="Sync from external faerie2 repo")
    parser.add_argument("--health", action="store_true", help="Show health report")
    parser.add_argument("--all", action="store_true", help="Run all sync tasks")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return 0
    
    if args.all or args.convert_json:
        print("[sync] Converting JSON files...")
        for json_file in PUBLICATIONS.rglob("*.json"):
            try:
                convert_json_to_md(str(json_file))
            except Exception as e:
                print(f"[sync] ERROR converting {json_file}: {e}")
    
    if args.all or args.scan:
        print("[sync] Routing documents to intents...")
        scan_and_route()
    
    if args.all or args.crystallizer:
        update_crystallizer_index()
    
    if args.all or args.validate_plugins:
        result = validate_plugins()
        print(f"[sync] Plugins: {result}")
    
    if args.all or args.sync_external:
        sync_external()
    
    if args.all or args.health:
        report = generate_health_report()
        print(f"[sync] Health: {report}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())