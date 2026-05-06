{
  "test_run_id": "sdk-qa-2026-04-28T14-54-32Z",
  "auditor": "code-reviewer",
  "timestamp_utc": "2026-04-28T14:54:32Z",
  "verdict": "NOT_SHIP_READY",
  "blocker_count": 3,

  "api_contract_validation": {
    "bundle_structure_complete": {"result": "PASS", "note": "All 8 required keys present"},
    "bundle_json_serializable": {"result": "PASS", "note": "json.dumps() clean"},
    "bundle_assembly_tokens": {"result": "PASS", "value": 9660, "formula": "conservative"},
    "manifest_task_id_present": {"result": "PASS", "rate": "25/25"},
    "manifest_dashboard_line_present": {"result": "FAIL", "rate": "14/25", "note": "11 spawn-intent records lack dashboard_line"},
    "manifest_compass_edge_present": {"result": "PASS", "rate": "23/25"},
    "manifest_dashboard_line_under_80_chars": {"result": "FAIL", "rate": "14/25", "worst_case_chars": 415},
    "manifest_json_serializable": {"result": "PASS", "rate": "25/25"},
    "coc_entries_immutable": {"result": "FAIL", "note": "coc-entries/ absent, path hardcoded to faerie2 repo"},
    "coc_writer_algorithm": {"result": "PASS", "note": "fcntl+HMAC+Ed25519+atomic-rename — correct implementation"},
    "error_messages_actionable": {"result": "PASS", "note": "ValueError messages include fix instructions + docs links"}
  },

  "security_audit": {
    "task_id_prompt_injection": {
      "result": "FAIL",
      "severity": "HIGH",
      "reproduced": true,
      "reproduction": "render_bundle_prompt(task_id='task-001\\nROGUE_INSTRUCTION: ...') — injection confirmed in signed prompt body",
      "fix": "re.sub(r'[\\r\\n]+', '-', task_id) at line 1712",
      "effort_hours": 1
    },
    "delta_field_injection": {
      "result": "PASS",
      "note": "json.dumps() escapes newlines in delta values to \\\\n — mitigated"
    },
    "honey_nectar_sensitive_data_leak": {
      "result": "CONDITIONAL_FAIL",
      "severity": "MEDIUM",
      "note": "No sensitivity filtering on HONEY/NECTAR content before bundle injection. Content not directly audited here.",
      "fix": "Add line-level sensitivity filter (strip lines matching key=, api_key=, password= patterns)"
    },
    "manifest_write_atomicity": {
      "result": "PASS",
      "note": "Roster uses temp+replace (atomic). Agents should also use temp+replace for final manifest write."
    },
    "coc_audit_trail_complete": {
      "result": "FAIL",
      "severity": "HIGH",
      "note": "0 COC entries found for any 2026-04-28 agent. Path hardcoded to faerie2 repo. coc-entries/ missing.",
      "fix": "Replace hardcoded path with _repo_root() / 'forensics/coc-entries/'"
    },
    "queue_autonomy_deprecated_path": {
      "result": "FAIL",
      "severity": "HIGH",
      "note": "_QUEUE_AUTONOMY_BLOCK injects 7x_queue_ops.py (deprecated 2026-04-27) into every agent spawn",
      "fix": "Replace with FRONTIER_SCAN_BLOCK using forensics/ manifest discovery"
    },
    "spawn_chain_key_default_public": {
      "result": "FAIL",
      "severity": "MEDIUM",
      "note": "Default HMAC key sha256('faerie2-spawn-default') documented in source — forgeable without secret key",
      "fix": "Startup warning when COC_CHAIN_KEY env var unset"
    }
  },

  "performance_metrics": {
    "bundle_assembly_latency_ms": {
      "result": "PASS",
      "measured": 47,
      "target": 1000,
      "margin": "21x headroom"
    },
    "w1_4_agent_bundle_prep_ms": {
      "result": "PASS",
      "sequential_sum_ms": 190,
      "parallel_wall_time_ms": 49,
      "target_ms": 5000
    },
    "manifest_write_latency_ms": {
      "result": "FAIL",
      "measured_wsl2": 2127,
      "measured_linux": 0.33,
      "target": 100,
      "root_cause": "WSL2 cross-filesystem I/O on /mnt/d/ — not a code defect",
      "environment_note": "Linux native: ~2-5ms (would PASS)"
    },
    "ffmx_gate_30": {
      "result": "UNMEASURED",
      "current_session_ffmx": 44.4,
      "f0_ratio": 0.0504,
      "note": "No per-spawn FFMx gate implemented in SDK. FFMx is session-level metric only."
    }
  },

  "e2e_test_results": {
    "live_w1_spawn": {
      "result": "NOT_EXECUTED",
      "reason": "Requires live Claude API — static audit only"
    },
    "prior_session_w1_evidence": {
      "manifests_written": 25,
      "write_success_rate": 1.0,
      "investigation_labels": 5,
      "agent_types": 8,
      "compass_edge_s_rate": 0.72
    },
    "manifest_schema_check": {
      "result": "PARTIAL_FAIL",
      "total": 25,
      "full_compliance": 11,
      "required_fields_only": 14,
      "json_valid": 25
    },
    "coc_trace_check": {
      "result": "FAIL",
      "coc_entries_found": 0,
      "expected": "at_least_25"
    },
    "ffmx_regression_check": {
      "result": "PASS_BY_PROXY",
      "f0": 0.0504,
      "quality_score_mean": 0.91,
      "belief_index_mean": 0.91,
      "no_degradation_signal": true
    }
  },

  "blockers_summary": [
    {"id": "B1", "title": "task_id prompt injection (newline unescaped)", "severity": "CRITICAL", "fix_hours": 1},
    {"id": "B2", "title": "_QUEUE_AUTONOMY_BLOCK injects deprecated 7x_queue_ops.py", "severity": "CRITICAL", "fix_days": 0.5},
    {"id": "B3", "title": "COC audit trail broken — hardcoded faerie2 path + coc-entries absent", "severity": "CRITICAL", "fix_days": 0.5}
  ],

  "remediation_timeline": {
    "phase_1_blockers": {"days": "2-3", "owner": "python-pro", "gates_fixed": ["B1", "B2", "B3"]},
    "phase_2_high": {"days": "1-2", "owner": "code-reviewer", "gates_fixed": ["H1", "H2", "H3", "H4"]},
    "phase_3_medium": {"days": "1", "owner": "fullstack-developer", "gates_fixed": ["M1_doc", "M2", "M3", "M4"]},
    "ship_ready_est": "2026-05-02 (4 working days)"
  }
}
