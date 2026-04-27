---
tags:
  - important
  - lumo
  - obsidian
title: blueprints lumo
date_created: 2026-03-10 11:57 am
date_modified: 2026-03-10 12:13 pm
share_link: https://share.note.sx/y2rf0upu#e1q6OLVXeMxJ1DMQKYUzdh321rwu/Xmu26uqIZMV3Gg
share_updated: 2026-03-10T12:07:13-04:00
type: meta
doc_hash: sha256:e41283b587513c76f961936adbb5f42600008f93b7f2da867f621cef09038685
hash_ts: 2026-03-29T16:10:49Z
hash_method: body-sha256-v1
---
# Blueprint Lumo
It uses Nunjucks templating (not Mustache or Templater), and it has a unique section-based system that preserves your edits while enforcing structure.
 
Here are the corrected blueprints tailored for your Cyber OSINT investigative analysis workflow.

## Create the Blueprint Files: 

Save the code blocks below as .blueprint files in a folder (e.g., Blueprints/).

Entity-Stub.blueprint
Investigation-Case.blueprint
Normalize-Frontmatter.blueprint

## Apply to Notes:

For new notes: Right-click a folder > Create note from blueprint > Select your blueprint.

For existing half-done notes: Open the note, ensure it has a WikiLink to the blueprint in the blueprint property (e.g., blueprint: [[Entity-Stub.blueprint]]), then run Blueprint: Apply blueprint.

## Bulk Update: Right-click a folder > 
Update all notes with blueprints.

### Entity/Topic Stub Blueprint
File: Blueprints/Entity-Stub.blueprint Purpose: Creates a standardized, self-contained stub for any entity (person, org, IP, domain) with normalized frontmatter.

---
type: entity
status: stub
created: {{ file.ctime }}
updated: {{ file.mtime }}
tags: [osint/investigation, entity, stub]
aliases: []
confidence_level: unassessed
source_quality: unverified
entity_name: "{{ file.basename }}"
entity_type: 
investigator: 
related_entities: []
investigation_status: initial_collection
priority: medium
last_reviewed: 
next_review: {{ moment().add(7, 'days').format('YYYY-MM-DD') }}

### blueprints lumo

{% section "Overview" %}
<!-- Brief summary of what this entity is -->
{% endsection %}

{% section "Key Attributes" %}
- **Entity Type:** 
- **Known Aliases:** 
- **Jurisdiction:** 
- **Operational Status:** 
{% endsection %}

{% section "OSINT Sources" %}

| Source | URL | Date Accessed | Reliability |
|--------|-----|---------------|-------------|
|        |     |               |             |

{% endsection %}

{% section "Evidence Summary" %}
<!-- Bullet points of verified findings -->
{% endsection %}

{% section "Open Questions" %}
<!-- What still needs investigation -->
{% endsection %}

{% section "Related Investigations" %}

dataview
LIST FROM "Investigations" 
WHERE contains(related_entities, this.entity_name)
SORT file.mtime DESC
{% endsection %}

{% section "Notes" %}

<!-- Raw observations, hypotheses, leads -->
{% endsection %}


---

### 2. Investigation Case Blueprint
**File:** `Blueprints/Investigation-Case.blueprint`
*Purpose: A structured case file for tracking active investigations, linking to entities, and managing timelines.*

```nunjucks
---
type: investigation
status: active
created: {{ file.ctime }}
updated: {{ file.mtime }}
tags: [osint/investigation, case, active]
case_id: CASE-{{ moment().format('YYYYMMDD') }}-001
lead_source: 
investigator: 
entities_involved: []
threat_level: unassessed
classification: internal
deadline: 
last_update: {{ moment().format('YYYY-MM-DD') }}
---

# {{ file.basename }}

{% section "Executive Summary" %}
<!-- 2-3 sentence overview for quick reference -->
{% endsection %}

{% section "Objectives" %}
- [ ] 
- [ ] 
- [ ] 
{% endsection %}

{% section "Timeline" %}
| Date | Event | Significance |
|------|-------|--------------|
|      |       |              |
{% endsection %}

{% section "Entities Under Investigation" %}

dataview
TABLE entity_type, confidence_level, investigation_status
FROM "Entities"
WHERE contains(related_entities, this.case_id) OR contains(file.name, this.case_id)

{% endsection %}

{% section "Intelligence Gathered" %}

Verified Facts
Unverified Leads
Contradictory Information
{% endsection %}

{% section "Methodology" %}

<!-- What techniques/tools were used -->
{% endsection %}

{% section "Analysis" %}

<!-- Your interpretive work, connections, patterns -->
{% endsection %}

{% section "Recommendations" %}

<!-- Next steps, resource needs, escalation paths -->
{% endsection %}

{% section "Appendix" %}

Raw Data Links
Tool Outputs
Chain of Custody Notes
{% endsection %}
```

