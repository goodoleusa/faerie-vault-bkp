/**
 * QuickAdd: Challenge Finding
 * Sets status=challenged, annotation_type=challenge.
 * Agents see this as: "human disagrees — review the reasoning."
 * Write your challenge in ## Your Annotations, then run this.
 */
module.exports = async (params) => {
    const file = params.app.workspace.getActiveFile();
    if (!file) { new Notice("No active file."); return; }

    await params.app.fileManager.processFrontMatter(file, (fm) => {
        fm.status = "challenged";
        fm.annotation_type = "challenge";
        fm.reviewed_at = new Date().toISOString();
    });

    new Notice("Finding challenged. Write details in '## Your Annotations', then Ctrl+Alt+C to commit.");
};
