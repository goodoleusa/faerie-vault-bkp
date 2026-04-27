---
type: blueprint
blueprint_id: blueprint_droplet
name: Droplet
version: "1.1"
created: 2026-03-29
updated: 2026-03-29
status: active
---

# Blueprint: Droplet

Real-time insight captures. Minimal schema — speed and honesty of capture over structure.
Droplets are the naive-observer moment before expertise filters it out. Bad droplets cost
nothing; lost insights cost everything. Written to LIVE-{date}.md append-only files.

## Metadata

| Field | Value |
|-------|-------|
| ID | blueprint_droplet |
| Output dir | 00-SHARED/Dashboards/Droplets/ |
| Agent types | All agents |
| Promotion target | NECTAR (via memory-keeper at /handoff) |
| File pattern | `LIVE-YYYY-MM-DD.md` (append-only, multiple agents share one daily file) |

## File Convention

- One file per calendar day: `LIVE-YYYY-MM-DD.md`
- Multiple agents append to the same file in the same session
- File itself has no frontmatter — individual droplets have inline metadata
- Never edit existing droplets — append only

## Droplet Format

Each droplet is a timestamped H3 block:

```markdown
### {YYYY-MM-DDTHH:MM:SSZ} — {agent_type}
**session:** {session_id}
**cat:** OBSERVATION | CONNECTION | HYPOTHESIS | TECHNIQUE | FIRST_IMPRESSION
**pri:** HIGH | MED | LOW

{insight body — 1-5 sentences. Poetic, intuitive, unfiltered. The seed of a thought,
not a conclusion. Write what you sense before you reason about it.}

---
```

## Category Guidance

| Cat | When |
|-----|------|
| OBSERVATION | Something noticed that doesn't fit a clean category yet |
| CONNECTION | Spans 2+ source documents or unrelated concepts — the "wait, this reminds me of..." |
| HYPOTHESIS | A tentative explanation — not verified, just worth tracking |
| TECHNIQUE | A reusable method just discovered or validated |
| FIRST_IMPRESSION | First contact with a dataset/document — before deep analysis |

## Structure Rules

- Body: 1-5 sentences. Unfiltered. Impressionistic is fine.
- Write the droplet BEFORE reasoning about it — the naive moment is the value
- `cat=FIRST_IMPRESSION` on first contact with any dataset (write before deep analysis)
- `cat=CONNECTION` when the insight spans 2+ source documents
- `pri=HIGH` → also emit to `~/.claude/memory/REVIEW-INBOX.md`
- Droplets are never deleted, only promoted via memory-keeper

## Validation Rules

- Timestamp must be ISO8601 to the second with Z suffix
- `cat` must be one of: OBSERVATION, CONNECTION, HYPOTHESIS, TECHNIQUE, FIRST_IMPRESSION
- `pri` must be one of: HIGH, MED, LOW
- Body must be non-empty (minimum 1 sentence)
- Append-only — no editing existing droplets

## Example Output

See `00-SHARED/Agent-Outbox/droplets/example-droplet-LIVE.md`
