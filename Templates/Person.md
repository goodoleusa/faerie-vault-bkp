---
type: entity
entity_type: person
status: stub
created: {{ file.ctime | moment("YYYY-MM-DD") }}
updated: {{ file.mtime | moment("YYYY-MM-DD") }}
tags: [osint, entity, person]
entity_name: "{{ file.basename }}"
aliases: []
date_of_birth:
nationality:
known_roles: []
affiliations: []
social_media: []
financial_connections: []
parent:
  - 
sibling:
  - 
child:
  - 
confidence_level: unassessed
source_quality: unverified
priority: medium
risk_level:
blueprint: "[[Person.blueprint]]"
doc_hash: sha256:c387c678091d2e32ef1fb757aa25fe80c8ba2f338a93270762305eebf8fa6c50
hash_ts: 2026-03-29T16:10:52Z
hash_method: body-sha256-v1
---

# {{ file.basename }}

{% section "Overview" %}
<!-- Who is this person? Why are they relevant to the investigation? -->
{% endsection %}

{% section "Identity" %}
| Field | Value |
|-------|-------|
| **Full Name** | {{ file.basename }} |
| **Aliases** | |
| **DOB** | |
| **Nationality** | |
| **Current Role** | |
| **Previous Roles** | |
{% endsection %}

{% section "Affiliations" %}
| Organization | Role | Period | Source |
|-------------|------|--------|--------|
| | | | |
{% endsection %}

{% section "Financial Connections" %}
<!-- Companies owned/directed, significant transactions, beneficial ownership -->
| Entity | Relationship | Evidence |
|--------|-------------|----------|
| | | |
{% endsection %}

{% section "Social Media & Online Presence" %}
| Platform | Handle/URL | Status | Notes |
|----------|-----------|--------|-------|
| | | | |
{% endsection %}

{% section "Timeline of Relevant Activity" %}
| Date | Activity | Source | Significance |
|------|----------|--------|--------------|
| | | | |
{% endsection %}

{% section "OSINT Sources" %}
| Source | URL | Date | Reliability |
|--------|-----|------|-------------|
| | | | |
{% endsection %}

{% section "Connections" %}
```dataview
LIST file.link
FROM "20-Entities"
WHERE contains(sibling, this.file.link)
SORT file.mtime DESC
```
{% endsection %}

{% section "Evidence Items" %}
```dataview
TABLE tier, confidence_level
FROM "30-Evidence"
WHERE contains(parent, this.file.link)
SORT tier ASC
```
{% endsection %}

{% section "Notes" %}
{% endsection %}
