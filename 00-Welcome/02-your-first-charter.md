# 02 — Your First Charter

You already have a charter — `setup.sh` wrote one called
`vault-welcome-first-charter` into `10-Charters/active/`. That one was on
the house. Now you write your second, and it's the first real one.

## Pick a real intent

Don't pick a toy. The discipline only sticks if the first charter is for
something you actually want to ship in the next two weeks. Examples:

- "Migrate my reading notes from Notion into this vault."
- "Set up a daily synthesis ritual where I write 100 words at 9am."
- "Build a small Obsidian dashboard that lists my last 7 days of
  Synthesis-Log entries."

If you can name a check that would prove it's done, you have a charter.
If you can't, you have a feeling — keep it in `20-Inspirations/` for now.

## Step 1 — Draft

Copy the template:

```bash
cp _meta/charter-template.json 10-Charters/drafts/my-first-real-charter.json
```

Open the draft and fill in (at minimum):

- `charter_id` — dotted-w4w address, e.g. `notes.migration.from-notion`
- `intent_address` — 3+ kebab-case items, e.g.
  `["notes", "migration", "from-notion"]`
- **`cluster_prefix` — EXACTLY 3 items** (schema-locked, no exceptions)
- `created` — current UTC, format `YYYY-MM-DDTHH:MM:SSZ`
- `eta` — when you think it ships, format `YYYY-MM-DD`
- `authors` — your handle
- `summary` — one paragraph; this is the map, not a todo list
- `phase_1_deliverables` — name + description + acceptance + expected_artifacts
- `non_goals` — what this charter explicitly will NOT do
- `acceptance_ritual` — the runnable end-to-end check
- `where_we_were` / `where_we_are` / `where_we_headed`

Leave `coc_chain` and `signed_by` alone — `_charter_lib` writes those.

### A note on `cluster_prefix`

Read `_meta/cluster-prefixes.md` if you haven't. The rule is:

> `cluster_prefix` MUST be a JSON array of EXACTLY 3 strings.

The schema (`_meta/schemas/charter.schema.json`) sets `minItems: 3` and
`maxItems: 3`. Five-item prefixes you may see in older charters
elsewhere are pre-lock; new charters must be 3.

## Step 2 — Promote

The draft becomes a real charter when you sign it and move it to active.
The library does both at once:

```bash
cd "$SWARMY_REPO"   # the swarmy install path you wired in setup.sh

python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
from _charter_lib import sign_and_promote
out = sign_and_promote(
    Path('/abs/path/to/this/vault/10-Charters/drafts/my-first-real-charter.json'),
    author='your-handle',
)
print(out)
"
```

What this does (in order):

1. Loads your draft.
2. Resolves `depends_on` charter IDs to content hashes (so your charter
   is chained into the ledger).
3. Builds a `coc_chain` block.
4. Writes the charter to `forensics/charters/active/<YYYY-MM-DD>_<charter_id>.json`
   (which — via the symlink from step 1 of setup — appears in your
   `10-Charters/active/` folder).
5. Signs it via `9x_agent_sign.py` if you have a keypair; otherwise
   leaves `_signing_status: "pending_human_signature"` for you to fill
   later.
6. Appends a `charter-created` entry to the swarmy install's
   `forensics/coc.jsonl`.
7. Deletes the draft (it's now lifted into the canonical tree).

## Step 3 — Verify

```bash
ls 10-Charters/active/
# you should see two files: the welcome charter from setup, and your new one
```

To check schema-validity:

```bash
python3 -c "
import json, jsonschema
schema = json.load(open('_meta/schemas/charter.schema.json'))
charter = json.load(open('10-Charters/active/<YOUR-CHARTER>.json'))
jsonschema.validate(charter, schema)
print('✓ schema-compliant')
"
```

## What now?

Your charter is in the swarm's frontier. Agents reading
`forensics/charters/active/` see it. When you spawn agents (via your
swarmy install's `/spawn` command or `scripts/spawn.py`) and they have
matching cluster_prefix overlap with your charter, they'll pick up
deliverables from it.

You don't need agents to use the vault. But this is where they enter,
when you want them.

## Common stumbles

- **`cluster_prefix` too long.** Schema rejects. Cut to exactly 3.
- **`depends_on` pointing at a charter that doesn't exist.** Library
  inserts `genesis` as a placeholder and writes a backfill marker.
  Surface in `where_we_were` so you can audit later.
- **No keypair → `pending_human_signature` everywhere.** Generate one
  via `python3 scripts/9x_agent_sign.py keygen <handle>` in the swarmy
  install. Then re-sign existing charters with the same script's `sign`
  subcommand.

## Next

→ `03-the-six-microagents.md`
