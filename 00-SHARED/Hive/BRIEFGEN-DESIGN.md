	---
type: dead-drop
drop_type: HANDOFF
from: python-pro
to: human
read: false
created: 2026-03-27
tags: [briefgen, agent-architecture, design]
doc_hash: sha256:296d298eb00f48f38992c062ecc006f4e33625ea924f123aa5c120b59a02e4a7
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:23Z
hash_method: body-sha256-v1
---

# Agent Brief Generator — Design Document

> `briefgen.py` lives at `{repo}/.claude/lib/briefgen.py` in both `data-analysis-engine` and `cybertemplate`.
> This document covers integration, vault path spec, example outputs, and the faerie roundup enhancement.

---

## 1. Vault Path Specification

```
{CT_VAULT}/Session-Briefs/{investigation_id}/{phase}/{run_id}-{brief_type}-{YYYY-MM-DD}.md
```

**Examples:**
```
00-SHARED/Session-Briefs/inv-critical-exposure/EXTEND/RUN009-stage-summary-2026-03-27.md
00-SHARED/Session-Briefs/inv-critical-exposure/EXTEND/RUN010-finding-promotion-2026-03-28.md
00-SHARED/Session-Briefs/inv-critical-exposure/PUBLISH/RUN011-session-summary-2026-03-29.md
00-SHARED/Session-Briefs/inv-critical-exposure/EXTEND/RUN009-blocker-flag-2026-03-27.md
```

**Brief types (`brief_type` enum):**

| Value | When to use |
|---|---|
| `session-summary` | End of full session — covers all work done that session |
| `stage-summary` | End of a pipeline stage (CLEAN, EXTEND, CURATE, etc.) |
| `finding-promotion` | When agent finds a Tier 1 / smoking-gun finding |
| `blocker-flag` | When agent hits a hard blocker that needs human decision |

**Local fallback** (when `CT_VAULT` / `FAERIE_VAULT` not set):
```
{repo}/.claude/memory/briefs/{investigation_id}/{phase}/{run_id}-{brief_type}-{date}.md
```

---

## 2. Agent Integration (TRAINING block in agent prompt)

Add these lines to the TRAINING block in any spawned agent's prompt. The block runs
**after OTJ reflection, before returning output to the parent.**

```python
# ── BRIEFGEN SHUTDOWN ──────────────────────────────────────────────────
import os, sys
from pathlib import Path

_LIB = Path(__file__).resolve().parent  # adjust if called from scripts/
if str(_LIB.parent / ".claude" / "lib") not in sys.path:
    sys.path.insert(0, str(_LIB.parent / ".claude" / "lib"))

try:
    from briefgen import AgentBriefGenerator, BriefInput, BriefType
    _gen = AgentBriefGenerator(
        session_id=os.environ.get("CLAUDE_SESSION_ID", f"session-{os.getpid()}"),
        repo_root=Path(__file__).resolve().parent,   # or explicit repo path
    )
    _result = _gen.write(BriefInput(
        agent_type="data-scientist",                 # change per agent type
        investigation_id=os.environ.get("INVESTIGATION_ID", "inv-default"),
        run_id=os.environ.get("PIPELINE_RUN_ID", "RUN000"),
        phase="EXTEND",                              # set to current phase
        brief_type=BriefType.STAGE_SUMMARY,
        narrative_body=_NARRATIVE,                   # str built during the run
        hypothesis_touches=_HYPOTHESIS_DELTAS,       # dict[str, float]
        evidence_tier_touched=_TIERS_TOUCHED,        # list[int]
        vault_parent=f"sprint-{os.environ.get('SPRINT_ID', 'unknown')}",
    ))
    print(f"[shutdown] Brief written: {_result.path}")
except Exception as _e:
    print(f"[shutdown] briefgen failed (non-fatal): {_e}", file=sys.stderr)
# ── END BRIEFGEN SHUTDOWN ───────────────────────────────────────────────
```

**Three variables the agent builds during its run:**

```python
_NARRATIVE = """
## What We Did
- Ran statistical battery on IP cluster data (n=863 events)
- Applied Bonferroni correction across 4 test families

## Key Findings
- 194.58.46.116 confirmed anomalous at p=0.006 post-correction
- H2 confidence raised from 0.72 → 0.78

## Open Questions
- Need second independent source for mrcomq attribution
- BGP withdrawal timing needs RPKI cross-check

## Next Steps
- evidence-curator: promote 194.58.46.116 to Tier 1
- research-analyst: mrcomq second source search
"""

_HYPOTHESIS_DELTAS = {"H2": 0.78, "H3": 0.80}
_TIERS_TOUCHED     = [1, 2]
```

