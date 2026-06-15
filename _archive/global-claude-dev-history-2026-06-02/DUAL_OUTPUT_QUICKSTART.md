# Dual-Output System Quick Start

**TL;DR:** Agents emit JSON manifest + vault narrative in one pass using `manifest_to_vault_narrative` library.

---

## 5-Minute Setup

### 1. Import Library (In Agent Code)

```python
from manifest_to_vault_narrative import render_vault_narrative
import json, os
from pathlib import Path
from datetime import datetime
```

### 2. Build Manifest (Dictionary)

```python
manifest = {
    'task_id': 'your-task-id',
    'mission': 'mission-name',
    'bearing': 'N',  # or S, E, W
    'from_label': 'source_task',
    'rationale': 'Why this discovery matters',
    'quality_score': 0.95,
    'discovered_work': [
        {'task_id': 'next-task', 'bearing': 'S', 'rationale': 'Unblocked'}
    ],
    'next_mission_node': {'bearing': 'S', 'rationale': 'Next phase'}
}
```

### 3. Write Manifest (JSON)

```python
date_iso = datetime.utcnow().date().isoformat()
manifest_path = Path(f'forensics/manifests/{date_iso}/{manifest["task_id"]}.json')
manifest_path.parent.mkdir(parents=True, exist_ok=True)
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)
```

### 4. Render & Write Vault Narrative (Markdown)

```python
vault_md = render_vault_narrative(
    manifest=manifest,
    session_id=os.environ.get('CLAUDE_SESSION_ID'),
    tags=[manifest['mission'].split('-')]
)
vault_path = Path(f'vault/Daily/{date_iso}/{manifest["mission"]}-{manifest["bearing"]}.md')
vault_path.parent.mkdir(parents=True, exist_ok=True)
vault_path.write_text(vault_md)
```

### 5. Done! 🎉

- ✅ Manifest written: `forensics/manifests/{date}/{task_id}.json`
- ✅ Narrative written: `vault/Daily/{date}/{mission}-{bearing}.md`

---

## Compass Bearings (Choose One)

| Bearing | Use When | Example |
|---------|----------|---------|
| **N** | Upstream task unblocked | Cert validation done → tier-1 unblocked |
| **S** | Ship next phase | Curation done → move to stats |
| **E** | Parallel work | Timestamp check (sister task) |
| **W** | Backtrack | Found contradiction → revisit baseline |

---

## Manifest Fields (Required)

| Field | Type | Example |
|-------|------|---------|
| `task_id` | string | `"cert-validation-001"` |
| `mission` | string | `"evidence-tier-v2"` |
| `bearing` | char | `"N"` |
| `from_label` | string | `"raw-cert-ingest"` |
| `rationale` | string | `"Certificate verification confirms..."` |
| `quality_score` | float 0.0-1.0 | `0.95` |
| `discovered_work` | list | `[{task_id, bearing, rationale}]` |
| `next_mission_node` | object | `{bearing, rationale}` |

---

## Full Code Example

```python
# Your agent's final output phase
from manifest_to_vault_narrative import render_vault_narrative
import json, os
from pathlib import Path
from datetime import datetime

# Build manifest from your work
manifest = {
    'task_id': 'cert-validation-001',
    'mission': 'evidence-tier-v2',
    'bearing': 'N',
    'from_label': 'raw-cert-ingest',
    'rationale': '241 Treasury cert nodes validated against crt.sh; 3 matches confirmed',
    'quality_score': 0.97,
    'discovered_work': [
        {
            'task_id': 'tier-1-smoking-gun',
            'bearing': 'S',
            'from_label': 'cert-validation-001',
            'to_label': 'tier-1-smoking-gun',
            'rationale': '3 valid certs unblock smoking gun tier'
        }
    ],
    'next_mission_node': {
        'bearing': 'S',
        'rationale': 'Move to Tier-1 curation + evidence bundle'
    }
}

# Write canonical manifest
date_iso = datetime.utcnow().date().isoformat()
manifest_path = Path(f'forensics/manifests/{date_iso}/{manifest["task_id"]}.json')
manifest_path.parent.mkdir(parents=True, exist_ok=True)
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

# Render vault narrative
vault_md = render_vault_narrative(
    manifest=manifest,
    session_id=os.environ.get('CLAUDE_SESSION_ID', 'unknown'),
    tags=['evidence', 'tier-v2', 'certificates']
)

# Write vault narrative
vault_path = Path(f'vault/Daily/{date_iso}/{manifest["mission"]}-{manifest["bearing"]}.md')
vault_path.parent.mkdir(parents=True, exist_ok=True)
vault_path.write_text(vault_md)

# Return summary
print(f"✅ Dual output emitted:")
print(f"  Manifest: {manifest_path}")
print(f"  Narrative: {vault_path}")
```

---

## What Gets Generated

### Manifest (JSON)
```json
{
  "task_id": "cert-validation-001",
  "mission": "evidence-tier-v2",
  "bearing": "N",
  ...
}
```

### Narrative (Markdown with Frontmatter)
```markdown
---
mission: evidence-tier-v2
bearing: N
bearing_symbol: 🧭
task_id: cert-validation-001
quality_score: 0.97
tags: ["evidence", "tier-v2", "certificates"]
---

# 🧭 Evidence Tier V2 — N Bearing

**Task ID:** `cert-validation-001`

## Discovery Snapshot

241 Treasury cert nodes validated against crt.sh; 3 matches confirmed

## Discovered Work

- **[[tier-1-smoking-gun]]** (⬇️)
  Bearing: Conclude / move downstream
  Rationale: 3 valid certs unblock smoking gun tier

...
```

---

## In Obsidian

1. View Daily/{date}/{mission}-{bearing}.md
2. Click [[task_id]] → navigate to that task's page
3. Open graph view (Cmd/Ctrl+P → "Juggl: Open graph")
4. See mission DAG with N/S/E/W bearings as edges

---

## Test Your Setup

```bash
python3 ~/.claude/hooks/test_manifest_to_vault_narrative.py
```

All 7 tests should pass ✅

---

## See Also

- Full guide: `launch/VAULT_AS_UI_IMPLEMENTATION_GUIDE.md`
- Templates: `~/.claude/templates/nunjucks/*.nunjucks`
- Library: `~/.claude/hooks/manifest_to_vault_narrative.py`

---

**Status: Ready to use. Copy code snippet above into your agent's final output phase.**
