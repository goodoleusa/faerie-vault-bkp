---
type: index
status: active
created: 2026-04-21
tags: [narrative, index]
up: ../README.md
down: [INVESTIGATION-NARRATIVE.md, F0-EVAL-2026-04-20.md]
---

> [↑ Readme](../README.md) · [⌂ Home](../../README.md)

# Investigation narrative (faerie CLI repo)

This repo ships **orchestration** (hooks, skills, queue). When you use it **as the project root**, **`docs/narrative/INVESTIGATION-NARRATIVE.md`** receives **auto-appended pointers** on each session end via **`scripts/4a_narrative_auto_update.py`**:

- Tier 1 **`promotion_log.json`** (if present)
- **`pri=HIGH`** MEM; **`pri=MED`** MEM with gap/question **`cat`** (see DAE **`docs/narrative/README.md`**)
- **HONEY Critical Blockers** (new lines)
- **`docs/gaps.md`** / active **`.claude/memory/investigations/<id>/gaps.md`** on edit

Invoked from **`.claude/hooks/session_stop_hook.py`** unless **`NARRATIVE_AUTO=0`** (or DAE/FAERIE alias).

**Manual spine:** blockers, strategic questions, **evidence gaps / progressive disclosure** — merge auto bullets on **`/handoff`**.

For a **dedicated investigation repo**, copy **`scripts/4a_narrative_auto_update.py`** and **`docs/narrative/`**; hooks resolve the project via **`REPO_ROOT`** / **`DAE_REPO_ROOT`** or **`cwd`**.

**Release bundles:** after changing hooks, **`python scripts/0b_build_release_bundles.py`**.
