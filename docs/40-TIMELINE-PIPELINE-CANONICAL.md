# 40-TIMELINE-PIPELINE-CANONICAL

Canonical reference for `scripts/timeline_pipeline.py` and its companion
library `scripts/_timeline_pipeline_lib.py`. This document is the single
source of truth for the five-stage timeline pipeline: from raw multi-source
evidence to viz-ready JSON, with full chain-of-custody.

## TL;DR

The pipeline runs in five idempotent stages, each driven by a YAML/JSON
config. From a clean repo, the full path to viz is:

```bash
# Stage 1: raw sources -> normalized CSVs (canonical 10-column schema)
python3 scripts/timeline_pipeline.py normalize \
    scripts/timeline_pipeline.examples/sources.yml.example

# Stage 2: group normalized files into topic-consolidated CSVs
python3 scripts/timeline_pipeline.py consolidate \
    scripts/timeline_pipeline.examples/topics.yml.example

# Stage 3: union consolidated files into a master timeline
python3 scripts/timeline_pipeline.py build-master --tier all

# Stage 4: apply per-subset filters to produce curated CSVs
python3 scripts/timeline_pipeline.py build-curated \
    scripts/timeline_pipeline.examples/filters.yml.example

# Stage 5: shape curated subsets for a specific viz library
python3 scripts/timeline_pipeline.py build-viz-ready --target timelinejs
```

Each stage appends a hash-chained entry to `forensics/coc.jsonl` so the
provenance of every viz-ready JSON is recoverable end-to-end. The CLI
emits a single JSON audit object on stdout under `--json`, making it
drop-in compatible with the OpenHands SDK BashTool and any agent that
parses subprocess stdout.

## Why this exists

Four reference scripts in `cybertemplate` (`transform_normalize_RUN008.py`,
`consolidate_normalized.py`, `normalize_unified_evidence_RUN007.py`, and
the most recent `build_master_full.py`) each re-implemented the same
pattern with per-investigation deltas. The repeated motif:

1. Read N raw evidence files in heterogeneous formats.
2. Normalize each to a shared schema with a parseable timestamp.
3. Group by topic / hypothesis / actor.
4. Union into a master timeline with dedup.
5. Filter into curated subsets for a particular visualization.
6. Re-shape the subset for the target viz library.

The pattern is portable; the per-investigation scripts are not. This
canonical pipeline captures the pattern as a config-driven tool so future
investigations declare their sources in YAML and run the pipeline — no
per-investigation builder copy-paste, no schema drift.

## Architecture

```
                  raw evidence (CSVs, JSON)
                          |
              [stage 1: normalize] <-- sources.yml
                          |
              forensics/normalized/{source_id}.csv   (canonical 10-col)
                          |
              [stage 2: consolidate] <-- topics.yml
                          |
              forensics/consolidated/consolidated_{topic}.csv
                          |
              [stage 3: build-master] <-- --tier {T1|T2|T3|all}
                          |
              data/timelines/00-master/master-timeline-{tier}.csv
                          |
              [stage 4: build-curated] <-- filters.yml
                          |
              data/timelines/00-master/curated/{filter_name}.csv
                          |
              [stage 5: build-viz-ready] <-- --target {timelinejs|visjs|d3}
                          |
              data/timelines/30-viz-ready/{library}/{name}.{library}.json

  Every stage:
    - reads its config / inputs (idempotent re-reads on rerun)
    - writes atomically (tmp + fsync + rename) so kill -9 cannot corrupt
    - records an `_<stage>_audit.json` next to its outputs
    - appends a hash-chained entry to forensics/coc.jsonl (unless --no-coc)
    - prints a stable JSON audit on stdout when --json is set
```

## Canonical schema

Every normalized / consolidated / master / curated CSV uses the same
10-column schema. Frozen — additions require a charter change.

