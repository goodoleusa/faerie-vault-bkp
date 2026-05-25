# AGENTS.md alignment (faerie ↔ data-analysis-engine)

## Terms (same everywhere)

| Section | Purpose |
|---------|---------|
| **Kickoff** | Cold start: **Resume** table (Now, Success, Do first, Blocked, Pointers, Hot files) |
| **Where to write** | Scratch vs AGENTS vs HONEY/NECTAR vs `~/.claude/AGENTS.md` vs agent cards |
| **When to update learnings** | Session end, OTJ, explicit `/faerie --learn` — not silent merge on every `/faerie` |
| **Scratch → AGENTS** | Promote only tagged lines; cap weekly churn |

## Layout differences (by repo)

| Repo | Memory layout |
|------|----------------|
| **data-analysis-engine** | Default **repo-local** `.claude/local-state` + `.claude/memory` — see `docs/DAE-SELF-CONTAINED.md` in that repo |
| **faerie / cybertemplate / faerie-cli** | **Global** `~/.claude/` **+** project `.claude/memory/` — unchanged; only **organization** of `AGENTS.md` matches |

## Optional tooling

**data-analysis-engine** ships `scripts/agent_learning_log.py` (append-only process-learning JSONL). Other repos may adopt the same script or ignore it; it does not change faerie’s global/project split.
