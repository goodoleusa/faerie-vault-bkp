/**
 * QuickAdd User Script: Commit Annotation
 *
 * Triggered via QuickAdd command palette or hotkey (Ctrl+Alt+C).
 * Reads the "## Your Annotations" section, SHA-256 hashes it,
 * writes ann_hash + ann_ts to frontmatter. The actual COC sync
 * happens when vault_annotation_sync.py fires (pre-session hook
 * or manual). This script is the "submit button."
 *
 * Setup in QuickAdd:
 *   1. Settings → QuickAdd → Manage Macros → New Macro: "Commit Annotation"
 *   2. Add step: User Script → point to this file
 *   3. Optionally bind to hotkey via Obsidian Hotkeys settings
 *
 * No Shell Commands, no Templater, no external process at commit time.
 * Pure Obsidian JS — the hashing runs inside Obsidian itself.
 */
module.exports = async (params) => {
    const { app, quickAddApi } = params;
    const file = app.workspace.getActiveFile();
    if (!file) {
        new Notice("No active file to commit.");
        return;
    }

    const content = await app.vault.read(file);

    // Extract ## Your Annotations section
    const annotationMatch = content.match(
        /##\s+Your Annotations\s*\n([\s\S]*?)(?=\n##\s|\n---\s*$|$)/
    );

    if (!annotationMatch || !annotationMatch[1].trim()) {
        new Notice("No annotation content found in '## Your Annotations' section.");
        return;
    }

    const annotationText = annotationMatch[1].trim();

    // SHA-256 hash the annotation content (Web Crypto API available in Obsidian)
    const encoder = new TextEncoder();
    const data = encoder.encode(annotationText);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    const annHash = `sha256:${hashHex}`;

    // Timestamp
    const annTs = new Date().toISOString();

    // Update frontmatter
    await app.fileManager.processFrontMatter(file, (fm) => {
        fm.ann_hash = annHash;
        fm.ann_ts = annTs;
        // Don't set ann_synced — that's for vault_annotation_sync.py
    });

    new Notice(`Annotation committed!\n${annHash.substring(0, 24)}...`);

    // Optional: log to a local commit-log for batch verification
    const logPath = "00-SHARED/Agent-Context/.hashes/annotation-commits.jsonl";
    const logEntry = JSON.stringify({
        file: file.path,
        ann_hash: annHash,
        ann_ts: annTs,
        annotation_length: annotationText.length,
    }) + "\n";

    try {
        const logFile = app.vault.getAbstractFileByPath(logPath);
        if (logFile) {
            await app.vault.append(logFile, logEntry);
        } else {
            // Create the log file if it doesn't exist
            const folder = app.vault.getAbstractFileByPath("00-SHARED/Agent-Context/.hashes");
            if (!folder) {
                await app.vault.createFolder("00-SHARED/Agent-Context/.hashes");
            }
            await app.vault.create(logPath, logEntry);
        }
    } catch (e) {
        // Non-fatal — the frontmatter hash is what matters
        console.log("Could not write annotation commit log:", e);
    }
};
