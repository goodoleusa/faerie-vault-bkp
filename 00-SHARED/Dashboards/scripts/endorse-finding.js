/**
 * QuickAdd: Endorse Finding
 * Sets status=endorsed, annotation_type=endorsement in frontmatter.
 * Agents see this as: "human confirmed this finding is sound."
 */
module.exports = async (params) => {
    const file = params.app.workspace.getActiveFile();
    if (!file) { new Notice("No active file."); return; }

    await params.app.fileManager.processFrontMatter(file, (fm) => {
        fm.status = "endorsed";
        fm.annotation_type = "endorsement";
        fm.reviewed_at = new Date().toISOString();
        fm.promotion_state = "promoted";
    });

    new Notice("Finding endorsed. Will sync to agent COC on next session.");
};
