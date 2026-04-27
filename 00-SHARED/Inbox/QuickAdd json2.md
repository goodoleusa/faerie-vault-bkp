---
type: meta
tags: []
doc_hash: sha256:a35299586d968fe1187a5e38d5d9edfed0fed06bf8de56c8c4a4834e99b70a3d
hash_ts: 2026-03-29T16:10:48Z
hash_method: body-sha256-v1
---
{
  "schemaVersion": 1,
  "quickAddVersion": "2.12.0",
  "createdAt": "2026-03-11T18:00:00.000Z",
  "rootChoiceIds": [
    "cyberops-tmpl-task",
    "cyberops-tmpl-person",
    "cyberops-tmpl-investigation",
    "cyberops-tmpl-entity",
    "cyberops-tmpl-evidence",
    "cyberops-tmpl-source",
    "cyberops-tmpl-daily",
    "cyberops-tmpl-org",
    "cyberops-macro-task",
    "cyberops-macro-person",
    "cyberops-macro-investigation",
    "cyberops-macro-entity",
    "cyberops-macro-evidence",
    "cyberops-macro-source",
    "cyberops-macro-daily",
    "cyberops-macro-org"
  ],
  "choices": [
    {
      "choice": {
        "id": "cyberops-tmpl-task",
        "name": "New Task",
        "type": "Template",
        "command": true,
        "templatePath": "Task-Inbox.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["00-Inbox"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Task"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-person",
        "name": "New Person",
        "type": "Template",
        "command": true,
        "templatePath": "Person.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["20-Entities/People"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Person"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-investigation",
        "name": "New Investigation",
        "type": "Template",
        "command": true,
        "templatePath": "Investigation-Case.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["10-Investigations"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Investigation"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-entity",
        "name": "New Entity Stub",
        "type": "Template",
        "command": true,
        "templatePath": "Entity-Stub.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["20-Entities"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Entity Stub"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-evidence",
        "name": "New Evidence Item",
        "type": "Template",
        "command": true,
        "templatePath": "Evidence-Item.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["30-Evidence"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Evidence Item"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-source",
        "name": "New Source",
        "type": "Template",
        "command": true,
        "templatePath": "Source-Assessment.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["70-Sources"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Source"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-daily",
        "name": "Today's Research Log",
        "type": "Template",
        "command": true,
        "templatePath": "Daily-Research.md",
        "fileNameFormat": { "enabled": true, "format": "{{DATE:YYYY-MM-DD}}-Research-{{VALUE}}" },
        "folder": { "enabled": true, "folders": ["01-Memories/shared"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": true, "placement": "afterSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["Today's Research Log"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-tmpl-org",
        "name": "New Organization (master)",
        "type": "Template",
        "command": true,
        "templatePath": "Organization-Master.md",
        "fileNameFormat": { "enabled": true, "format": "{{NAME}}" },
        "folder": { "enabled": true, "folders": ["20-Entities/Organizations"], "chooseWhenCreatingNote": false, "createInSameFolderAsActiveFile": false, "chooseFromSubfolders": false },
        "appendLink": { "enabled": false, "placement": "replaceSelection", "requireActiveFile": false, "linkType": "link" },
        "openFile": true,
        "fileOpening": { "location": "tab", "direction": "vertical", "mode": "default", "focus": true },
        "fileExistsMode": "Increment the file name",
        "setFileExistsBehavior": true
      },
      "pathHint": ["New Organization (master)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-task",
        "name": "New Task (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Task (with Blueprint)",
          "id": "cyberops-macro-task",
          "commands": [
            { "name": "New Task", "type": "Choice", "id": "c1000001-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-task" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000001-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Task (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-person",
        "name": "New Person (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Person (with Blueprint)",
          "id": "cyberops-macro-person",
          "commands": [
            { "name": "New Person", "type": "Choice", "id": "c1000002-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-person" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000002-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Person (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-investigation",
        "name": "New Investigation (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Investigation (with Blueprint)",
          "id": "cyberops-macro-investigation",
          "commands": [
            { "name": "New Investigation", "type": "Choice", "id": "c1000003-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-investigation" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000003-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Investigation (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-entity",
        "name": "New Entity Stub (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Entity Stub (with Blueprint)",
          "id": "cyberops-macro-entity",
          "commands": [
            { "name": "New Entity Stub", "type": "Choice", "id": "c1000004-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-entity" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000004-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Entity Stub (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-evidence",
        "name": "New Evidence Item (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Evidence Item (with Blueprint)",
          "id": "cyberops-macro-evidence",
          "commands": [
            { "name": "New Evidence Item", "type": "Choice", "id": "c1000005-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-evidence" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000005-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Evidence Item (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-source",
        "name": "New Source (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Source (with Blueprint)",
          "id": "cyberops-macro-source",
          "commands": [
            { "name": "New Source", "type": "Choice", "id": "c1000006-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-source" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000006-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Source (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-daily",
        "name": "Today's Research Log (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "Today's Research Log (with Blueprint)",
          "id": "cyberops-macro-daily",
          "commands": [
            { "name": "Today's Research Log", "type": "Choice", "id": "c1000007-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-daily" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000007-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["Today's Research Log (with Blueprint)"],
      "parentChoiceId": null
    },
    {
      "choice": {
        "id": "cyberops-macro-org",
        "name": "New Organization (master) (with Blueprint)",
        "type": "Macro",
        "command": true,
        "runOnStartup": false,
        "macro": {
          "name": "New Organization (master) (with Blueprint)",
          "id": "cyberops-macro-org",
          "commands": [
            { "name": "New Organization (master)", "type": "Choice", "id": "c1000008-0001-4001-8001-000000000001", "choiceId": "cyberops-tmpl-org" },
            { "name": "Blueprint: Apply blueprint", "type": "Obsidian", "id": "c1000008-0001-4001-8001-000000000002", "commandId": "blueprint:apply-blueprint" }
          ]
        }
      },
      "pathHint": ["New Organization (master) (with Blueprint)"],
      "parentChoiceId": null
    }
  ],
  "assets": []
}
