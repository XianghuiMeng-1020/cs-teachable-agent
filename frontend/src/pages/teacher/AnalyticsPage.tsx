import { useQuery } from "@tanstack/react-query";
import { teacherAnalytics, teacherStudents } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { MasteryHeatmap } from "@/components/teacher/MasteryHeatmap";
import { MisconceptionRanking } from "@/components/teacher/MisconceptionRanking";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from "recharts";
import { KU_DISPLAY_NAMES } from "@/lib/constants";

export function AnalyticsPage() {
  const { data: analytics } = useQuery({ queryKey: ["teacher", "analytics"], queryFn: teacherAnalytics });
  const { data: students = [] } = useQuery({ queryKey: ["teacher", "students"], queryFn: teacherStudents });

  const coverage = analytics?.knowledge_coverage ?? [];
  const kus = [...new Set(coverage.map((c: { unit_id: string }) => c.unit_id))].slice(0, 20);
  const rows = students.map((s: { user_id: number; username: string }) => ({ studentId: s.user_id, studentName: s.username }));

  const getCell = (_studentId: number, _unitId: string): "not_learned" | "partially" | "learned" | "proficient" | "misconception" => {
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

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>

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
    </div>
  );
}