| Column           | Purpose                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| `ts_iso`         | ISO-8601 UTC timestamp with `Z` suffix. Required (rows without are dropped). |
| `actor_cluster`  | One of {`russia`, `china`, `doge`, `foreign-unknown`, `federal-victim`, `observation`}. |
| `source_file`    | Origin filename / label (free-form, but stable per source).              |
| `event_type`     | Event class (e.g. `shodan_observation`, `prometheus_metric`, `cert_observation`). |
| `host_or_entity` | IP / hostname / instance identifier; empty when the source has none.    |
| `lat`            | Optional latitude (string-stored to keep CSV simple).                    |
| `lon`            | Optional longitude.                                                      |
| `hypothesis_tags`| Pipe-delimited tags from {`H1`,`H2`,`H3`,`H4`,`H5`,`NONE`}.              |
| `tier`           | One of {`T1`=smoking_gun, `T2`=strong_support, `T3`=contextual}.         |
| `raw_payload`    | JSON-encoded original record, truncated to 2KB with pruning indicator.   |

The frozen vocabularies live in `scripts/_timeline_pipeline_lib.py`:
`ACTOR_CLUSTERS`, `HYPOTHESIS_TAGS`, `TIER_SEMANTICS`, `CANONICAL_COLUMNS`,
`VIZ_LIBRARIES`. Do not invent new values; extend the vocab in lib + schema
+ this doc atomically.

## Config files

### sources.yml — stage 1 input

Schema: `forensics/schemas/shape/timeline-sources.schema.json`.

```yaml
sources:
  - id: shodan-azuregov                  # filename-safe; output is normalized/{id}.csv
    path: forensics/normalized/shodan/consolidated_shodan_azuregov.csv
    timestamp_column: timestamp           # column carrying the ts
    host_column: ip_str                   # optional host/entity column
    actor_cluster: federal-victim         # frozen vocab
    tier: T2                              # frozen vocab
    event_type: shodan_observation        # free-form label
    hypothesis_tags: [H3]                 # frozen vocab items
```

JSON-shaped sources work too — declare `records_key: <top-level array key>`
(default `records`) and use field names instead of CSV columns.

### topics.yml — stage 2 input

```yaml
topics:
  - name: shodan_federal                  # output: consolidated_{name}.csv
    description: "All shodan observations against federal/azure-gov surfaces."
    source_ids:                           # explicit by id
      - shodan-azuregov
      - shodan-azuregov-sql
    match_patterns:                       # additional glob matches
      - "shodan-*.csv"
```

### filters.yml — stage 4 input

Schema: `forensics/schemas/shape/timeline-filters.schema.json`.

```yaml
filters:
  - name: tier1_and_tier2
    description: "Smoking-gun + strong-support; default storytelling view."
    where: "tier in ('T1','T2')"          # safe DSL — NOT Python eval
    target_viz: timelinejs                # optional hint for stage 5
```

The filter DSL is intentionally tiny and parsed by an allow-listed clause
compiler (`tpl._compile_where`). Clauses join by ` AND `:

- `<field> == 'value'`
- `<field> != 'value'`
- `<field> in ('a','b','c')`
- `<field> contains 'substring'`
- `<field> matches 'regex'`
- `<field> startswith 'prefix'`

Field set = the 10 canonical columns. The DSL does not call `eval()` and
does not import user code. Unsupported syntax is rejected at compile.

## Worked example — building a foreign-actor T1 timeline

