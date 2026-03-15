import { useMemo, useState, useRef, useCallback } from "react";
import { cn } from "@/lib/utils";
import { KU_DISPLAY_NAMES } from "@/lib/constants";

export type UnitStatus = "unknown" | "partially_learned" | "learned" | "misconception" | "corrected";

export interface UnitNode {
  unit_id: string;
  status: UnitStatus;
  topic_group?: string;
}

export interface KnowledgeUnitDefinition {
  id: string;
  name?: string;
  description?: string;
  prerequisites?: string[];
  topic_group?: string;
  example_correct_code?: string;
}

const TOPIC_ORDER = [
  "variables_and_assignment",
  "input_output",
  "basic_data_types",
  "operators",
  "conditionals",
  "loops",
  "lists",
  "functions",
  "variables",
  "io",
  "types",
  "conditionals",
  "lists",
  "dml",
  "aggregation",
  "joins",
  "basics",
  "ml",
  "ethics",
  "other",
];

const statusRectStyles: Record<UnitStatus, string> = {
  unknown: "fill-slate-100 stroke-slate-300",
  partially_learned: "fill-amber-100 stroke-amber-400",
  learned: "fill-emerald-100 stroke-emerald-400",
  misconception: "fill-red-100 stroke-red-400 animate-pulse",
  corrected: "fill-blue-100 stroke-blue-400",
};

const statusTextStyles: Record<UnitStatus, string> = {
  unknown: "text-slate-400",
  partially_learned: "text-amber-700",
  learned: "text-emerald-700",
  misconception: "text-red-700",
  corrected: "text-blue-700",
};

interface KnowledgeGraphProps {
  units: UnitNode[];
  knowledgeUnitDefinitions?: KnowledgeUnitDefinition[] | null;
  className?: string;
}

