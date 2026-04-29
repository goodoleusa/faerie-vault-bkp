#!/usr/bin/env python3
"""
/spawn — Stigmergic Agent Spawner (Flywheel Orchestrator)

Direct invocation for multi-wave parallel agent spawning with zero dispatcher overhead.
Agents discover work via manifest chaining (investigation_label + compass edges).

Usage:
  /spawn <agent_type> <task_description> [--wave 1|2|3] [--run-background] [--investigation-label LABEL] [--model haiku|sonnet|opus]

Examples:
  /spawn data-analyst "Analyze token ledger" --investigation-label force-multiplier-index-44.4-breakdown
  /spawn documentation-engineer "Synthesize all outputs" --wave 3 --run-background --investigation-label ffmx
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import re
import time

# Import prescan cache service
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from prescan_cache import prescan_check_cached
except ImportError:
    # Fallback if cache not available
    def prescan_check_cached(*args, **kwargs):
        return False  # Cache unavailable, allow all spawns

# Agent types that can be spawned
AGENT_TYPES = [
    "data-analyst", "research-analyst", "ai-engineer", "documentation-engineer",
    "fullstack-developer", "python-pro", "code-reviewer", "knowledge-synthesizer",
    "security-auditor", "frontend-design", "data-engineer", "data-scientist",
    "evidence-curator", "stigmergy-scout"
]

# Wave parameters: W1=cheap haiku parallel, W2=selective haiku, W3=deep sonnet async
WAVE_CONFIG = {
    "1": {"name": "LIFTOFF", "max_parallel": 6, "model": "haiku", "inline": True},
    "2": {"name": "CRUISE", "max_parallel": 4, "model": "haiku", "inline": True},
    "3": {"name": "INSERTION", "max_parallel": 3, "model": "sonnet", "inline": False}
}

# Default team templates (auto-selected based on semantic intent)
DEFAULT_TEAMS = {
    "analysis": ["data-analyst", "research-analyst", "code-reviewer", "knowledge-synthesizer"],
    "synthesis": ["documentation-engineer", "knowledge-synthesizer", "research-analyst", "data-analyst"],
    "implementation": ["fullstack-developer", "python-pro", "code-reviewer", "ai-engineer"],
    "audit": ["security-auditor", "code-reviewer", "data-analyst", "knowledge-synthesizer"],
}

def read_formulas():
    """Read faerie2-formulas.json for context gating thresholds."""
    formulas_path = Path("/mnt/d/0local/.claude/faerie2-formulas.json")
    if formulas_path.exists():
        try:
            with open(formulas_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None

def read_altimeter():
    """Read altimeter.json for current context % fill."""
    altimeter_path = Path("/mnt/d/0local/.claude/altimeter.json")
    if altimeter_path.exists():
        try:
            with open(altimeter_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None

def auto_determine_wave(formulas, altimeter):
    """
    Auto-determine wave based on context % and formulas.
    W1: context < WAVE_1_SPAWN_MAX_CONTEXT_PCT
    W2: WAVE_1_SPAWN_MAX_CONTEXT_PCT <= context < WAVE_2_SPAWN_MAX_CONTEXT_PCT
    W3: WAVE_2_SPAWN_MAX_CONTEXT_PCT <= context < WAVE_3_SPAWN_MAX_CONTEXT_PCT
    ERROR: context >= WAVE_3_SPAWN_MAX_CONTEXT_PCT (compact imminent)
    """
    if not formulas or not altimeter:
        return "1", None  # Default to W1 if can't read

    try:
        context_pct = float(altimeter.get("context_pct", 50))
        w1_max = float(formulas.get("WAVE_1_SPAWN_MAX_CONTEXT_PCT", 70))
        w2_max = float(formulas.get("WAVE_2_SPAWN_MAX_CONTEXT_PCT", 80))
        w3_max = float(formulas.get("WAVE_3_SPAWN_MAX_CONTEXT_PCT", 87))

        if context_pct >= w3_max:
            return None, f"🔴 CONTEXT RED ALERT: {context_pct}% >= {w3_max}% (compact imminent). Do not spawn."
        elif context_pct >= w2_max:
            return "3", f"W3 INSERTION (context {context_pct}% in high zone)"
        elif context_pct >= w1_max:
            return "2", f"W2 CRUISE (context {context_pct}% in medium zone)"
        else:
            return "1", f"W1 LIFTOFF (context {context_pct}% in low zone)"
    except (ValueError, TypeError):
        return "1", None

def parse_args():
    parser = argparse.ArgumentParser(
        description="Stigmergic agent spawner — semantic intent → auto-team spawning",
        add_help=True
    )
    parser.add_argument("semantic_intent", nargs="?", default=None, help="High-level task intent (e.g., 'Analyze FFMx formula and generate comprehensive report')")
    parser.add_argument("--investigation-label", default="spawn-auto", help="Mission cluster label (auto-generated if not provided)")
    parser.add_argument("--wave", choices=["1", "2", "3"], default=None, help="Wave override: 1=LIFTOFF, 2=CRUISE, 3=INSERTION (auto-determined if not provided)")
    parser.add_argument("--run-background", action="store_true", help="W3 background mode")
    parser.add_argument("--team", help="Comma-separated agent types (default: auto-selected 4-agent team)")
    parser.add_argument("--model", choices=["haiku", "sonnet"], help="Model override (haiku default, sonnet for deep synthesis)")

    args = parser.parse_args()

    # Assume intent if not provided
    if not args.semantic_intent:
        args.semantic_intent = "Implement priority velocity improvements: prescan cache, bundle compression"

    # Auto-determine wave from context % if not provided
    if not args.wave:
        formulas = read_formulas()
        altimeter = read_altimeter()
        auto_wave, alert = auto_determine_wave(formulas, altimeter)
        if not auto_wave:
            print(f"❌ {alert}")
            sys.exit(1)
        if alert:
            print(f"ℹ️  {alert}")
        args.wave = auto_wave
    else:
        # User provided wave; check if it violates context gates
        formulas = read_formulas()
        altimeter = read_altimeter()
        if formulas and altimeter:
            try:
                context_pct = float(altimeter.get("context_pct", 50))
                w1_max = float(formulas.get("WAVE_1_SPAWN_MAX_CONTEXT_PCT", 70))
                w3_max = float(formulas.get("WAVE_3_SPAWN_MAX_CONTEXT_PCT", 87))

                if args.wave == "1" and context_pct >= w1_max:
                    print(f"⚠️  Context {context_pct}% exceeds W1 max {w1_max}%. Forcing W2 CRUISE.")
                    args.wave = "2"
                if context_pct >= w3_max:
                    print(f"🔴 Context {context_pct}% exceeds W3 max {w3_max}%. Compact imminent. Aborting spawn.")
                    sys.exit(1)
            except (ValueError, TypeError):
                pass

    return args

def read_context_bundle(investigation_label):
    """
    Assemble context bundle: HONEY + NECTAR + pollen + investigation hints.
    Returns bundle text for injection into agent prompt.
    """
    vault_path = Path("/mnt/d/0local/gitrepos/faerie-vault")

    bundle_parts = []

    # 1. Global HONEY
    honey_global = Path("/mnt/d/0LOCAL/.claude/HONEY.md")
    if honey_global.exists():
        with open(honey_global, 'r') as f:
            honey_text = f.read()[:800]  # Cap at 800 tokens
            bundle_parts.append(f"# Global Principles (HONEY)\n\n{honey_text}\n")

    # 2. Project HONEY
    honey_project = vault_path / ".claude" / "HONEY.md"
    if honey_project.exists():
        with open(honey_project, 'r') as f:
            honey_text = f.read()[:800]
            bundle_parts.append(f"# Project Principles (faerie-vault HONEY)\n\n{honey_text}\n")

    # 3. NECTAR tail-50 lines
    nectar_file = Path("/mnt/d/0LOCAL/.claude/NECTAR.md")
    if nectar_file.exists():
        with open(nectar_file, 'r') as f:
            lines = f.readlines()
            tail_lines = lines[-50:] if len(lines) > 50 else lines
            nectar_text = ''.join(tail_lines)
            bundle_parts.append(f"# Recent HIGH Findings (NECTAR tail-50)\n\n{nectar_text}\n")

    # 4. Investigation label discovery hints
    if investigation_label != "default":
        bundle_parts.append(f"\n# Investigation Context\n\nMission cluster: **{investigation_label}**\n")
        bundle_parts.append("Read manifests from forensics/{YYYY-MM-DD}/ with matching investigation_label.\n")
        bundle_parts.append("Agents in this cluster coordinate via manifest chaining (no SendMessage).\n")

    return "\n".join(bundle_parts)

def prescan_check(investigation_label, agent_type):
    """
    Check: has similar work been done in past 24h?
    Prevents duplicate spawning. Uses cache for 10× speedup.
    """
    vault_path = Path("/mnt/d/0local/gitrepos/faerie-vault")
    artifacts_dir = vault_path / "forensics" / "artifacts"

    if not artifacts_dir.exists():
        return True  # Pass if no artifacts yet

    # Use cached prescan check if available; fall back to linear scan if cache unavailable
    try:
        # Glob for matching artifacts; check each with cache for ~10× speedup
        for artifact in artifacts_dir.rglob(f"*{agent_type}*.md"):
            is_fresh = prescan_check_cached(artifact, investigation_label, agent_type, max_age_seconds=86400)
            if is_fresh:
                return False  # Fresh artifact found; skip spawn (work was done recently)
        return True  # No fresh artifacts found; prescan passed, proceed with spawn
    except (NameError, AttributeError, Exception):
        # Cache unavailable; fall back to linear stat-based scan
        import time
        now = time.time()
        cutoff = now - (24 * 3600)
        for artifact in artifacts_dir.rglob(f"*{agent_type}*.md"):
            if artifact.stat().st_mtime > cutoff:
                return False  # Artifact exists, modified <24h
        return True  # Prescan passed

def output_manifest(investigation_label, agent_type, task_description, wave):
    """
    Write manifest signal for this spawn.
    """
    vault_path = Path("/mnt/d/0local/gitrepos/faerie-vault")
    manifests_dir = vault_path / "forensics" / "manifests" / datetime.now().strftime("%Y-%m-%d")
    manifests_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%H-%M-%SZ")
    manifest_file = manifests_dir / f"{now}_manifest_task-spawn_{agent_type}_001.json"

    manifest = {
        "task_id": f"spawn-{investigation_label}",
        "agent_type": agent_type,
        "investigation_label": investigation_label,
        "wave": wave,
        "task_description": task_description,
        "timestamp": datetime.now().isoformat(),
        "compass_edge": "S",
        "next_task_queued": f"agent-execution-{agent_type}",
        "prescan_decision": "passed"
    }

    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    return manifest_file

def spawn_agents(agent_type, task_description, wave, investigation_label, model, run_background, spawn_requests):
    """
    Assemble spawn request (bundle + manifest) for execution.
    Collects agents into list; actual invocation happens in main().
    """
    # Assemble bundle
    bundle = read_context_bundle(investigation_label)

    # Check prescan
    if not prescan_check(investigation_label, agent_type):
        print(f"⛔ Prescan: artifact exists (<24h old) for {agent_type} on {investigation_label}. Skip spawn.")
        return

    # Write manifest signal
    manifest_file = output_manifest(investigation_label, agent_type, task_description, wave)
    print(f"📋 Manifest: {manifest_file}")

    # Determine model if not overridden
    if not model:
        model = WAVE_CONFIG[wave]["model"]

    # Build prompt with bundle context
    now = datetime.now().strftime("%H-%M-%SZ")
    prompt = f"""{bundle}

