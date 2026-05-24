{
  "schema_version": "1.0",
  "artifact_type": "validation_framework",
  "task_id": "velocity-acceleration-bundle-compression",
  "investigation_label": "velocity-acceleration",
  "agent_type": "data-analyst",
  "created_at": "2026-04-28T14:44:21Z",
  "framework_name": "Bundle Compression Validation Framework v1.0",
  "objective": "Prove bundle compression achieves 50-70% size reduction with zero capability loss. Measure before/after FFMx components, agent performance deltas, and context pressure stability.",

  "baseline_observations": {
    "current_bundle_sizes": {
      "sample_task_bundle_bytes": 5848,
      "honey_md_bytes": 62384,
      "nectar_md_bytes": 97816,
      "honey_tokens_estimated": 15596,
      "nectar_tokens_estimated": 24454,
      "typical_bundle_with_full_injection_tokens": 41050,
      "typical_bundle_with_tail30_nectar_tokens": 17096,
      "note": "HONEY 62KB and NECTAR 97KB represent the dominant cost drivers. Task-specific bundles (e.g., ffmx-investigation-init.json at 5.8KB) are already minimal; compression opportunity is in HONEY+NECTAR injection policy."
    },
    "current_agent_performance": {
      "sample_size": 9,
      "avg_quality_score": 0.908,
      "avg_belief_index": 0.900,
      "avg_manifest_truthfulness": 0.947,
      "min_quality_score": 0.85,
      "max_quality_score": 0.95,
      "std_quality_score": 0.029,
      "source": "forensics/manifests/2026-04-28/ — 9 scored manifests",
      "date_range": "2026-04-28"
    },
    "current_ffmx_components": {
      "discovery_coefficient": 7.78,
      "depth_efficiency_multiplier": 2.2,
      "parallelization_agents_per_wave": 4.0,
      "blockers_cleared_ratio": 0.714,
      "cost_efficiency": 0.54,
      "ffmx_measured": 44.4,
      "source": "forensics/artifacts/2026-04-28/150200Z_ffmx-formula-breakdown_force-multiplier-index_data-analyst_001.md"
    },
    "context_pressure_baseline": {
      "formula": "logistic_sigmoid: 1 / (1 + exp(-k * (fill - c_mid)))",
      "c_mid_tokens": 80000,
      "k_steepness": 0.0001,
      "instrumented_since": "2026-04-28 phase1-instrumentation",
      "source": "forensics/manifests/2026-04-28/14-00-00Z_manifest_phase1-instrumentation_python-pro_001.json",
      "note": "Phase 1 wired measure-only; actual fill tracked via session-metrics. Context pressure should remain stable or decrease post-compression (fewer tokens injected per bundle = lower pressure)."
    }
  },

  "metrics": {
    "primary": [
      {
        "metric_id": "M001",
        "name": "bundle.size_bytes",
        "description": "Total byte size of rendered bundle JSON written to forensics/bundles/{date}/",
        "measurement_method": "os.path.getsize() on bundle file at spawn time",
        "record_location": "manifest field: bundle_size_bytes",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "decrease",
        "target_reduction_pct": "50-70"
      },
      {
        "metric_id": "M002",
        "name": "bundle.token_count",
        "description": "Estimated token count of bundle (chars / 4, or exact via tokenizer if available)",
        "measurement_method": "len(bundle_content) // 4 at assembly time; record in manifest",
        "record_location": "manifest field: bundle_token_count",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "decrease",
        "target_reduction_pct": "50-70"
      },
      {
        "metric_id": "M003",
        "name": "ffmx.discovery_coefficient",
        "description": "New missions discovered per manifest written (missions clustered / manifests produced)",
        "measurement_method": "0x_mission_graph.py --query missions | count investigation_labels / manifest count",
        "record_location": "session-metrics/{date}.json field: discovery_coefficient",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable or increase",
        "regression_threshold": "drop > 10% from baseline (7.78 -> below 7.00 triggers alert)"
      },
      {
        "metric_id": "M004",
        "name": "ffmx.depth_efficiency",
        "description": "Tokens per manifest (measures how efficiently agents convert tokens to manifest outputs)",
        "measurement_method": "total_session_tokens / manifests_produced (from 9x_token_ledger.py)",
        "record_location": "session-metrics/{date}.json field: tokens_per_manifest",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "decrease (fewer tokens per manifest = more efficient)",
        "regression_threshold": "tokens_per_manifest increases > 10% from baseline (30,826 -> above 33,909 triggers alert)"
      },
      {
        "metric_id": "M005",
        "name": "ffmx.parallelization_rate",
        "description": "Average agents spawned per W1 wave",
        "measurement_method": "count agents in same session_id timestamp window (W1 window = within 60s)",
        "record_location": "session-metrics/{date}.json field: avg_w1_parallelization",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable",
        "regression_threshold": "drop below 3.0 agents/wave (from baseline 4.0) triggers alert"
      },
      {
        "metric_id": "M006",
        "name": "ffmx.blockers_cleared_ratio",
        "description": "North-edge tasks resolved per cycle (compass_edge='S' count / total spawned count)",
        "measurement_method": "grep compass_edge manifests | count S vs N/W",
        "record_location": "session-metrics/{date}.json field: blockers_cleared_ratio",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable or increase",
        "regression_threshold": "drop below 0.64 (10% below baseline 0.714) triggers alert"
      },
      {
        "metric_id": "M007",
        "name": "ffmx.cost_efficiency",
        "description": "Total session tokens vs vanilla baseline (measured by 9x_token_ledger.py)",
        "measurement_method": "session_total_tokens / vanilla_baseline_500K",
        "record_location": "session-metrics/{date}.json field: cost_ratio",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "decrease (lower cost ratio = cheaper)",
        "regression_threshold": "cost_ratio increases > 5% from baseline (0.54 -> above 0.567) triggers investigation"
      },
      {
        "metric_id": "M008",
        "name": "agent.quality_score",
        "description": "Per-manifest quality_score self-reported by agent",
        "measurement_method": "extract quality_score from each manifest JSON; compute session mean",
        "record_location": "manifest field: quality_score + aggregated in session-metrics",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable",
        "regression_threshold": "session mean drops > 5% from baseline (0.908 -> below 0.863 triggers alert)"
      },
      {
        "metric_id": "M009",
        "name": "agent.belief_index",
        "description": "Per-manifest belief_index (honesty in self-reporting)",
        "measurement_method": "extract belief_index from each manifest JSON; compute session mean",
        "record_location": "manifest field: belief_index + aggregated in session-metrics",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable",
        "regression_threshold": "session mean drops > 5% from baseline (0.900 -> below 0.855 triggers alert)"
      },
      {
        "metric_id": "M010",
        "name": "agent.manifest_truthfulness",
        "description": "Alignment between dashboard_line claims and actual artifact content",
        "measurement_method": "extract manifest_truthfulness where float; session mean; manual spot-check for dict form",
        "record_location": "manifest field: manifest_truthfulness",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable",
        "regression_threshold": "mean drops > 5% from baseline (0.947 -> below 0.900 triggers alert)"
      },
      {
        "metric_id": "M011",
        "name": "context_pressure.logistic_value",
        "description": "Logistic sigmoid pressure value at each spawn (0.0 = no pressure, 1.0 = full pressure)",
        "measurement_method": "0x_spawn_template.py context_pressure() logged to session-metrics per spawn",
        "record_location": "session-metrics/{date}.json phase2_shadow entries",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "stable or decrease",
        "regression_threshold": "mean context_pressure increases post-compression (compression not working if pressure rises)"
      },
      {
        "metric_id": "M012",
        "name": "manifest.write_latency_ms",
        "description": "Time from task_complete signal to manifest file written on disk (proxy for assembly overhead)",
        "measurement_method": "os.path.getmtime() of manifest minus task completion timestamp; log to session-metrics",
        "record_location": "session-metrics/{date}.json field: manifest_write_latency_ms",
        "phase_applicability": ["baseline", "compressed"],
        "expected_direction": "decrease (faster assembly with smaller bundles)",
        "note": "Currently not instrumented. Phase 1 of validation must add timing hook."
      }
    ],
    "secondary": [
      {
        "metric_id": "S001",
        "name": "bundle.nectar_section_bytes",
        "description": "Bytes contributed by NECTAR section within rendered bundle",
        "measurement_method": "measure NECTAR content string length in assembled bundle",
        "expected_compression_target": "60-75% reduction via HIGH/CRITICAL filter"
      },
      {
        "metric_id": "S002",
        "name": "bundle.pollen_section_bytes",
        "description": "Bytes contributed by pollen/MEM block section within rendered bundle",
        "measurement_method": "measure pollen content string length in assembled bundle",
        "expected_compression_target": "70-80% reduction via dedup + 1-line summaries"
      },
      {
        "metric_id": "S003",
        "name": "bundle.boilerplate_bytes",
        "description": "Bytes contributed by static boilerplate (background history, analysis appendix)",
        "measurement_method": "measure template sections not driven by dynamic data",
        "expected_compression_target": "40-50% reduction via Jinja2 conditional skipping for simple tasks"
      },
      {
        "metric_id": "S004",
        "name": "agent.capability_coverage",
        "description": "Binary smoke test: can compressed-bundle agent answer capability questions that full-bundle agent can? (5 standard probes)",
        "measurement_method": "Capability probe set (see Phase 3 protocol below); pass/fail per probe; compute pass rate",
        "regression_threshold": "Any capability probe fails that passed on full bundle = regression"
      }
    ]
  },

  "validation_protocol": {
    "phase_1": {
      "name": "Baseline Measurement",
      "objective": "Establish empirical bundle size and agent performance baselines before any compression applied",
      "spawn_count": "5-10 agents using current uncompressed 0x_spawn_template.py",
      "steps": [
        {
          "step": 1,
          "action": "Instrument 0x_spawn_template.py to record bundle_size_bytes and bundle_token_count in every manifest before spawn",
          "output": "Every manifest gains two new fields: bundle_size_bytes, bundle_token_count"
        },
        {
          "step": 2,
          "action": "Run 5-10 standard spawns across at least 2 agent types (data-analyst, ai-engineer) on real investigation tasks",
          "output": "5-10 manifests with baseline bundle_size_bytes, quality_score, belief_index"
        },
        {
          "step": 3,
          "action": "Record NECTAR section bytes, pollen section bytes, and boilerplate bytes per spawn (before assembly completes)",
          "output": "Per-section breakdown for each spawn"
        },
        {
          "step": 4,
          "action": "Run context_pressure() from phase2 instrumentation at each spawn; record to session-metrics",
          "output": "Context pressure baseline distribution (mean, std, min, max)"
        },
        {
          "step": 5,
          "action": "Aggregate: compute session means for M001-M012. Store in forensics/artifacts/{date}/baseline_metrics_phase1.json",
          "output": "Locked baseline JSON with all metric means and std devs"
        }
      ],
      "acceptance_criteria": "Minimum 5 spawns with bundle_size_bytes recorded. Context pressure mean computed. Quality/belief/truthfulness averages within 0.05 of historical (0.908 / 0.900 / 0.947).",
      "estimated_duration": "1 session (1-2 hours instrumentation + 5-10 spawns)",
      "risk": "LOW — measure-only, zero behavioral change. Phase 1 fails only if instrumentation hook breaks assembly."
    },
    "phase_2": {
      "name": "Compression Application and Compressed Baseline Capture",
      "objective": "Apply compression per documentation-engineer design spec; measure compressed bundle metrics",
      "compression_methods_to_test": [
        {
          "method_id": "C1",
          "name": "NECTAR selective filter",
          "description": "Inject only HIGH/CRITICAL priority NECTAR entries (filter by priority field or recency)",
          "implementation": "Add --nectar-filter flag to 0x_spawn_template.py; default threshold: CRITICAL+HIGH only",
          "expected_savings": "60-75% NECTAR section reduction (24,454 tokens -> 6,100-9,800 tokens)",
          "risk": "MEDIUM — agents may miss MEDIUM context that was load-bearing for certain tasks. Capability probe in Phase 3 validates."
        },
        {
          "method_id": "C2",
          "name": "Pollen deduplication + 1-line summaries",
          "description": "Group pollen MEM blocks by (agent, category); keep most recent + 1-line summary of prior entries",
          "implementation": "pollen_compressor.py (~100-150 LOC); integrate into assemble_bundle()",
          "expected_savings": "70-80% pollen section reduction (1,200 tokens -> 240-360 tokens per typical session)",
          "risk": "LOW — pollen is ephemeral by design; 1-line summaries preserve signal without full detail"
        },
        {
          "method_id": "C3",
          "name": "Jinja2 template conditionals for boilerplate",
          "description": "Skip background-history and analysis-appendix sections when task_complexity=simple",
          "implementation": "Add task_complexity param to bundle assembly; Jinja2 conditional blocks",
          "expected_savings": "40-50% boilerplate reduction for simple tasks; 0% for complex tasks",
          "risk": "LOW — conditional skip, not deletion. Complex tasks retain full boilerplate."
        }
      ],
      "steps": [
        {
          "step": 1,
          "action": "Implement C1 (NECTAR filter) first in isolation. Apply to same 5-task set as Phase 1 baseline.",
          "output": "5 manifests with C1 compression; bundle_size_bytes for C1-only"
        },
        {
          "step": 2,
          "action": "Implement C2 (pollen dedup) in isolation. Apply to same 5-task set.",
          "output": "5 manifests with C2 compression; bundle_size_bytes for C2-only"
        },
        {
          "step": 3,
          "action": "Implement C3 (template conditionals) in isolation. Apply to same 5-task set (task_complexity=simple).",
          "output": "5 manifests with C3 compression; bundle_size_bytes for C3-only"
        },
        {
          "step": 4,
          "action": "Apply C1+C2+C3 combined. Run 5 spawns. Record combined bundle_size_bytes and all M001-M012 metrics.",
          "output": "Combined compression manifests + session-metrics"
        },
        {
          "step": 5,
          "action": "Compute compression ratios: (baseline_bytes - compressed_bytes) / baseline_bytes for each method and combined",
          "output": "compression_ratios.json: per-method and combined reduction percentages"
        }
      ],
      "acceptance_criteria": "Combined C1+C2+C3 achieves >= 50% bundle_size_bytes reduction vs Phase 1 baseline. Agent quality_score mean >= Phase 1 mean - 0.05.",
      "estimated_duration": "1-2 sessions (implementation + 15-20 spawns)",
      "risk": "MEDIUM — C1 poses highest risk if agents exhibit capability degradation on tasks requiring MEDIUM-priority NECTAR context. Isolate C1 failures before combining."
    },
    "phase_3": {
      "name": "FFMx Comparison, Capability Probes, and Gate Validation",
      "objective": "Compare FFMx components, run capability smoke tests, validate safety gates hold",
      "steps": [
        {
          "step": 1,
          "action": "Run FFMx component calculation on Phase 2 session data (same formula as Lane 1 ffmx breakdown artifact)",
          "calculation": "FFMx = (Discovery × Depth × Parallelization × Blockers) / Cost",
          "output": "ffmx_post_compression.json with all 5 components + computed FFMx"
        },
        {
          "step": 2,
          "action": "Delta comparison: Phase 1 vs Phase 2 FFMx components (absolute and percentage delta per component)",
          "output": "ffmx_delta.json: component deltas, direction (improvement/regression/stable), flag if any component drops > 10%"
        },
        {
          "step": 3,
          "action": "Run capability probe set (5 probes) on both full-bundle and compressed-bundle agents",
          "capability_probes": [
            {
              "probe_id": "CP01",
              "description": "Agent correctly identifies current investigation_label from bundle context",
              "pass_criterion": "Agent uses correct investigation_label in manifest without prompt hint"
            },
            {
              "probe_id": "CP02",
              "description": "Agent correctly follows compass bearing (N/S/E/W) from prior manifest next_task_queued",
              "pass_criterion": "Agent reads prior manifest and routes task correctly to next bearing"
            },
            {
              "probe_id": "CP03",
              "description": "Agent recalls a HIGH-priority finding from NECTAR and cites it in artifact",
              "pass_criterion": "At least 1 HIGH/CRITICAL NECTAR entry cited in artifact bibliography"
            },
            {
              "probe_id": "CP04",
              "description": "Agent produces quality_score >= 0.80 on a standard research task",
              "pass_criterion": "quality_score >= 0.80 in manifest"
            },
            {
              "probe_id": "CP05",
              "description": "Agent does NOT exhibit hallucination about missing MEDIUM-priority context",
              "pass_criterion": "Compressed agent acknowledges limited pollen context if relevant, rather than fabricating detail"
            }
          ],
          "output": "capability_probes_results.json: pass/fail per probe, per method (C1/C2/C3/combined)"
        },
        {
          "step": 4,
          "action": "Check context_pressure post-compression: mean logistic_value should be lower or equal to Phase 1 baseline",
          "output": "context_pressure_delta.json: before/after pressure comparison"
        },
        {
          "step": 5,
          "action": "Final report: summarize all gates. Flag regressions. Produce go/no-go recommendation per compression method.",
          "output": "validation_result_summary.json with gate_status per M001-M012, capability_probe_status, and final recommendation"
        }
      ],
      "acceptance_criteria": "All safety gates pass (see safety_gates section). All 5 capability probes pass for combined compression. FFMx post-compression >= 40.0 (90% of baseline 44.4). Context pressure stable or decreased.",
      "estimated_duration": "1 session (analysis + probe execution)",
      "risk": "LOW — this phase is measurement and comparison only. No further behavioral change."
    }
  },

  "safety_gates": {
    "description": "These gates are evaluated in Phase 3. ANY gate failure triggers automatic revert or investigation hold.",
    "gates": [
      {
        "gate_id": "G001",
        "metric": "ffmx.discovery_coefficient",
        "baseline_value": 7.78,
        "threshold": "drop > 10%",
        "trigger_level": 7.00,
        "action_if_triggered": "REVERT C1 (NECTAR filter most likely culprit — discovery relies on NECTAR clustering signals). Hold compression deployment.",
        "severity": "HIGH"
      },
      {
        "gate_id": "G002",
        "metric": "agent.quality_score (session mean)",
        "baseline_value": 0.908,
        "threshold": "drop > 5%",
        "trigger_level": 0.863,
        "action_if_triggered": "INVESTIGATE — identify which agent types regress. Likely a MEDIUM NECTAR entry was load-bearing for that agent type. Adjust C1 filter threshold to include relevant MEDIUM entries.",
        "severity": "HIGH"
      },
      {
        "gate_id": "G003",
        "metric": "agent.belief_index (session mean)",
        "baseline_value": 0.900,
        "threshold": "drop > 5%",
        "trigger_level": 0.855,
        "action_if_triggered": "INVESTIGATE — belief_index drop suggests agents uncertain about context (missing NECTAR context making them less confident). Adjust C1 threshold.",
        "severity": "MEDIUM"
      },
      {
        "gate_id": "G004",
        "metric": "context_pressure.logistic_value (session mean)",
        "baseline_value": "measured in Phase 1",
        "threshold": "INCREASE post-compression",
        "trigger_level": "any mean increase > 2%",
        "action_if_triggered": "CRITICAL ALERT — compression not working as intended. Bundle tokens are not decreasing context fill. Check assembly pipeline for token injection bugs.",
        "severity": "CRITICAL"
      },
      {
        "gate_id": "G005",
        "metric": "bundle.size_bytes",
        "baseline_value": "measured in Phase 1",
        "threshold": "reduction < 30%",
        "trigger_level": "less than 30% reduction from baseline",
        "action_if_triggered": "INVESTIGATE — compression underperforming. Check which method (C1/C2/C3) is not delivering expected savings. Likely C1 if NECTAR entries are mostly already CRITICAL.",
        "severity": "MEDIUM"
      },
      {
        "gate_id": "G006",
        "metric": "capability_probes",
        "baseline_value": "5 of 5 pass on full bundle",
        "threshold": "any probe fails on compressed bundle that passed on full bundle",
        "trigger_level": "< 5 of 5 pass rate on compressed bundle",
        "action_if_triggered": "INVESTIGATE per probe. CP03 failure -> C1 too aggressive (removing HIGH entries). CP02 failure -> C2 removing compass-bearing pollen. CP05 failure -> agent hallucinating about missing context.",
        "severity": "HIGH"
      },
      {
        "gate_id": "G007",
        "metric": "ffmx.cost_efficiency (cost_ratio)",
        "baseline_value": 0.54,
        "threshold": "increase > 5%",
        "trigger_level": 0.567,
        "action_if_triggered": "INVESTIGATE — compression should reduce tokens, not increase them. Check for accidental verbosity added by compression metadata.",
        "severity": "MEDIUM"
      }
    ],
    "gate_evaluation_order": ["G004", "G006", "G001", "G002", "G005", "G003", "G007"],
    "auto_revert_gates": ["G004", "G006", "G001"],
    "investigation_hold_gates": ["G002", "G003", "G005", "G007"],
    "all_pass_means": "Compression is safe to deploy. Proceed to velocity-acceleration-bundle-compression-implementation task."
  },

  "tradeoff_analysis": {
    "optimization_targets": [
      {
        "target": "Bundle size reduction (50-70%)",
        "mechanism": "NECTAR filter (60-75% of NECTAR section) + pollen dedup (70-80% of pollen section) + template conditionals (40-50% boilerplate for simple tasks)",
        "estimated_combined_token_savings": "Current 17,096 token bundles (HONEY + tail-30 NECTAR + pollen + task) -> 8,500-11,000 tokens post-compression",
        "ffmx_impact": "POSITIVE — depth efficiency (M004) should improve: fewer bundle tokens leave more reasoning budget for pure task work. FFMx cost_efficiency component should decrease (lower cost ratio)."
      },
      {
        "target": "Faster manifest writes and lower context burn in assembly phase",
        "mechanism": "Smaller bundles = less text to process at assembly + inject time. Manifest write latency (M012) expected to decrease.",
        "estimated_time_savings": "10-15% assembly latency reduction (assembly is I/O + template rendering, not inference; savings are modest)",
        "ffmx_impact": "MINOR POSITIVE on parallelization — slightly faster spawns allow tighter piston wave timing."
      },
      {
        "target": "Reduced context pressure per spawn",
        "mechanism": "Fewer tokens injected per bundle directly lowers context fill at spawn time. Logistic sigmoid (context_pressure) shifts left (lower pressure).",
        "ffmx_impact": "POSITIVE — lower pressure means W1/W2/W3 piston wave thresholds are hit less frequently by assembly overhead alone, preserving more context for reasoning."
      }
    ],
    "risks_and_tradeoffs": [
      {
        "risk": "NECTAR MEDIUM entries contain load-bearing context for certain agent types",
        "probability": "MEDIUM",
        "impact": "Agent quality_score drop on tasks requiring domain-specific MEDIUM findings (e.g., a MEDIUM-priority bug fix pattern that an agent needs but C1 filter excludes)",
        "mitigation": "G002 gate catches this. Mitigation: per-agent-type NECTAR filter thresholds (data-analyst gets broader NECTAR; ai-engineer gets narrower). Implement as agent_type -> filter_threshold mapping in config.",
        "tradeoff": "Compression gains partially offset by needing agent-type-specific filter config (adds complexity to assembly)"
      },
      {
        "risk": "Pollen 1-line summaries lose nuance for long multi-turn sessions",
        "probability": "LOW",
        "impact": "Agents in W3 INSERTION (deep synthesis) may produce lower-depth artifacts if pollen summaries omit mid-session pivots",
        "mitigation": "C2 risk is lower for W1/W2 (fresh sessions with minimal pollen). Apply C2 only when pollen entries > 5; preserve full detail when pollen entries <= 5.",
        "tradeoff": "Conditional pollen compression adds logic to pollen_compressor.py but prevents capability loss in W3 agents"
      },
      {
        "risk": "Template conditionals (C3) skip context that was implicitly load-bearing for agent reasoning",
        "probability": "LOW",
        "impact": "Simple tasks that need background history as anchoring context may produce lower-quality manifests",
        "mitigation": "C3 applies only to task_complexity=simple (explicitly tagged). Agent can override by requesting full bundle via manifest field: bundle_mode=full. Safety escape valve prevents silent degradation.",
        "tradeoff": "Agent needs to know when to request full bundle; adds a self-assessment responsibility to agent spawn protocol"
      },
      {
        "risk": "Compression metadata adds overhead that partially offsets savings",
        "probability": "LOW",
        "impact": "If compression adds bundle_compression_log fields to manifests (~200 tokens), net savings are reduced",
        "mitigation": "Log compression metadata to session-metrics (separate file), NOT to manifest. Manifest stays clean. G007 gate catches any cost_ratio increase from overhead.",
        "tradeoff": "Forensic trail for compression is in session-metrics, not manifest; slightly harder to audit per-manifest but preserves manifest size discipline"
      },
      {
        "risk": "Losing context depth for W3 INSERTION agents (deep synthesis specialists)",
        "probability": "MEDIUM",
        "impact": "W3 agents rely on full NECTAR for cross-session synthesis. C1 filter that removes MEDIUM NECTAR entries may thin cross-investigation signals.",
        "mitigation": "Implement wave-aware compression: W1/W2 use aggressive compression (C1+C2+C3); W3 uses light compression (C2 only, preserve full NECTAR for synthesis depth). Wave parameter already exists in spawn template.",
        "tradeoff": "W3 savings are lower (C2 only = ~70-80% pollen savings, but full NECTAR preserved). W3 bundle still 30-40% smaller, but not 50-70%. Accept reduced target for W3."
      }
    ],
    "compression_targets_by_wave": {
      "W1_LIFTOFF": {
        "compression_methods": ["C1", "C2", "C3"],
        "expected_size_reduction": "55-70%",
        "justification": "W1 agents do triage/routing (haiku model). They need compass navigation signals but not full NECTAR depth. Full compression safe."
      },
      "W2_CRUISE": {
        "compression_methods": ["C1", "C2"],
        "expected_size_reduction": "45-60%",
        "justification": "W2 agents do feature work (sonnet model). C1+C2 reduces NECTAR+pollen; full boilerplate preserved for complex task reasoning."
      },
      "W3_INSERTION": {
        "compression_methods": ["C2"],
        "expected_size_reduction": "20-35%",
        "justification": "W3 agents do deep synthesis (sonnet model). Full NECTAR preserved for cross-session pattern recognition. Only pollen dedup applied."
      }
    }
  },

  "implementation_checklist": {
    "instrumentation_required_before_phase1": [
      "Add bundle_size_bytes field to 0x_spawn_template.py assemble_bundle() output — write to manifest at spawn time",
      "Add bundle_token_count field (len(bundle) // 4) to manifest at spawn time",
      "Add NECTAR section bytes and pollen section bytes breakdown to session-metrics entry (not manifest)",
      "Add manifest_write_latency_ms timing hook (task_complete_ts to manifest_mtime)",
      "Verify context_pressure() from phase2 instrumentation is logging to session-metrics per spawn"
    ],
    "compression_implementation_sequence": [
      "1. Implement C2 (pollen_compressor.py) first — lowest risk, high ROI",
      "2. Implement C1 (NECTAR filter) with agent_type -> threshold config mapping",
      "3. Implement C3 (template conditionals) with task_complexity parameter",
      "4. Add wave-aware compression dispatch (W1/W2/W3 get different method sets)",
      "5. Add bundle_mode=full escape valve to agent spawn protocol"
    ]
  },

  "success_criteria": {
    "primary": "Bundle size reduction >= 50% for W1 LIFTOFF spawns (most frequent wave)",
    "secondary": "All safety gates G001-G007 pass (no regression on FFMx, agent quality, or capability probes)",
    "tertiary": "FFMx post-compression >= 44.4 (stable or improved — compression should increase FFMx by improving cost efficiency)",
    "stretch": "Bundle size reduction >= 65% for W1 spawns AND FFMx increases to >= 48.0 (driven by cost_efficiency improvement from 0.54 to ~0.47)"
  },

  "related_artifacts": {
    "ffmx_baseline": "forensics/artifacts/2026-04-28/150200Z_ffmx-formula-breakdown_force-multiplier-index_data-analyst_001.md",
    "compression_design": "forensics/manifests/2026-04-28/14-00-00Z_manifest_velocity-acceleration_documentation-engineer_001.json",
    "phase2_shadow_instrumentation": "forensics/manifests/2026-04-28/05-28-47Z_manifest_phase2-shadow-mode_python-pro_001.json",
    "phase1_instrumentation": "forensics/manifests/2026-04-28/14-00-00Z_manifest_phase1-instrumentation_python-pro_001.json"
  }
}
