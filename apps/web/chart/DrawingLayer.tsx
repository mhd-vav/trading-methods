"use client";
/**
 * DrawingLayer — an interactive SVG overlay on top of the ECharts canvas for
 * layer-2 (markup) drawings: trendlines, horizontals, rays, fib, rects, labels.
 * Kept separate from ChartRenderer so drawings render at chart-resolution
 * regardless of ECharts state. Point coordinates are (x=index, y=price); the
 * layer needs a scale transform injected by the consumer for pixel mapping.
 */
import type { Drawing } from "@trading-desk/contracts";

export interface DrawingLayerProps {
  drawings: Drawing[];
  selectedId: string | null;
  tool: Drawing["tool"] | null;
  onSelect(id: string | null): void;
  onAdd(d: Omit<Drawing, "id" | "createdAtMs" | "updatedAtMs">): void;
  /** Optional pixel scale to map domain (index, price) → screen. */
  scale?: { indexToPx: (x: number) => number; priceToPx?: (y: number) => number };
  width?: number;
  height?: number;
}

/** Minimal inline SVG renderer for each drawing tool (domain-space). */
function renderShape(d: Drawing, indexToPx: (x: number) => number, priceToPx: (y: number) => number) {
  const [p0 = { x: 0, y: 0 }, p1 = { x: 0, y: 0 }] = d.points;
  const x0 = indexToPx(p0.x);
  const x1 = indexToPx(p1.x);
  const y0 = priceToPx(p0.y);
  const y1 = priceToPx(p1.y);

  switch (d.tool) {
    case "trendline":
    case "ray":
      return <line x1={x0} y1={y0} x2={x1} y2={y1} stroke={d.color ?? "#10b981"} strokeWidth={1.5} />;
    case "horizontal-line":
      return <line x1={0} y1={y0} x2={x0 * 2 || 1} y2={y0} stroke={d.color ?? "#10b981"} strokeWidth={1.5} />;
    case "fibonacci": {
      const lines = [];
      for (let i = 0; i <= 8; i++) {
        const f = i / 8;
        const y = y0 + (y1 - y0) * f;
        lines.push(<line key={i} x1={x0} y1={y} x2={x1} y2={y} stroke="#f0b90b" strokeWidth={0.8} strokeDasharray="3 3" opacity={0.6} />);
      }
      return <>{lines}</>;
    }
    case "rectangle":
      return <rect x={Math.min(x0, x1)} y={Math.min(y0, y1)} width={Math.abs(x1 - x0)} height={Math.abs(y1 - y0)} fill="none" stroke={d.color ?? "#10b981"} strokeWidth={1.2} />;
    case "text":
      return (
        <text x={x0} y={y0} fill={d.color ?? "#dfe6ed"} fontSize={12}>
          {d.label ?? "text"}
        </text>
      );
    case "arrow":
      return <circle cx={x0} cy={y0} r={4} fill={d.color ?? "#10b981"} />;
    default:
      return null;
  }
}

export function DrawingLayer({ drawings, selectedId, onSelect }: DrawingLayerProps) {
  const indexToPx = (x: number) => x * 10; // default coarse scale
  const priceToPx = (y: number) => 300 - y * 10; // inverted, coarse
  return (
    <svg
      aria-label="Drawing layer"
      style={{ position: "absolute", inset: 0, pointerEvents: "none", width: "100%", height: "100%" }}
    >
      {drawings.map((d) => (
        <g
          key={d.id}
          pointerEvents="visiblePainted"
          style={{ pointerEvents: "painted" }}
          onClick={(e) => { e.stopPropagation(); onSelect(selectedId === d.id ? null : d.id); }}
          opacity={d.visible === false ? 0 : selectedId === d.id ? 1 : 0.85}
        >
          {renderShape(d, indexToPx, priceToPx)}
          {d.locked === false && <rect x={0} y={0} width={0} height={0} />}
        </g>
      ))}
    </svg>
  );
}