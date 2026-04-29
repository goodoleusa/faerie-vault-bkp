#!/usr/bin/env python3
"""
/spawn direct invoker — assemble bundle and return Agent() invocation params.

This script is called by the model (main context is the harness).
Returns structured dict that the model parses to invoke Agent() directly.

Usage:
  python3 spawn-direct.py <semantic_intent> [--wave 1|2|3] [--investigation-label LABEL] ...

Output:
  JSON dict with keys: subagent_type, prompt, model, run_in_background, investigation_label, team_size

Model then calls: Agent(subagent_type=..., prompt=..., run_in_background=...)
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
import subprocess

# Wave config (matches run.py)
WAVE_CONFIG = {
    "1": {"name": "LIFTOFF", "max_parallel": 6, "model": "haiku", "background": False},
    "2": {"name": "CRUISE", "max_parallel": 4, "model": "haiku", "background": False},
    "3": {"name": "INSERTION", "max_parallel": 1, "model": "sonnet", "background": True}
}

TEAMS = {
    "analysis": ["data-analyst", "research-analyst", "code-reviewer", "knowledge-synthesizer"],
    "synthesis": ["documentation-engineer", "knowledge-synthesizer", "research-analyst", "data-analyst"],
    "implementation": ["fullstack-developer", "python-pro", "code-reviewer", "ai-engineer"],
    "audit": ["security-auditor", "code-reviewer", "data-analyst", "knowledge-synthesizer"],
}

def read_formulas():
    """Read faerie2-formulas.json for context checks."""
    path = Path("/mnt/d/0local/.claude/faerie2-formulas.json")
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def read_altimeter():
    """Read altimeter.json for context percentage."""
    path = Path("/mnt/d/0local/.claude/altimeter.json")
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {"context_pct": 50}

def check_context_warnings(formulas, altimeter):
    """Check context fill and warn if approaching limits. Does NOT gate spawning."""
    try:
        pct = float(altimeter.get("context_pct", 50))
        red_alert = float(formulas.get("IMMUTABLE_CONSTANTS", {}).get("AUTO_COMPACT_PCT_THRESHOLD", {}).get("value", 93.5))

        if pct >= red_alert:
            return f"RED ALERT: {pct}% context >= {red_alert}% (compact imminent)"
        elif pct >= 85:
            return f"CAUTION: {pct}% context is high. Consider compacting after this wave."
        return None
    except:
        return None

def select_team(intent, custom=None):
    """Auto-select team based on semantic intent."""
    if custom:
        return custom.split(",")
    intent_lower = intent.lower()
    if any(w in intent_lower for w in ["audit", "review", "check", "security"]):
        return TEAMS["audit"]
    elif any(w in intent_lower for w in ["build", "implement", "code", "develop"]):
        return TEAMS["implementation"]
    elif any(w in intent_lower for w in ["summarize", "synthesize", "report", "document"]):
        return TEAMS["synthesis"]
    else:
        return TEAMS["analysis"]

def read_bundle(label):
    """Assemble context bundle for agents."""
    parts = []

    # Global HONEY
    honey = Path("/mnt/d/0LOCAL/.claude/HONEY.md")
    if honey.exists():
        with open(honey) as f:
            parts.append(f"# Global Principles\n\n{f.read()[:1000]}\n")

    # NECTAR tail-50
    nectar = Path("/mnt/d/0LOCAL/.claude/NECTAR.md")
    if nectar.exists():
        with open(nectar) as f:
            lines = f.readlines()
            parts.append(f"# Recent Findings (NECTAR tail-50)\n\n{''.join(lines[-50:])}\n")

    # Bundle template
    template = Path("/mnt/d/0local/gitrepos/faerie2/.claude/scripts/0x_spawn_bundle_template.md")
    if template.exists():
        with open(template) as f:
            parts.append(f"# Bundle Structure (Self-Describing)\n\n{f.read()[:2000]}\n")

    # Investigation label hint
    if label != "default":
        parts.append(f"\n**Investigation Label:** {label}\n")
        parts.append("Read forensics/manifests/ to discover work. Agents coordinate via compass edges.\n")

    return "\n".join(parts)

def build_prompt(agent_type, bundle, wave, label, semantic_intent, wave_name):
    """Build agent-specific prompt with context."""
    return f"""{bundle}

---

# Task Assignment

**Agent:** {agent_type}
**Wave:** {wave} ({wave_name})
**Investigation:** {label}
**Intent:** {semantic_intent}

Navigate via investigation_label + frontier scan.
Write manifest to: forensics/manifests/{{YYYY-MM-DD}}/{{HH-MM-SS}}Z_manifest_{{investigation}}_{{agent}}.json
"""

def main():
    parser = argparse.ArgumentParser(
        description="Assemble spawn bundle and return Agent() invocation params."
    )
    parser.add_argument("semantic_intent", nargs="?", default="Analyze and improve system efficiency")
    parser.add_argument("--investigation-label", default=None)
    parser.add_argument("--wave", choices=["1", "2", "3"], default="1")
    parser.add_argument("--run-background", action="store_true")
    parser.add_argument("--team", default=None)
    parser.add_argument("--model-override", default=None)
    args = parser.parse_args()

    # Check context warnings (non-blocking, informational only)
    formulas = read_formulas()
    altimeter = read_altimeter()
    warning = check_context_warnings(formulas, altimeter)

    # Generate investigation label if not provided
    if not args.investigation_label:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        args.investigation_label = f"spawn-{ts}"

    # Select team
    team = select_team(args.semantic_intent, args.team)

    # Get wave config
    wave_config = WAVE_CONFIG[args.wave]
    model = args.model_override or wave_config["model"]
    background = args.run_background or wave_config["background"]

    # Read context bundle once, reuse for all agents
    bundle = read_bundle(args.investigation_label)

    # Build spawn directives for all agents in team
    directives = []
    for idx, agent_type in enumerate(team):
        prompt = build_prompt(
            agent_type,
            bundle,
            args.wave,
            args.investigation_label,
            args.semantic_intent,
            wave_config["name"]
        )

        directive = {
            "agent_idx": idx + 1,
            "team_size": len(team),
            "subagent_type": agent_type,
            "prompt": prompt,
            "model": model,
            "run_in_background": background,
            "investigation_label": args.investigation_label,
            "wave": args.wave,
            "wave_name": wave_config["name"]
        }
        directives.append(directive)

    # Output summary and directives as JSON lines
    # Model will parse these and invoke Agent() for each
    if warning:
        print(f"# CONTEXT WARNING: {warning}")

    print(f"# /spawn summary:")
    print(f"# Intent: {args.semantic_intent}")
    print(f"# Team: {', '.join(team)} ({len(team)} agents)")
    print(f"# Wave: {args.wave} ({wave_config['name']})")
    print(f"# Label: {args.investigation_label}")
    print(f"# Model: {model}, Background: {background}")
    print()

    # Output directives as JSON lines for model to parse
    for directive in directives:
        print(json.dumps(directive))

if __name__ == "__main__":
    main()
