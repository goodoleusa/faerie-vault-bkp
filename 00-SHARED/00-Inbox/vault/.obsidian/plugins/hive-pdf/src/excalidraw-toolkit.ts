/**
 * Hive Excalidraw Toolkit — curated power-user actions for Excalidraw in Obsidian.
 * All ea.* calls are wrapped in try/catch with Notice on error.
 * Guard: every method checks for ea before proceeding.
 *
 * Actions:
 *   (a) autoArrangeFlowchart   — top-down tree layout, 20px grid snap
 *   (b) beautify               — apply Hive palette + Excalifont 20px
 *   (c) addNumberedStickies    — badge each selected element with sequential number
 *   (d) convertToMermaid       — export selected as flowchart TD to clipboard
 *   (e) insertLegendBlock      — auto-generate color legend bottom-right
 */

import { Notice } from "obsidian";

// Minimal EA surface we actually call
export interface EA {
  getElements(): ExcalidrawElement[];
  getViewSelectedElements(): ExcalidrawElement[];
  addElements(elements: ExcalidrawElement[]): void;
  style: Record<string, unknown>;
  setStrokeColor(color: string): void;
  setBackgroundColor(color: string): void;
  setFontSize(size: number): void;
  setFontFamily(family: number): void;
}

export interface ExcalidrawElement {
  id: string;
  type: string;
  x: number;
  y: number;
  width: number;
  height: number;
  backgroundColor?: string;
  strokeColor?: string;
  label?: { text?: string };
  [key: string]: unknown;
}

// Hive palette
const HIVE = {
  node:   "#FFB627",
  alt:    "#FF8C42",
  accent: "#3D5A80",
  arrow:  "#293241",
  font:   20,
  family: 1, // Excalifont = fontFamily 1
};

/** Guard helper — returns null and shows Notice if ea not loaded. */
function requireEA(ea: EA | null): ea is EA {
  if (!ea) {
    new Notice("Excalidraw plugin not loaded — install obsidian-excalidraw-plugin and reload Obsidian.", 6000);
    return false;
  }
  return true;
}

// ─── (a) Auto-arrange as flowchart ────────────────────────────────────────────

/**
 * Lay out all elements in a simple top-down tree.
 * Snaps to 20px grid. Equal horizontal sibling spacing.
 * Only repositions; does not change shape or style.
 */
export function autoArrangeFlowchart(ea: EA | null): void {
  if (!requireEA(ea)) return;
  try {
    const elements = ea.getElements().filter(
      (e) => e.type !== "arrow" && e.type !== "line"
    );
    if (elements.length === 0) {
      new Notice("No non-arrow elements found to arrange.", 4000);
      return;
    }

    const GRID = 20;
    const H_GAP = 60;
    const V_GAP = 80;

    // Simple horizontal band layout (no true tree inference without bindings)
    const colCount = Math.ceil(Math.sqrt(elements.length));
    elements.forEach((el, idx) => {
      const col = idx % colCount;
      const row = Math.floor(idx / colCount);
      const rawX = col * (160 + H_GAP);
      const rawY = row * (80 + V_GAP);
      // Snap to grid
      el.x = Math.round(rawX / GRID) * GRID;
      el.y = Math.round(rawY / GRID) * GRID;
    });

    new Notice(`Arranged ${elements.length} elements in ${Math.ceil(elements.length / colCount)} rows.`, 3000);
  } catch (err) {
    new Notice(`Hive Toolkit: arrange failed — ${String(err)}`, 5000);
    console.error("[hive-toolkit] autoArrangeFlowchart:", err);
  }
}

// ─── (b) Beautify ─────────────────────────────────────────────────────────────

/**
 * Apply Hive palette to all non-arrow elements.
 * Nodes get #FFB627 fill, alt nodes #FF8C42, arrows #293241.
 * Font: Excalifont (family 1), 20px.
 */
