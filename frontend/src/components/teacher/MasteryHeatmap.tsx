import { useMemo } from "react";

export interface HeatmapCell {
  studentId: number;
  studentName: string;
  unitId: string;
  status: "not_learned" | "partially" | "learned" | "proficient" | "misconception";
}

const statusColors: Record<HeatmapCell["status"], string> = {
  not_learned: "#F1F5F9",
  partially: "#FEF3C7",
  learned: "#D1FAE5",
  proficient: "#059669",
  misconception: "#FCA5A5",
};

interface MasteryHeatmapProps {
  rows: { studentId: number; studentName: string }[];
  columns: string[];
  getCell: (studentId: number, unitId: string) => HeatmapCell["status"];
  className?: string;
}

export function MasteryHeatmap({ rows, columns, getCell, className = "" }: MasteryHeatmapProps) {
  return (
    <div className={`overflow-auto rounded-xl border border-stone-200 bg-white p-4 ${className}`}>
      <div className="inline-block min-w-full">
        <table className="w-full text-xs">
          <thead>
            <tr>
              <th className="sticky left-0 z-10 border-b border-r border-stone-200 bg-stone-50 px-2 py-2 text-left font-medium text-stone-600">Student</th>
              {columns.map((col) => (
                <th key={col} className="border-b border-stone-200 px-1 py-2 font-medium text-stone-600" style={{ transform: "rotate(-45deg)", whiteSpace: "nowrap", width: 24 }}>
                  {col.length > 8 ? col.slice(0, 7) + "…" : col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.studentId}>
                <td className="sticky left-0 z-10 border-r border-stone-100 bg-white py-1 font-medium text-stone-700">{row.studentName}</td>
                {columns.map((unitId) => {
                  const status = getCell(row.studentId, unitId);
                  return (
                    <td key={unitId} className="border-b border-stone-100 p-0.5">
                      <div
                        className="h-5 w-5 rounded-sm"
                        style={{ backgroundColor: statusColors[status] }}
                        title={`${row.studentName} — ${unitId}: ${status}`}
                      />
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
