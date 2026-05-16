---
type: narrative
status: active
created: 2026-04-20
tags: [literature, stigmergy, biology, grasse]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Stigmergy-in-Software-Systems]]"]
child: []
doc_hash: sha256:644091f6ae612dde78008697cd81a05160bc38d6f651d0a2abad860bad770a14
hash_ts: 2026-04-20T21:59:40Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [→ Software Systems](Stigmergy-in-Software-Systems.md) · [⌂ Home](../HOME.md)

# Stigmergy — Origins (Grassé, 1959)

## The Discovery

In 1959, French zoologist Pierre-Paul Grassé observed something unexpected in termite mounds. Individual termites appeared to act randomly. Yet the colony produced architecturally complex, thermally regulated structures that no single termite understood or planned. The colony was coordinating without communicating.

Grassé coined the term **stigmergy** (from Greek *stigma*, mark, and *ergon*, work) to describe the mechanism: an agent's work leaves a trace in the environment, and that trace triggers further work by other agents. The trace is the message. No agent needs to know which other agent left the trace, or why. The environment is the coordination medium.

The canonical example: a termite carries a ball of material. When it encounters a pheromone-marked location, it deposits the ball and adds its own pheromone. Other termites are drawn to pheromone-rich spots, deposit there, amplify the signal. Columns emerge, arches form, chambers develop — from pure local behavior and environmental state.

## Why This Matters for Faerie

The faerie multi-agent system implements stigmergy structurally. A manifest file at a predictable path is the pheromone trail. An agent writing to `wave2-evidence-curator-result.json` is depositing a ball of material. A downstream agent that scans `~/.claude/hooks/state/wave*-result.json` and finds a manifest is following the trail. No direct message. No relay. Just filesystem state as coordination.

When this works, the system exhibits the same property Grassé observed: complex coordinated output from agents that never directly communicated. When it fails — because manifests aren't being read (high OMR), or because agents are being told where to look (low SDR), or because chains don't form (CD = 0) — the system degrades to direct messaging. Coordination becomes sequential and bottlenecked by main session attention.

## Extensions

Theraulaz and Bonabeau (1999) formalized stigmergy for software multi-agent systems and identified two types:
- **Sematectonic:** coordination via physical environment changes (a termite ball that others can see)
- **Marker-based:** coordination via symbolic marks (pheromones, manifests, queue entries)

Faerie uses marker-based stigmergy. The `triggered_by` field in manifests (schema v2) is the explicit pheromone record — it makes the trace machine-readable for the CD metric.

## Related Metrics

- [[../00-Metrics/si/OMR-Orphaned-Manifest-Rate|OMR]] — did the trace reach anyone?
- [[../00-Metrics/si/SDR-Stigmergic-Discovery-Rate|SDR]] — did agents navigate by traces or by instructions?
- [[../00-Metrics/si/CD-Cascade-Depth|CD]] — how deep did the trace cascade?

**Source:** Grassé, P.-P. (1959). La reconstruction du nid et les coordinations inter-individuelles chez *Bellicositermes natalensis* et *Cubitermes* sp. La théorie de la stigmergie. *Insectes Sociaux*, 6, 41–80.
