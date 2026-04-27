---
type: meta
tags: []
doc_hash: sha256:844061a6ff64a60d4d7e89dc102f1541cb444f5cfcba32c0e28beb165bfec0b3
hash_ts: 2026-03-29T16:09:47Z
hash_method: body-sha256-v1
---
<!-- MEM agent=python-pro ts=2026-03-27T22:35:00Z session=misplaced-detect-20260327 cat=TECHNIQUE pri=MED av=2026-03-18_0.92 -->
**[TECHNIQUE]** Per-pattern re flags in detection lists prevent IGNORECASE from defeating case-sensitive heuristics
When building pattern lists for text classification, store (pattern, label, flags) tuples not just (pattern, label).
The proper-noun entity detector requires case-sensitive matching — `[A-Z][a-z]{2,}` — but sibling patterns
benefit from IGNORECASE. Encoding flags per-tuple (0 vs re.IGNORECASE) preserves both without switching the
calling code. Learned: the bug was invisible until output count hit 400+ false positives on "pending autotune
completion" etc. Root cause: re.IGNORECASE makes [A-Z] match lowercase letters entirely.
Files: /mnt/c/Users/amand/.claude/scripts/crystallize.py
Next: Add to AGENTS.md Training section as cross-agent reminder before next regex detection task.
<!-- /MEM -->

<!-- MEM agent=python-pro ts=2026-03-27T22:35:00Z session=misplaced-detect-20260327 cat=OBSERVATION pri=MED av=2026-03-18_0.92 -->
**[OBSERVATION]** Scope-lock before writing regex patterns — test against real file content before integrating
This task required 4 rounds of pattern refinement because initial regex was not tested against the actual
corpus. The proper noun pattern fired on "Last Training", "Blind-handoff", "pending autotune" — all normal
training prose — because (1) re.IGNORECASE was inherited from sibling patterns, and (2) the exclusion list
was underspecified for tool/env vocabulary. Protocol: for any detector, write a standalone test harness
first (`_test_patterns()`), run it against representative samples from the target corpus, achieve <5%
false-positive rate, THEN integrate into the scanner.
Files: /mnt/c/Users/amand/.claude/scripts/crystallize.py
Next: Extract test harness into crystallize.py as `--test-patterns` flag for future maintainers.
<!-- /MEM -->