---

# Task Assignment

**Wave:** {wave} ({WAVE_CONFIG[wave]['name']})
**Investigation label:** {investigation_label}
**Task:** {task_description}

Navigate via manifest chaining: read forensics/manifests/ for work discovery within this investigation_label.
Write manifest outcome to: forensics/manifests/{datetime.now().strftime('%Y-%m-%d')}/{now}_manifest_task-{investigation_label}_*.json
"""

    # Spawn status
    print(f"🚀 Spawning: {agent_type} (Wave {wave}/{WAVE_CONFIG[wave]['name']}, model={model})")

    # Determine run mode
    run_background_flag = run_background or (WAVE_CONFIG[wave]["inline"] is False)

    # Add to spawn requests list for execution
    spawn_requests.append({
        "agent_type": agent_type,
        "prompt": prompt,
        "model": model,
        "run_background": run_background_flag,
        "investigation_label": investigation_label,
    })

def select_team(semantic_intent, custom_team=None):
    """Auto-select a complementary agent team based on semantic intent."""
    if custom_team:
        return custom_team.split(",")

    # Simple keyword-based routing to team templates
    intent_lower = semantic_intent.lower()
    if any(w in intent_lower for w in ["audit", "review", "check", "security", "vulnerability"]):
        return DEFAULT_TEAMS["audit"]
    elif any(w in intent_lower for w in ["build", "implement", "code", "develop", "feature"]):
        return DEFAULT_TEAMS["implementation"]
    elif any(w in intent_lower for w in ["summarize", "synthesize", "report", "document", "narrative"]):
        return DEFAULT_TEAMS["synthesis"]
    else:
        return DEFAULT_TEAMS["analysis"]  # default: analysis

def generate_role_prompt(agent_type, semantic_intent, investigation_label, bundle_prefix):
    """Generate a role-specific prompt for each agent."""
    role_hints = {
        "data-analyst": "Your role: Extract and analyze data. Compute metrics, identify patterns, produce dashboards.",
        "research-analyst": "Your role: Research and literature synthesis. Find sources, validate hypotheses, cross-correlate findings.",
        "code-reviewer": "Your role: Code quality and architecture review. Assess design, security, maintainability.",
        "knowledge-synthesizer": "Your role: Cross-domain integration. Connect findings from other agents, synthesize patterns.",
        "documentation-engineer": "Your role: Narrative synthesis and publication. Produce clear, well-structured reports.",
        "fullstack-developer": "Your role: System design and implementation. Build end-to-end solutions.",
        "python-pro": "Your role: Production Python code. Write type-safe, high-quality implementations.",
        "ai-engineer": "Your role: AI/ML systems and optimization. Improve prompts, model selection, inference.",
        "security-auditor": "Your role: Forensic security analysis. Identify vulnerabilities, assess compliance.",
        "frontend-design": "Your role: UI/UX and design. Create polished, intuitive interfaces.",
    }

    role_text = role_hints.get(agent_type, "Your role: Contribute your expertise to the team effort.")

    return f"""{bundle_prefix}

