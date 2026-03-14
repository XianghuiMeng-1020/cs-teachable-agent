import { useQuery } from "@tanstack/react-query";
import { teacherAnalytics } from "@/api/client";
import { Users, BookOpen, AlertTriangle, MessageSquare } from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { ActivityFeed } from "@/components/teacher/ActivityFeed";
import { MisconceptionRanking } from "@/components/teacher/MisconceptionRanking";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export function OverviewPage() {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ["teacher", "analytics"],
    queryFn: teacherAnalytics,
  });

  const trendData = (analytics?.mastery_trend ?? []).map((d: { date: string; avg_mastery: number }) => ({
    date: d.date,
    mastery: Math.round((d.avg_mastery ?? 0) * 100),
  }));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Overview</h1>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Total Students"
          value={analytics?.student_count ?? 0}
          icon={Users}
          iconColor="bg-brand-50 text-brand-500"
          loading={isLoading}
        />
        <StatCard
          label="Avg Mastery"
          value={analytics?.avg_mastery != null ? `${Math.round(analytics.avg_mastery * 100)}%` : "—"}
          icon={BookOpen}
          iconColor="bg-emerald-50 text-success"
          loading={isLoading}
        />
        <StatCard
          label="Active Misconceptions"
          value={Object.values(analytics?.active_misconception_counts ?? {}).reduce((a, b) => a + b, 0) || 0}
          icon={AlertTriangle}
          iconColor="bg-amber-50 text-warning"
          loading={isLoading}
        />
        <StatCard
          label="Sessions Today"
          value="—"
          icon={MessageSquare}
          iconColor="bg-accent-50 text-accent-500"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Mastery trend</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v: number) => [`${v}%`, "Mastery"]} />
                <Line type="monotone" dataKey="mastery" stroke="#06B6D4" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Misconception ranking</h2>
          <MisconceptionRanking counts={analytics?.active_misconception_counts ?? {}} />
        </Card>
      </div>

      <Card padding="md">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Recent activity</h2>
        <ActivityFeed items={analytics?.recent_activity ?? []} />
      </Card>
    </div>
  );
}
