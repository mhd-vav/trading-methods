"use client";
/** VolumePane — ATR (and future volume-derived indicators) readout. */
import type { IndicatorResult } from "@trading-desk/contracts";

export function VolumePane({ indicators }: { indicators: IndicatorResult[] }) {
  if (indicators.length === 0) return null;
  return (
    <div style={{ display: "flex", gap: 12, padding: "4px 10px", fontSize: 12, color: "#9aa7b5", borderTop: "1px solid #242a33" }}>
      {indicators.map((ind) => {
        const last = ind.line[ind.line.length - 1];
        return (
          <span key={ind.kind} style={{ fontFamily: "monospace" }}>
            {ind.kind.toUpperCase()}: <span style={{ color: "#dfe6ed" }}>{last ? last.y.toFixed(4) : "—"}</span>
          </span>
        );
      })}
    </div>
  );
}