### 3. Normalize Frontmatter Blueprint
**File:** `Blueprints/Normalize-Frontmatter.blueprint`
*Purpose: To be applied to your "half-done" notes. It injects missing standard fields without deleting your existing custom frontmatter.*

```nunjucks
---
type: 
status: 
created: {{ file.ctime }}
updated: {{ file.mtime }}
tags: [osint/investigation, needs-review]
needs_processing: true
normalized_date: {{ moment().format('YYYY-MM-DD') }}
original_file: "{{ file.basename }}"
---

# {{ file.basename }}

{% section "Content" %}
<!-- Paste your existing note content here -->
{% endsection %}

{% section "Processing Checklist" %}
- [ ] Frontmatter normalized
- [ ] Tags standardized
- [ ] Entity types assigned
- [ ] Confidence levels assessed
- [ ] Related entities linked
- [ ] Status updated from "stub"
{% endsection %}
4. Dashboard: Track Unprocessed Stubs
File: Dashboards/Unprocessed-Stubs.md Note: This is a regular Markdown note (not a blueprint) that uses Dataview to monitor your progress.

# Unprocessed OSINT Stubs

## Needs Normalization

```dataview
TABLE status, type, created, needs_processing
FROM ""
WHERE contains(tags, "osint/investigation") AND status = "stub"
SORT created ASC
By Investigation Status
TABLE investigation_status, confidence_level, priority
FROM ""
WHERE contains(tags, "osint/investigation") AND status = "stub"
GROUP BY investigation_status
Overdue Reviews
TABLE next_review, entity_name, priority
FROM ""
WHERE contains(tags, "osint/investigation") AND status = "stub" AND next_review < date(today)
SORT next_review ASC
```

Quick Actions
[[Unprocessed-Stubs|Refresh Dashboard]]
[[Blueprints/Entity-Stub.blueprint|New Entity Stub]]
[[Blueprints/Investigation-Case.blueprint|New Investigation Case]]

### Key Differences from Templater/Breadcrumbs
1.  **Non-Destructive:** Unlike Templater, Blueprint **never overwrites** existing content in a section. If you edit the "Evidence Summary" section, running the blueprint again keeps your edits but fills in missing sections.
2.  **Frontmatter Merging:** It adds missing properties to the frontmatter but **never removes** properties you manually added. This solves your "confusing frontmatter" issue with Breadcrumbs.
3.  **Nunjucks Syntax:** Uses `{{ variable }}` for values and `{% section "Name" %}` for content blocks.
4.  **Moment.js:** Uses `moment()` for dates (e.g., `{{ moment().format('YYYY-MM-DD') }}`) instead of Templater's `tp.date`.

### Migration Workflow for Your Half-Done Notes
1.  **Link the Blueprint:** Open a half-done note. Add `blueprint: [[Normalize-Frontmatter.blueprint]]` to its frontmatter.
2.  **Apply:** Run `Blueprint: Apply blueprint` (or right-click the file in the explorer).
3.  **Result:** The note will now have standardized `type`, `status`, and `tags` fields. Your original content remains intact in the `Content` section.
4.  **Refine:** Manually move content from the generic "Content" section into the specific sections (e.g., "Evidence Summary") as you process the note.
5.  **Switch Templates:** Once a note is a proper "Entity," change its blueprint link to `[[Entity-Stub.blueprint]]` and re-apply to get the full entity structure.

This setup should give you the structure you need without the fragility of Templater or the confusion of manual frontmatter management.