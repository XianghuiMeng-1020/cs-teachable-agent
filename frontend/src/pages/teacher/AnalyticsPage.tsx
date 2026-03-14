import { useQuery } from "@tanstack/react-query";
import { teacherAnalytics, teacherStudents } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { MasteryHeatmap } from "@/components/teacher/MasteryHeatmap";
import { MisconceptionRanking } from "@/components/teacher/MisconceptionRanking";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { KU_DISPLAY_NAMES } from "@/lib/constants";
import { Download } from "lucide-react";

export function AnalyticsPage() {
  const { data: analytics } = useQuery({ queryKey: ["teacher", "analytics"], queryFn: teacherAnalytics });
  const { data: students = [] } = useQuery({ queryKey: ["teacher", "students"], queryFn: teacherStudents });

  const coverage = analytics?.knowledge_coverage ?? [];
  const kus = [...new Set(coverage.map((c: { unit_id: string }) => c.unit_id))].slice(0, 20);
  const rows = students.map((s: { user_id: number; username: string }) => ({ studentId: s.user_id, studentName: s.username }));

  const statusMap = new Map<string, string>();
  for (const s of analytics?.student_unit_status ?? []) {
    statusMap.set(`${(s as { user_id: number; unit_id: string }).user_id}:${(s as { unit_id: string }).unit_id}`, (s as { status: string }).status);
  }
  const getCell = (studentId: number, unitId: string): "not_learned" | "partially" | "learned" | "proficient" | "misconception" => {
    const status = statusMap.get(`${studentId}:${unitId}`);
    if (status === "learned" || status === "partially_learned") return "learned";
    if (status === "misconception") return "misconception";
    if (status === "corrected") return "partially";
    return "not_learned";
  };

  const radarData = kus.slice(0, 6).map((uid) => ({
    subject: KU_DISPLAY_NAMES[uid] ?? uid,
    value: (() => {
      const c = coverage.find((x: { unit_id: string }) => x.unit_id === uid);
      return c && c.total_students ? Math.round((c.students_learned / c.total_students) * 100) : 0;
    })(),
    fullMark: 100,
  }));

  const trendData = (analytics?.mastery_trend ?? []).map((d: { date?: string; avg_mastery?: number }) => ({
    date: d.date ?? "",
    mastery: typeof d.avg_mastery === "number" ? Math.round(d.avg_mastery * 100) : 0,
  }));

  const handleExport = () => {
    const payload = {
      exported_at: new Date().toISOString(),
      student_count: analytics?.student_count,
      avg_mastery: analytics?.avg_mastery,
      knowledge_coverage: analytics?.knowledge_coverage,
      mastery_trend: analytics?.mastery_trend,
      active_misconception_counts: analytics?.active_misconception_counts,
      student_unit_status: analytics?.student_unit_status,
      recent_activity: analytics?.recent_activity,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `analytics-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
        <Button variant="secondary" icon={Download} onClick={handleExport}>
          Export data (JSON)
        </Button>
      </div>

      <Card padding="md">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Mastery heatmap (KU × Student)</h2>
        <MasteryHeatmap rows={rows} columns={kus} getCell={getCell} className="min-h-[300px]" />
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Misconception ranking</h2>
          <MisconceptionRanking counts={analytics?.active_misconception_counts ?? {}} />
        </Card>
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Teaching coverage</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name="Coverage" dataKey="value" stroke="#6366F1" fill="#6366F1" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {trendData.length > 0 && (
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Mastery trend (last 7 days)</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(v: number) => [`${v}%`, "Avg mastery"]} />
                <Line type="monotone" dataKey="mastery" stroke="#6366F1" strokeWidth={2} dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {(analytics?.recent_activity?.length ?? 0) > 0 && (
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Recent activity</h2>
          <ul className="space-y-2">
            {(analytics?.recent_activity ?? []).slice(0, 10).map((a: { student?: string; action?: string; result?: string; timestamp?: string }, i: number) => (
              <li key={i} className="flex flex-wrap items-center gap-2 rounded-lg border border-slate-100 px-3 py-2 text-sm">
                <span className="font-medium text-slate-800">{a.student}</span>
                <span className="text-slate-600">{a.action}</span>
                {a.result != null && <span className="text-slate-500">{a.result}</span>}
                <span className="ml-auto text-xs text-slate-400">{a.timestamp ?? ""}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
