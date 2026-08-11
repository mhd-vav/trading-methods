"use client";
/**
 * useDrawingState — manages chart drawings: CRUD, selection, locking, visibility,
 * and (debounced) persistence callback. Drawings are the Phase 2 objects that
 * must persist server-side in Phase 5.
 */
import { useCallback, useRef, useState } from "react";
import type { Drawing } from "@trading-desk/contracts";

export interface UseDrawingState {
  drawings: Drawing[];
  selectedId: string | null;
  tool: Drawing["tool"] | null;
  setTool(t: Drawing["tool"] | null): void;
  addDrawing(d: Omit<Drawing, "id" | "createdAtMs" | "updatedAtMs">): Drawing;
  updateDrawing(id: string, patch: Partial<Omit<Drawing, "id">>): void;
  deleteDrawing(id: string): void;
  select(id: string | null): void;
  movePoint(drawingId: string, pointIndex: number, x: number, y: number): void;
  persist(): void;
  hasChanges: boolean;
}

export interface DrawingStateOptions {
  initial?: Drawing[];
  onPersist?: (drawings: Drawing[]) => void;
  debounceMs?: number;
}

export function useDrawingState(opts: DrawingStateOptions = {}): UseDrawingState {
  const [drawings, setDrawings] = useState<Drawing[]>(opts.initial ?? []);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [tool, setTool] = useState<Drawing["tool"] | null>(null);
  const [hasChanges, setHasChanges] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const addDrawing = useCallback((d: Omit<Drawing, "id" | "createdAtMs" | "updatedAtMs">): Drawing => {
    const now = Date.now();
    const drawing: Drawing = {
      ...d,
      id: `drw-${now}-${Math.random().toString(36).slice(2, 8)}`,
      createdAtMs: now,
      updatedAtMs: now,
      locked: d.locked ?? false,
      visible: d.visible ?? true,
    };
    setDrawings((prev) => [...prev, drawing]);
    setHasChanges(true);
    setSelectedId(drawing.id);
    return drawing;
  }, []);

  const updateDrawing = useCallback((id: string, patch: Partial<Omit<Drawing, "id">>) => {
    setDrawings((prev) =>
      prev.map((d) => (d.id === id ? { ...d, ...patch, updatedAtMs: Date.now() } : d)),
    );
    setHasChanges(true);
  }, []);

  const deleteDrawing = useCallback((id: string) => {
    setDrawings((prev) => prev.filter((d) => d.id !== id));
    setSelectedId((sel) => (sel === id ? null : sel));
    setHasChanges(true);
  }, []);

  const select = useCallback((id: string | null) => setSelectedId(id), []);

  const movePoint = useCallback((drawingId: string, pointIndex: number, x: number, y: number) => {
    setDrawings((prev) =>
      prev.map((d) =>
        d.id === drawingId
          ? { ...d, points: d.points.map((p, i) => (i === pointIndex ? { x, y } : p)), updatedAtMs: Date.now() }
          : d,
      ),
    );
    setHasChanges(true);
  }, []);

  const persist = useCallback(() => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      opts.onPersist?.(drawings);
      setHasChanges(false);
    }, opts.debounceMs ?? 400);
  }, [drawings, opts]);

  return {
    drawings,
    selectedId,
    tool,
    setTool,
    addDrawing,
    updateDrawing,
    deleteDrawing,
    select,
    movePoint,
    persist,
    hasChanges,
  };
}
