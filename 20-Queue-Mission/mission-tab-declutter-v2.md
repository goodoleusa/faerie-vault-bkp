---
type: mission-node
status: draft
created: 2026-05-26
tags: [swarmy-oh-unified, bearing-s]
task_id: mission-tab-declutter-v2
mission: swarmy-oh-unified
bearing: S
timestamp: 2026-05-26T15:11:27
node_path: 20-Mission-Graph/mission-tab-declutter-v2.md
source_manifest: /mnt/d/0local/gitrepos/faerie2/forensics/manifests/2026-05-24/20260524T223159Z_manifest_swarmy-oh-unified_mission-tab-declutter-v2_frontend-design.json
prev_entry_hash: 87f35b848e80ef21851343f2a96f42e94502d38b0fdeb6db4bbf823fc5fdc213
entry_hash: 19754cc5b562598ed42641d4d11d19c15dd7aded695fdf14f09224537135756d
---

# mission-tab-declutter-v2

**Mission:** swarmy-oh-unified
**Status:** draft
**Bearing:** South (ship)
**Completion:** `promote` — Mission tab now has one primary viz (GraphToggle/TableGridGraph). SwarmLivePanel is always-mounted, CSS-transitioned via data-open attribute — no remount, no SSE disconnect on toggle. Chat drawer removed from Mission tab entirely. Visual rule enforced: at most one source of separation per panel; whitespace instead of nested borders.

## Summary

Mission tab: single hero graph, edge-tab live drawer, no competing panels

## Outbound Edges

*(no outbound edges)*

## Inbound Edges

*(no inbound edges)*
