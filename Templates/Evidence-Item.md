---
type: evidence
status: unprocessed
created: {{ file.ctime | moment("YYYY-MM-DD hh:mm a") }}
updated: {{ file.mtime | moment("YYYY-MM-DD hh:mm a") }}
tags: [osint, evidence]
evidence_id: "{{ file.basename }}"
source_file:
source_sha256:
source_type:
confidence_level: unassessed
source_quality: unverified
hypothesis_support: []
parent:
  - 
sibling:
  - 
child:
  - 
tier:
pipeline_run:
date_collected:
date_analyzed:
blueprint: "[[Evidence-Item.blueprint]]"
doc_hash: sha256:1a2a8d20381035abc2ff039f52cd86d310bf04a4338f3d637a216248bcaf6882
ann_hash: ""
ann_synced: false
hash_ts: 2026-04-06T22:36:22Z
hash_method: body-sha256-v1
---

# {{ file.basename }}

{% section "Summary" %}
<!-- One paragraph: what is this evidence, what does it show -->
{% endsection %}

{% section "Provenance" %}
| Field | Value |
|-------|-------|
| **Source File** | |
| **SHA-256** | |
| **Collection Date** | |
| **Collector** | |
| **Pipeline Run** | |
| **Original URL** | |
{% endsection %}

{% section "Content" %}
<!-- Key data points extracted from this evidence -->
{% endsection %}

{% section "Analysis" %}
<!-- What does this evidence mean in context? -->
{% endsection %}

{% section "Hypothesis Relevance" %}
| Hypothesis | Supports/Contradicts | Strength | Notes |
|-----------|---------------------|----------|-------|
| H1 - Insider | | | |
| H2 - Pipeline | | | |
| H3 - Breach | | | |
| H4 - Handoff | | | |
| H5 - Payoff | | | |
{% endsection %}

{% section "Quality Assessment" %}
| Dimension | Score (1-5) | Notes |
|-----------|------------|-------|
| Authenticity | | |
| Reliability | | |
| Relevance | | |
| Corroboration | | |
| Timeliness | | |
{% endsection %}

{% section "Related Evidence" %}
```dataview
LIST file.link
FROM "30-Evidence"
WHERE contains(sibling, this.file.link) AND file.name != this.file.name
SORT confidence_level DESC
```
{% endsection %}

{% section "Notes" %}
{% endsection %}
