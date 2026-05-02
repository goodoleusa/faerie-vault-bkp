#!/usr/bin/env python3
"""
7x_ffmx_calculator.py — Focused Force Multiplier (FFMx) Measurement Automation

Purpose: Measure FFMx = (A × Q × E^k) / T across a sprint, comparing to baseline.
- A = artifacts (manifests written)
- Q = quality (average quality_score from manifests)
- E = emergence (monkeybranching_depth: how deep do agent spawning chains nest?)
- T = tokens_burned (context tokens consumed in sprint)

Formula: FFMx = (A × Q × E^k) / T
  where k=1.5 (emergence is exponential; depth scales as 3/2 power)

Output: JSON with FFMx score, components, comparison to baseline, and delta.

Usage:
  python3 7x_ffmx_calculator.py \\
    --manifests-dir forensics/manifests/2026-04-28 \\
    --investigation-label terminology-cleanup-sprint \\
    --sprint-start-time "2026-04-28T00:00:00Z" \\
    --sprint-end-time "2026-04-28T23:59:59Z" \\
    --baseline forensics/mutation-baselines/baseline-terminology-ephemeral-T0.json \\
    --output forensics/mutation-baselines/ffmx-2026-04-28-terminology-cleanup.json

"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import statistics


class FFMxCalculator:
    """Calculate Focused Force Multiplier for a sprint."""

    def __init__(self, manifests_dir: str, baseline_path: Optional[str] = None):
        """
        Initialize calculator.

        Args:
            manifests_dir: Path to forensics/manifests/{YYYY-MM-DD}/
            baseline_path: Optional path to baseline JSON for comparison
        """
        self.manifests_dir = Path(manifests_dir)
        self.baseline = None

        if baseline_path:
            with open(baseline_path) as f:
                self.baseline = json.load(f)

    def load_manifests_by_label(
        self,
        investigation_label: str,
        sprint_start: str,
        sprint_end: str
    ) -> List[Dict]:
        """
        Load manifests matching investigation_label within time window.

        Args:
            investigation_label: e.g., "terminology-cleanup-sprint"
            sprint_start: ISO timestamp
            sprint_end: ISO timestamp

        Returns:
            List of manifest dicts
        """
        manifests = []
        start_dt = datetime.fromisoformat(sprint_start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(sprint_end.replace('Z', '+00:00'))

        if not self.manifests_dir.exists():
            raise FileNotFoundError(f"Manifests dir not found: {self.manifests_dir}")

        # Find all manifest JSON files in directory
        for manifest_file in sorted(self.manifests_dir.glob("*.json")):
            try:
                with open(manifest_file) as f:
                    manifest = json.load(f)

                # Filter by investigation_label
                if manifest.get("investigation_label") != investigation_label:
                    continue

                # Filter by timestamp
                timestamp_str = manifest.get("timestamp_utc") or manifest.get("timestamp")
                if not timestamp_str:
                    continue

                try:
                    ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except ValueError:
                    continue

                if start_dt <= ts <= end_dt:
                    manifests.append(manifest)
            except (json.JSONDecodeError, IOError):
                continue

        return manifests

    def calculate_artifacts(self, manifests: List[Dict]) -> int:
        """
        Count manifests written (artifacts).

        Args:
            manifests: List of manifest dicts

        Returns:
            Count of manifests (A in FFMx formula)
        """
        return len(manifests)

    def calculate_quality(self, manifests: List[Dict]) -> float:
        """
        Calculate average quality_score.

        Args:
            manifests: List of manifest dicts

        Returns:
            Average quality_score (Q in FFMx formula)
        """
        if not manifests:
            return 0.0

        quality_scores = []
        for m in manifests:
            # Use quality_score field; if missing, estimate from belief_index
            q = m.get("quality_score")
            if q is None:
                # Fallback: average belief components
                belief = m.get("belief_index")
                if belief is not None:
                    q = belief
                else:
                    # Default conservative estimate
                    q = 0.50
            quality_scores.append(float(q))

        return statistics.mean(quality_scores) if quality_scores else 0.5

    def calculate_emergence_depth(self, manifests: List[Dict]) -> Tuple[int, Dict]:
        """
        Calculate monkeybranching depth (how deep do agent generations nest?).

        Emergence depth is measured by:
        1. Identify manifest parent-child relationships (parent_task field)
        2. Build a DAG of agent lineage
        3. Find maximum path length in DAG
        4. Return max_depth + metadata

        Args:
            manifests: List of manifest dicts

        Returns:
            Tuple of (max_depth, metadata_dict)

        Depth semantics:
        - Depth 1: Agent A writes manifest (root)
        - Depth 2: Agent B reads A's manifest + spawns Agent C
        - Depth 3: Agent C reads A+B manifests + spawns Agent D
        - Depth N: longest chain in the monkeybranching tree
        """
        if not manifests:
            return 0, {}

        # Build parent-child mapping
        task_id_to_manifest = {m.get("task_id"): m for m in manifests}

        # Identify parent-child relationships
        parent_to_children = {}  # parent_task_id -> [child_task_ids]
        task_parents = {}  # task_id -> parent_task_id

        for m in manifests:
            task_id = m.get("task_id")
            parent_task = m.get("parent_task")

            if parent_task:
                task_parents[task_id] = parent_task
                if parent_task not in parent_to_children:
                    parent_to_children[parent_task] = []
                parent_to_children[parent_task].append(task_id)

        # Find root nodes (manifests with no parent)
        roots = [m.get("task_id") for m in manifests if m.get("task_id") not in task_parents]

        # DFS to find max depth from each root
        def max_depth_from(task_id: str, visited: set) -> int:
            """Recursive DFS for longest path from task_id."""
            if task_id in visited:
                return 0
            visited.add(task_id)

            children = parent_to_children.get(task_id, [])
            if not children:
                return 1

            return 1 + max(max_depth_from(child, visited) for child in children)

        max_depth = 0
        deepest_chain = []

        for root in roots:
            depth = max_depth_from(root, set())
            if depth > max_depth:
                max_depth = depth
                # Trace the chain for reporting
                deepest_chain = self._trace_longest_chain(root, parent_to_children)

        metadata = {
            "max_depth": max_depth,
            "root_count": len(roots),
            "total_parent_child_links": len(task_parents),
            "deepest_chain": deepest_chain,
            "branching_coefficient": self._calculate_branching_coefficient(
                parent_to_children, len(manifests)
            ),
        }

        return max_depth, metadata

    def _trace_longest_chain(self, root: str, parent_to_children: Dict) -> List[str]:
        """Trace the longest chain from a root node."""
        chain = [root]
        current = root

        while current in parent_to_children and parent_to_children[current]:
            # Follow the first (largest) child
            next_node = max(
                parent_to_children[current],
                key=lambda x: len(parent_to_children.get(x, []))
            )
            chain.append(next_node)
            current = next_node

        return chain

    def _calculate_branching_coefficient(self, parent_to_children: Dict, total_manifests: int) -> float:
        """
        Calculate average branching factor (children per parent).

        Branching coefficient = total_children / total_parents
        High = wide parallelization; Low = deep sequential lineage
        """
        if not parent_to_children:
            return 0.0

        total_children = sum(len(children) for children in parent_to_children.values())
        avg_branching = total_children / len(parent_to_children) if parent_to_children else 0.0

        return round(avg_branching, 2)

    def estimate_tokens_burned(
        self,
        manifests: List[Dict],
        default_tokens_per_manifest: int = 30800
    ) -> int:
        """
        Estimate tokens burned in sprint.

        Heuristic:
        - Use manifest artifact_size_bytes as proxy for reasoning depth (artifact size = problem complexity)
        - Multiply by tokens-per-byte calibration (roughly 0.1 tokens per byte for code/text)
        - Sum across all manifests
        - Fallback to artifact count × default_tokens_per_manifest

        Args:
            manifests: List of manifest dicts
            default_tokens_per_manifest: Conservative estimate (30.8K tokens observed in baseline)

        Returns:
            Estimated tokens_burned (T in FFMx formula)
        """
        total_tokens = 0
        artifacts_with_size = 0

        # Method 1: Use artifact_size_bytes if available
        for m in manifests:
            artifact_size = m.get("artifact_size_bytes")
            if artifact_size:
                # Heuristic: ~0.1 tokens per byte for text artifacts
                # (conservative; actual may be higher for dense reasoning)
                estimated_tokens = int(artifact_size * 0.125)  # 0.125 ≈ 0.1-0.15 tokens/byte
                total_tokens += estimated_tokens
                artifacts_with_size += 1

        # Method 2: Fallback for missing artifact_size
        artifacts_without_size = len(manifests) - artifacts_with_size
        total_tokens += artifacts_without_size * default_tokens_per_manifest

        return total_tokens

    def calculate_ffmx(
        self,
        artifacts: int,
        quality: float,
        emergence_depth: int,
        tokens_burned: int,
        emergence_power: float = 1.5
    ) -> float:
        """
        Calculate FFMx = (A × Q × E^k) / T

        Args:
            artifacts: Count of manifests (A)
            quality: Average quality_score 0.0-1.0 (Q)
            emergence_depth: Max monkeybranching depth (E)
            tokens_burned: Total tokens in sprint (T)
            emergence_power: Exponent for emergence (k=1.5; exponential growth)

        Returns:
            FFMx score
        """
        if tokens_burned <= 0:
            return 0.0

        # Prevent division by zero; emergence_depth=0 means no spawning (score = A×Q/T)
        emergence_factor = emergence_depth ** emergence_power if emergence_depth > 0 else 1.0

        ffmx = (artifacts * quality * emergence_factor) / tokens_burned

        return ffmx

    def compare_to_baseline(self, current_ffmx: float, baseline_ffmx: Optional[float]) -> Dict:
        """
        Compare current FFMx to baseline.

        Args:
            current_ffmx: Current sprint FFMx
            baseline_ffmx: Baseline FFMx (from T+0)

        Returns:
            Dict with improvement_percent, pass_fail, note
        """
        if baseline_ffmx is None or baseline_ffmx == 0:
            return {
                "baseline_available": False,
                "improvement_percent": None,
                "pass_fail": "unknown",
                "note": "Baseline unavailable; first measurement (T+0)"
            }

        improvement_percent = ((current_ffmx - baseline_ffmx) / baseline_ffmx) * 100
        threshold = 50  # Success = 50% improvement (FFMx_post / FFMx_pre >= 1.5)
        pass_fail = "pass" if improvement_percent >= threshold else "caution"

        return {
            "baseline_available": True,
            "baseline_ffmx": round(baseline_ffmx, 2),
            "current_ffmx": round(current_ffmx, 2),
            "improvement_percent": round(improvement_percent, 1),
            "threshold_percent": threshold,
            "pass_fail": pass_fail,
            "note": (
                f"FFMx improved {improvement_percent:.1f}% "
                f"(target: >= {threshold}%; {'PASS' if improvement_percent >= threshold else 'CAUTION'})"
            )
        }

    def run(
        self,
        investigation_label: str,
        sprint_start: str,
        sprint_end: str,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Run full FFMx calculation and output results.

        Args:
            investigation_label: e.g., "terminology-cleanup-sprint"
            sprint_start: ISO timestamp
            sprint_end: ISO timestamp
            output_path: Optional path to write JSON output

        Returns:
            Dict with FFMx results
        """
        # Load manifests
        manifests = self.load_manifests_by_label(
            investigation_label, sprint_start, sprint_end
        )

        if not manifests:
            print(f"[WARN] No manifests found for label '{investigation_label}' in time range.")
            return {}

        print(f"[INFO] Loaded {len(manifests)} manifests for '{investigation_label}'")

        # Calculate components
        artifacts = self.calculate_artifacts(manifests)
        quality = self.calculate_quality(manifests)
        emergence_depth, emergence_meta = self.calculate_emergence_depth(manifests)
        tokens_burned = self.estimate_tokens_burned(manifests)

        # Calculate FFMx
        ffmx = self.calculate_ffmx(artifacts, quality, emergence_depth, tokens_burned)

        # Extract baseline FFMx (if available)
        baseline_ffmx = None
        if self.baseline and "ffmx" in self.baseline.get("measurements", {}):
            baseline_ffmx = self.baseline["measurements"]["ffmx"].get("baseline_ffmx")

        # Compare to baseline
        comparison = self.compare_to_baseline(ffmx, baseline_ffmx)

        # Build result
        result = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "investigation_label": investigation_label,
            "sprint_window": {
                "start": sprint_start,
                "end": sprint_end
            },
            "measurements": {
                "artifacts_count": artifacts,
                "quality_average": round(quality, 3),
                "emergence_depth": emergence_depth,
                "emergence_metadata": emergence_meta,
                "tokens_burned_estimated": tokens_burned,
                "emergence_power_exponent": 1.5
            },
            "ffmx_calculation": {
                "formula": "FFMx = (A × Q × E^1.5) / T",
                "components": {
                    "A_artifacts": artifacts,
                    "Q_quality": round(quality, 3),
                    "E_emergence_depth": emergence_depth,
                    "E_raised_to_power": round(emergence_depth ** 1.5, 3),
                    "T_tokens": tokens_burned
                },
                "result": round(ffmx, 2)
            },
            "baseline_comparison": comparison,
            "manifests_analyzed": [m.get("task_id") for m in manifests],
            "manifest_count": len(manifests)
        }

        # Write output
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"[OK] FFMx result written to {output_file}")

        return result


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate Focused Force Multiplier (FFMx) for a sprint"
    )
    parser.add_argument(
        "--manifests-dir",
        required=True,
        help="Path to forensics/manifests/{YYYY-MM-DD}/"
    )
    parser.add_argument(
        "--investigation-label",
        required=True,
        help="Investigation label to filter manifests by"
    )
    parser.add_argument(
        "--sprint-start-time",
        required=True,
        help="Sprint start time (ISO format, e.g., 2026-04-28T00:00:00Z)"
    )
    parser.add_argument(
        "--sprint-end-time",
        required=True,
        help="Sprint end time (ISO format, e.g., 2026-04-28T23:59:59Z)"
    )
    parser.add_argument(
        "--baseline",
        default=None,
        help="Path to baseline JSON for comparison"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write FFMx result JSON"
    )

    args = parser.parse_args()

    # Run calculator
    calc = FFMxCalculator(args.manifests_dir, args.baseline)
    result = calc.run(
        investigation_label=args.investigation_label,
        sprint_start=args.sprint_start_time,
        sprint_end=args.sprint_end_time,
        output_path=args.output
    )

    # Print result
    print("\n" + "=" * 70)
    print("FFMx CALCULATION RESULT")
    print("=" * 70)
    if result:
        ffmx_result = result.get("ffmx_calculation", {}).get("result", 0)
        comparison = result.get("baseline_comparison", {})
        print(f"FFMx Score: {ffmx_result}")
        print(f"Artifacts: {result['measurements']['artifacts_count']}")
        print(f"Quality: {result['measurements']['quality_average']:.2f}")
        print(f"Emergence Depth: {result['measurements']['emergence_depth']}")
        print(f"Tokens Burned: {result['measurements']['tokens_burned_estimated']:,}")
        print()
        if comparison.get("baseline_available"):
            print(f"Baseline Comparison: {comparison.get('note')}")
    print("=" * 70)


if __name__ == "__main__":
    main()