```bash
# 1. Declare sources covering Russia + China cert observations + tier-1 events
cat > /tmp/sources-foreign.yml <<EOF
sources:
  - id: certs-russia-aeza
    path: forensics/normalized/certs/russia_aeza_certs.csv
    timestamp_column: not_before
    host_column: ip
    actor_cluster: russia
    tier: T2
    event_type: cert_observation
    hypothesis_tags: [H4]
  - id: tier1-smoking-gun-events
    path: forensics/evidence_tiers/tier1_smoking_gun.json
    records_key: records
    timestamp_column: first_observed
    host_column: entity_value
    actor_cluster: observation
    tier: T1
    event_type: smoking_gun
    hypothesis_tags: [H1, H2, H3, H4]
EOF

# 2. Normalize
python3 scripts/timeline_pipeline.py normalize /tmp/sources-foreign.yml

# 3. Skip topic consolidation (only two sources) — go straight to master
cat > /tmp/topics-foreign.yml <<EOF
topics:
  - name: foreign_seed
    source_ids: [certs-russia-aeza, tier1-smoking-gun-events]
EOF
python3 scripts/timeline_pipeline.py consolidate /tmp/topics-foreign.yml

# 4. Master across all tiers
python3 scripts/timeline_pipeline.py build-master --tier all

# 5. Curate to "T1 + foreign-actor only"
cat > /tmp/filters-foreign.yml <<EOF
filters:
  - name: smoking_gun_foreign
    where: "tier == 'T1' AND actor_cluster in ('russia','china')"
    target_viz: timelinejs
EOF
python3 scripts/timeline_pipeline.py build-curated /tmp/filters-foreign.yml

# 6. Shape for TimelineJS
python3 scripts/timeline_pipeline.py build-viz-ready --target timelinejs \
    --source data/timelines/00-master/curated/smoking_gun_foreign.csv
```

Each stage records an audit JSON next to its outputs and appends to
`forensics/coc.jsonl`. The viz JSON at
`data/timelines/30-viz-ready/timelinejs/smoking_gun_foreign.timelinejs.json`
is traceable through the COC tail back to the raw `russia_aeza_certs.csv`
sha256.

## Migrating from per-investigation builders

The reference script `build_master_full.py` (cybertemplate, 486 lines) is
the cleanest extant pattern. Below is its before/after under the canonical
pipeline.

### Before (build_master_full.py — excerpt)

```python
SOURCES = [
    {"rel": "data/viz/normalized/consolidated/consolidated_shodan_azuregov.csv",
     "ts_col": "timestamp", "ip_col": "ip_str",
     "actor_cluster": "federal-victim", "event_type": "shodan_observation", "tier": "T2"},
    # ... five more inline source dicts ...
]
# ... 400 lines of: PID lock + signal handlers + parse_ts + truncate_payload +
#                   dedup + actor/tier/event counters + atomic CSV/JSON writers +
#                   per-source streaming loop + audit JSON writer ...
```

### After (canonical pipeline)

```yaml
# sources.yml
sources:
  - id: shodan-azuregov
    path: data/viz/normalized/consolidated/consolidated_shodan_azuregov.csv
    timestamp_column: timestamp
    host_column: ip_str
    actor_cluster: federal-victim
    tier: T2
    event_type: shodan_observation
  # ... five more entries ...
```

```bash
python3 scripts/timeline_pipeline.py normalize sources.yml
python3 scripts/timeline_pipeline.py build-master --tier all
```

The 486 lines collapse to ~30 lines of YAML + two CLI invocations. PID
locking, signal handling, atomic writes, dedup, audits, and COC chaining
are inherited from the library — no per-investigation re-implementation,
no schema drift.

## OpenHands SDK / CLI integration

`scripts/timeline_pipeline.py` is designed to be drop-in callable from the
OpenHands BashTool / RunCommand surface. Conventions honored:

- **`--json` flag** on every subcommand emits a single, well-formed JSON
  audit object on stdout. Progress log lines route to stderr. The audit
  has stable top-level keys (`stage`, `audits`, `audit_path`) that OH
  tool wrappers can rely on.
- **`-` for stdin config** on `normalize`, `consolidate`, `build-curated`.
  Lets an OH agent stream config without writing to disk:

  ```python
  result = bash_tool.run(
      cmd="python3 scripts/timeline_pipeline.py normalize - --json",
      stdin=yaml.dump({"sources": [...]}),
  )
  audit = json.loads(result.stdout)
  ```

- **Stable exit codes**: 0 ok, 1 verify-coc mismatch, 2 usage/config error,
  3 stage error. OH tool wrappers gate downstream actions on `exit_code`.
