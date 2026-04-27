/**
 * QuickAdd: Promote to Evidence
 * Sets promotion_state=promoted, status=annotated.
 * This signals: "I've reviewed this, it belongs in 30-Evidence."
 * The actual file move is manual (drag in Obsidian) — this sets the metadata.
 */
module.exports = async (params) => {
    const { app, quickAddApi } = params;
    const file = app.workspace.getActiveFile();
    if (!file) { new Notice("No active file."); return; }

    const tier = await quickAddApi.inputPrompt(
        "Evidence tier?",
        "1 (smoking gun), 2 (strong), 3 (contextual), 4 (catalog)"
    );

    await app.fileManager.processFrontMatter(file, (fm) => {
        fm.promotion_state = "promoted";
        fm.status = "annotated";
        fm.promoted_at = new Date().toISOString();
        if (tier) fm.tier = parseInt(tier) || tier;
    });

    new Notice(`Promoted to evidence (Tier ${tier || '?'}). Move to 30-Evidence/ when ready.`);
};
