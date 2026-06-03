# Unified Vault UX — Five Surfaces, One Filesystem

The swarmy UX is not a single application. It's a constellation of surfaces
that share state through the vault and the MCP tool layer. Each surface
exists because it's the best place to do one mode of work. None of them
"wins" — the integration is the product.

The **Hive web UI** (chat-mvp dashboards) is where you steer. Agent rosters,
mission frontiers, bearing badges, the live event ticker — it answers
"what is the swarm doing right now, and where should it go next?" You come
here to dispatch, not to think long-form.

The **Recursive Canvas** in the dev space is where you sketch. It's the
vibe-coding surface: rapid prototyping, structural doodles, the place
ideas land before they have names. Low friction, high churn. Most of what
happens here is throwaway, and that's the point.

**Obsidian-in-docker** is where prose lives. Daily synthesis, narrative
threads, the slow accreting kind of writing that needs a reader-cold test.
The vault filesystem underneath Obsidian is what the rest of the system
also reads, so writing here is not siloed — it's just the surface best
tuned for sustained prose.

**Excalidraw** cross-cuts both. Commit topology, mind maps, visual
ideation that's too structured for the canvas but too pictorial for
Obsidian. It lives wherever it's most useful and embeds into the other
surfaces.

The **swarmy-hive-plugin** is the bridge. It lets Obsidian see the swarm:
agent status, manifest trails, mission graph. It's what makes the vault
not just a notes folder but a window into the live system.

Users move between these surfaces by intent, not by tool branding. You
sketch on the canvas, dispatch from the Hive, write in Obsidian, draw in
Excalidraw, and the plugin keeps the seams from showing. State flows
through the vault filesystem; coordination flows through the MCP tools.
The surfaces don't compete — they specialize. The integration is what
ships.

---

## Operational addendum (2026-05-22, agent-b cut 6)

> Concrete wiring landed this session: the Hive dashboard now contains
> a 📓 Vault sub-tab (`HivePanelV2.jsx` → `VaultPreviewPane.jsx`), and
> the operator reaches Obsidian *through* the Hive rather than as a
> separate app. Mandate framing: **"Obsidian is not THE ui, it's
> part of it."**

### The Hive → Obsidian path (full diagram)

```
   swarmy.retrofuture.tech                      vault-dev.retrofuture.tech
   ┌─────────────────────────┐                  ┌──────────────────────┐
   │  Hive · 🐝              │                  │  Obsidian browser    │
   │  sub-tabs:              │   click          │  (KasmVNC streaming  │
   │    📋  Missions          │   "Open          │   the real binary)   │
   │    🔮  Vibe             │   Obsidian"      │                      │
   │    📊  DAG              │   ───────────►   │  swarmy-hive-plugin  │
   │    🌸  Live Swarm        │                  │  registered + loaded │
   │    📓  Vault  ◄── NEW    │                  │                      │
   │       │ status buckets  │                  │  Two-layer canvas    │
   │       │ recent daily    │                  │  Commit topology     │
   │       │ Open Obsidian   │                  │  Status-tag (NEW)    │
   └─────────────────────────┘                  │  Card templates(NEW) │
                                                │  Commit-to-charter(N)│
                                                └──────────────────────┘
                       │                                  │
                       └─────────────┬────────────────────┘
                                     ▼
                ┌─────────────────────────────────────┐
                │  /mnt/d/0local/faerie-vault/        │
                │  Bind-mounted into BOTH containers  │
                │  (Obsidian + OpenHands agent)       │
                │  Single source of truth.            │
                └─────────────────────────────────────┘
```

### What landed this session

| Cut | Artifact | Effect |
|---|---|---|
| 2 | Template shelves folded into vault (`_meta/`, `00-Welcome/`, `10-Charters/`, `80-Publications/`) | Charters can now be authored *in* the vault with templates |
| 3 | `deploy/scripts/09-install-swarmy-hive-plugin.sh` | One-shot installs plugin into vault's `.obsidian/plugins/hive/` |
| 4 | `VaultPreviewPane.jsx` + new Hive sub-tab `📓 Vault` | Vault is now visible from the Hive without iframe |
| 5 | `swarmy-hive-plugin/src/canvas-recursive.ts` (≤220 LOC) | Status-tag commands + card-template presets + commit-to-charter |
| 6 | This addendum | Operational doc for next agent + operator |

### Day-1 operator runbook

```bash
# 1. Install the plugin into the operational vault.
bash deploy/scripts/09-install-swarmy-hive-plugin.sh

# 2. Restart the Obsidian container so it picks up the plugin.
docker restart swarmy-vault

# 3. Open the Hive.
open https://swarmy.retrofuture.tech
#    → click 🐝 Hive tab
#    → click 📓 Vault sub-tab
#    → see status-bucket counts + recent daily list
#    → click 🪟 Open Obsidian for full editing

# 4. In Obsidian (first time only):
#    Settings → Community Plugins → enable "Hive"
#    (the install script also writes community-plugins.json so this
#     step is auto-skipped on subsequent installs.)

# 5. Try the new canvas commands (Ctrl/Cmd-P inside Obsidian):
#    "Canvas: status → 📝 Annotating"
#    "Canvas: apply decker template"
#    "Canvas: commit to forensics/charters/active/"
```

### Decision: preview-pane (option B) not iframe (option A)

Three reasons, listed in increasing order of importance:

1. **Technical:** `vault-dev.retrofuture.tech` sits behind basic_auth.
   An iframe would need credential forwarding. KasmVNC ships
   `X-Frame-Options: SAMEORIGIN` blocking embed regardless.
2. **Aesthetic:** Obsidian fills its viewport with sidebars + tab
   bars. Embedding it shrinks the Hive's real estate to almost
   nothing useful while making the Obsidian view itself cramped.
3. **Conceptual (decisive):** *Obsidian is not THE ui; it's part of
   it.* An iframe would silently re-elevate Obsidian to "the main
   surface inside the Hive." The preview pane keeps Hive as the
   conductor and Obsidian as one instrument.
