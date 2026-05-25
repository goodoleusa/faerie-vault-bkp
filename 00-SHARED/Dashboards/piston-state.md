---
type: dashboard
status: active
tags: [dashboard, piston, waves, queue, agents]
parent: Dashboards/INDEX
up: Dashboards/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:7d9d3f0aa2b24664bd5bbe6af5881c0449be3347a3b69f7fbd5f35fa75b80235
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](INDEX.md) · [⌂ Home](../../HOME.md)

# Piston State

Narrative for understanding current wave, queue depth, and agents in flight.
For live data: `python3 ~/.claude/scripts/9x_lean_query.py --get-wave`

---

## Reading Piston State

```bash
python3 ~/.claude/scripts/9x_lean_query.py --get-all
```

Output:
```
wave=W2  context=42%  agents=2  queue=pending:8,queued:33,complete:127
```

---

## Wave States

| State | Meaning | What to do |
|-------|---------|------------|
| W1 | First-stage agents running or just ran | Wait; W2 launches after W1 returns |
| W2 | Feature agents running or just ran | Wait; W3 launches after W2 returns |
| W3 | Background synthesis running | Normal — W3 runs async |
| idle | No wave active | `/faerie` to start or `/run` to claim tasks |

---

## Context States

```
context_pct: 42    ← current fill %
wave_state: W2     ← last wave launched
agents_in_flight: 2 ← agents still running
deferred_reason: null ← why wave was deferred (if applicable)
```

**Healthy session arc:**
```
W1 launches → W1 returns (context ~15%) → W2 launches → W2 returns (context ~30%)
→ respond → W3 launches (context ~35%) → W3 runs in background
→ auto-compact at ~85%+ if session is long
```

---

## Queue Sections

The queue is organized into sections that map to wave assignment:

| Section | Priority | Wave | Description |
|---------|----------|------|-------------|
| Blockers | HIGH | W1 | Tasks blocking other tasks |
| Critical path | HIGH | W1/W2 | Highest-value milestone work |
| Breadth | MED | W2 | Parallel work, non-blocking |
| Backlog | LOW | W3/bg | Future work, no urgency |

---

## Agents In Flight

When `agents_in_flight > 0`, agents are running in background (W3 or background tasks).
These will write manifests when complete. `/handoff` collects them.

To check which agents are in flight:
```bash
ls ~/.claude/hooks/state/wave*-*-result.json | \
  xargs -I{} python3 -c "import json,sys; d=json.load(open('{}'));
print(d.get('agent','?'), d.get('status','?'))"
```

---

## Related

- [[system-health]] — full health including eval and memory
- [[../Architecture/piston-waves]] — piston technical reference
- [[../Hive/piston-rocket-physics]] — the wave model explained
- [[../Skills-Reference/faerie]] — /faerie skill reference
