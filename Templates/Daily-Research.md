---
type: daily
status: active
created: {{ file.ctime | moment("YYYY-MM-DD hh:mm a") }}
updated: {{ file.mtime | moment("YYYY-MM-DD hh:mm a") }}
tags: [daily, research-log]
date: {{ moment().format('YYYY-MM-DD') }}
investigator:
focus_areas: []
blueprint: "[[Daily-Research.blueprint]]"
doc_hash: sha256:b3731fd8a1870628a8ffd71495c80a51c03344d8123ea01b26a7d6d2d2b017e2
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# Research Log — {{ moment().format('YYYY-MM-DD') }}

{% section "Today's Focus" %}
<!-- What are you investigating today? -->
{% endsection %}

{% section "Findings" %}
<!-- Key discoveries, with sources -->
{% endsection %}

{% section "New Entities Identified" %}
<!-- List any new IPs, domains, people, organizations discovered today -->
- [ ] Created entity note for:
{% endsection %}

{% section "Questions Raised" %}
<!-- New questions that emerged from today's research -->
{% endsection %}

{% section "Tasks Generated" %}
<!-- New tasks to put in 00-Inbox -->
{% endsection %}

{% section "Context Snapshot" %}
<!-- End-of-day summary for async handoff to agents or collaborators -->
{% endsection %}
