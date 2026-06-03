---
type: mission-node
status: final
created: 2026-04-27
tags: [faerie2-shipping, bearing-s]
task_id: ship-queue-deprecation-audit
investigation_label: faerie2-shipping
compass_edge: S
timestamp: 2026-04-27T14:30:15
node_path: mission-graph/ship-queue-deprecation-audit.md
source_manifest: /mnt/d/0local/gitrepos/faerie2/forensics/manifests/2026-04-27/14-30-15Z_manifest_ship-queue-deprecation-audit_shipping-orchestrator_001.json
prev_entry_hash: 27cf470df6192e374fec681a277f438b4f56c36830253e6e45981ceb0fd689a1
entry_hash: 0ca0a1560331b5167394dbec9f6f5b307319654bdd454f6e77c3b04b9a0092f4
---

# ship-queue-deprecation-audit

**Mission:** faerie2-shipping
**Status:** final
**Bearing:** 🔓 South

## Summary
Queue fully deprecated; compass graph active. One blocker: 8x_taskcreate_to_queue references non-existent 7x_queue_ops.py. Ready for compass-only routing.
## Eval Metrics
- **Quality:** 0.85
- **Belief:** 0.82

## Key Insights
- deprecated_hooks: {'count': 3, 'status': 'all_have_shims', 'shims_emit_deprecation_warning': True, 'delegate_to_mission_graph': True}
- critical_blocker: {'file': 'hooks/8x_taskcreate_to_queue.py', 'issue': 'calls non-existent 7x_queue_ops.py', 'impact': 'TaskCreate tasks lost; never reach mission graph', 'severity': 'HIGH', 'fix': 'convert_to_mission_shim'}
- compass_replacement_status: {'mission_autorun': 'ACTIVE', 'mission_janitor': 'ACTIVE', 'intent_to_mission': 'ACTIVE', 'mission_graph_cli': 'ACTIVE', 'manifest_schema_ready': True}
- **Discovery:** [{'task': 'fix-taskcreate-to-mission', 'description': 'Convert 8x_taskcreate_to_queue.py to 8x_taskcreate_to_mission_shim.py; remove 7x_queue_ops.py dependency', 'investigation_label': 'faerie2-shipping', 'priority': 'HIGH', 'agent_type_hint': 'code-reviewer'}]


## Next Steps
(no next task)
