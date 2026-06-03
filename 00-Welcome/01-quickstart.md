# 01 — Quickstart

Welcome. This vault is the seed. You are the gardener.

## What you have

You just cloned (or had cloned for you) a vault scaffold designed to
collaborate with a **swarmy install** — the Claude/OpenHands-driven
multi-agent system that lives in a separate repository. The vault is
where *you* think. The swarmy install is where the *agents* work. The two
are wired together by symlinks, schemas, and a small set of discipline
templates that ship in `_meta/`.

## Pre-flight check

You need:

1. A working **swarmy install** on the same machine.
   - If you don't have one yet: `git clone https://github.com/goodoleusa/swarmy ~/swarmy`
   - The install needs to be runnable (Python 3.10+, the scripts directory present).
2. **Obsidian** (any recent version).
3. Optional but recommended: a personal ed25519 keypair under
   `$SWARMY_REPO/forensics/reputation/keys/<your-handle>.{key,pub}`. If you
   don't have one, your first charters will be marked
   `pending_human_signature` — you can backfill signatures later via
   `scripts/9x_agent_sign.py`.

## Wire-up (one command)

```bash
bash _meta/setup.sh /abs/path/to/your/swarmy/install your-handle
```

This is **idempotent**. Re-run it any time the symlinks get broken or you
move your swarmy install.

What it does:

| Step | Effect |
|------|--------|
| 1 | Symlinks `10-Charters/active/` → `<swarmy>/forensics/charters/active/` |
| 2 | Symlinks `10-Charters/closed/` → `<swarmy>/forensics/charters/closed/` |
| 3 | Copies `_meta/.env.example` → `_meta/.env` and fills in your swarmy path |
| 4 | Writes a welcome charter to the active folder, signed with your handle |
| 5 | Prints next-steps |

After setup, open the vault folder in Obsidian. The Breadcrumbs plugin
config in `.obsidian/plugins/breadcrumbs/data.json` is pre-tuned for the
compass-bearing model (N/S/E/W — see `_meta/microagents/compass/`).

## The tour (5 minutes)

Open these files in order:

1. **This file** — `00-Welcome/01-quickstart.md` (you are here).
2. **`02-your-first-charter.md`** — walks you through writing a real
   charter using `_charter_lib`. Do this with a small, real intent — not
   a toy.
3. **`03-the-six-microagents.md`** — the six discipline skills that load
   automatically when you (or your agents) mention their trigger words.
   You don't need to memorize them; they self-introduce in context.

## The four top-level folders

| Folder | Role | Analogy |
|--------|------|---------|
| `00-Welcome/` | Onboarding (this directory). Read once, delete or keep, your call. | Welcome packet at a new job |
| `10-Charters/` | Mission contracts. `drafts/` is yours; `active/` and `closed/` are symlinks into the swarmy install's forensic tree. | Project briefs |
| `20-Inspirations/` | Pollen — raw fiber. Half-thoughts, screenshots, links, voice-notes. | A field notebook |
| `30-Synthesis-Log/` | Nectar — what you've refined from raw pollen. | A daybook |
| `80-Publications/` | Droplets — finished swatches you want to preserve in the selvage. | A portfolio |

The numbering convention is Johnny.Decimal-adjacent: the gaps (40–70) are
left empty so you can grow your own categories without renumbering.

## Discipline, in one paragraph

Charters declare intent (`cluster_prefix` is **exactly 3 items**, no
exceptions — see `_meta/cluster-prefixes.md`). Agents return manifests
that cite their evidence and pick a `completion_choice` from a canonical
13-item vocabulary. Everything chains by content-hash into a forensic
ledger. The microagents in `_meta/microagents/` enforce the rituals
without you needing to memorize them.

You will absorb the rest by doing.

## When things break

- **Symlinks gone after a git pull:** re-run `bash _meta/setup.sh`. Idempotent.
- **Charter rejected as schema-invalid:** check `_meta/cluster-prefixes.md`
  — 99% of the time it's a cluster_prefix length problem.
- **Charter has no signature:** generate a keypair via
  `python3 <swarmy>/scripts/9x_agent_sign.py keygen <your-handle>`.

## Next

→ `02-your-first-charter.md`
