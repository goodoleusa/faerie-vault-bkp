# Main Context Discipline (mth00088)

**Doctrine:** Main is a switchboard, not a worker. Every token main spends reading, editing, or receiving full agent output is a token that cannot fund another spawn. These 7 rules enforce switchboard mode at load time.

---

## Rule 1 — No Read of bundle JSONLs

**Why:** `emit-bundles` already returns `spawn_prompt` as its output. Reading the bundle file afterward to verify content costs ~800 tokens for zero additional value.

**Before (bad):**
```
# Main reads bundle to inspect
Read("/mnt/.../forensics/bundles/20260424_bundle_task-81_main_a1b2c3d4.jsonl")
# → 800 tokens consumed, same info already in spawn_prompt return value
```

**After (good):**
```python
# spot-check only when auditing:
bash("tail -c 200 bundle.jsonl")   # ~20 tokens
```

**Savings: ~800 tok per occurrence avoided**

---

## Rule 2 — Scalar reads only from state files

**Why:** Reading a full settings/state JSON to extract one value loads 500–2000 tokens of irrelevant context.

**Before (bad):**
```
Read("/mnt/d/0local/gitrepos/faerie2/settings.json")
# → full 1200-line file, 2000 tokens, to find one queue_size value
```

**After (good):**
```bash
python3 -c "import json; print(json.load(open('settings.json'))['queue_size'])"
# → 1 line output, ~5 tokens
```

**Savings: ~500–2000 tok per read avoided**

---

## Rule 3 — Never Read settings.json or scripts in main

**Why:** Scripts and settings are 200–2000 token blobs of content main has no use for. Code review and config inspection is agent work.

**Before (bad):**
```
Read("/mnt/d/0local/gitrepos/faerie2/scripts/7x_spawn_template.py")
# → 1600-line script, ~3000 tokens
```

**After (good):**
```
spawn(agent="code-reviewer", task="inspect spawn template for X", run_in_background=True)
# → main receives 1-line dashboard_line on completion
```

**Savings: ~1000–3000 tok per read avoided**

---

## Rule 4 — Never Edit in main

**Why:** The break-even between inline Edit and spawning python-pro is approximately 10 input tokens. Any patch longer than a single variable rename costs less in a spawn than in-context composition + verification.

**Before (bad):**
```
Edit("/mnt/.../scripts/7x_spawn_template.py", old="X", new="Y")
# Main burns context reading file, computing diff, verifying result
# 300–3000 tokens depending on file size
```

**After (good):**
```
spawn(agent="python-pro", task="patch 7x_spawn_template.py: replace X with Y", run_in_background=True)
# → main cost: ~50 tokens for spawn prompt
```

**Savings: 300–3000 tok per edit avoided**

---

## Rule 5 — run_in_background: true on every Agent spawn

**Why:** Foreground agent results land fully in main context — the entire agent output becomes part of main's token budget. Background mode delivers only a TaskNotification (~20 tokens) plus whatever main reads from the manifest (~80 chars for dashboard_line).

**Before (bad):**
```python
Agent(prompt="...", run_in_background=False)
# Agent returns 2000 words of findings → 3000 tokens injected into main
```

**After (good):**
```python
Agent(prompt="... MANIFEST_RETURN: /mnt/.../manifest.json", run_in_background=True)
# Main receives notification, reads jq .dashboard_line → ~80 tokens
```

**Exception:** Only use foreground when you literally need the agent's raw output text in the next sentence (rare).

**Savings: ~500–2000 tok per spawn**

---

## Rule 6 — Bash output discipline

**Why:** Default Bash output (ls -la, full JSON print, verbose logs) dumps hundreds of tokens of noise into context.

**Pattern table:**

| Instead of | Use | Savings |
|---|---|---|
| `ls -la forensics/manifests/` | `ls forensics/manifests/ \| wc -l` | ~200 tok |
| `cat manifest.json` | `jq -r '.dashboard_line' manifest.json` | ~400 tok |
| `python3 script.py` | `python3 script.py 2>&1 \| tail -1` | ~300 tok |
| `git log` | `git log --oneline -5` | ~200 tok |

**Savings: ~200–500 tok per command**

---

## Rule 7 — Suppress stderr when switchboarding

**Why:** When main is routing (not auditing), stderr warnings from scripts are noise. They land in context and cost tokens without changing the routing decision.

**Before (bad):**
```bash
python3 scripts/7x_spawn_template.py render --template w2-analysis --params '{...}'
# → 10 lines of DeprecationWarning + progress bars → 300 tokens of noise
```

**After (good):**
```bash
python3 scripts/7x_spawn_template.py render --template w2-analysis --params '{...}' 2>/dev/null
# → clean output only
```

**Exception:** When auditing hook failures or diagnosing errors, remove the suppression.

**Savings: ~100–300 tok per command when switchboarding**

---

## Worst Current Habits Diagnosed (2026-04-25 session)

1. **Reading bundle files after emit-bundles returned** — seen in multiple W1 launches; each instance cost ~800 tokens on top of the spawn setup cost.
2. **Foreground agent spawns for background-eligible tasks** — the most common violation; a W2 synthesis agent returning inline consumed ~2500 tokens of main context.
3. **Full JSON reads to check one field** — `Read(settings.json)` to confirm `enforce_mode` value; 1200 lines read for a 1-value check.
4. **Editing scripts inline in main** — `7x_spawn_template.py` patched directly in main twice in the same session; each cost ~1000 tokens including read+edit+verify cycle.
5. **`ls -la` for directory status** — decorative output (permissions, sizes, dates) consumed 400 tokens when `wc -l` would have returned a single number.

---

## Token Budget Impact Projection

Enforcing all 7 rules on a typical W1 (6 spawns) + W2 (3 spawns) session:

| Rule | Violations/session (est.) | Tok saved/violation | Total saved |
|---|---|---|---|
| 1 Bundle reads | 2 | 800 | 1600 |
| 2 Scalar reads | 4 | 500 | 2000 |
| 3 Settings/scripts | 2 | 1500 | 3000 |
| 4 Inline edits | 3 | 800 | 2400 |
| 5 Foreground agents | 5 | 1200 | 6000 |
| 6 Bash output | 8 | 300 | 2400 |
| 7 Stderr suppression | 6 | 200 | 1200 |
| **Total** | | | **~18,600 tok/session** |

At 200K context limit, 18,600 tokens = ~9% additional runway per session.

---

## Reference

- mth00086: Main-Inference Heuristic (what main is allowed to do)
- mth00088: Main Context Discipline (how main avoids doing too much)
- `7x_spawn_template.py`: `_SPAWN_BOILERPLATE` injects switchboard-mode reminder into every agent
- CLAUDE.md: `## Main Context Discipline (mth00088)` section (compact form)