---

# Task Assignment

**Semantic Intent:** {semantic_intent}
**Investigation Label:** {investigation_label}
**Agent Type:** {agent_type}

{role_text}

You are part of a 4-agent team working in parallel on this investigation. Coordinate via manifest chaining (investigation_label clusters in forensics/). Read forensics/manifests/ to discover parallel work and blockers.

Write your manifest outcome to: forensics/manifests/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H-%M-%S')}Z_manifest_task-{investigation_label}_*.json
"""

def main():
    args = parse_args()

    # Validate wave
    if args.wave not in WAVE_CONFIG:
        print(f"❌ Invalid wave: {args.wave}")
        sys.exit(1)

    # Auto-select team
    team = select_team(args.semantic_intent, args.team)
    print(f"🎯 Semantic Intent: {args.semantic_intent}")
    print(f"👥 Team: {', '.join(team)}")
    print(f"🌊 Wave: {args.wave} ({WAVE_CONFIG[args.wave]['name']})")

    # Generate investigation label if not provided
    if args.investigation_label == "spawn-auto":
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        args.investigation_label = f"spawn-{ts}"

    # Collect spawn requests
    spawn_requests = []
    print(f"\n📋 Assembling {len(team)} agents...")
    for agent_type in team:
        spawn_agents(
            agent_type=agent_type,
            task_description=args.semantic_intent,
            wave=args.wave,
            investigation_label=args.investigation_label,
            model=args.model,
            run_background=args.run_background,
            spawn_requests=spawn_requests
        )

    # Output spawn requests as machine-readable JSON for skill harness
    spawn_output = {
        "investigation_label": args.investigation_label,
        "wave": args.wave,
        "semantic_intent": args.semantic_intent,
        "requests": spawn_requests
    }
    # Print as single-line JSON for reliable parsing by skill harness
    print(json.dumps(spawn_output))

if __name__ == "__main__":
    main()
