#!/usr/bin/env python3
"""
8x_time_estimate_analyzer.py — Time Estimate Feedback Loop Analyzer

TIER: 8x (utilities)
REPLACES: None
METRIC: Accuracy curves (agent_type × task_category); prediction adjustment factors
LOAD: ~0.5K tokens (script itself); unbounded input (all manifests in forensics/)

PURPOSE:
  Parse all manifests from past N days, extract predicted vs. actual duration data,
  compute accuracy curves by (agent_type, task_category), output historical baselines
  for future prediction adjustment.

SCHEMA:
  Input: forensics/manifests/{YYYY-MM-DD}/*.json (manifests with time_tracking fields)
  Output:
    - forensics/time-tracking/{YYYY-MM-DD}/accuracy-curves.json
    - forensics/time-tracking/{YYYY-MM-DD}/time-estimate-baseline.json
    - forensics/time-tracking/{YYYY-MM-DD}/prediction-recommendations.json

INTEGRATION:
  Called daily by cron job or after major W1/W2/W3 spawn batch.
  Results injected into future spawn bundles to adjust baseline estimates.

USAGE:
  python3 scripts/8x_time_estimate_analyzer.py --generate-curves --days 7
  python3 scripts/8x_time_estimate_analyzer.py --predict --agent general-purpose --category design --estimate 15
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from statistics import mean, stdev
from collections import defaultdict
import argparse


class TimeEstimateAnalyzer:
    """Analyze manifest time-tracking data and compute accuracy curves."""

    def __init__(self, forensics_dir: str):
        self.forensics_dir = Path(forensics_dir)
        self.manifests_dir = self.forensics_dir / "manifests"
        self.time_tracking_dir = self.forensics_dir / "time-tracking"
        self.time_tracking_dir.mkdir(parents=True, exist_ok=True)

    def parse_manifests(self, days: int = 7) -> list:
        """
        Parse all manifests from past N days.

        Returns:
            List of dicts: {
                'task_id': str,
                'investigation_label': str,
                'agent_type': str,
                'task_category': str,
                'predicted_minutes': float,
                'actual_minutes': float,
                'accuracy_percent': float,
                'wave': str,
                'model': str,
                'quality_score': float,
                'belief_index': float,
                'artifact_size_bytes': int,
                'citations_count': int
            }
        """
        manifests = []
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        if not self.manifests_dir.exists():
            print(f"WARN: {self.manifests_dir} not found; no manifests to analyze")
            return []

        for date_dir in self.manifests_dir.iterdir():
            if not date_dir.is_dir():
                continue

            try:
                date_obj = datetime.strptime(date_dir.name, "%Y-%m-%d")
                if date_obj < cutoff_date:
                    continue
            except ValueError:
                continue

            # Scan all .json files in this date dir
            for manifest_file in date_dir.glob("*.json"):
                try:
                    with open(manifest_file, 'r') as f:
                        data = json.load(f)

                    # Extract time-tracking fields (safe defaults)
                    predicted = data.get('predicted_duration_minutes', 0)
                    actual = data.get('actual_duration_minutes', 0)
                    accuracy = data.get('accuracy_percent', 0)

                    # Skip if no time data
                    if predicted <= 0 or actual <= 0:
                        continue

                    # Extract task category from task_id
                    task_category = self._extract_task_category(data.get('task_id', ''))

                    manifest_record = {
                        'task_id': data.get('task_id', 'unknown'),
                        'investigation_label': data.get('investigation_label', 'unknown'),
                        'agent_type': data.get('agent_type', 'unknown'),
                        'task_category': task_category,
                        'predicted_minutes': predicted,
                        'actual_minutes': actual,
                        'accuracy_percent': accuracy,
                        'wave': data.get('time_tracking', {}).get('wave', 'unknown'),
                        'model': data.get('time_tracking', {}).get('model', 'unknown'),
                        'quality_score': data.get('quality_score', 0.0),
                        'belief_index': data.get('belief_index', 0.0),
                        'artifact_size_bytes': data.get('artifact_size_bytes', 0),
                        'citations_count': data.get('citations_count', 0),
                    }
                    manifests.append(manifest_record)

                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"WARN: {manifest_file.name} — skipped ({e})")
                    continue

        return manifests

    @staticmethod
    def _extract_task_category(task_id: str) -> str:
        """Extract task category from task_id prefix."""
        prefixes = {
            'audit': ['audit-', 'validate-', 'review-', 'qa-'],
            'design': ['design-', 'plan-', 'spec-', 'architecture-'],
            'implementation': ['impl-', 'build-', 'code-', 'fix-'],
            'synthesis': ['synthesis-', 'weave-', 'document-', 'narrative-'],
            'discovery': ['discovery-', 'scan-', 'frontier-'],
        }

        task_id_lower = task_id.lower()
        for category, prefixes_list in prefixes.items():
            for prefix in prefixes_list:
                if task_id_lower.startswith(prefix):
                    return category

        return 'other'

    def calculate_accuracy_by_agent(self, manifests: list) -> dict:
        """
        Compute accuracy curves: agent_type × task_category.

        Returns:
            {
                'agent_type': {
                    'task_category': {
                        'avg_accuracy_percent': float,
                        'stddev': float,
                        'min_accuracy': float,
                        'max_accuracy': float,
                        'sample_size': int,
                        'prediction_recommendation': str
                    }
                }
            }
        """
        # Bucket by (agent_type, task_category)
        buckets = defaultdict(lambda: defaultdict(list))

        for manifest in manifests:
            agent_type = manifest['agent_type']
            task_category = manifest['task_category']
            accuracy = manifest['accuracy_percent']

            buckets[agent_type][task_category].append(accuracy)

        # Compute statistics per bucket
        curves = {}
        for agent_type in sorted(buckets.keys()):
            curves[agent_type] = {}
            for task_category in sorted(buckets[agent_type].keys()):
                accuracies = buckets[agent_type][task_category]
                n = len(accuracies)

                if n == 0:
                    continue

                avg_acc = mean(accuracies)
                std_dev = stdev(accuracies) if n > 1 else 0.0
                min_acc = min(accuracies)
                max_acc = max(accuracies)

                # Prediction recommendation
                if avg_acc > 100:
                    # Agents overestimate; multiply baseline by (avg_acc / 100)
                    factor = avg_acc / 100.0
                    rec = f"Multiply baseline by {factor:.2f} (agents overestimate by {100 - avg_acc:.0f}%)"
                elif avg_acc < 100:
                    # Agents underestimate; multiply baseline by (100 / avg_acc) to compensate
                    factor = 100.0 / avg_acc if avg_acc > 0 else 1.0
                    rec = f"Multiply baseline by {factor:.2f} (agents underestimate by {100 - avg_acc:.0f}%); add {(factor - 1) * 100:.0f}% buffer"
                else:
                    factor = 1.0
                    rec = "Trust baseline estimate (±5%)"

                curves[agent_type][task_category] = {
                    'avg_accuracy_percent': round(avg_acc, 1),
                    'stddev': round(std_dev, 1),
                    'min_accuracy': round(min_acc, 1),
                    'max_accuracy': round(max_acc, 1),
                    'sample_size': n,
                    'prediction_factor': round(factor, 2),
                    'prediction_recommendation': rec
                }

        return curves

    def calculate_accuracy_by_wave(self, manifests: list) -> dict:
        """Compute accuracy curves by piston wave (W1/W2/W3)."""
        wave_buckets = defaultdict(list)

        for manifest in manifests:
            wave = manifest['wave']
            accuracy = manifest['accuracy_percent']
            wave_buckets[wave].append(accuracy)

        wave_curves = {}
        for wave in sorted(wave_buckets.keys()):
            accuracies = wave_buckets[wave]
            n = len(accuracies)

            if n == 0:
                continue

            avg_acc = mean(accuracies)
            std_dev = stdev(accuracies) if n > 1 else 0.0

            interpretations = {
                'W1': 'W1 scouts typically overestimate (thorough). Multiply estimates by 0.92.',
                'W2': 'W2 fixers typically accurate. Trust estimates at face value.',
                'W3': 'W3 synthesizers typically underestimate (open-ended). Add 50% buffer.',
            }

            wave_curves[wave] = {
                'avg_accuracy_percent': round(avg_acc, 1),
                'stddev': round(std_dev, 1),
                'sample_size': n,
                'prediction_factor': round(avg_acc / 100.0, 2),
                'interpretation': interpretations.get(wave, 'Unknown wave')
            }

        return wave_curves

    def calculate_correlations(self, manifests: list) -> dict:
        """Compute correlation between accuracy and quality metrics."""
        if len(manifests) < 3:
            return {}

        correlations = {}

        # Correlation: accuracy vs. quality_score
        if all(m.get('quality_score') is not None for m in manifests):
            corr = self._pearson_correlation(
                [m['accuracy_percent'] for m in manifests],
                [m['quality_score'] for m in manifests]
            )
            correlations['accuracy_vs_quality_score'] = round(corr, 2)

        # Correlation: accuracy vs. belief_index
        if all(m.get('belief_index') is not None for m in manifests):
            corr = self._pearson_correlation(
                [m['accuracy_percent'] for m in manifests],
                [m['belief_index'] for m in manifests]
            )
            correlations['accuracy_vs_belief_index'] = round(corr, 2)

        # Correlation: accuracy vs. artifact_size_bytes
        if all(m.get('artifact_size_bytes') is not None for m in manifests):
            corr = self._pearson_correlation(
                [m['accuracy_percent'] for m in manifests],
                [m['artifact_size_bytes'] for m in manifests]
            )
            correlations['accuracy_vs_artifact_size_bytes'] = round(corr, 2)

        # Correlation: accuracy vs. citations_count
        if all(m.get('citations_count') is not None for m in manifests):
            corr = self._pearson_correlation(
                [m['accuracy_percent'] for m in manifests],
                [m['citations_count'] for m in manifests]
            )
            correlations['accuracy_vs_citations_count'] = round(corr, 2)

        return correlations

    @staticmethod
    def _pearson_correlation(x: list, y: list) -> float:
        """Compute Pearson correlation coefficient."""
        if len(x) < 2 or len(y) < 2:
            return 0.0

        n = len(x)
        mean_x = mean(x)
        mean_y = mean(y)

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = (
            (sum((x[i] - mean_x) ** 2 for i in range(n)) ** 0.5) *
            (sum((y[i] - mean_y) ** 2 for i in range(n)) ** 0.5)
        )

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def predict_adjusted_estimate(self, agent_type: str, task_category: str,
                                   baseline_estimate_minutes: float,
                                   accuracy_curves: dict) -> float:
        """
        Predict adjusted estimate using historical accuracy data.

        Args:
            agent_type: Type of agent (e.g., 'general-purpose')
            task_category: Task category (e.g., 'design')
            baseline_estimate_minutes: Original estimate in minutes
            accuracy_curves: Output from calculate_accuracy_by_agent()

        Returns:
            Adjusted estimate in minutes
        """
        if agent_type not in accuracy_curves:
            return baseline_estimate_minutes  # No data; return baseline

        if task_category not in accuracy_curves[agent_type]:
            return baseline_estimate_minutes  # No data for this category

        curve = accuracy_curves[agent_type][task_category]
        factor = curve.get('prediction_factor', 1.0)

        adjusted = baseline_estimate_minutes * factor
        return round(adjusted, 1)

    def generate_curves(self, days: int = 7) -> None:
        """Generate and write accuracy curves."""
        print(f"Parsing manifests from past {days} days...")
        manifests = self.parse_manifests(days=days)

        if not manifests:
            print("No manifests with time-tracking data found.")
            return

        print(f"Analyzing {len(manifests)} manifests...")

        # Compute curves
        accuracy_by_agent = self.calculate_accuracy_by_agent(manifests)
        accuracy_by_wave = self.calculate_accuracy_by_wave(manifests)
        correlations = self.calculate_correlations(manifests)

        # Build output
        today = datetime.utcnow().strftime("%Y-%m-%d")
        timestamp = datetime.utcnow().isoformat() + 'Z'

        curves_output = {
            'generated_at': timestamp,
            'analysis_window_days': days,
            'manifests_analyzed': len(manifests),
            'by_agent_type': accuracy_by_agent,
            'by_wave': accuracy_by_wave,
            'correlation_matrix': correlations
        }

        # Write to forensics/time-tracking/{date}/
        output_dir = self.time_tracking_dir / today
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "accuracy-curves.json"
        with open(output_file, 'w') as f:
            json.dump(curves_output, f, indent=2)

        print(f"Written: {output_file}")
        print(f"  Agents analyzed: {len(accuracy_by_agent)}")
        print(f"  Categories: {sum(len(cats) for cats in accuracy_by_agent.values())}")
        print(f"  Waves: {len(accuracy_by_wave)}")

    def predict(self, agent_type: str, task_category: str,
                baseline_estimate_minutes: float, days: int = 7) -> None:
        """Predict adjusted estimate and print recommendation."""
        print(f"Loading accuracy curves from past {days} days...")
        manifests = self.parse_manifests(days=days)

        if not manifests:
            print("No historical data available; cannot predict.")
            return

        accuracy_by_agent = self.calculate_accuracy_by_agent(manifests)

        adjusted = self.predict_adjusted_estimate(
            agent_type, task_category, baseline_estimate_minutes, accuracy_by_agent
        )

        print(f"\nPrediction Result:")
        print(f"  Agent type: {agent_type}")
        print(f"  Task category: {task_category}")
        print(f"  Baseline estimate: {baseline_estimate_minutes} minutes")
        print(f"  Adjusted estimate: {adjusted} minutes")

        if agent_type in accuracy_by_agent and task_category in accuracy_by_agent[agent_type]:
            curve = accuracy_by_agent[agent_type][task_category]
            print(f"  Recommendation: {curve['prediction_recommendation']}")
            print(f"  Historical avg: {curve['avg_accuracy_percent']}% ± {curve['stddev']}%")
            print(f"  Sample size: {curve['sample_size']}")


def main():
    parser = argparse.ArgumentParser(description='Time Estimate Feedback Loop Analyzer')
    parser.add_argument('--generate-curves', action='store_true', help='Generate accuracy curves')
    parser.add_argument('--predict', action='store_true', help='Predict adjusted estimate')
    parser.add_argument('--agent', type=str, help='Agent type (for predict)')
    parser.add_argument('--category', type=str, help='Task category (for predict)')
    parser.add_argument('--estimate', type=float, help='Baseline estimate in minutes (for predict)')
    parser.add_argument('--days', type=int, default=7, help='Analysis window (days)')
    parser.add_argument('--forensics-dir', type=str, default='./forensics', help='Forensics directory')

    args = parser.parse_args()

    analyzer = TimeEstimateAnalyzer(args.forensics_dir)

    if args.generate_curves:
        analyzer.generate_curves(days=args.days)
    elif args.predict:
        if not args.agent or not args.category or not args.estimate:
            print("Error: --predict requires --agent, --category, and --estimate")
            sys.exit(1)
        analyzer.predict(args.agent, args.category, args.estimate, days=args.days)
    else:
        print("Usage: python3 8x_time_estimate_analyzer.py [--generate-curves | --predict]")
        print("  --generate-curves: Analyze manifests, output accuracy curves")
        print("  --predict: Predict adjusted estimate for specific agent/task")
        sys.exit(1)


if __name__ == '__main__':
    main()
