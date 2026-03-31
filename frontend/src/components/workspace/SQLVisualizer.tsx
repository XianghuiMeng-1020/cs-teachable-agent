import { useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";
import { cn } from "@/lib/utils";

export interface SQLVisualizerProps {
  /** Column names */
  columns: string[];
  /** Row data: array of objects with column keys */
  rows: Record<string, unknown>[];
  /** Show bar chart for first numeric column (if any) */
  showChart?: boolean;
  className?: string;
}

export function SQLVisualizer({ columns, rows, showChart = false, className }: SQLVisualizerProps) {
  const chartData = useMemo(() => {
    if (!showChart || columns.length === 0 || rows.length === 0) return [];
    const firstCol = columns[0];
    const secondCol = columns[1];
    const numericCol = [firstCol, secondCol].find((c) => {
      const val = rows[0]?.[c];
      return typeof val === "number" || (typeof val === "string" && !Number.isNaN(Number(val)));
    });
    if (!numericCol) return [];
    return rows.slice(0, 20).map((r) => ({
      name: String(r[columns[0]] ?? ""),
      value: Number(r[numericCol]) || 0,
    }));
  }, [columns, rows, showChart]);

  if (columns.length === 0) {
    return (
      <div className={cn("rounded-lg border border-stone-200 bg-stone-50 p-4 text-sm text-stone-500", className)}>
        No result set to display.
      </div>
    );
  }

  return (
    <div className={cn("space-y-3", className)}>
      <div className="overflow-x-auto rounded-lg border border-stone-200">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-stone-200 bg-stone-50">
              {columns.map((col) => (
                <th key={col} className="px-3 py-2 font-medium text-stone-700">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 50).map((row, i) => (
              <tr key={i} className="border-b border-stone-100 last:border-0">
                {columns.map((col) => (
                  <td key={col} className="px-3 py-2 font-mono text-stone-800">
                    {row[col] != null ? String(row[col]) : "NULL"}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length > 50 && (
          <p className="px-3 py-2 text-xs text-stone-500">Showing first 50 of {rows.length} rows.</p>
        )}
      </div>
      {showChart && chartData.length > 0 && (
        <div className="h-[160px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
              <XAxis dataKey="name" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 10 }} width={32} />
              <Tooltip />
              <Bar dataKey="value" fill="#0D9488" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
