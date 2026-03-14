import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export interface ComprehensiveReportItem {
  problem_id: string;
  passed: boolean;
  problem_statement: string;
}

interface ComprehensiveReportProps {
  totalRun: number;
  totalPassed: number;
  results: ComprehensiveReportItem[];
  overallSummary?: string;
}

const PASS_COLOR = "#10B981";
const FAIL_COLOR = "#EF4444";

export function ComprehensiveReport({
  totalRun,
  totalPassed,
  results,
  overallSummary,
}: ComprehensiveReportProps) {
  const pieData = [
    { name: "Passed", value: totalPassed, color: PASS_COLOR },
    { name: "Failed", value: totalRun - totalPassed, color: FAIL_COLOR },
  ];

  const barData = results.map((r) => ({
    problem_id: r.problem_id,
    passed: r.passed ? 1 : 0,
    failed: r.passed ? 0 : 1,
    fullLabel: r.problem_statement,
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-6">
        <div className="text-3xl font-bold text-slate-900">
          {totalPassed}/{totalRun}
        </div>
        <div className="h-20 w-20">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={22}
                outerRadius={32}
                paddingAngle={2}
                dataKey="value"
              >
                {pieData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>
        {overallSummary && (
          <p className="text-sm text-slate-600">{overallSummary}</p>
        )}
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={barData}
            layout="vertical"
            margin={{ top: 4, right: 16, left: 80, bottom: 4 }}
          >
            <XAxis type="number" domain={[0, 1]} tickFormatter={() => ""} />
            <YAxis type="category" dataKey="problem_id" width={76} tick={{ fontSize: 11 }} />
            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload?.length) return null;
                const d = payload[0].payload;
                return (
                  <div className="rounded-lg border border-slate-200 bg-white p-2 text-xs shadow-card">
                    <p className="font-mono text-slate-600">{d.problem_id}</p>
                    <p className="mt-1 text-slate-500">{d.fullLabel?.slice(0, 80)}...</p>
                    <p className={d.passed ? "text-success" : "text-danger"}>
                      {d.passed ? "PASS" : "FAIL"}
                    </p>
                  </div>
                );
              }}
            />
            <Bar dataKey="passed" stackId="a" fill={PASS_COLOR} name="Passed" radius={[0, 2, 2, 0]} />
            <Bar dataKey="failed" stackId="a" fill={FAIL_COLOR} name="Failed" radius={[0, 2, 2, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
