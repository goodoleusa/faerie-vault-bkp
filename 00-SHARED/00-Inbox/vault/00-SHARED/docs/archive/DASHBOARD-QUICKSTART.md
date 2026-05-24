# Dashboard quickstart (two windows)

> **TL;DR:**
> - Run `python3 ~/.claude/hooks/state/dashboard.py` in a second terminal window.
> - Set `FAERIE_PROJECT_ROOT` env var to the repo you're working in.
> - `/faerie` may start the dashboard automatically if hooks are configured.
> - If the frame is blank: check `~/.claude/hooks/state/` for state files written by hooks.


**Hooks first:** With a proper **`~/.claude/settings.json`**, **`/faerie`** Turn 1 (and related launch paths) **may start `dashboard.py` for you**. This document is for **project root**, watch interval, launcher env, vault, and **troubleshooting** — especially the **operator fallback** when no frame appears.

**Repo [README.md](../README.md)** covers install + per-OS copy-paste; **this file is the full dashboard article**. **Why manual `dashboard.py` is not the default story:** [`docs/DESIGN-QUESTIONS.md`](DESIGN-QUESTIONS.md).

**Claude Code only** — requires the CLI/editor integration that runs hooks and writes `~/.claude/hooks/state/` (not Claude Desktop).

**Faerie branch / repo-agnostic:** The Mission Control frame is specced for **`/faerie`**. It does **not** assume a particular product or repo name. Set **`FAERIE_PROJECT_ROOT`** (or run from that repo’s git root) so HONEY + scratch match the workspace you care about; the title bar shows that folder’s basename. Global queue rows may still list tasks tagged with other project names — that is queue metadata, not a dashboard default.

**Combined dashboard (Windows + macOS + Linux):** The frame reads **`sprint-queue.json`** from `~/.claude/hooks/state/` (or **`CLAUDE_HOOKS_STATE`**). All orchestration releases use the **same** queue contract (`sprint_queue_lock.py` + `queue_ops` / `claim_task`). To see **one** queue across collaborators, point **`CLAUDE_HOOKS_STATE`** at the **same** directory on every machine (shared drive or replicated folder that includes the queue scripts — see **`hooks/state/SPRINT_QUEUE.md`**). **`json_lock`** is not used for this file.

**Obsidian:** Async partner notes live under **`ObsidianVault/00-SHARED/`**; optional alignment with shared Claude state is documented in **`ObsidianVault/00-SHARED/CLAUDE-COLLAB.md`**.

The faerie **dashboard** is a separate Python process. It reads session heartbeats, queue state, and memory files, then redraws a fixed terminal frame. It does **not** consume tokens in your Claude Code session.

**Project data** (HONEY tiers, hypotheses, scratch “connections”) comes from the **project root** resolved in this order:

1. Environment variable **`FAERIE_PROJECT_ROOT`** or **`REPO_ROOT`**
2. Otherwise `git rev-parse --show-toplevel` from the **current working directory** when you start the dashboard
3. Otherwise **`cwd`**

Run the watcher from a shell whose cwd is your project repo, or export `FAERIE_PROJECT_ROOT` explicitly (works on Windows, WSL, or macOS).

---

## Window 1 — Claude Code (CLI)

1. `cd` your repo (or open it in Cursor / VS Code with Claude Code).
2. Start the CLI: `claude`
3. Run **`/faerie`** (Turn 1).

On Turn 1, the faerie hook may spawn the dashboard in the background. If you do **not** see the dashboard frame, use Window 2.

---

## Window 2 — Live dashboard (watch mode)

### One-time: sync `dashboard.py` into `~/.claude`

From **PowerShell** (adjust source if your clone path differs):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude" | Out-Null
Copy-Item "D:\path\to\flowsearch\.claude\dashboard.py" "$env:USERPROFILE\.claude\dashboard.py" -Force
```

From **Unix / WSL**:

```bash
mkdir -p ~/.claude
cp /path/to/flowsearch/.claude/dashboard.py ~/.claude/dashboard.py
```

### Run the watcher (this window stays open)

**Option A — cd to your project, then run** (git root → project HONEY/scratch):

```bash
cd /path/to/your/project
export FAERIE_PROJECT_ROOT="$(pwd)"   # optional if cwd is already the repo root
python3 ~/.claude/dashboard.py --watch
```

**Option B — explicit project root:**

```bash
FAERIE_PROJECT_ROOT=/path/to/your/project python3 ~/.claude/dashboard.py --watch
```

**PowerShell:**

```powershell
$env:FAERIE_PROJECT_ROOT = "D:\path\to\your\project"
python "$env:USERPROFILE\.claude\dashboard.py" --watch
```

The default refresh interval when you pass `--watch` with no number is **30** seconds. Custom interval:

```bash
python3 ~/.claude/dashboard.py --watch 5
```

### Optional: title bar label

```bash
export FAERIE_DASHBOARD_SUBTITLE="my investigation"
python3 ~/.claude/dashboard.py --watch
```

Override the **repo** segment of the title (default = basename of `FAERIE_PROJECT_ROOT` / git root):

```bash
export FAERIE_DASHBOARD_REPO_LABEL="client-alpha"
python3 ~/.claude/dashboard.py --watch
```

### One-shot render (no loop)

```bash
python3 ~/.claude/dashboard.py
```

---

## Optional: test the hook launcher

If hooks are installed under `~/.claude/hooks/state/`:

**PowerShell:**

```powershell
python "$env:USERPROFILE\.claude\hooks\state\faerie-dashboard-launcher.py"
```

**WSL:**

```bash
python3 ~/.claude/hooks/state/faerie-dashboard-launcher.py
```

---

## Shared Obsidian folder (Syncthing)

Session presence files can mirror into `ObsidianVault/00-SHARED/sessions` when configured:

- Set **`FAERIE_VAULT_SHARED`** to the absolute path of your `.../ObsidianVault/00-SHARED` directory, **or**
- Keep the flowsearch repo layout so `repo/ObsidianVault/00-SHARED` exists next to `.claude/` (auto-detected).

If neither applies, heartbeats still work locally under `~/.claude/hooks/state/sessions/`; vault mirror is skipped.

---

## If the dashboard shows wrong or empty project data

- Confirm **session heartbeats** under `~/.claude/hooks/state/sessions/`.
- Set **`FAERIE_PROJECT_ROOT`** to the repo whose `.claude/memory/HONEY.md` and scratch files you expect.
- Run **`python3 ~/.claude/dashboard.py`** once (no `--watch`) from the same environment to verify paths.

---

## Other “dashboard” features

Some codebases expose investigation or analytics dashboards via their own HTTP APIs (e.g. a site `api_server`). That is separate from this terminal dashboard.
