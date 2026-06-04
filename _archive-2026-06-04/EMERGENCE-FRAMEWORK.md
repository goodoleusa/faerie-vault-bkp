---
type: reference
status: live
created: 2026-04-27
updated: 2026-04-27
tags: [emergence, stigmergy, faerie-vault, framework]
---

> **Breadcrumb:** faerie-vault > EMERGENCE-FRAMEWORK

# Emergence and Stigmergy — faerie-vault Reference

**faerie-vault is a template.** The emergence and stigmergy framework that powers faerie2 applies directly to your vault.

This doc points to the canonical framework docs (in faerie2/) and explains how to recognize emergence patterns in your own agentic workflows.

---

## Quick Links

**Canonical framework (in faerie2):**
- 📘 [3x-EMERGENCE.md](../faerie2/docs/3x-EMERGENCE.md) — Formal definitions, five patterns, academic citations, f(0) mathematics, reputation system
- 📘 [4x-RESEARCH-PAPER-OUTLINE.md](../faerie2/docs/4x-RESEARCH-PAPER-OUTLINE.md) — 8 arXiv papers surveyed, 5 novel contributions, publication pathway

**Vault hub (in faerie-vault):**
- 📋 [EMERGENCE-AND-STIGMERGY.md](./00-SHARED/Hive/EMERGENCE-AND-STIGMERGY.md) — Central reference with examples and links
- 📋 [RESEARCH-PAPER-OUTLINE-faerie2.md](./00-SHARED/Hive/RESEARCH-PAPER-OUTLINE-faerie2.md) — Vault mirror of research findings

**Release notes:**
- 📊 [RELEASE-NOTES-v1.5.md](../faerie2/docs/releases/RELEASE-NOTES-v1.5.md) — v1.5 release with emergence framework, reputation system, measured improvements

---

## What It Means for Your Vault

When you use this template, you're implementing a system where:

1. **Agents coordinate via your vault** — They leave traces (frontmatter, timestamps, investigation_labels)
2. **Emergence happens naturally** — At sufficient density, coordinated behavior emerges without explicit rules
3. **Stigmergy is your tool** — Agents read each other's documents (via compass edges, investigation_labels, droplets) and act independently

### Three Patterns to Watch For

**Pattern 1: Task Decomposition**  
You find that work breaks down automatically — one agent identifies a problem, writes it to a manifest, and another agent picks it up without being asked. This is stigmergic task decomposition.

**Pattern 2: Self-Generalization**  
One agent fixes a problem in one context (e.g., plugin config in faerie-vault), and another agent sees the same pattern and applies it elsewhere (e.g., CT_VAULT). No coordination needed.

**Pattern 3: Distributed Detection**  
Multiple agents working on different aspects of a problem independently arrive at compatible solutions because they all read the same manifests and understand each other's findings.

---

## Your Vault as Stigmergic Substrate

These vault structures enable emergence:

- **00-SHARED/Droplets/** — Agents discover nuggets of insight here and apply them
- **00-SHARED/Hive/** — Central location where findings bubble up; agents read this to learn
- **00-Inbox/Daily/{YYYY-MM-DD}/** — Daily work appears here; agents find work to do
- **Frontmatter fields** (type, status, investigation_label, etc.) — Signals that agents read and respond to
- **Breadcrumb lines** — Navigation hints that help agents understand document relationships

---

## Toolkit

- **Obsidian plugins** (all configured and ready): linter (injects frontmatter), make-md (clusters by investigation_label), dataview (queries frontmatter), file-title-updater (sync filename ↔ title)
- **CLI scripts** (reference from faerie2/scripts/): compass_query.py (shows graph topology), mission_graph_ops.py (routes work), coc_writer.py (tracks changes)
- **Manifest convention** — Every agent output includes `compass_edge`, `next_task_queued`, `investigation_label` (see VAULT-SCHEMA.md)

---

## How to Spot Emergence in Your System

You're experiencing emergence when:
1. Work gets done by agents reading each other's traces, not explicit assignment
2. Fixes generalize across contexts without central instruction
3. New capabilities appear (e.g., self-healing, self-detection) that no single agent was programmed to have
4. The system catches its own errors and signals for repair

This is not a bug. This is the system working as designed.

---

**Canonical docs are in faerie2. This template is ready for emergence.**

Updated: 2026-04-27
