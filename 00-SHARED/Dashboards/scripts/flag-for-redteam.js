/**
 * QuickAdd: Flag for Red Team
 * Sets status=red-team-requested, adds red-team tag.
 * vault_annotation_sync creates a sprint queue task for /run to pick up.
 */
module.exports = async (params) => {
    const { app, quickAddApi } = params;
    const file = app.workspace.getActiveFile();
    if (!file) { new Notice("No active file."); return; }

    const hypothesis = await quickAddApi.inputPrompt(
        "Which hypothesis to red-team?",
        "H1, H2, H3, H4, or H5"
    );
    if (!hypothesis) return;

    await app.fileManager.processFrontMatter(file, (fm) => {
        fm.status = "red-team-requested";
        fm.red_team_target = hypothesis.trim().toUpperCase();
        fm.reviewed_at = new Date().toISOString();
        const tags = fm.tags || [];
        if (!tags.includes("red-team")) tags.push("red-team");
        fm.tags = tags;
    });

    new Notice(`Red team requested for ${hypothesis}. Will queue on next /run.`);
};
