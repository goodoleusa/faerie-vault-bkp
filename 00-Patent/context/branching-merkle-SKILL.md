---
name: branching-merkle
description: |
  Git-shaped COC branching, Merkle rollup, and signed-merge acceptance ritual.
  When parallel agent waves need isolated write lanes, they fork a branch, write
  internal hash-chained entries, compute a Merkle root over the branch, then
  bring all that work back to main via a SIGNED two-parent merge manifest.
  Forensically airtight: anyone can walk the main chain, find the merge entry,
  follow the Merkle root pointer, and verify every branch entry's inclusion proof.
type: knowledge
triggers:
  - branch
  - branching
  - fork
  - coc branch
  - merkle rollup
  - merkle root
  - merge ritual
  - acceptance manifest
  - two-parent merge
  - branch merge
  - coc fork
  - branch lifecycle
  - parallel agent wave
  - signed merge
  - inclusion proof
  - branch acceptance
  - forensic branch
  - coc-branches
  - branch genesis
  - fork-point anchor
_bundle_note: "FULL COPY from .agents/skills/branching-merkle/SKILL.md for publication-prep-2026-05-25. Supports whitepaper §5.2 (Merkle rollup + signed-merge acceptance ritual claim). Key figures: branch-merge COC entries with Ed25519 signatures appear at coc.jsonl lines 223 + 226 (the live evidence). The five-step lifecycle FORK→WRITE→ROLLUP→MERGE→VERIFY is this skill's core claim."
---

# branching-merkle — Git-shaped COC for parallel agent waves

The COC ledger (`forensics/coc.jsonl`) is normally a **linear hash-chained
append-only log**. Branching extends this into a **Git-shaped structure**:
parallel write lanes that merge back with cryptographic proof of every entry.

The lifecycle is distinct from mission graph querying (why this is its own
skill, not an extension of `mission/`):

```
FORK    open a named branch at a fork-point anchor in the main chain
WRITE   agents write internally hash-chained entries to the branch file
ROLLUP  compute a Merkle root over all branch entry hashes
MERGE   write a signed two-parent acceptance manifest to main
VERIFY  anyone walks main → hits merge → follows Merkle root → verifies all
```

---

## The fork question — when do you fork vs write to main?

Fork when ANY of these apply:

| Trigger | Why it warrants a branch |
|---|---|
| **Parallel-team wave writing 10+ manifests** | Linear main becomes a bottleneck; branch gives each wave its own lock-free write lane |
| **Exploratory / uncertain-merge work** | Branch can be abandoned without polluting main; no merge = no forensic noise |
| **Multi-day work that might be abandoned** | A dead branch is a clean forensic record of what was tried; it doesn't clutter the main timeline |
| **Sensitivity-isolated work** | Branch-level ACL: forensics/coc-branches/ can have different visibility than coc.jsonl |
| **Agent wave size >= 3 concurrent agents on same mission** | Concurrent lock contention on the main file; per-branch fcntl.flock eliminates the bottleneck |

**Do NOT fork when:**

