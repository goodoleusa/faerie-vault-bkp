---
type: reference
status: active
tags: [skill, droplet, insight, capture]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:fd7b043b992f35b565f065425ed409860a20d91ec5e9283e67137bba482076af
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /droplet — Insight Capture

Writes an insight to the droplets vault. Use when something clicks —
a cross-domain connection, a surprise, a gut signal.

---

## Invocation

```
/droplet
```

Interactive: faerie asks for the insight text and category, then appends
to the active LIVE-{date}.md droplet file.

---

## Droplet vs Pollen

| Droplet | Pollen |
|---------|--------|
| Inspired thought, cross-domain connection | Technical finding, data-rooted |
| "This pattern feels like X in domain Y" | "3 database constraints caught errors at line 120" |
| Written before reasoning (naive moment) | Written during analysis |
| Lives in vault Droplets/ | Lives in pollen-{SID}.md |

Write droplets when the signal is: "wait, this is interesting." Before your brain explains it.

---

## Format

```markdown
### 2026-04-24T15:30:00Z — documentation-engineer
**agent_run_id:** ar-20260424-abc123
**cat:** CONNECTION
**pri:** MED

Two-layer validation appears in API + SDK + CLI simultaneously.
Defense in depth is not just security architecture — it is validation architecture.
Every layer should validate independently, not trust upstream.

---
```

---

## Categories

| Category | When |
|----------|------|
| `HEADLINE` | Assumption just flipped or broke |
| `CONNECTION` | Observation from domain A explains domain B |
| `FIRST_IMPRESSION` | Friction or hesitation mid-explanation |
| `TECHNIQUE` | Working method that solved something |
| `OBSERVATION` | Generic noticing (lower value — use sparingly) |

---

## Promotion

HIGH priority droplets → promoted to NECTAR at /handoff.
All droplets → discoverable by future agents at task boundaries.
One droplet per run is mandatory minimum.

---

## Related

- [[handoff]] — /handoff promotes HIGH droplets to NECTAR
- [[../Hive/stigmergic-recursion]] — how agents discover droplets
- [[../Glossary/terms]] — droplet, pollen, NECTAR defined
