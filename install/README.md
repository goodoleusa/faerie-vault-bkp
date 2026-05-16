# faerie2 — Install Flow

Top-level install walkthrough. See `../INSTALL.md` for the full reference with
platform notes, B2 setup, and rollback.

This file exists as the **canonical entry point** for a fresh install. It prescribes
an order that captures honest pre-faerie data before you adopt any faerie feature.

---

## Order of operations (do these in order)

### Step 0 — Clone + base install

```bash
git clone git@github.com:Persistech/faerie.git
cd faerie
bash scripts/install.sh --no-clobber    # safe merge; see ../INSTALL.md for alternatives
```

This lands the faerie files in `~/.claude/` but does **not** wire the hooks into
your `settings.json`. Crucially: you are still running effectively-vanilla Claude
Code at this point.

### Step 1 — Capture a vanilla baseline BEFORE enabling faerie

**Why first?** Once you wire the hooks and start using `/faerie`, your sessions
are no longer vanilla. If you skip this step you lose the chance to get a clean
pre-adoption baseline — the counterfactual disappears.

Your baseline does not have to be huge. One to two sessions on the three canonical
baseline tasks gives you enough signal to defend any ROI claim you make later.

```bash
# From faerie2 repo root:
python3 scripts/install/vanilla_baseline.py --activate
```

That command:
- Backs up your current `settings.json` to `settings.json.faerie-on.{timestamp}`
- Writes a minimal hooks-free settings (Claude Code native + teams flag only)
- Records a forensic COC entry (hash-chained, tamper-evident)
- Prints "NEXT STEPS" instructions

Open a **new terminal**, run `claude`, and work through one or more tasks from
`baseline-tasks/`:

- `baseline-tasks/task-01-code-audit.md`
- `baseline-tasks/task-02-doc-synthesis.md`
- `baseline-tasks/task-03-data-investigation.md`

When done, return to any shell (new or existing, doesn't matter) and run:

```bash
python3 scripts/install/vanilla_baseline.py --deactivate
```

That:
- Restores your real `settings.json` from backup
- Archives the vanilla session transcript(s) into `baseline-runs/{session_id}/`
- Extracts metrics (tokens, tool uses, subagent spawns, duration) into `metadata.json`
- Records a second COC entry

Aggregate across runs (safe to run any time, as often as you like):

```bash
python3 scripts/install/vanilla_baseline.py --collect
# -> baseline-runs/SUMMARY.json
```

Full protocol, troubleshooting, and forensic verification commands are in
`../docs/BASELINE-PROTOCOL.md`.

### Step 2 — Wire faerie into settings.json

Now (and only now) add the hooks from `../INSTALL.md` Step 3. Running faerie before
capturing vanilla loses the clean baseline permanently.

### Step 3 — Verify

```bash
cd /mnt/d/path/to/any/repo
claude
/faerie
```

You should see a faerie dashboard. Your `baseline-runs/` folder should have at
least one archived vanilla session to compare against.

### Step 4 — Ongoing cadence

Once a month:

1. Run `--activate` → open fresh terminal → work the three baseline tasks → `--deactivate`
2. Run the same three tasks in a normal faerie session
3. Run `--collect` to refresh `baseline-runs/SUMMARY.json`
4. Run `python3 scripts/eval/eval_harness.py --ab-vanilla` to compute the per-task
   delta report

---

## Files this flow touches

- `~/.claude/settings.json` — swapped in and out; backups kept, never clobbered
- `~/.claude/state/VANILLA_BASELINE_ACTIVE` — flag file tracking activation
- `baseline-runs/{session_id}/` — archived transcripts + metadata
- `baseline-runs/SUMMARY.json` — aggregated metrics
- `forensics/baseline-runs-coc.jsonl` — hash-chained COC

## Files this flow NEVER touches

- `~/.claude/HONEY.md`, `~/.claude/NECTAR.md` — your memory stays intact
- `~/.claude/projects/*/` — transcripts stay where Claude CLI put them; we only COPY
  into baseline-runs, never move or delete
- Any repo's `forensics/` other than `faerie2/forensics/` — vanilla baselining is
  a faerie-level concern, not an investigation concern