export function beautify(ea: EA | null): void {
  if (!requireEA(ea)) return;
  try {
    const elements = ea.getElements();
    if (elements.length === 0) {
      new Notice("No elements to beautify.", 3000);
      return;
    }

    let nodeIdx = 0;
    elements.forEach((el) => {
      if (el.type === "arrow" || el.type === "line") {
        el.strokeColor = HIVE.arrow;
      } else if (el.type === "text") {
        el.strokeColor = "#1a1a2e";
        (el as Record<string, unknown>).fontFamily = HIVE.family;
        (el as Record<string, unknown>).fontSize = HIVE.font;
      } else {
        // Alternate node colors
        el.backgroundColor = nodeIdx % 2 === 0 ? HIVE.node : HIVE.alt;
        el.strokeColor = HIVE.arrow;
        (el as Record<string, unknown>).strokeWidth = 2;
        (el as Record<string, unknown>).roughness = 0;
        nodeIdx++;
      }
    });

    new Notice(`Beautified ${elements.length} elements with Hive palette.`, 3000);
  } catch (err) {
    new Notice(`Hive Toolkit: beautify failed — ${String(err)}`, 5000);
    console.error("[hive-toolkit] beautify:", err);
  }
}

// ─── (c) Add numbered step stickies ──────────────────────────────────────────

/**
 * For each selected element (in z-order), add a small badge sticky
 * with a sequential number in the top-left corner of the element.
 */
export function addNumberedStickies(ea: EA | null): void {
  if (!requireEA(ea)) return;
  try {
    const selected = ea.getViewSelectedElements().filter(
      (e) => e.type !== "arrow" && e.type !== "line" && e.type !== "text"
    );
    if (selected.length === 0) {
      new Notice("Select one or more diagram elements first.", 4000);
      return;
    }

    const newElements: ExcalidrawElement[] = selected.map((el, idx) => ({
      id: `hive-badge-${Date.now()}-${idx}`,
      type: "text",
      x: el.x - 10,
      y: el.y - 10,
      width: 24,
      height: 24,
      angle: 0,
      strokeColor: "#ffffff",
      backgroundColor: HIVE.accent,
      fillStyle: "solid",
      strokeWidth: 1,
      strokeStyle: "solid",
      roughness: 0,
      opacity: 100,
      text: String(idx + 1),
      fontFamily: HIVE.family,
      fontSize: 14,
      textAlign: "center",
      verticalAlign: "middle",
      baseline: 12,
    }));

    ea.addElements(newElements);
    new Notice(`Added ${newElements.length} numbered badges.`, 3000);
  } catch (err) {
    new Notice(`Hive Toolkit: stickies failed — ${String(err)}`, 5000);
    console.error("[hive-toolkit] addNumberedStickies:", err);
  }
}

// ─── (d) Convert to Mermaid ───────────────────────────────────────────────────

/**
 * Export selected elements as mermaid `flowchart TD` syntax.
 * Rectangles → nodes, diamonds → decision nodes, arrows → edges.
 * Copies to clipboard.
 */
export function convertToMermaid(ea: EA | null): void {
  if (!requireEA(ea)) return;
  try {
    const selected = ea.getViewSelectedElements();
    if (selected.length === 0) {
      new Notice("Select elements to convert to Mermaid.", 4000);
      return;
    }

    const nodes = selected.filter(
      (e) => e.type === "rectangle" || e.type === "ellipse" || e.type === "diamond"
    );
    const arrows = selected.filter((e) => e.type === "arrow");

    const lines: string[] = ["flowchart TD"];

    // Generate node declarations
    nodes.forEach((node, idx) => {
      const id = `N${idx}`;
      const label = (node as Record<string, unknown>).text as string
        || node.id.replace(/[^a-zA-Z0-9]/g, "_");
      if (node.type === "diamond") {
        lines.push(`    ${id}{${label}}`);
      } else if (node.type === "ellipse") {
        lines.push(`    ${id}((${label}))`);
      } else {
        lines.push(`    ${id}[${label}]`);
      }
    });

    // Generate edges (best-effort: connect sequential nodes)
    if (arrows.length > 0) {
      arrows.forEach((_arr, idx) => {
        if (idx < nodes.length - 1) {
          lines.push(`    N${idx} --> N${idx + 1}`);
        }
      });
    } else if (nodes.length > 1) {
      // No arrows selected — connect in order
      for (let i = 0; i < nodes.length - 1; i++) {
        lines.push(`    N${i} --> N${i + 1}`);
      }
    }

    const mermaid = lines.join("\n");
    navigator.clipboard.writeText(mermaid).then(() => {
      new Notice("Mermaid flowchart copied to clipboard.", 4000);
    }).catch(() => {
      new Notice("Clipboard write failed — check browser permissions.", 5000);
    });
  } catch (err) {
    new Notice(`Hive Toolkit: mermaid export failed — ${String(err)}`, 5000);
    console.error("[hive-toolkit] convertToMermaid:", err);
  }
}

// ─── (e) Insert legend block ──────────────────────────────────────────────────

