#!/usr/bin/env python3
"""
7x_formula_gates.py — Formula-driven spawn gates (terminology-cleanup-sprint W2)

TIER: 7x_
REPLACES: ad-hoc inference-based spawn decisions in run.py
METRIC: formula_driven_spawn_decisions (target: 60% -> 80% formula-driven)
LOAD: sauce

Implements four formula gaps identified in audit-formulas-w1.5 manifest:

  Gap 1 (wire-gap-1-w2-spawn):
    FFMx threshold gate for W2 spawn. Block W2 if forecast_ffmx < 0.8x baseline.
    LOC: ~15. ROI: 15% context savings (prevents low-value spawns).

  Gap 2 (wire-gap-2-agent-selection):
    Agent score formula: composite = belief_index*0.4 + quality_score*0.3 + routing_weight*0.3
    LOC: ~25. ROI: 25% fit improvement over keyword-only routing.

  Gap 3 (wire-gap-3-context-budget):
    Context budget for spawn wave: tokens_available / agents_planned >= per_agent_floor.
    LOC: ~15. ROI: 5% efficiency gain (prevents over-spawning on thin budgets).

  Gap 5 (wire-gap-5-w3-abort):
    W3 abort logic: block W3 if session FFMx < 0.8 x session_baseline.
    LOC: ~12. ROI: 8% token savings (aborts deep synthesis on weak sessions).

Usage:
  python3 7x_formula_gates.py --gate w2-spawn \
    --manifests-dir forensics/manifests/2026-04-28 \
    --investigation-label terminology-cleanup-sprint \
    --baseline-path forensics/mutation-baselines/ffmx-T0-baseline-2026-04-28.json

  python3 7x_formula_gates.py --gate agent-score \
    --task-keywords "python implementation wiring" \
    --agent-manifests '[{"agent_id":"python-pro","belief_index":0.9,"quality_score":0.85,"routing_weight":0.9}]'

  python3 7x_formula_gates.py --gate context-budget \
    --tokens-remaining 80000 --agents-planned 4 --wave 2

  python3 7x_formula_gates.py --gate w3-abort \
    --manifests-dir forensics/manifests/2026-04-28 \
    --investigation-label terminology-cleanup-sprint \
    --baseline-path forensics/mutation-baselines/ffmx-T0-baseline-2026-04-28.json

  python3 7x_formula_gates.py --gate all \
    --manifests-dir forensics/manifests/2026-04-28 \
    --investigation-label terminology-cleanup-sprint \
    --tokens-remaining 80000 --agents-planned 3 --wave 2 \
    --baseline-path forensics/mutation-baselines/ffmx-T0-baseline-2026-04-28.json

Output (all gates): JSON with gate verdicts + reasons.
Exit code: 0 = all pass, 1 = any gate blocked/abort, 2 = error.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------

# Gap 1 / Gap 5: FFMx threshold ratios
FFMx_W2_THRESHOLD_RATIO: float = 0.80   # Block W2 if forecast FFMx < 0.80 x baseline
FFMx_W3_ABORT_RATIO: float = 0.80       # Abort W3 if session FFMx < 0.80 x baseline

# Gap 2: Agent composite score weights
AGENT_SCORE_WEIGHTS: dict[str, float] = {
    "belief_index": 0.40,    # Honesty first: do manifests match outcomes?
    "quality_score": 0.30,   # Output quality second
    "routing_weight": 0.30,  # Trust/reputation third
}

# Gap 3: Context budget floors per wave
CONTEXT_FLOOR_PER_AGENT: dict[str, int] = {
    "1":  8_000,   # W1 LIFTOFF: haiku, cheap, 8K floor
    "2": 12_000,   # W2 CRUISE: sonnet, 12K floor
    "3": 20_000,   # W3 INSERTION: sonnet deep synthesis, 20K floor
}

# Minimum context safety buffer (always reserved before compact)
SAFETY_BUFFER: int = 10_000

# -------------------------------------------------------------------------
# Shared: manifest loader
# -------------------------------------------------------------------------

def load_manifests(manifests_dir: str, investigation_label: str) -> list[dict]:
    """Load manifests matching investigation_label from directory."""
    dir_path = Path(manifests_dir)
    if not dir_path.exists():
        return []
    manifests = []
    for f in sorted(dir_path.glob("*.json")):
        try:
            with open(f) as fh:
                m = json.load(fh)
            if m.get("investigation_label") == investigation_label:
                manifests.append(m)
        except (json.JSONDecodeError, OSError):
            continue
    return manifests


def _load_baseline_ffmx(baseline_path: Optional[str]) -> Optional[float]:
    """Load FFMx baseline value from JSON file. Supports multiple schema variants."""
    if not baseline_path:
        return None
    path = Path(baseline_path)
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        ffmx = (
            data.get("measurements", {}).get("ffmx", {}).get("baseline_ffmx")
            or data.get("ffmx_calculation", {}).get("result")
            or data.get("ffmx_baseline")
            or data.get("baseline_ffmx")
        )
        return float(ffmx) if ffmx is not None else None
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return None


def _compute_session_ffmx(manifests: list[dict]) -> tuple[float, dict]:
    """Compute FFMx from a list of manifests. Returns (ffmx, components)."""
    quality_scores = [float(m["quality_score"]) for m in manifests if "quality_score" in m]
    q = statistics.mean(quality_scores) if quality_scores else 0.5
    a = len(manifests)
    high_belief = [m for m in manifests if float(m.get("belief_index", 0)) > 0.7]
    e = max(1, len(high_belief) // 3 + 1)
    token_sum = sum(
        int(float(m.get("artifact_size_bytes", 0)) * 0.125) if m.get("artifact_size_bytes")
        else 30_800
        for m in manifests
    )
    t = max(1, token_sum)
    ffmx = (a * q * (e ** 1.5)) / t
    components = {
        "A_artifacts": a,
        "Q_quality_avg": round(q, 3),
        "E_emergence_proxy": e,
        "T_tokens_estimated": t,
    }
    return round(ffmx, 4), components


# -------------------------------------------------------------------------
# Gap 1: FFMx W2 Spawn Gate
# -------------------------------------------------------------------------

def gate_w2_spawn(
    manifests_dir: str,
    investigation_label: str,
    baseline_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Gap 1: FFMx threshold gate for W2 spawn.

    Block W2 if forecast_ffmx < 0.80 x baseline. Prevents low-value spawns
    when the sprint is tracking below the force-multiplier threshold.

    Returns dict with gate_name, decision (pass|blocked), reason, forecast_ffmx.
    """
    manifests = load_manifests(manifests_dir, investigation_label)
    baseline_ffmx = _load_baseline_ffmx(baseline_path)

    if not manifests:
        return {
            "gate_name": "w2-spawn-ffmx",
            "gap_id": "wire-gap-1-w2-spawn",
            "decision": "blocked",
            "reason": "No manifests found -- cannot forecast FFMx; block cautiously",
            "forecast_ffmx": 0.0,
            "baseline_ffmx": baseline_ffmx,
            "manifests_analyzed": 0,
            "components": {},
        }

    forecast_ffmx, components = _compute_session_ffmx(manifests)

    if baseline_ffmx is None:
        decision = "pass"
        reason = "No baseline available -- first sprint, gate open"
    elif forecast_ffmx >= baseline_ffmx * FFMx_W2_THRESHOLD_RATIO:
        decision = "pass"
        reason = (
            f"Forecast FFMx {forecast_ffmx:.4f} >= "
            f"{FFMx_W2_THRESHOLD_RATIO:.0%} x baseline {baseline_ffmx:.4f} "
            f"= {baseline_ffmx * FFMx_W2_THRESHOLD_RATIO:.4f} -- W2 gate open"
        )
    else:
        decision = "blocked"
        reason = (
            f"Forecast FFMx {forecast_ffmx:.4f} < "
            f"{FFMx_W2_THRESHOLD_RATIO:.0%} x baseline {baseline_ffmx:.4f} "
            f"= {baseline_ffmx * FFMx_W2_THRESHOLD_RATIO:.4f} -- W2 gate blocked"
        )

    return {
        "gate_name": "w2-spawn-ffmx",
        "gap_id": "wire-gap-1-w2-spawn",
        "decision": decision,
        "reason": reason,
        "forecast_ffmx": forecast_ffmx,
        "baseline_ffmx": baseline_ffmx,
        "threshold_ratio": FFMx_W2_THRESHOLD_RATIO,
        "manifests_analyzed": len(manifests),
        "components": components,
    }