- **No global mutable state**: the lib functions are pure-ish (write side
  effects only via atomic_write_*); safe to call from inside a sub-agent.
- **PID lock per stage**: concurrent same-stage runs are blocked. Cross-
  stage runs in parallel are supported (different PID files).
- **No mandatory non-stdlib deps** except pandas (only imported by the
  charter-related sibling scripts, not by this pipeline). PyYAML is
  optional — JSON config is accepted on every path.

Example OH SDK tool wrapper sketch:

```python
from openhands.tools import bash

def run_pipeline_stage(stage: str, config: dict) -> dict:
    """Wrap one pipeline stage as an OH-callable tool."""
    proc = bash(
        f"python3 scripts/timeline_pipeline.py {stage} - --json",
        stdin=json.dumps(config),
        cwd="/workspace/faerie2",
    )
    if proc.exit_code != 0:
        raise RuntimeError(f"{stage} failed: {proc.stderr}")
    return json.loads(proc.stdout)
```

## COC integrity guarantees

Every durable write the pipeline performs is recorded in
`forensics/coc.jsonl` as a hash-chained JSONL entry. The chain rule
(implemented in `tpl.append_coc_entry`):

- `parent_hash` of entry N = `entry_hash` of entry N-1 (or `"genesis"`).
- `entry_hash` = sha256 of canonical-JSON of the entry with the
  `entry_hash` field removed.
- Canonical-JSON = `sort_keys=True, separators=(",",":")`, UTF-8.

Verify the chain at any time:

```bash
python3 scripts/timeline_pipeline.py verify-coc
# Exit code 0 = chain valid; 1 = mismatch detected. Output is JSON.
```

Use `--no-coc` to skip chain appends for dev / dry-run iteration.

## Anti-patterns (do not do these)

1. **Per-investigation copy-paste builders.** If you find yourself
   editing `build_master_full.py` to add a new investigation, stop:
   declare it in `sources.yml` and call `timeline_pipeline normalize`.
2. **Hardcoded actor / hypothesis / tier values.** Use the frozen
   vocabulary in `_timeline_pipeline_lib.py`. Extending the vocab
   requires a charter change so downstream consumers stay aligned.
3. **Schema drift in normalized CSVs.** Always emit the 10 canonical
   columns in order. The pipeline drops rows that fail to parse
   `ts_iso`; downstream stages assume the schema is universal.
4. **Non-atomic writes.** Use `tpl.atomic_write_csv` / `atomic_write_text`
   for every durable output. A kill -9 mid-write must never leave a
   half-finished CSV in canonical locations.
5. **Inline secrets in raw_payload.** The 2KB truncation does NOT redact;
   it just prunes. If your source contains secrets, redact before
   normalize, not after.
6. **Bypassing `--json` in agent integrations.** When OH agents call the
   pipeline, always use `--json` so the audit is parseable; mixing log
   lines with JSON breaks tool wrappers.

## Related canonical references

- `forensics/schemas/shape/timeline-sources.schema.json` — JSON Schema for sources.yml
- `forensics/schemas/shape/timeline-filters.schema.json` — JSON Schema for filters.yml
- `.agents/skills/timeline-pipeline/SKILL.md` — microagent fire-on-keyword guide
- `forensics/charters/active/2026-05-21_canonical-timeline-pipeline.json` — charter

## Source inspiration (read-only references)

These four scripts in `cybertemplate/` were the inputs from which the
pattern was extracted. Do NOT depend on them at runtime; they remain
in-place as per-investigation history.

- `cybertemplate/scripts/transform_normalize_RUN008.py`
- `cybertemplate/scripts/consolidate_normalized.py`
- `cybertemplate/scripts/normalize_unified_evidence_RUN007.py`
- `cybertemplate/forensics/ephemeral/2026-05-21/timeline-master-full-vs-curated-02/build_master_full.py`

---

*The pipeline is the pattern. The pattern is portable. The config is the
investigation.*
