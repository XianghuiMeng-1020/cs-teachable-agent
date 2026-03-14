import { useMemo } from "react";
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
  prerequisites?: string[];
  topic_group?: string;
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

  return (
    <div className={cn("overflow-auto rounded-xl border border-slate-200 bg-white p-4", className)}>
      <svg
        viewBox={`0 0 ${byGroup.length * colWidth} ${Math.max(...byGroup.map((c) => c.nodes.length * rowHeight), 1)}`}
        className="w-full min-h-[200px]"
        style={{ maxHeight: "400px" }}
      >
        {edges.map((e, i) => {
          const from = nodePos.pos[e.from];
          const to = nodePos.pos[e.to];
          if (!from || !to) return null;
          return (
            <line
              key={`${e.from}-${e.to}-${i}`}
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke="currentColor"
              strokeOpacity={0.2}
              strokeWidth={1}
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
            return (
              <g key={node.unit_id}>
                <rect
                  x={x}
                  y={y}
                  width={nodeWidth}
                  height={nodeHeight}
                  rx={6}
                  className={cn("stroke-[1.5] transition-colors duration-300", statusRectStyles[node.status])}
                />
                <text
                  x={x + nodeWidth / 2}
                  y={y + nodeHeight / 2}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className={cn("text-[11px] font-medium fill-current", statusTextStyles[node.status])}
                >
                  {label.length > 12 ? label.slice(0, 11) + "…" : label}
                </text>
              </g>
            );
          })
        )}
      </svg>
    </div>
  );
}