# -------------------------------------------------------------------------
# Gap 5: W3 Abort Gate
# -------------------------------------------------------------------------

def gate_w3_abort(
    manifests_dir: str,
    investigation_label: str,
    baseline_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Gap 5: Abort W3 INSERTION if session FFMx < 0.80 x baseline.

    W3 is deep synthesis (expensive sonnet tokens). If the session is already
    underperforming, W3 will compound the deficit. Abort early and route to
    a lighter W2 re-scoping instead (8% token savings per sprint).

    Returns dict with gate_name, decision (pass|abort), reason, session_ffmx.
    """
    manifests = load_manifests(manifests_dir, investigation_label)
    baseline_ffmx = _load_baseline_ffmx(baseline_path)

    if not manifests:
        return {
            "gate_name": "w3-abort-ffmx",
            "gap_id": "wire-gap-5-w3-abort",
            "decision": "abort",
            "reason": "No manifests for investigation_label -- abort W3; no signal to synthesize",
            "session_ffmx": 0.0,
            "baseline_ffmx": baseline_ffmx,
            "manifests_analyzed": 0,
            "fallback_recommendation": "Spawn W2 re-scoping agent (stigmergy-scout) to reassess mission",
        }

    session_ffmx, _ = _compute_session_ffmx(manifests)

    if baseline_ffmx is None:
        decision = "pass"
        reason = "No baseline -- first sprint; W3 allowed (no deficit possible)"
        fallback = None
    elif session_ffmx >= baseline_ffmx * FFMx_W3_ABORT_RATIO:
        decision = "pass"
        reason = (
            f"Session FFMx {session_ffmx:.4f} >= "
            f"{FFMx_W3_ABORT_RATIO:.0%} x baseline {baseline_ffmx:.4f} -- W3 allowed"
        )
        fallback = None
    else:
        decision = "abort"
        reason = (
            f"Session FFMx {session_ffmx:.4f} < "
            f"{FFMx_W3_ABORT_RATIO:.0%} x baseline {baseline_ffmx:.4f} "
            f"= {baseline_ffmx * FFMx_W3_ABORT_RATIO:.4f} -- W3 aborted; "
            f"route to W2 re-scoping instead (8% token savings)"
        )
        fallback = "Spawn W2 re-scoping agent (stigmergy-scout) to reassess mission coherence"

    return {
        "gate_name": "w3-abort-ffmx",
        "gap_id": "wire-gap-5-w3-abort",
        "decision": decision,
        "reason": reason,
        "session_ffmx": session_ffmx,
        "baseline_ffmx": baseline_ffmx,
        "threshold_ratio": FFMx_W3_ABORT_RATIO,
        "manifests_analyzed": len(manifests),
        "fallback_recommendation": fallback,
    }


# -------------------------------------------------------------------------
# Gap 2: Agent Score Formula
# -------------------------------------------------------------------------

def score_agent_deterministic(
    agent_manifest: dict[str, Any],
    task_keywords: Optional[str] = None,
) -> float:
    """
    Gap 2: Deterministic composite agent score for routing decisions.

    Formula:
      composite = belief_index * 0.40 + quality_score * 0.30 + routing_weight * 0.30

    belief_index (0.0-1.0): honesty in self-reporting (do dashboards match outcomes?)
    quality_score (0.0-1.0): output quality from last manifest
    routing_weight (0.0-1.0): reputation trust score (from reputation-schema.json)

    Domain keyword bonus (optional): +0.05 per matching keyword in role/KPI (capped at +0.15)

    Why belief_index carries the highest weight (0.40):
    A dishonest agent degrades manifest truthfulness and corrupts the entire stigmergy
    layer. A low-quality but honest agent can be retrained. A dishonest agent creates
    silent corruption that cascades through compass graph navigation.

    Args:
        agent_manifest: dict with belief_index, quality_score, routing_weight (0.0-1.0).
                        Optional: "role" and "kpi" strings for domain keyword bonus.
        task_keywords: optional space-separated keywords for domain match bonus

    Returns:
        composite score 0.0-1.0 (higher = better fit for task)
    """
    belief = max(0.0, min(1.0, float(agent_manifest.get("belief_index", 0.5))))
    quality = max(0.0, min(1.0, float(agent_manifest.get("quality_score", 0.5))))
    routing = max(0.0, min(1.0, float(agent_manifest.get("routing_weight", 0.5))))

    composite = (
        belief  * AGENT_SCORE_WEIGHTS["belief_index"]
        + quality * AGENT_SCORE_WEIGHTS["quality_score"]
        + routing * AGENT_SCORE_WEIGHTS["routing_weight"]
    )

    # Domain keyword bonus: +0.05 per match, capped at +0.15
    if task_keywords:
        role_text = f"{agent_manifest.get('role', '')} {agent_manifest.get('kpi', '')}".lower()
        keyword_matches = sum(
            1 for kw in task_keywords.lower().split() if kw.strip() and kw in role_text
        )
        composite += min(0.15, keyword_matches * 0.05)

    return round(min(1.0, composite), 4)


def rank_agents(
    agent_manifests: list[dict[str, Any]],
    task_keywords: Optional[str] = None,
    top_n: int = 3,
) -> dict[str, Any]:
    """
    Gap 2: Rank agent manifests by composite score.

    Agents with composite_score < 0.50 are flagged as "recovery" agents;
    they must decline HIGH/CRITICAL work per mth00099.
    """
    scored = []
    for agent in agent_manifests:
        composite = score_agent_deterministic(agent, task_keywords)
        scored.append({
            "agent_id": agent.get("agent_id", agent.get("agent_type", "unknown")),
            "composite_score": composite,
            "belief_index": round(float(agent.get("belief_index", 0.5)), 3),
            "quality_score": round(float(agent.get("quality_score", 0.5)), 3),
            "routing_weight": round(float(agent.get("routing_weight", 0.5)), 3),
            "status": "healthy" if composite >= 0.50 else "recovery",
            "score_breakdown": {
                "belief_contribution": round(float(agent.get("belief_index", 0.5)) * 0.40, 4),
                "quality_contribution": round(float(agent.get("quality_score", 0.5)) * 0.30, 4),
                "routing_contribution": round(float(agent.get("routing_weight", 0.5)) * 0.30, 4),
            },
        })

    scored.sort(key=lambda x: x["composite_score"], reverse=True)
    top = scored[:top_n]

    healthy = [a["agent_id"] for a in top if a["status"] == "healthy"]
    recovery = [a["agent_id"] for a in top if a["status"] == "recovery"]

    return {
        "gate_name": "agent-score-formula",
        "gap_id": "wire-gap-2-agent-selection",
        "formula": "composite = belief_index*0.40 + quality_score*0.30 + routing_weight*0.30",
        "task_keywords": task_keywords,
        "ranked_agents": top,
        "healthy_agents": healthy,
        "recovery_agents": recovery,
        "routing_recommendation": (
            f"Route to {top[0]['agent_id']} (composite={top[0]['composite_score']})"
            if top else "No agents provided"
        ),
    }


# -------------------------------------------------------------------------
# Gap 3: Context Budget Gate
# -------------------------------------------------------------------------

def gate_context_budget(
    tokens_remaining: int,
    agents_planned: int,
    wave: str = "2",
) -> dict[str, Any]:
    """
    Gap 3: Context budget allocation gate for wave spawning.

    Formula:
      usable = tokens_remaining - SAFETY_BUFFER
      budget_per_agent = usable / agents_planned
      pass if budget_per_agent >= CONTEXT_FLOOR_PER_AGENT[wave]

    Over-spawning on thin budgets causes agents to get auto-compacted mid-task,
    producing partial manifests that pollute the stigmergy layer. The floor
    ensures each agent has enough runway to complete work and write manifest.

    W1 floor = 8K  tokens (haiku, cheap, fast)
    W2 floor = 12K tokens (sonnet, moderate depth)
    W3 floor = 20K tokens (sonnet, deep synthesis)

    Args:
        tokens_remaining: context tokens available right now
        agents_planned: how many agents you intend to spawn
        wave: "1" | "2" | "3"

    Returns:
        dict with decision (pass|blocked), max_safe_agents, budget_per_agent, reason.
    """
    if wave not in CONTEXT_FLOOR_PER_AGENT:
        wave = "2"

    floor = CONTEXT_FLOOR_PER_AGENT[wave]
    usable = max(0, tokens_remaining - SAFETY_BUFFER)

    if agents_planned <= 0:
        return {
            "gate_name": "context-budget",
            "gap_id": "wire-gap-3-context-budget",
            "decision": "blocked",
            "reason": "agents_planned must be > 0",
            "max_safe_agents": 0,
            "budget_per_agent": 0,
            "floor_per_agent": floor,
            "tokens_remaining": tokens_remaining,
            "usable_tokens": usable,
        }

    budget_per_agent = usable // agents_planned
    max_safe_agents = usable // floor if floor > 0 else agents_planned

    if budget_per_agent >= floor:
        decision = "pass"
        reason = (
            f"Budget {budget_per_agent:,} tok/agent >= floor {floor:,} tok (W{wave}) "
            f"-- spawn {agents_planned} agents OK"
        )
    else:
        decision = "blocked"
        reason = (
            f"Budget {budget_per_agent:,} tok/agent < floor {floor:,} tok (W{wave}) "
            f"-- reduce to {max_safe_agents} agents or defer to next cycle"
        )

    return {
        "gate_name": "context-budget",
        "gap_id": "wire-gap-3-context-budget",
        "decision": decision,
        "reason": reason,
        "max_safe_agents": max_safe_agents,
        "agents_planned": agents_planned,
        "budget_per_agent": budget_per_agent,
        "floor_per_agent": floor,
        "tokens_remaining": tokens_remaining,
        "safety_buffer": SAFETY_BUFFER,
        "usable_tokens": usable,
        "wave": wave,
    }


# -------------------------------------------------------------------------
# All Gates Runner
# -------------------------------------------------------------------------

def run_all_gates(
    manifests_dir: str,
    investigation_label: str,
    tokens_remaining: int,
    agents_planned: int,
    wave: str = "2",
    baseline_path: Optional[str] = None,
    task_keywords: Optional[str] = None,
    agent_manifests: Optional[list[dict]] = None,
) -> dict[str, Any]:
    """Run all four formula gates and return unified verdict."""
    g1 = gate_w2_spawn(manifests_dir, investigation_label, baseline_path)
    g2 = rank_agents(agent_manifests or [], task_keywords)
    g3 = gate_context_budget(tokens_remaining, agents_planned, wave)
    g5 = gate_w3_abort(manifests_dir, investigation_label, baseline_path)

    blocked_gates = []
    for name, gate in [("w2-spawn-ffmx", g1), ("context-budget", g3), ("w3-abort-ffmx", g5)]:
        if gate.get("decision") not in ("pass",):
            blocked_gates.append(name)

    all_pass = len(blocked_gates) == 0

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "investigation_label": investigation_label,
        "wave": wave,
        "all_pass": all_pass,
        "blocked_gates": blocked_gates,
        "gates": {
            "w2_spawn_ffmx": g1,
            "agent_score_formula": g2,
            "context_budget": g3,
            "w3_abort_ffmx": g5,
        },
        "summary": (
            "All gates pass -- proceed with spawn"
            if all_pass
            else f"Gate(s) blocked: {', '.join(blocked_gates)}"
        ),
    }


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Formula-driven spawn gates (Gaps 1/2/3/5 from audit-formulas-w1.5)"
    )
    parser.add_argument(
        "--gate",
        choices=["w2-spawn", "agent-score", "context-budget", "w3-abort", "all"],
        required=True,
        help="Which gate to evaluate",
    )
    parser.add_argument("--manifests-dir", default="forensics/manifests/2026-04-28")
    parser.add_argument("--investigation-label", default="")
    parser.add_argument("--baseline-path", default=None)
    parser.add_argument("--tokens-remaining", type=int, default=80_000)
    parser.add_argument("--agents-planned", type=int, default=3)
    parser.add_argument("--wave", default="2", choices=["1", "2", "3"])
    parser.add_argument("--task-keywords", default=None)
    parser.add_argument(
        "--agent-manifests",
        default="[]",
        help='JSON list of agent manifest dicts with belief_index, quality_score, routing_weight',
    )
    parser.add_argument("--output-json", action="store_true")

    args = parser.parse_args()

    if args.gate == "w2-spawn":
        result = gate_w2_spawn(args.manifests_dir, args.investigation_label, args.baseline_path)
    elif args.gate == "agent-score":
        try:
            agents = json.loads(args.agent_manifests)
        except json.JSONDecodeError:
            agents = []
        result = rank_agents(agents, args.task_keywords)
    elif args.gate == "context-budget":
        result = gate_context_budget(args.tokens_remaining, args.agents_planned, args.wave)
    elif args.gate == "w3-abort":
        result = gate_w3_abort(args.manifests_dir, args.investigation_label, args.baseline_path)
    elif args.gate == "all":
        try:
            agent_manifests = json.loads(args.agent_manifests)
        except json.JSONDecodeError:
            agent_manifests = []
        result = run_all_gates(
            manifests_dir=args.manifests_dir,
            investigation_label=args.investigation_label,
            tokens_remaining=args.tokens_remaining,
            agents_planned=args.agents_planned,
            wave=args.wave,
            baseline_path=args.baseline_path,
            task_keywords=args.task_keywords,
            agent_manifests=agent_manifests,
        )
    else:
        parser.print_help()
        sys.exit(2)

    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        decision = result.get("decision") or ("PASS" if result.get("all_pass") else "BLOCKED")
        gate_name = result.get("gate_name", result.get("gap_id", args.gate))
        print(f"\n[{gate_name}] {decision}")
        print(f"  {result.get('reason') or result.get('summary', '')}")
        if "max_safe_agents" in result:
            print(f"  Max safe agents: {result['max_safe_agents']}")
        if "routing_recommendation" in result:
            print(f"  {result['routing_recommendation']}")
        print()

    # Exit: 0=pass, 1=blocked/abort, 2=error
    final = result.get("decision") or ("pass" if result.get("all_pass") else "blocked")
    sys.exit(0 if final in ("pass",) else 1)


if __name__ == "__main__":
    main()
