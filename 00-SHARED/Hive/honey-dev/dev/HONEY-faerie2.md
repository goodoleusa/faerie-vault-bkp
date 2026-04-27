# faerie2 — Meta-Agent Orchestration (Collaborator Seed)

Crystallized context for macOS/Linux collaborators. Canonical dev repo at `/mnt/d/0LOCAL/gitrepos/faerie2/`.

---

## Core Concepts

[sys | principle | permanent | 1.0] **faerie** — orchestrates specialized subagents (data-engineer, evidence-curator, researcher, writer, publisher) on complex multi-phase tasks. Commands: `/faerie` (start) → `/queue` (view) → `/run` (claim) → `/handoff` (end) → `/crystallize` (NECTAR→HONEY).

[mth | memory | permanent | 1.0] **Memory flow:** session start reads HONEY.md (prefs/facts) + NECTAR.md tail-30 (recent findings) → agents write scratch observations → /handoff promotes scratch → NECTAR appends → /crystallize compresses NECTAR findings into HONEY (only multi-agent validated, human-reviewed, proven impact).

[rule | principle | permanent | 1.0] **HONEY law:** ≤200 lines, dense only. Format: `[id | type | ttl | confidence] entry`. Never crystallize single-session. NECTAR: unbounded, append-only narrative forever (court-admissible forensic trail). HONEY: crystallized seed for fast cold-start.

---

## Agent Routing (5 Core Types)

| Type | When | Task |
|------|------|------|
| **data-engineer** | ETL, pipeline, CSV | Ingest XLSX + deduplicate + normalize |
| **evidence-curator** | Tiering, quality, bundling | Tier evidence T1/T2/T3 + score confidence |
| **research-analyst** | OSINT, BGP, cert, synthesis | Look up AS ownership + history |
| **report-writer** | Findings → prose, reports | Turn findings into publishable summary |
| **fullstack-developer** | UI, D3 viz, dashboards, admin | Build timeline viz + admin panel |

Spawn with `Agent` tool (Claude Code CLI) or `/subagent-spawn` command. Categories: `-data` (engineer→auditor→scientist), `-evidence` (curator→reviewer→coc-manager), `-analysis` (scientist→analyst→synthesizer), `-pipeline` (orchestrator→distributor→coordinator), `-publish` (writer→dev→admin→ipfs-pub), `-workflows` (8-step AUDIT→PUBLISH), `-ingest` (10-agent pipeline).

---

## Operational Model

[mth | method | permanent | 1.0] **Modes:** Normal = `/faerie` (full orchestration). Debug-only = direct `/run` (no orchestration).

[mth | method | permanent | 1.0] **State progression:** Scratch (working notes) → REVIEW-INBOX (HIGH flags) → NECTAR.md (validated findings, session end) → HONEY.md (crystallized facts, 3+ sessions + human validation).

[mth | method | permanent | 1.0] **Vault (optional):** Obsidian vault at `ObsidianVault/`. Hub: `00-SHARED/LAUNCH/`. Auto-synced via Syncthing. Agents write; humans annotate + promote.

---

## Environment (macOS/Linux)

- **No WSL.** All paths native Unix. Settings: `~/.config/Claude/settings.json` (Linux) or `~/Library/Application Support/Claude/settings.json` (macOS).
- **Python 3.10+**. Claude CLI: https://github.com/anthropics/claude-cli or `brew install anthropic-cli`.
- **Setup:** `python3 scripts/setup-collab.py` appends investigation context to `~/.claude/memory/HONEY.md`.

---

## Key Files

| File | Purpose |
|------|---------|
| `.claude/commands/faerie.md` | `/faerie` skill |
| `~/.claude/memory/HONEY.md` | Global crystallized facts |
| `~/.claude/memory/NECTAR.md` | Append-only validated findings |
| `~/.claude/memory/REVIEW-INBOX.md` | HIGH priority flags |
| `~/.claude/hooks/state/sprint-queue.json` | Queued tasks + status |
| `.claude/memory/scratch-{SESSION_ID}.md` | Working notes (ephemeral) |

---

## Investigation-Specific HONEY (Optional)

Create repo-level HONEY.md at `{repo}/.claude/memory/HONEY.md` (gitignored):

```
[hyp | finding | 90d | 0.95] H1 — Treasury exposed via cert rotation + WHOIS dates
[gap | gap | permanent | 0.70] Missing: Bloomberg TLS DB for federal domains
[rule | method | 1yr | 1.0] Tier 1 requires 3+ independent sources + SHA-256 anchor
```

---

## Quick Start

```bash
cd /path/to/faerie2
claude
/faerie              # Initialize (reads HONEY.md + NECTAR.md tail-30)
/queue               # See queued tasks
/run                 # Claim + execute first HIGH task
```

After work:
```bash
/handoff             # Session end: promote scratch → NECTAR.md
```

Next session:
```bash
claude
/faerie              # Loads updated HONEY.md + NECTAR.md
/run                 # Resume
```

---

## Integration with DAE (data-analysis-engine)

```bash
cd /path/to/data-analysis-engine
claude
/data-ingest         # Spawns agent team for full pipeline
```

Setup: `python3 scripts/setup-collab.py` appends context to global HONEY.md.

---

## Collaboration Arc

```
User task → /faerie (context + queue)
  → /run (spawn agents)
  → agents work (scratch)
  → /handoff (scratch → NECTAR.md)
  → membot (score, benchmark)
  → next /faerie (HONEY + NECTAR)
```

Every session teaches the system.

---

## Essential Rules

- **Launch from repo:** `cd /path/to/repo && claude` (never Windows paths)
- **Spawn = doing.** Use `Agent` tool. Never work inline on substantial tasks.
- **HONEY ≤ 200 lines.** Over budget → crystallize first.
- **Manifest-driven.** Tasks reference previous outputs via git hash (no duplication).
- **HIGH flags promoted immediately.** HIGH → REVIEW-INBOX + vault + human same session.
- **One writer per file.** Agents write scratch + queue; humans read + annotate.

---

## Documentation

- **ARCHITECTURE.md** — full orchestration blueprint
- **README.md** — quick start + philosophy
- **.claude/LAUNCH.md** — entry map + skills
- **~/.claude/rules/memory.md** — global memory system
- **~/.claude/rules/agent-lifecycle.md** — agent startup + self-update

---

## macOS/Linux Specific

No WSL path conversion. All paths native.

On macOS, if Claude CLI not in PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.zshrc or ~/.bash_profile
which claude && claude --version
```
