---
source: /mnt/d/0local/gitrepos/reckon/forensics/ephemeral/2026-06-05/oh-parity-skill/oh-parity-scratch.py
promoted: 2026-06-05T18:53:33.968226+00:00
---

# oh-parity-scratch.py

```
"""
SPRAY — oh-parity skill session scratch
mission: parity.claude-oh.sync
date: 2026-06-05

APPROACH A: pure JSON diff
  - load .claude/hooks.json
  - load .openhands/hooks.json
  - compare 8 top-level keys
  - per-key: count matchers, commands, timeouts; flag missing/extra
  - invokes hookdoctor session-health (which runs mirror_check if present)
  - modes: --check (nonzero on drift), --report (human summary)

APPROACH B: structural diff (compare full serialized values)
  - normalize unicode in OH hooks.json (has \uXXXX escapes, Claude has bare chars)
  - compare normalized values per key
  - simpler: detect exact drift vs semantic drift

Decision: Use APPROACH A (structural per-key diff) since the keys have
heterogeneous shape (lists of objects). We want to know WHICH keys differ
and HOW (count mismatch, command mismatch).

Key insight from reading both hooks.json files:
- .claude/hooks.json has 8 top-level keys including $comment
- .openhands/hooks.json has 8 top-level keys
- They are intentionally different: OH has extra hooks (creature-manifest-drive,
  f0_inline_op_gate, spawn-contract-enforcer, session-health hookdoctor call)
- The intent of mirror_check is to verify structural parity of SHARED hooks,
  not that they are identical

CANONICAL 8 KEYS as stated in brief:
  pre_tool_use, post_tool_use, user_prompt_submit, session_start, stop,
  session_end, post_tool_use_evidence_archive, $comment

hookdoctor.py mirror_check:
  Looking at hookdoctor.py, the mirror_check path is:
  ROOT / ".openhands/scripts/mirror_check.py"
  But this file likely doesn't exist — let's check the --check vs --report flow.

parity_sync.py design:
  - _repo_root() -> walk up from __file__ looking for .openhands/
  - load both hooks.json
  - for each of the 8 top-level keys, compare normalized JSON
  - report per-key: MATCH / DRIFT / MISSING
  - invoke hookdoctor.py session-health (which runs mirror_check advisory)
  - --check: exit nonzero on any drift
  - --report: human-readable summary

TIGHTEN: drop hookdoctor invocation approach details, keep it simple:
  invoke hookdoctor mirror_check if scripts/hookdoctor.py + the mirror_check path exists
  otherwise invoke hookdoctor session-health which does it internally

CRYSTALLIZE path: scripts/parity_sync.py
"""

```
