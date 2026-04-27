---
type: task
status: pending
created: {{ file.ctime | moment("YYYY-MM-DD HH:mm") }}
updated: {{ file.mtime | moment("YYYY-MM-DD HH:mm") }}
tags:
  - task
  - inbox
  - faerie
task_id: TASK-{{ moment().format('YYYYMMDDHHmm') }}
queue_task_id:
task_type: work
priority: MED
assignee:
requester:
skill_required:
deadline:
completed_date:
result_summary:
review_verdict: pending
output_files: []
output_location:
context_bundle:
parent:
  - 
sibling:
  - 
child:
  - 
touched_by:
  - 
task_signature:
vault_path:
source:
sha256:
memory_lane: queue
promotion_state: capture
nectar_ref:
faerie_session:
bundle_ref:
blueprint: "[[Task-Inbox]]"
doc_hash: sha256:49436c90da47e49741c24f35a9ac527a5a017f7af022e10699eb84e258393441
hash_ts: 2026-03-29T16:10:52Z
hash_method: body-sha256-v1
---

# {{ file.basename }}

<!--
  Faerie / queue alignment (canonical on disk: ~/.claude/hooks/state/sprint-queue.json):
  - When /task or sprint-prep enqueues work, set queue_task_id to the JSON id (e.g. sprint-20260315-018).
  - task_type: work | train (DAE unified queue). Sprint-prep JSON may also use session_sprint | data_ingest | launch_phase | generic — use sprint_kind below if you mirror both.
  - priority must be HIGH | MED | LOW for queue routers and Dataview.
  - context_bundle: optional path to a sealed sprint / handoff folder for /run T2.5 loading.
  - memory_lane / promotion_state / faerie_session / nectar_ref / bundle_ref: vault faerie schema — see 00-META/12-ASYNC-HUMAN-AGENT-BRIDGE.
  - Parent/sibling/child: quote wikilinks in lists, e.g. - "[[00-SHARED/Inbox/Parent-Task]]". See 00-META/10-TASK-LINEAGE-AND-HANDBACK.
-->

{% section "Task Description" %}
<!-- What needs to be done? Be specific enough for an agent to execute autonomously. -->
{% endsection %}

{% section "Context" %}
<!-- Background: wikilinks to investigations, entities, evidence.
     Persistent thread context: 00-SHARED/Memories/shared/ and project .claude/memory/ (NECTAR, HONEY via /faerie + /memory). -->
{% endsection %}

{% section "Acceptance Criteria" %}
- [ ]
- [ ]
{% endsection %}

{% section "Output" %}
<!-- Align with 00-SHARED handoff: Agent-Outbox for deliveries, Human-Inbox flags for HIGH review. -->

**Expected output location:** (e.g. `00-SHARED/Agent-Outbox/…` or case folders under `10-Investigations/`)
**Expected format:** Markdown / JSON / Report

{% endsection %}

{% section "Agent Execution Log" %}
<!-- Filled by executing agent — append timestamped entries. -->
{% endsection %}

{% section "Compressed summary (for handback / next agent)" %}
<!-- Required for handback: learnings, conclusions, open questions, what the next agent must know. See 00-META/10-TASK-LINEAGE-AND-HANDBACK. -->
- 
{% endsection %}

{% section "Agent Learnings" %}
<!-- Longer form; human reviews. Rare swarm-wide notes → 00-SHARED/Memories/agents/agent-logbook.md -->
{% endsection %}

{% section "For the human (async)" %}
<!-- Same contract as 00-META/12-ASYNC-HUMAN-AGENT-BRIDGE: checkboxes + append-only human notes. -->
- [ ] Read and acknowledged
- [ ] Decision / promote / defer (one line)

**Human notes (append-only):**

- 
{% endsection %}

{% section "For the next agent run" %}
<!-- Instructions after human edits; do not clear human section above. -->
- 
{% endsection %}

{% section "Task lineage" %}
<!-- Mirror frontmatter parent / child / sibling with wikilinks. Creating a subtask: set child parent + add child link on this note. -->
**Parent:** 
**Children:** 
**Siblings:** 
{% endsection %}

{% section "Review" %}
<!-- After agent completion -->

**Reviewed by:**
**Review date:**
**Verdict:** pending / approved / needs-revision
**Feedback:**

{% endsection %}
