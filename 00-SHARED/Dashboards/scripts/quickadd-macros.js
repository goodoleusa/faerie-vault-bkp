/**
 * quickadd-macros.js — QuickAdd macro library
 *
 * Install: QuickAdd → Manage Macros → new macro → "User Script" → pick this file
 * Each exported function = one macro. Add to QuickAdd choices as needed.
 *
 * QuickAdd replaces Shell Commands plugin — run any Python/shell script from here.
 */

// ─── Helpers ──────────────────────────────────────────────────────────────────

const { exec } = require("child_process");

function run(cmd, successMsg) {
  return new Promise((resolve) => {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        new Notice(`❌ ${err.message}`, 8000);
        console.error(stderr);
      } else {
        new Notice(`✅ ${successMsg || "Done"}`, 3000);
      }
      resolve();
    });
  });
}

// ─── Vault Sync ───────────────────────────────────────────────────────────────

/**
 * Sync vault brief + priority file from ~/.claude state.
 * Invoke: QuickAdd → "Sync Vault Brief"
 */
module.exports = async (params) => {
  const { quickAddApi, app } = params;
  const choice = await quickAddApi.suggester(
    ["Sync brief only (fast)", "Full sync (inbox + NECTAR)", "Priority file only"],
    ["--brief-only", "", "--priority-only"]
  );
  const py = "python3";
  const script = "C:/Users/amand/.claude/scripts/vault_narrative_sync.py";
  await run(`${py} "${script}" ${choice}`, "Vault sync complete");
};

// ─── Mermaid Regen ────────────────────────────────────────────────────────────

/**
 * Regenerate mermaid flowchart from current note's headings.
 * Invoke: QuickAdd → "Regen Mermaid"
 */
