---
type: meta
tags: []
doc_hash: sha256:5e410c3f62091fd3d4f9dcb2a05668f0747e21938b977b7a20e618ef618076f2
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---
# QuickAdd + Blueprint — Step-by-step setup

Quick guide to wire QuickAdd and Blueprint so you can create notes in the right folder and have Blueprint fill placeholders. **Blueprint has no settings UI** — you use commands. **QuickAdd** is where you configure templates and macros.

---

## 0. Quick start: import the package (recommended)

This vault includes a **QuickAdd package** you can import so you don’t have to add every choice by hand:

1. **Run the setup script** (optional but recommended):  
   From the vault root, run `.\scripts\setup_cyberops_vault.ps1` (Windows) or `./scripts/setup_cyberops_vault.sh` (Bash). It creates any missing vault folders and then prints the next steps.
2. **Import the package:**  
   In Obsidian: **Settings → QuickAdd** → scroll to **Packages** → **Import package…** → select **`CyberOps-QuickAdd.quickadd.json`** (in /scripts/).
3. **Set template path (if QuickAdd can't find templates):**  
   **Settings → QuickAdd** → set **Template folder path** to **`Templates`** (vault-relative). The package uses paths like `Task-Inbox.md`; QuickAdd resolves them under this folder.
4. For each choice in the import dialog, choose **Import** (or **Duplicate** if you already have your own choices with the same names).
5. **Reload QuickAdd** or restart Obsidian. Use **Command Palette → QuickAdd** → pick any “(with Blueprint)” macro.

**Requirements:** Blueprint and QuickAdd plugins installed; **Templates/** folder must contain the `.md` template files (they ship with this vault). **Set QuickAdd → Template folder path to `Templates`** so paths like `Task-Inbox.md` resolve; otherwise QuickAdd may report "couldn't find the path" until you set it. If the package fails to import (e.g. QuickAdd schema change), use the manual checklist in §4b below and then export a new package from QuickAdd for your vault.

**If you prefer or need to set things up by hand**, follow the full manual instructions in **§3** (Add each Template choice), **§4** (Add each Macro), and **§5b** (Checklist) below — no package required.

---

## 1. Plugin configs (no UI for Blueprint)

- **Blueprint**: Enable the plugin. No settings to fill. You only use:
  - **Command Palette** → “Blueprint: New note from blueprint” (when in a folder)
  - **Command Palette** → “Blueprint: Apply blueprint to note” (cursor in a note)
  - **Command Palette** → “Blueprint: Update all notes with blueprints” (in a folder)
- **QuickAdd**: Settings → QuickAdd. Set **Template folder path** to **`Templates`** (vault-relative) so that template paths like `Task-Inbox.md` resolve to `Templates/Task-Inbox.md`. No need to touch other QuickAdd options for this workflow.

---

## 1b. QuickAdd input / global settings (optional)

These are **plugin-level toggles** in **Settings → QuickAdd**. They are not stored in the package file; set them once per vault if you want them.

| Setting | What it does | Recommendation for CyberOps |
|--------|----------------|------------------------------|
| **Use multi-line input prompt instead of single line** | Input modal is a textarea so you can paste multiple lines (e.g. research snippets, agent handoffs). | **Yes** — better for pasting blocks. |
| **Persist input prompt drafts** | Keeps draft text in the input modal so if you cancel and reopen the same choice later in the session, your draft is still there. | **Yes** — helpful when you’re interrupted or want to tweak before submitting. |
| **Use editor selection as default capture value** | When you run a Capture (or Template that uses `{{VALUE}}`) and have text selected, that selection is prefilled as the value. | **Yes** — fits “capture selection into daily log” / append workflows. |
| **One-page input for choices (Beta)** | Resolves variables up front and shows a **single dynamic form** before running the template/capture: all `{{VALUE:name}}`, `{{VDATE:...}}`, `{{FIELD:...}}` in one modal instead of one prompt at a time. Works with Template and Capture; macros get partial support (our “(with Blueprint)” macros run the template step first, so that step gets the one-page form). | **Try it** — cleaner UX; cancel in the modal falls back to step-by-step prompts. Beta: report issues if you see odd behavior. |
| **Format template variables as proper Obsidian property types (Beta)** | QuickAdd writes `{{VALUE:...}}` into frontmatter as proper types: arrays → list properties, numbers → number, booleans → checkbox, etc., instead of everything as a string. | **Optional** — enable if you want cleaner YAML (e.g. `sources: - a - b` from one prompt). Turn off if you see unwanted list/date formatting (e.g. commas in text becoming lists). |

**Where to set:** Settings → QuickAdd → scroll to the **Input** / **Beta** area. The package does not export or import these; they are global QuickAdd settings for this vault.

---

## 1c. QuickAdd Global Variables (reusable snippets)

**Global variables** are vault-scoped snippets you reference as `{{GLOBAL_VAR:<name>}}`. They expand **before** other tokens (e.g. `{{VALUE:...}}`, `{{VDATE:...}}`), so a snippet can contain prompts that run when you use it. They work in template paths, file name format, folder paths, and template/capture content.

**Setup:** Settings → QuickAdd → **Global Variables** → Add a **name** and **value** (free text; value can include other QuickAdd tokens). Save is automatic. These are **not** stored in the package — define them once per vault.

### Recommended globals for CyberOps

| Name | Value | Use for |
|------|--------|---------|
| **TodayDate** | `{{DATE:YYYY-MM-DD}}` | Any path or text that needs “today” (e.g. research log heading). |
| **ResearchFolder** | `01-Memories/shared` | Single source for daily research folder; use in Template “Create in folder” or capture target path. |
| **InboxFolder** | `00-Inbox` | Tasks and quick captures; reuse in folder paths. |
| **LeadSource** | `{{VALUE:lead_source, Tip-off, OSINT, Internal, Legal, Media, Other}}` | Investigation lead_source: one prompt, same options everywhere. |
| **ThreatLevel** | `{{VALUE:threat_level, unassessed, low, medium, high, critical}}` | Investigation threat_level in frontmatter or templates. |
| **AgentName** | `{{VALUE:agent}}` | “Who is logging?” — use in research log file name or content. |
| **HandoffBlock** | `Agent: {{VALUE:agent}}\nHandoff: {{VALUE:handoff}}` | Snippet for agent handoffs; use inside a Capture that inserts at cursor (see below). |
| **CaseIdPrefix** | `CASE-{{DATE:YYYYMMDD}}-` | Investigation case_id prefix; use in template as `{{GLOBAL_VAR:CaseIdPrefix}}001` or append `{{VALUE:suffix}}`. |

You can nest globals (e.g. a global whose value references another `{{GLOBAL_VAR:...}}`); QuickAdd limits depth to 5 to avoid cycles. Typing `{{GLOBAL_VAR:` in a template or choice field triggers autocomplete for your names.

### Using global variables daily (when writing)

- **In templates:** Put `{{GLOBAL_VAR:...}}` in template body, frontmatter, file name format, or folder path. When you run a Template choice (or “(with Blueprint)” macro), QuickAdd expands globals first, then runs any `{{VALUE:...}}` / `{{VDATE:...}}` prompts. Example: in an Investigation template, set `lead_source: "{{GLOBAL_VAR:LeadSource}}"` so every new investigation uses the same lead_source dropdown.
- **In captures:** In a Capture choice, set “Format” or “Content” to something like `- {{GLOBAL_VAR:TodayDate}} {{VALUE:note}}` or `{{GLOBAL_VAR:HandoffBlock}}`. When you run the capture (e.g. “Append to daily research” or “Insert handoff at cursor”), you get one form (or sequential prompts) and the result is inserted with the global expanded.
- **Optional Capture for handoffs:** Add a **Capture** choice named e.g. “Insert handoff snippet”. Set “Capture format” to `{{GLOBAL_VAR:HandoffBlock}}`, “Insert at cursor” (or append to a specific file). Run it from any note when you want to drop a standard agent handoff block; QuickAdd will prompt for `agent` and `handoff`, then insert the block.
- **Paths:** In any Template choice, you can set “Create in folder” to `{{GLOBAL_VAR:ResearchFolder}}` or `{{GLOBAL_VAR:InboxFolder}}` so the folder is controlled in one place. If you later change the global, all choices using it follow.

You don’t type `{{GLOBAL_VAR:...}}` into a note and have it expand on save — expansion happens when a **QuickAdd choice runs** (template, capture, or macro). Daily use = run QuickAdd from the Command Palette; the choices that use globals will show consistent prompts and paths.

---

## 2. Template vs “New note with Blueprint” (macro)

- **Template only** (e.g. “New Task”, “New Person”): Creates a new note from the template file in the chosen folder. The note contains the raw template text, including **unresolved placeholders** like `{{ file.basename }}`, `{{ moment() }}`, etc. You must run **Blueprint: Apply blueprint to note** yourself (Command Palette) to fill those in.
- **Macro “(with Blueprint)”** (e.g. “New Task (with Blueprint)”): Runs the Template choice (creates the note) and then runs **Blueprint: Apply blueprint to note** in one go. The new note is created and placeholders are filled (filename, dates, etc.) without a second step. Use the macro when you want a ready-to-edit note; use the template alone when you want to create first and apply the blueprint later (e.g. after moving the file).

---

## 3. Manual setup — Add a **Template** choice (one per note type)

Use the steps below if you did not import the package or it failed. For each note type (Task, Person, Investigation, etc.) you want from the command palette:

1. **QuickAdd** → **Configure** (or Settings → QuickAdd → open the modal).
2. Click **Add choice**.
3. Choose **Template**.
4. Fill the form:

| Field | What to pick / enter |
|-------|----------------------|
| **Name** | e.g. `New Task` or `New Person`. This is what you see in the QuickAdd list. |
| **Template path** | Vault-relative path to the `.md` in `Templates/`. Examples: `Templates/Task-Inbox.md`, `Templates/Person.md`, `Templates/Investigation-Case.md`, `Templates/Entity-Stub.md`, `Templates/Evidence-Item.md`, `Templates/Source-Assessment.md`, `Templates/Daily-Research.md`, `Templates/Organization-Master.md`. |
| **Create in folder** | The folder where the new note should be created. Examples: `00-Inbox`, `20-Entities/People`, `10-Investigations`, `20-Entities`, `30-Evidence`, `70-Sources`, `01-Memories/shared`, `20-Entities/Organizations`. Use one folder per template. |
| **File name format** | How the filename is built. Use `{{NAME}}` when QuickAdd should prompt for a name (e.g. person name, case name). Use `{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}` for daily research (prompts for “VALUE” = agent name). For tasks, `{{NAME}}` is fine. So: Task → `{{NAME}}`, Person → `{{NAME}}`, Investigation → `{{NAME}}`, Entity Stub → `{{NAME}}`, Evidence → `{{NAME}}`, Source → `{{NAME}}`, Daily Research → `{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}`, Organization (master) → `{{NAME}}`. |
| **Append link** | Your choice. “Disabled” = don’t insert a link in the current note. “Enabled (skip if no active file)” is handy so you don’t get errors when no note is open. |
| **Increment file name** | On = if the file already exists, QuickAdd will add a number (e.g. `Note 1`). Usually **On** to avoid overwriting. |
| **Open** | On = open the new note after creation. Usually **On**. “New tab” = open in a new tab. |
| **File already exists behavior** | What to do if the file exists. “Increment the file name” matches the increment setting above. “Nothing” = just open the existing file. |

5. Save the choice. It appears in **Command Palette** → **QuickAdd** → &lt;your name&gt;.

**Example — “New Person”:**

- Name: `New Person`
- Template path: `Templates/Person.md`
- Create in folder: `20-Entities/People`
- File name format: `{{NAME}}`
- Append link: Disabled (or Enabled skip if no active file)
- Increment file name: On
- Open: On
- File already exists: Increment the file name

**Example — “Today’s Research Log”:**

- Name: `Today's Research Log`
- Template path: `Templates/Daily-Research.md`
- Create in folder: `01-Memories/shared`
- File name format: `{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}`  
  (QuickAdd will prompt for VALUE = agent name)
- Rest as above.

After running the template, the new note is created with the **template content** (from `Templates/*.md`). Those templates already have a `blueprint: "[[...]]"` in frontmatter. To resolve `{{ file.basename }}` and dates, run **Blueprint: Apply blueprint to note** once with the new note open — or use a macro (below).

---

## 4. Add a **Macro** (create + apply blueprint in one go)

Macros run a sequence of steps. Use one macro per “create then apply” flow so you don’t have to run Blueprint manually.

1. **QuickAdd** → **Configure**.
2. **Add choice** → **Macro**.
3. **Name** the macro, e.g. `New Task (with Blueprint)` or `New Person (with Blueprint)`.
4. **Add steps** in this order:
   - **Step 1**: “QuickAdd: Run choice” → pick the **Template** choice you created (e.g. “New Task” or “New Person”). This creates the note and opens it.
   - **Step 2**: “Obsidian command” (or “Execute command”) → choose **“Blueprint: Apply blueprint to note”**. This fills in `{{ file.basename }}`, dates, etc. from the blueprint.
5. Save the macro.

When you run the macro from **Command Palette** → **QuickAdd** → &lt;macro name&gt;, QuickAdd will:
1. Run the template (prompt for name if you used `{{NAME}}`, create file in folder, open it).
2. Run “Apply blueprint to note” on that note.

**Macro options you might see:**

- **Capture/input**: If you want the macro to ask for a value and pass it to the template, add a “Capture” step before “Run choice” and use the variable in the template’s file name format (e.g. `{{VALUE}}`). For simple “prompt for name” flows, the Template choice’s “File name format” with `{{NAME}}` already prompts; you don’t need an extra capture in the macro unless you want a custom prompt.
- **Wait**: Usually not needed between “Run choice” and “Apply blueprint”; the new note is already open.
- **Conditionals**: Leave off unless you have a multi-branch workflow.

---

## 5. Reference — Template choices and folders

| QuickAdd choice (suggested name) | Template path | Create in folder | File name format |
|----------------------------------|--------------|------------------|-------------------|
| New Task | `Templates/Task-Inbox.md` | `00-Inbox` | `{{NAME}}` |
| New Person | `Templates/Person.md` | `20-Entities/People` | `{{NAME}}` |
| New Investigation | `Templates/Investigation-Case.md` | `10-Investigations` | `{{NAME}}` |
| New Entity Stub | `Templates/Entity-Stub.md` | `20-Entities` | `{{NAME}}` |
| New Evidence Item | `Templates/Evidence-Item.md` | `30-Evidence` | `{{NAME}}` |
| New Source | `Templates/Source-Assessment.md` | `70-Sources` | `{{NAME}}` |
| Today's Research Log | `Templates/Daily-Research.md` | `01-Memories/shared` | `{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}` |
| New Organization (master) | `Templates/Organization-Master.md` | `20-Entities/Organizations` | `{{NAME}}` |

Create one Template choice per row, then one Macro per row if you want “create + apply” in one shot (e.g. “New Person (with Blueprint)” runs the “New Person” template then applies the blueprint).

---

## 5b. Checklist — Template choices and Macros to add

Use this as a tick list when configuring QuickAdd. For each row in the table above:

**Template choices** (QuickAdd → Configure → Add choice → Template):

- [ ] **New Task** — Template: `Templates/Task-Inbox.md`, Folder: `00-Inbox`, File name: `{{NAME}}`
- [ ] **New Person** — Template: `Templates/Person.md`, Folder: `20-Entities/People`, File name: `{{NAME}}`
- [ ] **New Investigation** — Template: `Templates/Investigation-Case.md`, Folder: `10-Investigations`, File name: `{{NAME}}`
- [ ] **New Entity Stub** — Template: `Templates/Entity-Stub.md`, Folder: `20-Entities`, File name: `{{NAME}}`
- [ ] **New Evidence Item** — Template: `Templates/Evidence-Item.md`, Folder: `30-Evidence`, File name: `{{NAME}}`
- [ ] **New Source** — Template: `Templates/Source-Assessment.md`, Folder: `70-Sources`, File name: `{{NAME}}`
- [ ] **Today's Research Log** — Template: `Templates/Daily-Research.md`, Folder: `01-Memories/shared`, File name: `{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}` (VALUE = agent name)
- [ ] **New Organization (master)** — Template: `Templates/Organization-Master.md`, Folder: `20-Entities/Organizations`, File name: `{{NAME}}`

**Macros** (QuickAdd → Configure → Add choice → Macro). Each macro: Step 1 = "QuickAdd: Run choice" → pick the Template above; Step 2 = "Obsidian command" → **Blueprint: Apply blueprint to note**.

- [ ] **New Task (with Blueprint)** → runs "New Task" then Apply blueprint
- [ ] **New Person (with Blueprint)** → runs "New Person" then Apply blueprint
- [ ] **New Investigation (with Blueprint)** → runs "New Investigation" then Apply blueprint
- [ ] **New Entity Stub (with Blueprint)** → runs "New Entity Stub" then Apply blueprint
- [ ] **New Evidence Item (with Blueprint)** → runs "New Evidence Item" then Apply blueprint
- [ ] **New Source (with Blueprint)** → runs "New Source" then Apply blueprint
- [ ] **Today's Research Log (with Blueprint)** → runs "Today's Research Log" then Apply blueprint
- [ ] **New Organization (master) (with Blueprint)** → runs "New Organization (master)" then Apply blueprint

After adding, reload QuickAdd (or restart Obsidian) so the choices appear in Command Palette → QuickAdd.

---

## 6. Optional — QuickAdd data.json (manual config)

If you prefer to edit the config file instead of the UI:

- Path: `.obsidian/plugins/quickadd/data.json`
- Template choice shape (conceptual): `{ "id": "uuid", "name": "New Person", "type": "Template", "data": { "templatePath": "Templates/Person.md", "folder": "20-Entities/People", "fileNameFormat": "{{NAME}}", "appendLink": false, "open": true, ... } }`
- Macro shape: `{ "id": "uuid", "name": "New Person (with Blueprint)", "type": "Macro", "data": { "steps": [ { "type": "QuickAddRunChoice", "choiceId": "<id of New Person>" }, { "type": "ObsidianCommand", "commandId": "blueprint:apply" } ] } }`

Filling the UI (sections 2–3) is usually easier than editing JSON.

---

## 7. Summary

- **Quick path:** Import **CyberOps-QuickAdd.quickadd.json** (Settings → QuickAdd → Packages → Import package). See §0.
- **Manual path (just in case):** Use **§3** to add each Template choice, **§4** to add each Macro (template → Apply blueprint), and **§5b** as a tick list. No package needed.
- **Blueprint**: No config. Use commands: new note from blueprint, apply blueprint to note, update all.
- **QuickAdd**: Add **Template** choices (template path, folder, file name format, open/increment). Add **Macro** choices that run a Template choice then “Blueprint: Apply blueprint to note.” Optionally add **Global Variables** (§1c) and use them in templates/captures for consistent prompts and paths.
- **Result**: Command Palette → QuickAdd → pick “New Person (with Blueprint)” (or similar) → enter name → note is created in the right folder and Blueprint fills placeholders.

See **[[01-ARCHITECTURE#12. QuickAdd + Blueprints (Obsidian)]]** for the high-level picture and **[[0a-SpiderFoot-Runs/README]]** for where to put SpiderFoot CSV runs.