---

## 3. Example Brief Outputs

### Example A — stage-summary (data-scientist, EXTEND phase)

```yaml
---
type: brief
status: pending
created: 2026-03-27
updated: 2026-03-27
tags: [data-scientist, inv-critical-exposure, EXTEND, stage-summary]
brief_type: stage-summary
agent_type: data-scientist
agent_version: 2026-03-19_0.94
run_id: RUN009
phase: EXTEND
investigation_id: inv-critical-exposure
faerie_session: session-abc123
hypothesis_touches:
  H2: 0.78
  H3: 0.80
evidence_tier_touched: [1, 2]
git_commit: cedbfa6
coc_entry_hashes:
  - 3f4a8c12bd9e...
  - 7a1d5f22c044...
coc_hash_count: 47
parent: ["[[critical-exposure-sprint-4]]"]
sibling: ["[[RUN009-session-summary]]"]
child: []
memory_lane: session
promotion_state: capture
chain_id: inv-critical-exposure
agent_hash: 705b75631d4b4472
agent_author: data-scientist
---

<!-- AGENT-GENERATED-START -->
# Agent Brief — RUN009 / EXTEND (data-scientist)

> Generated: 2026-03-27T18:00:00+00:00  |  Agent: `data-scientist` v`2026-03-19_0.94`  |  Commit: `cedbfa6`

## What We Did
...

## Navigation (ExcaliBrain)
- Parent: [[critical-exposure-sprint-4]]
- Sibling: [[RUN009-session-summary]]
- Hypothesis: [[H2]] (confidence post-run: `0.78`)
- Hypothesis: [[H3]] (confidence post-run: `0.80`)

## Forensic Linkage
Chain-of-custody entries that drove conclusions:
- `3f4a8c12bd9e...`
- `7a1d5f22c044...`

Total entries this session: **47**
Verify: `python3 .claude/hooks/forensic_coc.py verify --session session-abc123`
<!-- AGENT-GENERATED-END -->

<!-- HUMAN-ANNOTATIONS-START -->
## Your Annotations
_preserved across reruns_

## Review Decision
- [ ] Promote to NECTAR
```

---

### Example B — finding-promotion (evidence-curator, Tier 1 find)

```yaml
type: brief
brief_type: finding-promotion
agent_type: evidence-curator
run_id: RUN009
phase: CURATE
investigation_id: inv-critical-exposure
hypothesis_touches:
  H2: 0.92
evidence_tier_touched: [1]
```

Narrative body includes:
```markdown
## What Was Found
194.58.46.116 promoted to Tier 1. Bonferroni-corrected Fisher's exact p=0.006 (n=863,
4-family correction). Meets threshold: independent lab replication possible from public BGP data.

## Why It Matters
Anchors H2 (Packetware data pipeline) to a statistically confirmed anomaly on the Frankfurt
OVH cluster. Combined with certificate evidence this is publishable.

## Evidence Chain
- Source: stat_battery_20260322.py → audit_results/RUN009-stat-ip-cluster.json
- COC entries: [hash1, hash2, hash3]
- Prior tier: 2 → New tier: 1

## Open Questions
- Still need routing table proof of BGP announcement timing
```

---

### Example C — blocker-flag (research-analyst, attribution gap)

```yaml
type: brief
brief_type: blocker-flag
agent_type: research-analyst
run_id: RUN010
phase: EXTEND
investigation_id: inv-critical-exposure
```

Narrative body:
```markdown
## Blocker
mrcomq / "The Com" attribution is stalled. Only one source (Perplexity summary, no
primary citation). Cannot advance H4 to Tier 1 without second independent source.

## What Was Tried
- Shodan historical records: no hit on handle
- GitHub search: no public profile match
- WHOIS history on associated domain: inconclusive

## What Needs Human Decision
Researcher must decide: (a) deprioritize H4, (b) authorise deep-web forum search,
or (c) publish with explicit "unverified" caveat.

## Next Steps for Next Agent
If (b) approved: search-specialist with query bundle in scripts/audit_results/mrcomq-leads-RUN010.json
```

---

## 4. Faerie Roundup Enhancement

`/faerie` at session start should read the latest brief from each investigation folder
and merge with the existing `faerie-brief.json` context. Pseudocode:

```python
def faerie_roundup_briefs(vault_root: Path, investigations: list[str]) -> list[dict]:
    """
    For each investigation, find the most recent brief file in any phase.
    Returns list of frontmatter dicts for context injection.
    """
    briefs = []
    briefs_root = vault_root / "Session-Briefs"
    if not briefs_root.exists():
        return briefs

    for inv_id in investigations:
        inv_dir = briefs_root / inv_id
        if not inv_dir.exists():
            continue
        # Glob all .md files across all phase subdirs, sort by mtime descending
        candidates = sorted(
            inv_dir.glob("**/*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        # Include: most recent of each brief_type (session, stage, finding, blocker)
        seen_types: set[str] = set()
        for md_file in candidates:
            fm = _parse_frontmatter(md_file)  # extract YAML block
            if not fm or fm.get("type") != "brief":
                continue
            bt = fm.get("brief_type", "unknown")
            if bt not in seen_types:
                seen_types.add(bt)
                fm["_source_path"] = str(md_file)
                # Include human annotations if present
                content = md_file.read_text(encoding="utf-8")
                if "<!-- HUMAN-ANNOTATIONS-START -->" in content:
                    ann_section = content.split("<!-- HUMAN-ANNOTATIONS-START -->", 1)[1]
                    fm["_human_annotations"] = ann_section[:2000]  # cap at 2K
                briefs.append(fm)
            if len(seen_types) >= 4:  # got all brief types for this inv
                break

    return briefs


def inject_briefs_into_context(faerie_brief_json: dict, briefs: list[dict]) -> dict:
    """Merge brief summaries into the faerie session context."""
    faerie_brief_json["recent_agent_briefs"] = [
        {
            "investigation": b.get("investigation_id"),
            "run_id": b.get("run_id"),
            "phase": b.get("phase"),
            "brief_type": b.get("brief_type"),
            "agent_type": b.get("agent_type"),
            "updated": b.get("updated"),
            "promotion_state": b.get("promotion_state"),
            "hypothesis_touches": b.get("hypothesis_touches", {}),
            "human_annotations": b.get("_human_annotations", ""),
            "path": b.get("_source_path", ""),
        }
        for b in briefs
    ]
    return faerie_brief_json
```

**Where this runs:** In the `/faerie` command startup block, after loading `faerie-brief.json`
and before building the context summary. The resulting `recent_agent_briefs` list becomes
part of the context bundle injected into the session.

**Human annotation loop:** If any brief has `promotion_state: capture` AND human annotations
are non-empty (human has annotated it), faerie surfaces a prompt:
```
[BRIEF READY] RUN009/EXTEND data-scientist annotated → promote to NECTAR? [y/n]
```

---

## 5. Membot Sprint Crystallization

At sprint end, membot reads all briefs written during the sprint:

```python
# In membot shutdown / crystallize flow:
sprint_briefs = list(vault_root.glob(
    f"Session-Briefs/{investigation_id}/**/*.md"
))
# Filter to this sprint's date range
# Extract narrative_body sections
# Synthesize into NECTAR.md entries grouped by hypothesis
```

The brief's `agent_hash` field lets membot detect duplicate runs (same hash = same narrative
= skip). The `promotion_state` field drives the queue: `capture` → membot processes,
`promoted` → already in NECTAR, `crystallized` → already in HONEY.

---

## 6. Error Handling Reference

| Situation | briefgen behaviour |
|---|---|
| `CT_VAULT` not set | Writes to `{repo}/.claude/memory/briefs/` (local fallback) |
| COC JSONL missing | Logs WARNING to stderr; writes brief without hash links |
| Vault path not writable | Raises `OSError` — agent should catch and log, not crash |
| Human already annotated | Annotation fence detected → preserved verbatim; only agent section replaced |
| `local_claude.py` not on path | Falls back to `{repo}/.claude/lib/` relative path resolution |
| `git` not available | `git_commit` field set to `"unknown"` — no crash |
| Agent card missing | `agent_version` set to `"baseline"` — no crash |

---

## 7. File Locations

| File | Purpose |
|---|---|
| `{repo}/.claude/lib/briefgen.py` | Module (both repos) |
| `{vault}/00-SHARED/Session-Briefs/{inv}/{phase}/*.md` | Written briefs |
| `{vault}/00-SHARED/00-META/BRIEFGEN-DESIGN.md` | This document |

