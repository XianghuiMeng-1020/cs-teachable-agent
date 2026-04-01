import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { teacherAnalytics } from "@/api/client";
import { Users, BookOpen, AlertTriangle, MessageSquare } from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { ActivityFeed } from "@/components/teacher/ActivityFeed";
import { MisconceptionRanking } from "@/components/teacher/MisconceptionRanking";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export function OverviewPage() {
  const { t } = useTranslation();
  const { data: analytics, isLoading } = useQuery({
    queryKey: ["teacher", "analytics"],
    queryFn: teacherAnalytics,
  });

  const trendData = (analytics?.mastery_trend ?? []).map((d: { date: string; avg_mastery: number }) => ({
    date: d.date,
    mastery: Math.round((d.avg_mastery ?? 0) * 100),
  }));

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">{t("nav.overview")}</h1>
        <p className="mt-1 text-stone-500">{t("teacher.overviewDesc")}</p>
      </div>

      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        <StatCard
          label={t("teacher.totalStudents")}
          value={analytics?.student_count ?? 0}
          icon={Users}
          iconColor="bg-brand-50 text-brand-700"
          loading={isLoading}
        />
        <StatCard
          label={t("teacher.avgMastery")}
          value={analytics?.avg_mastery != null ? `${Math.round(analytics.avg_mastery * 100)}%` : "—"}
          icon={BookOpen}
          iconColor="bg-emerald-50 text-emerald-700"
          loading={isLoading}
        />
        <StatCard
          label={t("teacher.activeMisconceptions")}
          value={Object.values(analytics?.active_misconception_counts ?? {}).reduce((a, b) => a + b, 0) || 0}
          icon={AlertTriangle}
          iconColor="bg-amber-50 text-amber-700"
          loading={isLoading}
        />
        <StatCard
          label={t("teacher.sessionsToday")}
          value={analytics?.sessions_today ?? 0}
          icon={MessageSquare}
          iconColor="bg-sky-50 text-sky-700"
          loading={isLoading}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="font-serif text-heading text-stone-900 mb-4">{t("teacher.masteryTrend")}</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E7E5E4" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#78716C" }} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#78716C" }} axisLine={false} tickLine={false} />
                <Tooltip
                  formatter={(v: number) => [`${v}%`, t("nav.mastery")]}
                  contentStyle={{ borderRadius: "8px", border: "1px solid #E7E5E4", fontSize: "12px" }}
                />
                <Line type="monotone" dataKey="mastery" stroke="#0D9488" strokeWidth={2} dot={{ r: 3, fill: "#0D9488" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card padding="md">
          <h2 className="font-serif text-heading text-stone-900 mb-4">{t("teacher.misconceptionRanking")}</h2>
          <MisconceptionRanking counts={analytics?.active_misconception_counts ?? {}} />
        </Card>
      </div>

      <Card padding="md">
        <h2 className="font-serif text-heading text-stone-900 mb-4">{t("teacher.recentActivity")}</h2>
        <ActivityFeed items={analytics?.recent_activity ?? []} />
      </Card>
    </div>
  );
}
