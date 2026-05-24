# SPAWN-BOILERPLATE — Required in every agent spawn prompt

Copy the relevant sections into every spawn prompt. Three required blocks:
Manifest Write, Forensic Trace, and Streaming. The Stigmergy block is standard.

Canonical location: `/mnt/d/0local/gitrepos/faerie2/docs/SPAWN-BOILERPLATE.md`
(Requested location `.claude/SPAWN-BOILERPLATE.md` was write-restricted in this sandbox.)

---

## 1. Manifest Write (always use this two-path pattern)

Write your manifest to BOTH paths. Try canonical first; fall back to repo-relative.
Write the path that actually succeeded into your trace file.

```
CANONICAL (try first):
  /mnt/d/0LOCAL/.claude/hooks/state/{wave}-{agent_type}-result.json

FALLBACK (always writable, repo-relative):
  /mnt/d/0local/gitrepos/faerie2/.claude/manifests/{wave}-{agent_type}-result.json
```

Manifest must include at minimum:
```json
{
  "agent": "{agent_type}",
  "ts": "{ISO8601}",
  "wave": {int},
  "task_id": "{task-xxx or null}",
  "output_path": "{full path to primary output file}",
  "dashboard_line": "{<=80 chars for Turn 0 dashboard}",
  "files_written": ["{paths}"],
  "next": "{recommended next step or none}"
}
```

Python helper available (import or copy inline):
```python
import sys
sys.path.insert(0, "/mnt/d/0local/gitrepos/faerie2/scripts")
from agent_state_relay import write_manifest
result = write_manifest(my_data, wave=2, agent_type="python-pro")
# result: {"path": "...", "source": "canonical"|"fallback", "success": bool}
```

---

## 2. Forensic Trace (required at end of every agent run)

Before returning your final output, write a trace file:

```
PATH: /mnt/d/0local/gitrepos/faerie2/.claude/manifests/{wave}-{agent_type}.trace.json
```

Trace format:
```json
{
  "ts": "{ISO8601 -- time trace was written}",
  "agent_type": "{your agent type, e.g. python-pro}",
  "session_id": "{AGENT_SESSION_ID if available, else null}",
  "wave": {int},
  "task_id": "{task-xxx or null}",
  "tool_calls": [
    {"tool": "Read",  "path": "...",          "ts": "{ISO8601}"},
    {"tool": "Write", "path": "...",          "ts": "{ISO8601}"},
    {"tool": "Bash",  "cmd_summary": "...",   "ts": "{ISO8601}"},
    {"tool": "Edit",  "path": "...",          "ts": "{ISO8601}"},
    {"tool": "Glob",  "pattern": "...",       "ts": "{ISO8601}"},
    {"tool": "Grep",  "pattern": "...",       "ts": "{ISO8601}"}
  ],
  "files_read": ["{absolute paths of files you read}"],
  "files_written": ["{absolute paths of files you wrote or edited}"],
  "decisions": [
    "{short description of each key choice made -- algorithm, library, path, etc.}"
  ],
  "manifest_path": "{full path to your manifest JSON -- canonical or fallback}",
  "manifest_hash": "{sha256:... of manifest file}",
  "prev_entry_hash": "{sha256:genesis if first trace, else entry_hash of previous trace in staging dir}",
  "entry_hash": "{sha256 of this dict with entry_hash field excluded}"
}
```

Computing entry_hash (Python):
```python
import hashlib, json

def compute_entry_hash(trace: dict) -> str:
    without_hash = {k: v for k, v in trace.items() if k != "entry_hash"}
    raw = json.dumps(without_hash, sort_keys=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(raw).hexdigest()}"

trace["entry_hash"] = compute_entry_hash(trace)
```

Computing manifest_hash:
```python
from pathlib import Path
import hashlib

def sha256_file(path: str) -> str:
    return f"sha256:{hashlib.sha256(Path(path).read_bytes()).hexdigest()}"

trace["manifest_hash"] = sha256_file(manifest_path)
```

---

## 3. Streaming

```
python3 /mnt/d/0LOCAL/.claude/scripts/memory_bridge.py \
  --stream --task {TASK_ID} --agent {AGENT_TYPE} --emit progress "..."
```

Always use /mnt/d/ paths explicitly in all script calls -- never ~ or /mnt/c/.

Emit types: finding, droplet, decision, progress, summary.
Cadence: 5-20 entries per run. Emit after each significant step.

---

## 4. Stigmergy (standard block -- include in every spawn)

```
STREAMING + STIGMERGY:
- Stream reasoning to your private trail (scratch MEM blocks or memory_bridge --stream)
- Write to the SHARED output path progressively -- draft at milestones, not just final
- Use frontmatter status: in-progress -> draft -> final to signal completeness
- If the shared output path already has content: READ IT FIRST, then build on it
The private stream is your COC trail. The shared output is the pheromone for the next agent.
Both layers. Always.
```

---

## 5. Quick Checklist (pre-return)

Before returning your final output, confirm all of the following:

- [ ] Manifest written (canonical attempted, fallback used if needed)
- [ ] Trace file written to staging manifests dir with valid entry_hash
- [ ] Streaming summary emitted via memory_bridge
- [ ] MEM HANDOFF block written to `{repo}/.claude/memory/scratch-{SESSION_ID}.md`
- [ ] Return format: `MANIFEST: {path} | dashboard_line: {<=80 chars}`

---

## Reference

- Relay script: `/mnt/d/0local/gitrepos/faerie2/scripts/agent_state_relay.py`
- Collector script: `/mnt/d/0local/gitrepos/faerie2/scripts/subagent_coc_collector.py`
- Collector prints template: `python3 scripts/subagent_coc_collector.py --template`
- Staging dir: `/mnt/d/0local/gitrepos/faerie2/.claude/manifests/` (create with `mkdir -p`)
- Canonical state: `/mnt/d/0LOCAL/.claude/hooks/state/`
- Forensics COC: `/mnt/d/0LOCAL/.claude/memory/forensics/agent-coc.jsonl`
