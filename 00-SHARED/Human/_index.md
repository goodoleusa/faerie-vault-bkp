---
type: dir-index
title: "Human — your annotations (parallel COC chain)"
emoji: "🧑"
N: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
S: ['[../Daily/_index](../Daily/_index.md)']
E: ['[../COC-Entries/_index](../COC-Entries/_index.md)']
W: ['[../HELP/HOW-ANNOTATION-COC-WORKS](../HELP/HOW-ANNOTATION-COC-WORKS.md)']
tags: [dir-index, human, coc-human]
---

# 🧑 Human — `{YYYY-MM-DD}/m-{ts}.md`

Your annotations live in a **parallel COC chain** (`coc-human.jsonl`) so
they never pollute the AI's atomic notes. POSTed to MCP via the hive
plugin; hash-tracked independently of the agent stream.

Mirrors `faerie2/forensics/coc-human.jsonl` (system of record for human
products).

## Today's annotations

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/Human/${today}"`).sort(p => p.file.name, 'desc');
dv.table(['When', 'Note'], pages.map(p => [p.file.name, dv.fileLink(p.file.path)]));
```
