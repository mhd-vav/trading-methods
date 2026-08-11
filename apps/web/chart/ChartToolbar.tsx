"use client";
/** ChartToolbar — interval selector, drawing tools, indicator add, fit-all, save. */
import type { IndicatorKind, Timeframe } from "@trading-desk/contracts";
import type { Drawing } from "@trading-desk/contracts";

const INTERVALS: Timeframe[] = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"];
const DRAW_TOOLS: Drawing["tool"][] = ["trendline", "horizontal-line", "ray", "fibonacci", "rectangle", "text", "arrow"];
const INDICATORS: { kind: IndicatorKind; label: string }[] = [
  { kind: "sma", label: "SMA" },
  { kind: "ema", label: "EMA" },
  { kind: "rsi", label: "RSI" },
  { kind: "macd", label: "MACD" },
  { kind: "atr", label: "ATR" },
  { kind: "bollinger", label: "BB" },
];

export interface ChartToolbarProps {
  symbol: string;
  interval: Timeframe;
  onInterval(iv: Timeframe): void;
  drawingTool: Drawing["tool"] | null;
  onDrawingTool(t: Drawing["tool"] | null): void;
  onAddIndicator(kind: IndicatorKind): void;
  onClearIndicator(): void;
  onFitAll(): void;
  hasDrawingChanges: boolean;
  onSaveDrawings(): void;
}

export function ChartToolbar({
  symbol,
  interval,
  onInterval,
  drawingTool,
  onDrawingTool,
  onAddIndicator,
  onClearIndicator,
  onFitAll,
  hasDrawingChanges,
  onSaveDrawings,
}: ChartToolbarProps) {
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center", padding: "6px 10px", flexWrap: "wrap", borderBottom: "1px solid #242a33" }}>
      <strong>{symbol}</strong>

      <select
        aria-label="Interval"
        value={interval}
        onChange={(e) => onInterval(e.target.value as Timeframe)}
        style={{ background: "#0e1319", color: "#dfe6ed", border: "1px solid #242a33", borderRadius: 4, padding: "2px 6px" }}
      >
        {INTERVALS.map((iv) => (
          <option key={iv} value={iv}>{iv}</option>
        ))}
      </select>

      <div role="group" aria-label="Drawing tools" style={{ display: "flex", gap: 4 }}>
        {DRAW_TOOLS.map((t) => (
          <button
            key={t}
            aria-pressed={drawingTool === t}
            onClick={() => onDrawingTool(drawingTool === t ? null : t)}
            title={t}
            style={drawingTool === t ? selectedStyle : baseStyle}
          >
            {t === "trendline" ? "↗" : t === "horizontal-line" ? "―" : t === "ray" ? "→" : t === "fibonacci" ? "Φ" : t === "rectangle" ? "▭" : t === "text" ? "A" : "⤴"}
          </button>
        ))}
      </div>

      <select
        aria-label="Add indicator"
        defaultValue=""
        onChange={(e) => {
          if (e.target.value) onAddIndicator(e.target.value as IndicatorKind);
          e.target.value = "";
        }}
        style={{ background: "#0e1319", color: "#dfe6ed", border: "1px solid #242a33", borderRadius: 4, padding: "2px 6px" }}
      >
        <option value="" disabled>+ Indicator</option>
        {INDICATORS.map((i) => (
          <option key={i.kind} value={i.kind}>{i.label}</option>
        ))}
      </select>

      <button onClick={onClearIndicator} style={baseStyle}>Clear</button>
      <button onClick={onFitAll} style={baseStyle}>Fit</button>
      {hasDrawingChanges && (
        <button onClick={onSaveDrawings} style={{ ...baseStyle, background: "#10b981" }}>Save</button>
      )}
    </div>
  );
}

const baseStyle: React.CSSProperties = {
  background: "#0e1319",
  color: "#dfe6ed",
  border: "1px solid #242a33",
  borderRadius: 4,
  padding: "2px 8px",
  cursor: "pointer",
};
const selectedStyle: React.CSSProperties = {
  ...baseStyle,
  background: "#10b981",
  borderColor: "#10b981",
};