module.exports.regenMermaid = async (params) => {
  const { app } = params;
  const file = app.workspace.getActiveFile();
  if (!file) { new Notice("No active file"); return; }
  const content = await app.vault.read(file);

  const headingRe = /^(#{1,4})\s+(.+)$/gm;
  const headings = [];
  let m;
  while ((m = headingRe.exec(content)) !== null) {
    headings.push({ level: m[1].length, text: m[2].trim() });
  }
  if (!headings.length) { new Notice("No headings found"); return; }

  // Validate: 1 H1, no jumps
  const h1s = headings.filter(h => h.level === 1);
  if (h1s.length > 1) new Notice(`⚠️ ${h1s.length} H1s found — should be 1`, 5000);
  for (let i = 1; i < headings.length; i++) {
    if (headings[i].level - headings[i-1].level > 1) {
      new Notice(`⚠️ Heading jump at "${headings[i].text}" (H${headings[i-1].level}→H${headings[i].level})`, 5000);
    }
  }

  // Build mermaid
  const themeInit = `%%{init: {"theme": "base", "themeVariables": {
  "primaryColor": "#1E6B5A", "primaryTextColor": "#E8FFF8",
  "primaryBorderColor": "#4BC8A8", "secondaryColor": "#8FBE9B",
  "secondaryTextColor": "#0D2B20", "tertiaryColor": "#0D2B2B",
  "lineColor": "#4BC8A8", "edgeLabelBackground": "#1A4A3A",
  "fontFamily": "monospace"
}}}%%`;

  const slug = (t, i) => `n${i}_${t.toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 12)}`;
  const classDefs = [
    "classDef h1 fill:#1E6B5A,stroke:#4BC8A8,color:#E8FFF8,font-weight:bold,font-size:14px",
    "classDef h2 fill:#2D9B83,stroke:#4BC8A8,color:#E8FFF8,font-size:13px",
    "classDef h3 fill:#3AAA90,stroke:#4BC8A8,color:#E8FFF8,font-size:12px",
    "classDef h4 fill:#8FBE9B,stroke:#2D9B83,color:#0D2B20,font-size:11px",
  ].join("\n    ");

  let nodeLines = "", edgeLines = "";
  const stack = [];
  headings.forEach((h, i) => {
    const id = slug(h.text, i);
    const label = h.text.length > 28 ? h.text.slice(0, 25) + "…" : h.text;
    nodeLines += `    ${id}["${label}"]:::h${h.level}\n`;
    while (stack.length && stack[stack.length - 1].level >= h.level) stack.pop();
    if (stack.length) edgeLines += `    ${stack[stack.length - 1].id} --> ${id}\n`;
    stack.push({ level: h.level, id });
  });

  const mermaidBlock = "```mermaid\n" + themeInit + "\nflowchart TD\n" + nodeLines + "\n" + edgeLines + "\n    " + classDefs + "\n```";

  let newContent;
  if (content.match(/```mermaid[\s\S]*?```/)) {
    newContent = content.replace(/```mermaid[\s\S]*?```/, mermaidBlock);
  } else {
    // Insert after "Architecture Map" heading or at end
    newContent = content.replace(/(## Architecture Map[^\n]*\n)/, `$1\n${mermaidBlock}\n`);
    if (newContent === content) newContent = content + "\n\n" + mermaidBlock;
  }

  await app.vault.modify(file, newContent);
  new Notice("✅ Mermaid chart regenerated", 3000);
};

// ─── Header Validator ─────────────────────────────────────────────────────────

/**
 * Validate H1 uniqueness + no heading jumps in current note.
 * Invoke: QuickAdd → "Validate Headers"
 */
module.exports.validateHeaders = async (params) => {
  const { app } = params;
  const file = app.workspace.getActiveFile();
  if (!file) { new Notice("No active file"); return; }
  const content = await app.vault.read(file);

  const headingRe = /^(#{1,4})\s+(.+)$/gm;
  const headings = [];
  let m;
  while ((m = headingRe.exec(content)) !== null) {
    headings.push({ level: m[1].length, text: m[2].trim() });
  }

  const issues = [];
  const h1s = headings.filter(h => h.level === 1);
  if (h1s.length !== 1) issues.push(`H1 count: ${h1s.length} (expected 1)`);

  for (let i = 1; i < headings.length; i++) {
    const diff = headings[i].level - headings[i-1].level;
    if (diff > 1) {
      issues.push(`Jump H${headings[i-1].level}→H${headings[i].level} at "${headings[i].text}"`);
    }
  }

  if (issues.length === 0) new Notice("✅ Header structure valid", 3000);
  else new Notice("⚠️ Issues:\n" + issues.join("\n"), 8000);
};

// ─── Annotation Commit ────────────────────────────────────────────────────────

/**
 * Hash the "## Your Annotations" section → write ann_hash to frontmatter.
 * This is what Ctrl+Alt+C does (commit-annotation.js) — same logic here.
 * Invoke: QuickAdd → "Commit Annotation" (or keep as Ctrl+Alt+C hotkey)
 */
module.exports.commitAnnotation = async (params) => {
  const { app } = params;
  const file = app.workspace.getActiveFile();
  if (!file) { new Notice("No active file"); return; }
  const content = await app.vault.read(file);

  const annotSection = content.match(/## Your Annotations\s*\n([\s\S]*?)(?:\n---|\n## |\n```|\Z)/);
  if (!annotSection) { new Notice("No '## Your Annotations' section found"); return; }

  const annText = annotSection[1].trim();
  if (!annText) { new Notice("Annotations section is empty"); return; }

  // SHA-256 via SubtleCrypto (available in Obsidian's Electron context)
  const msgBuffer = new TextEncoder().encode(annText);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  const hashHex = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, "0")).join("");

  const ts = new Date().toISOString();
  let newContent = content;

  // Update ann_hash in frontmatter
  if (newContent.match(/^ann_hash:/m)) {
    newContent = newContent.replace(/^ann_hash:.*$/m, `ann_hash: "sha256:${hashHex.slice(0, 16)}"`);
  } else {
    newContent = newContent.replace(/^---\n([\s\S]*?)---/, `---\n$1ann_hash: "sha256:${hashHex.slice(0, 16)}"\n---`);
  }
  if (newContent.match(/^ann_ts:/m)) {
    newContent = newContent.replace(/^ann_ts:.*$/m, `ann_ts: "${ts}"`);
  } else {
    newContent = newContent.replace(/^---\n([\s\S]*?)---/, `---\n$1ann_ts: "${ts}"\n---`);
  }

  await app.vault.modify(file, newContent);
  new Notice(`✅ Annotation committed\nsha256:${hashHex.slice(0, 16)}`, 4000);
};

// ─── Inbox Router ─────────────────────────────────────────────────────────────

/**
 * Run inbox_router.py to atomize REVIEW-INBOX into findings/flags.
 */
module.exports.routeInbox = async (params) => {
  await run(
    `python3 "C:/Users/amand/.claude/scripts/inbox_router.py"`,
    "Inbox routed — check Human-Inbox/findings/ and Human-Inbox/flags/"
  );
};