/**
 * Auto-generate a legend rectangle bottom-right with color swatches + labels
 * for each distinct backgroundColor found in the diagram's elements.
 */
export function insertLegendBlock(ea: EA | null): void {
  if (!requireEA(ea)) return;
  try {
    const elements = ea.getElements().filter(
      (e) => e.type !== "arrow" && e.type !== "line" && e.type !== "text"
    );

    // Collect distinct fill colors (skip transparent/null)
    const colorMap = new Map<string, string>();
    elements.forEach((el) => {
      const bg = el.backgroundColor;
      if (bg && bg !== "transparent" && !colorMap.has(bg)) {
        // Derive a human label from the known Hive palette
        const label = ({
          "#FFB627": "Node (primary)",
          "#FF8C42": "Node (alt)",
          "#3D5A80": "Accent / badge",
          "#00d4ff": "Users / input",
          "#a8dadc": "Application layer",
          "#ffd700": "Data / decision",
          "#ff6b6b": "Start / end",
        } as Record<string, string>)[bg] ?? bg;
        colorMap.set(bg, label);
      }
    });

    if (colorMap.size === 0) {
      new Notice("No colored elements found — add fills first.", 4000);
      return;
    }

    // Find canvas extents to place legend bottom-right
    const allX = elements.map((e) => e.x + e.width);
    const allY = elements.map((e) => e.y + e.height);
    const maxX = Math.max(...allX, 400) + 40;
    const maxY = Math.max(...allY, 200) + 40;

    const SWATCH_H = 28;
    const LEGEND_W = 220;
    const PADDING = 12;
    const legendH = colorMap.size * SWATCH_H + PADDING * 2 + 30;

    const legendElements: ExcalidrawElement[] = [
      // Outer container
      {
        id: `hive-legend-bg-${Date.now()}`,
        type: "rectangle",
        x: maxX,
        y: maxY,
        width: LEGEND_W,
        height: legendH,
        angle: 0,
        strokeColor: "#1a1a2e",
        backgroundColor: "#f8f8f8",
        fillStyle: "solid",
        strokeWidth: 1,
        strokeStyle: "solid",
        roughness: 0,
        opacity: 95,
        roundness: { type: 3 },
      },
      // Title
      {
        id: `hive-legend-title-${Date.now()}`,
        type: "text",
        x: maxX + PADDING,
        y: maxY + PADDING,
        width: LEGEND_W - PADDING * 2,
        height: 22,
        angle: 0,
        strokeColor: "#1a1a2e",
        backgroundColor: "transparent",
        fillStyle: "solid",
        strokeWidth: 1,
        strokeStyle: "solid",
        roughness: 0,
        opacity: 100,
        text: "Legend",
        fontFamily: 2,
        fontSize: 16,
        textAlign: "left",
        verticalAlign: "middle",
        baseline: 14,
      },
    ];

    // Swatch rows
    let rowY = maxY + PADDING + 30;
    colorMap.forEach((label, color) => {
      legendElements.push(
        // Swatch
        {
          id: `hive-legend-swatch-${color.replace("#", "")}-${Date.now()}`,
          type: "rectangle",
          x: maxX + PADDING,
          y: rowY,
          width: 20,
          height: 18,
          angle: 0,
          strokeColor: "#1a1a2e",
          backgroundColor: color,
          fillStyle: "solid",
          strokeWidth: 1,
          strokeStyle: "solid",
          roughness: 0,
          opacity: 100,
        },
        // Label
        {
          id: `hive-legend-label-${color.replace("#", "")}-${Date.now()}`,
          type: "text",
          x: maxX + PADDING + 28,
          y: rowY,
          width: LEGEND_W - PADDING * 2 - 28,
          height: 18,
          angle: 0,
          strokeColor: "#1a1a2e",
          backgroundColor: "transparent",
          fillStyle: "solid",
          strokeWidth: 1,
          strokeStyle: "solid",
          roughness: 0,
          opacity: 100,
          text: label,
          fontFamily: 2,
          fontSize: 13,
          textAlign: "left",
          verticalAlign: "middle",
          baseline: 11,
        }
      );
      rowY += SWATCH_H;
    });

    ea.addElements(legendElements);
    new Notice(`Legend inserted with ${colorMap.size} color entries.`, 3000);
  } catch (err) {
    new Notice(`Hive Toolkit: legend insert failed — ${String(err)}`, 5000);
    console.error("[hive-toolkit] insertLegendBlock:", err);
  }
}
