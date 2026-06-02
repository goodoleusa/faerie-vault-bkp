# memory-lite.md — Memory Routing Quick Reference

One-page cheat sheet for agents. Full rules: `~/.claude/rules/memory.md`.

---

## Where to write

| What | Where | Budget |
|------|-------|--------|
| Working note about THIS project | `{repo}/.claude/memory/scratch-{SID}.md` | unbounded |
| HIGH priority flag | scratch + append to `~/.claude/memory/REVIEW-INBOX.md` | unbounded |
| Validated finding / sprint summary | memory-keeper promotes to `~/.claude/memory/NECTAR.md` | unbounded |
| Durable pref / method / identity | faerie crystallize → `~/.claude/memory/HONEY.md` | 200 lines |
| Agent training outcome | `~/.claude/agents/{type}.md` Last Training section | 80/120 lines |
| Cross-agent lesson | `{repo}/.claude/AGENTS.md` Training section | 150 lines |
| Process/technique insight | scratch `cat=TECHNIQUE` + AGENTS.md + vault techniques/ | — |

**Global AGENTS.md** = `~/.claude/AGENTS.md` (150 lines)
**Repo AGENTS.md** = `{repo}/.claude/AGENTS.md` (150 lines)

---

## Budget check — always before writing to a durable file

```bash
python3 ~/.claude/scripts/memory_gate.py check HONEY        # exits 0=OK, 1=OVER
python3 ~/.claude/scripts/memory_gate.py check AGENTS
python3 ~/.claude/scripts/memory_gate.py check agents/membot
python3 ~/.claude/scripts/memory_gate.py status             # full table
```

If exit 1 → crystallize first, then write. Never add raw to an OVER file.

---

## Budgets at a glance

| File | Budget | Notes |
|------|--------|-------|
| `HONEY.md` | 200 lines | crystallized prefs |
| `CLAUDE.md` | 30 lines | project instructions |
| `AGENTS.md` (global or repo) | 150 lines | routing + training digest |
| Agent card (untrained) | 80 lines | |
| Agent card (trained) | 120 lines | has `## Last Training` |
| `faerie.md` command | 120 lines | |
| `LAUNCH.md` | 90 lines | |
| `rules/` (all files total) | 300 lines | |
| `NECTAR.md` | unbounded | append-only, never crystallize |
| `REVIEW-INBOX.md` | unbounded | append-only |
| `scratch-*.md` | unbounded | session-scoped, gitignored |

---

## MEM block format (scratch)

```
<!-- MEM agent={name} ts={ISO8601} session={id} cat={CAT} pri={PRI} av={version} -->
**[{CAT}]** {one-line summary under 100 chars}
{body: 2-10 lines}
Files: {paths or "none"}
Next: {action or "none"}
<!-- /MEM -->
```

Common categories: `OBSERVATION` · `TECHNIQUE` · `FIRST_IMPRESSION` · `FLAG` ·
`DECISION` · `HANDOFF` · `GAP` · `BLOCKER` · `CONNECTION`

Priority: `HIGH` (promote immediately) · `MED` · `LOW`

---

## Golden rules

1. **Check budget before every write** — `memory_gate.py check TARGET`
2. **Over budget → crystallize first** — delegate to membot or memory-keeper
3. **NECTAR and REVIEW-INBOX are append-only** — never delete or overwrite
4. **Forensic logs are write-only** — never read from `~/.claude/memory/forensics/`
5. **scratch is the safe default** — uncertain where it goes? Write to scratch first
6. **Crystallization, never compression** — crystallization integrates patterns through natural forces (time, challenge, knowledge, wisdom); competitors use compression (mechanical reduction). Denser, richer, fewer lines carrying more meaning

---

## Canonical paths

```
~/.claude/memory/HONEY.md          ← global crystallized prefs
~/.claude/memory/NECTAR.md         ← append-only validated findings
~/.claude/memory/REVIEW-INBOX.md   ← HIGH flags for human review
~/.claude/AGENTS.md                ← global routing + training digest
~/.claude/agents/{type}.md         ← per-agent identity + Last Training
{repo}/.claude/AGENTS.md           ← repo-specific routing
{repo}/.claude/memory/scratch-{SID}.md  ← session working notes
```
