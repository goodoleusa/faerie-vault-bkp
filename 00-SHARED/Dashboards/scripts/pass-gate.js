/**
 * QuickAdd: Pass Gate
 * For gate-review notes: sets status=passed, records gate decision.
 * Equivalent to `python3 scripts/gate_pass.py pass N` but from Obsidian.
 */
module.exports = async (params) => {
    const { app, quickAddApi } = params;
    const file = app.workspace.getActiveFile();
    if (!file) { new Notice("No active file."); return; }

    const confirm = await quickAddApi.yesNoPrompt(
        "Pass this pipeline gate?",
        "This approves the current phase and allows the next /data-ingest run to proceed."
    );
    if (!confirm) return;

    await app.fileManager.processFrontMatter(file, (fm) => {
        fm.status = "passed";
        fm.passed_at = new Date().toISOString();
        fm.reviewer = "researcher";
    });

    // Log to the annotation commits
    const logPath = "00-SHARED/Agent-Context/.hashes/annotation-commits.jsonl";
    const logEntry = JSON.stringify({
        type: "gate_pass",
        file: file.path,
        gate: file.basename,
        passed_at: new Date().toISOString(),
    }) + "\n";

    try {
        const logFile = app.vault.getAbstractFileByPath(logPath);
        if (logFile) await app.vault.append(logFile, logEntry);
    } catch (e) { console.log("Gate pass log:", e); }

    new Notice("Gate PASSED. Next /data-ingest run can proceed.");
};