export function KnowledgeGraph({ units, knowledgeUnitDefinitions, className }: KnowledgeGraphProps) {
  const [selectedUnitId, setSelectedUnitId] = useState<string | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<{ from: string; to: string } | null>(null);
  const [transform, setTransform] = useState({ scale: 1, tx: 0, ty: 0 });
  const containerRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<{ x: number; y: number } | null>(null);

  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setTransform((t) => ({ ...t, scale: Math.max(0.5, Math.min(2, t.scale + delta)) }));
    },
    []
  );
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button === 0) dragRef.current = { x: e.clientX, y: e.clientY };
  }, []);
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (dragRef.current) {
      const dx = e.clientX - dragRef.current.x;
      const dy = e.clientY - dragRef.current.y;
      dragRef.current = { x: e.clientX, y: e.clientY };
      setTransform((t) => ({ ...t, tx: t.tx + dx, ty: t.ty + dy }));
    }
  }, []);
  const handleMouseUp = useCallback(() => {
    dragRef.current = null;
  }, []);

  const defsById = useMemo(() => {
    const m: Record<string, KnowledgeUnitDefinition> = {};
    for (const d of knowledgeUnitDefinitions ?? []) {
      m[d.id] = d;
    }
    return m;
  }, [knowledgeUnitDefinitions]);

  const byGroup = useMemo(() => {
    const map: Record<string, UnitNode[]> = {};
    for (const u of units) {
      const g = u.topic_group ?? "other";
      if (!map[g]) map[g] = [];
      map[g].push(u);
    }
    const ordered = TOPIC_ORDER.filter((g) => map[g]?.length).concat(
      Object.keys(map).filter((g) => !TOPIC_ORDER.includes(g))
    );
    return ordered.map((g) => ({ group: g, nodes: map[g] ?? [] }));
  }, [units]);

  const nodePos = useMemo(() => {
    const pos: Record<string, { x: number; y: number }> = {};
    const colWidth = 100;
    const rowHeight = 44;
    const nodeWidth = 72;
    const nodeHeight = 32;
    byGroup.forEach((col, ci) => {
      col.nodes.forEach((node, ni) => {
        pos[node.unit_id] = {
          x: ci * colWidth + (colWidth - nodeWidth) / 2 + nodeWidth / 2,
          y: ni * rowHeight + (rowHeight - nodeHeight) / 2 + nodeHeight / 2,
        };
      });
    });
    return { pos, colWidth: 100, rowHeight: 44, nodeWidth: 72, nodeHeight: 32 };
  }, [byGroup]);

  const edges = useMemo(() => {
    if (!knowledgeUnitDefinitions?.length) return [];
    const out: { from: string; to: string }[] = [];
    for (const d of knowledgeUnitDefinitions) {
      for (const p of d.prerequisites ?? []) {
        if (nodePos.pos[d.id] && nodePos.pos[p]) out.push({ from: p, to: d.id });
      }
    }
    return out;
  }, [knowledgeUnitDefinitions, nodePos.pos]);

  const colWidth = 100;
  const rowHeight = 44;
  const nodeWidth = 72;
  const nodeHeight = 32;

  const viewW = byGroup.length * colWidth;
  const viewH = Math.max(...byGroup.map((c) => c.nodes.length * rowHeight), 1);
  const selectedDef = selectedUnitId ? defsById[selectedUnitId] : null;

  return (
    <div className={cn("flex flex-col rounded-xl border border-slate-200 bg-white overflow-hidden", className)}>
      <div
        ref={containerRef}
        className="overflow-hidden min-h-[200px] max-h-[400px] cursor-grab active:cursor-grabbing"
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <svg
          viewBox={`0 0 ${viewW} ${viewH}`}
          className="w-full h-full block"
          style={{
            transform: `translate(${transform.tx}px, ${transform.ty}px) scale(${transform.scale})`,
            transformOrigin: "0 0",
          }}
        >
          {edges.map((e, i) => {
            const from = nodePos.pos[e.from];
            const to = nodePos.pos[e.to];
            if (!from || !to) return null;
            const isSelected = selectedEdge?.from === e.from && selectedEdge?.to === e.to;
            return (
              <line
                key={`${e.from}-${e.to}-${i}`}
                x1={from.x}
                y1={from.y}
                x2={to.x}
                y2={to.y}
                stroke="currentColor"
                strokeOpacity={isSelected ? 0.5 : 0.2}
                strokeWidth={isSelected ? 2 : 1}
                className="text-slate-300"
              />
            );
          })}
          {byGroup.map((col, ci) =>
            col.nodes.map((node, ni) => {
              const x = ci * colWidth + (colWidth - nodeWidth) / 2;
              const y = ni * rowHeight + (rowHeight - nodeHeight) / 2;
              const label =
                defsById[node.unit_id]?.name ?? KU_DISPLAY_NAMES[node.unit_id] ?? node.unit_id;
              const isSelected = selectedUnitId === node.unit_id;
              return (
                <g
                  key={node.unit_id}
                  onClick={() => setSelectedUnitId((id) => (id === node.unit_id ? null : node.unit_id))}
                  className="cursor-pointer"
                >
                  <rect
                    x={x}
                    y={y}
                    width={nodeWidth}
                    height={nodeHeight}
                    rx={6}
                    className={cn(
                      "stroke-[1.5] transition-colors duration-300",
                      statusRectStyles[node.status],
                      isSelected && "stroke-2 stroke-brand-500 ring-2 ring-brand-500/30"
                    )}
                  />
                  <text
                    x={x + nodeWidth / 2}
                    y={y + nodeHeight / 2}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className={cn("text-[11px] font-medium fill-current pointer-events-none", statusTextStyles[node.status])}
                  >
                    {label.length > 12 ? label.slice(0, 11) + "…" : label}
                  </text>
                </g>
              );
            })
          )}
        </svg>
      </div>
      {selectedDef && (
        <div className="border-t border-slate-200 p-3 bg-slate-50 dark:bg-slate-900/30 text-sm">
          <p className="font-medium text-slate-800 dark:text-slate-200">{selectedDef.name ?? selectedDef.id}</p>
          {selectedDef.description && (
            <p className="mt-1 text-slate-600 dark:text-slate-400">{selectedDef.description}</p>
          )}
          {selectedDef.prerequisites?.length ? (
            <p className="mt-1 text-xs text-slate-500">Prerequisites: {selectedDef.prerequisites.join(", ")}</p>
          ) : null}
          {selectedDef.example_correct_code && (
            <pre className="mt-2 rounded bg-slate-100 dark:bg-slate-800 p-2 text-xs overflow-x-auto">
              {selectedDef.example_correct_code}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
