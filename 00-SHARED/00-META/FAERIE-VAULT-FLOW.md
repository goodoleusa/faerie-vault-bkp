---
type: system-design
tags: [architecture, mermaid, data-flow, faerie]
parent: "[[INDEX]]"
up: "[[00-SHARED/Hive/_index|Hive]]"
sibling:
  - "[[00-SHARED/Dashboards/system/System-Architecture|System Architecture]]"
status: active
doc_hash: sha256:51dfae7fcd3a75988eb4bba5a201675e528d672439dcb3b7734d36e7ff158224
hash_ts: 2026-04-07T02:49:50Z
hash_method: body-sha256-v1
---

> [[HOME]] > [[INDEX|00-META]] > **Faerie-Vault Data Flow**

# Faerie ↔ Vault Data Flow

How Claude CLI sessions, memory layers, and the Obsidian vault connect.

```mermaid
graph TD
    A[Claude CLI Session] -->|MEM blocks| B[scratch-SESSION.md]
    B -->|memory-keeper promotes| C[NECTAR.md]
    C -->|faerie crystallize| D[HONEY.md]
    A -->|agent writes| E[00-SHARED/Agent-Outbox]
    E -->|human promotes| F[30-Evidence / 01-PROTECTED]
    A -->|HIGH flags| G[Human-Inbox/flags]
    H[Human in Obsidian] -->|annotations| I[00-SHARED/Queue]
    I -->|vault_annotation_sync| A
    H -->|vault Queue edit| J[sprint-queue.md]
    J -->|queue_vault_sync import| K[sprint-queue.json]
    K -->|faerie Turn-1| A
```

---

## Memory Layer Detail

```mermaid
graph LR
    subgraph LOCAL["Local (~/.claude/memory/)"]
        HONEY[HONEY.md\nseed — dense]
        NECTAR[NECTAR.md\nnarrative — unbounded]
        INBOX[REVIEW-INBOX.md\nhuman review queue]
    end
    subgraph VAULT["Vault (00-SHARED/)"]
        AO[Agent-Outbox\nwork products]
        HI[Human-Inbox\nfindings + flags]
        Q[Queue\nsprint tasks]
        D[Droplets\nreal-time insights]
    end
    subgraph REPO["{repo}/.claude/memory/"]
        SCR[scratch-SID.md\nworking notes]
    end

    SCR -->|memory-keeper| NECTAR
    SCR -->|HIGH flags| INBOX
    NECTAR -->|crystallize| HONEY
    SCR -->|agent writes| AO
    AO -->|human review| HI
    D -->|promote| NECTAR
```

---

## Write Routing Quick Reference

| Observation type | Destination |
|-----------------|-------------|
| Session working notes | `{repo}/.claude/memory/scratch-{SID}.md` |
| HIGH priority flag | Also `~/.claude/memory/REVIEW-INBOX.md` |
| Validated finding | memory-keeper → `~/.claude/memory/NECTAR.md` |
| Durable fact / preference | faerie crystallize → `~/.claude/memory/HONEY.md` |
| Agent work product | `00-SHARED/Agent-Outbox/` |
| Real-time insight | `00-SHARED/Droplets/LIVE-{date}.md` |

---

*[[00-SHARED/Hive/SYSTEM-GUIDE|System Guide]] · [[00-SHARED/Dashboards/system/System-Architecture|Full Architecture]] · [[INDEX|Meta]]*