- Work is a single manifest (branch overhead exceeds benefit — just write to main)
- Urgent hot-fix that must land on main NOW (skip branch, merge later if needed)
- Session-local exploration (use `forensics/ephemeral/` — it's already isolated; no COC branch needed)
- Sequential work (B starts only after A seals) — no concurrency = no branch justification

**Decision rule:** If your wave will write >= 10 manifests OR 3+ agents run concurrently on
the same mission → fork. Otherwise → write to main.

---

## The fork ritual

```bash
python3 scripts/mission_graph.py branch <name> [--from <hash>]
```

What this does:
1. Reads current main COC tail hash (or the `--from` hash if specified)
2. Creates `forensics/coc-branches/<name>.jsonl`
3. Writes a **branch genesis entry** — `prev_entry_hash = main_tail_hash` (the fork-point anchor)
4. Sets `coc_chain.branch = "<name>"` on all subsequent entries in this file
5. Creates `forensics/coc-branches/<name>.meta.json` with status `open`

The genesis entry's `prev_entry_hash` IS the link back to main. The branch
is anchored in the main timeline at the exact moment of fork.

**Naming convention:** `<mission-slug>-<wave-id>` — e.g. `branching-merkle-w1`.
Use kebab, no dots (dots are reserved for mission IDs).

---

## Branch life — writing to the branch

Agents write to the branch normally via `1g_coc_core.py` with `branch=<name>`:

```python
append_coc_entry(payload, branch="branching-merkle-w1")
```

Under the hood:
- Writes to `forensics/coc-branches/<name>.jsonl` (NOT `coc.jsonl`)
- `coc_chain.branch = "<name>"` stamped on every entry
- Each entry's `prev_entry_hash` points to the prior entry IN THE BRANCH (internal chain)
- The genesis entry's `prev_entry_hash` points to the main fork-point (cross-chain anchor)
- `fcntl.flock` is per-branch-file (concurrent multi-branch work is lock-free across branches)

Agents are **unaware of branching complexity** — they call the same `append_coc_entry()` API.
The branch routing is ambient, wired by the infrastructure.

---

## The Merkle rollup

```bash
python3 scripts/mission_graph.py merkle-root <branch>
```

What this does:
1. Reads `forensics/coc-branches/<branch>.jsonl` — all entries in order
2. Collects each entry's `coc_chain.entry_hash` (sha256, same algo as main chain)
3. Calls `_merkle_tree.build_merkle_tree(leaves)` — produces `{root, levels}`
4. Writes `forensics/coc-branches/<branch>.merkle-root.json`:

```json
{
  "branch": "<name>",
  "merkle_root": "<hex>",
  "leaf_count": 47,
  "algo": "sha256",
  "computed_at": "<iso-utc>",
  "levels": ["<level-0-hashes>", "..."]
}
```

The Merkle root is a **single hash that cryptographically commits to every
entry in the branch**. You cannot change any branch entry without changing
the root.

---

## The acceptance ritual — merge

The merge ritual brings a branch back to main as a **two-parent signed manifest**:

### Step 1: Author the acceptance manifest

```json
{
  "task_id": "<branch-accept-task-id>",
  "mission": "<same mission as the branch>",
  "lifecycle_judgment": {
    "kind": "promote",
    "rationale": "Branch branching-merkle-w1 (47 entries) reviewed and accepted."
  },
  "coc_chain": {
    "parent_hashes": [
      "<main_prior_tail_hash>",
      "<branch_merkle_root>"
    ],
    "branch": "main",
    "entry_hash_algo": "sha256",
    "entry_hash": "<computed-by-hook>",
    "signed_by": "ed25519:<key-id>"
  },
  "branch_merge": {
    "branch_name": "<name>",
    "merkle_root": "<hex>",
    "merkle_root_file": "forensics/coc-branches/<name>.merkle-root.json",
    "leaf_count": 47,
    "fork_point_hash": "<main-hash-at-fork>"
  }
}
```

**The two parents are:**
1. `main_prior_tail_hash` — the last entry on main before the merge (main chain continuity)
2. `branch_merkle_root` — the Merkle root over all branch entries (branch summary proof)

### Step 2: Execute the merge

```bash
python3 scripts/mission_graph.py merge <branch> --acceptance-manifest <path>
```

### Step 3: Verify (any time, any auditor)

```bash
python3 scripts/mission_graph.py verify --include-branches
```

Forensically airtight: no trust required in the operator. The math proves it.

---

## Anti-patterns

- **Forking for single-manifest work** — overhead outweighs benefit; write to main
- **Merging without signing** — unsigned acceptance manifest is rejected; sign before merge
- **Writing to a merged branch** — meta.json `status: merged` means sealed; create a new branch
- **Using a branch to hide work from audit** — branches are equally auditable; the merge entry is on main

---

## See also

- `scripts/mission_graph.py` — `branch`, `merkle-root`, `merge`, `verify --include-branches` verbs
- `scripts/_merkle_tree.py` — canonical Merkle implementation
- `forensics/charters/proposals/2026-05-25Z__charter__rekor-merkle-root-public-anchor__goodoleusa.json` — Phase 3 Rekor proposal
- `forensics/coc-branches/` — all branch files (jsonl + merkle-root.json + meta.json per branch)
