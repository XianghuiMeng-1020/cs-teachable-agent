import { useMemo } from "react";
import { cn } from "@/lib/utils";
import { KU_DISPLAY_NAMES } from "@/lib/constants";

export type UnitStatus = "unknown" | "partially_learned" | "learned" | "misconception" | "corrected";

export interface UnitNode {
  unit_id: string;
  status: UnitStatus;
  topic_group?: string;
}

const TOPIC_ORDER = [
  "variables",
  "io",
  "types",
  "operators",
  "conditionals",
  "loops",
  "lists",
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
  className?: string;
}

export function KnowledgeGraph({ units, className }: KnowledgeGraphProps) {
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

  const colWidth = 90;
  const rowHeight = 44;
  const nodeWidth = 64;
  const nodeHeight = 32;

  return (
    <div className={cn("overflow-auto rounded-xl border border-slate-200 bg-white p-4", className)}>
      <svg
        viewBox={`0 0 ${byGroup.length * colWidth} ${Math.max(...byGroup.map((c) => c.nodes.length * rowHeight), 1)}`}
        className="w-full min-h-[200px]"
        style={{ maxHeight: "400px" }}
      >
        {byGroup.map((col, ci) =>
          col.nodes.map((node, ni) => {
            const x = ci * colWidth + (colWidth - nodeWidth) / 2;
            const y = ni * rowHeight + (rowHeight - nodeHeight) / 2;
            const label = KU_DISPLAY_NAMES[node.unit_id] ?? node.unit_id;
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
