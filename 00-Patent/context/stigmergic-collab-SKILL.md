---
name: stigmergic-collab
description: >-
  Realtime multi-agent coordination via an append-only JSONL blackboard. Use
  when 2+ agents are spawned in the same wave and their file surfaces overlap
  (parallel E-bearing work on the same charter). Prevents file collisions and
  enables live handoffs without message-passing. Trigger: "collab", "realtime
  coordination", "parallel agents same files", "blackboard", "CLAIM",
  "HANDOFF", "shared surface".
type: knowledge
triggers:
  - collab
  - blackboard
  - CLAIM
  - HANDOFF
  - realtime coordination
  - parallel agents same files
  - shared surface
_bundle_note: "FULL COPY from .agents/skills/stigmergic-collab/SKILL.md for publication-prep-2026-05-25. Supports whitepaper §4.3 (stigmergic blackboard claim) and the shape multi_agent.realtime_collab.blackboard (current_count=1, first instance commit 07daafe0). Key evidence: 13 events, 2-hour session, zero collisions, one live HANDOFF — all validated."
---

# stigmergic-collab — Realtime Blackboard Protocol

When 2+ agents operate in the same wave on overlapping file surfaces, async
manifest handoff alone is insufficient: by the time one agent writes its final
manifest, the other may already have claimed the same file. This skill
describes the **append-only JSONL blackboard** — the realtime coordination
layer that sits BELOW manifest exchange and ABOVE individual agent prompts.

**Relation to stigmergy-only doctrine:** The blackboard IS the stigmergic
layer for realtime work. Agents do not message each other; they write
structured events to a shared file in `forensics/manifests/{date}/` and
read the tail before each new action. The filesystem is still the only
coordination channel — the blackboard just gives it a finer-grained grammar.

---

## The pattern in one paragraph

When two or more agents must collaborate on overlapping file surfaces in real
time, they coordinate via an append-only JSONL blackboard at a deterministic
path in `forensics/manifests/{YYYY-MM-DD}/`. Before editing any file, each
agent appends a `CLAIM` line citing the file paths it is about to touch.
After completing a chunk of work, it appends a `COMPLETE` line citing the
same files plus any notes for the other agent. When one agent notices an
opportunity or dependency for the other, it appends a `HANDOFF` line tagged
with a compass bearing. Before appending any new `CLAIM`, the agent reads
the last ~30 lines of the blackboard (tail-read discipline) to discover what
its peers currently own. The result: zero file collisions and explicit live
handoffs without any message-passing.

**Validated in commit `07daafe0`:** VISIONARY + ARTISAN ran 13 blackboard
events across a 2-hour session (7 doctrine components + 7 UI files). Zero
collisions. One live HANDOFF (ARTISAN registered VISIONARY's 7 components as
live palette items in `draggable-primitives.js` the moment VISIONARY's
COMPLETE line cited them). Blackboard at:
`forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`

---

## Blackboard path convention

```
forensics/manifests/{YYYY-MM-DD}/collab-realtime__{team-label}.jsonl
```

Where `{team-label}` is the kebab-toast team identifier already used in
the wave's filename grammar (e.g. `visionary-artisan`, `maker-bridge`).

The file is created by the queen / dispatcher at spawn time with an opening
`channel_open` event. It is never written to `forensics/ephemeral/` — it
lives directly in `manifests/` because it IS the canonical coordination
record, not an ephemeral scratch.

---

## Event grammar

Each line is one JSON object. One line per event. Append only.

### STARTUP
Presence signal. Each agent appends one STARTUP line when it begins work.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "STARTUP",
  "mission": "<mission-w3w>",
  "planned_deliverables": ["D1: ...", "D2: ..."],
  "note": "<free-form context>"
}
```

### CLAIM
Lock declaration. Append BEFORE editing any file. Lists every path the
agent intends to touch in this work chunk.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "CLAIM",
  "files": ["abs/or/repo-relative/path.jsx", "..."],
  "purpose": "<80 chars: what this chunk does>"
}
```

### COMPLETE
Work-finished signal. Append AFTER finishing the chunk.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "COMPLETE",
  "files": ["path.jsx", "..."],
  "notes": "<what was built/changed>",
  "handoff_to_{peer}": "<optional: specific note for the other agent>"
}
```

### HANDOFF
Bearing-tagged opportunity. Append when you notice something the other
agent should act on.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "HANDOFF",
  "bearing": "E|N|S|W",
  "to": "<peer-agent-type>",
  "note": "<what the opportunity is, 120 chars>",
  "ref_file": "<the file or path this refers to>"
}
```

### REFUSE (new grammar, 2026-05-25)
Graph-visible refusal. Releases the CLAIM; does NOT end the session.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "REFUSE",
  "files": ["<the paths you had claimed>"],
  "reason": "<which lens fired: dual-use | scope | authorization | cumulative | intent | alternative | conversation>",
  "rationale": "<400 chars full seven-lens analysis>",
  "alt_routing": "<what legitimate adjacent work exists, if any>"
}
```

---

## Tail-read discipline (mandatory before every CLAIM)

Before appending any CLAIM, the agent reads the last ~30 lines of the
blackboard:

```bash
tail -30 forensics/manifests/$(date +%Y-%m-%d)/collab-realtime__{team-label}.jsonl
```

A CLAIM is "active" from the moment it appears until a matching COMPLETE
appears citing the same file. Any file in an active CLAIM is exclusive to
the claiming agent.

---

## Worked example (commit 07daafe0)

The reference implementation is
`forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`.

Key sequence:
1. Queen opens channel: `channel_open` with forbidden zones for unrelated live files.
2. VISIONARY: `STARTUP` → `CLAIM` (7 doctrine components) → `COMPLETE` (ships all 7, notes for ARTISAN).
3. ARTISAN: `STARTUP` → `CLAIM` (6 UI files) → reads VISIONARY's `COMPLETE` → registers VISIONARY's 7 components as live palette items in `draggable-primitives.js` within the same ARTISAN `COMPLETE`.
4. ARTISAN: `HANDOFF` bearing=E to VISIONARY pointing at an open slot in `VibeStudioTab.jsx`.
5. VISIONARY: `COMPLETE` on CreaturesBoard, then `HANDOFF` bearing=E to ARTISAN.

Result: 13 events, zero collisions, one explicit live handoff that caused
immediate downstream action (doctrine components wired into the canvas
palette the moment they shipped).

---

## When NOT to use this pattern

- **Single-agent tasks** — no coordination needed; write the manifest.
- **Purely sequential work** — async manifest handoff is sufficient (no overlap).
- **Cross-session coordination** — blackboards are ephemeral to one wave.
  Cross-session work uses charter + manifest routing, not a blackboard.
- **>4 agents** — combinatorial tail-read complexity grows; consider
  partitioning file surfaces so each sub-pair gets its own blackboard.

---

## See also

- `collab/SKILL.md` — compact always-inherited operational subset of this skill
- `forage/SKILL.md` — when wide mode involves 2+ agents on overlapping surfaces, wire a blackboard
- `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` — reference implementation
