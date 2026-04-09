import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { teacherAnalytics, teacherStudents } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { MasteryHeatmap } from "@/components/teacher/MasteryHeatmap";
import { MisconceptionRanking } from "@/components/teacher/MisconceptionRanking";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { KU_DISPLAY_NAMES } from "@/lib/constants";
import { Download, RefreshCw, AlertCircle, FileSpreadsheet } from "lucide-react";
import { useState } from "react";

type ExportFormat = "json" | "csv";

export function AnalyticsPage() {
  const { t } = useTranslation();
  const [exportFormat, setExportFormat] = useState<ExportFormat>("json");
  
  // M-28: Add skeleton loading, error handling, and M-33: real-time refresh (30s polling)
  const { 
    data: analytics, 
    isLoading, 
    isError, 
    refetch,
    isFetching 
  } = useQuery({ 
    queryKey: ["teacher", "analytics"], 
    queryFn: teacherAnalytics,
    refetchInterval: 30000, // 30s polling for near real-time
    staleTime: 10000,
  });
  const { 
    data: students = [],
    isLoading: isLoadingStudents,
    isError: isStudentsError,
    refetch: refetchStudents 
  } = useQuery({ 
    queryKey: ["teacher", "students"], 
    queryFn: teacherStudents,
    refetchInterval: 30000,
    staleTime: 10000,
  });

  // M-28: Error state with retry
  if (isError || isStudentsError) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-stone-900">{t("teacher.analyticsTitle")}</h1>
        <Card padding="lg" className="text-center py-12">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-stone-900 mb-2">
            {t("teacher.loadError", { defaultValue: "加载数据时出错" })}
          </h2>
          <p className="text-stone-500 mb-6">
            {t("teacher.loadErrorDesc", { defaultValue: "无法获取分析数据，请稍后重试" })}
          </p>
          <div className="flex justify-center gap-3">
            <Button onClick={() => refetch()} icon={RefreshCw}>
              {t("common.retry", { defaultValue: "重试" })}
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  // M-29: Sort KUs alphabetically for stable column order
  const coverage = analytics?.knowledge_coverage ?? [];
  const kus = [...new Set(coverage.map((c: { unit_id: string }) => c.unit_id))]
    .sort((a, b) => (KU_DISPLAY_NAMES[a] ?? a).localeCompare(KU_DISPLAY_NAMES[b] ?? b))
    .slice(0, 20);
  const rows = students.map((s: { user_id: number; username: string }) => ({ studentId: s.user_id, studentName: s.username }));

  const statusMap = new Map<string, string>();
  for (const s of analytics?.student_unit_status ?? []) {
    statusMap.set(`${(s as { user_id: number; unit_id: string }).user_id}:${(s as { unit_id: string }).unit_id}`, (s as { status: string }).status);
  }
  // M-30: Distinguish partially_learned from learned
  const getCell = (studentId: number, unitId: string): "not_learned" | "partially" | "learned" | "proficient" | "misconception" => {
    const status = statusMap.get(`${studentId}:${unitId}`);
    if (status === "learned") return "learned";
    if (status === "partially_learned") return "partially";
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

  // M-31: Export in JSON or CSV format
  const handleExport = () => {
    const dateStr = new Date().toISOString().slice(0, 10);
    
    if (exportFormat === "csv") {
      // Generate CSV export
      const headers = ["Student ID", "Student Name", "Knowledge Unit", "Status"];
      const rows_data: string[][] = [];
      
      for (const student of students) {
        for (const ku of kus) {
          const status = statusMap.get(`${student.user_id}:${ku}`) || "not_learned";
          rows_data.push([
            String(student.user_id),
            student.username,
            KU_DISPLAY_NAMES[ku] ?? ku,
            status,
          ]);
        }
      }
      
      const csvContent = [
        headers.join(","),
        ...rows_data.map((row) => 
          row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(",")
        ),
      ].join("\n");
      
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `analytics-export-${dateStr}.csv`;
      a.click();
      URL.revokeObjectURL(a.href);
    } else {
      // JSON export (default)
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
      a.download = `analytics-export-${dateStr}.json`;
      a.click();
      URL.revokeObjectURL(a.href);
    }
  };

  // M-28: Skeleton loading state
  if (isLoading || isLoadingStudents) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-10 w-32" />
        </div>
        <Card padding="md">
          <Skeleton className="h-6 w-32 mb-4" />
          <Skeleton className="h-[300px] w-full" />
        </Card>
        <div className="grid gap-6 lg:grid-cols-2">
          <Card padding="md">
            <Skeleton className="h-6 w-40 mb-4" />
            <Skeleton className="h-48 w-full" />
          </Card>
          <Card padding="md">
            <Skeleton className="h-6 w-40 mb-4" />
            <Skeleton className="h-48 w-full" />
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-stone-900">{t("teacher.analyticsTitle")}</h1>
        <div className="flex items-center gap-2">
          {/* M-31: Export format selector */}
          <div className="flex bg-stone-100 rounded-lg p-1 mr-2">
            <button
              onClick={() => setExportFormat("json")}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                exportFormat === "json" 
                  ? "bg-white text-stone-900 shadow-sm" 
                  : "text-stone-500 hover:text-stone-700"
              }`}
            >
              JSON
            </button>
            <button
              onClick={() => setExportFormat("csv")}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors flex items-center gap-1 ${
                exportFormat === "csv" 
                  ? "bg-white text-stone-900 shadow-sm" 
                  : "text-stone-500 hover:text-stone-700"
              }`}
            >
              <FileSpreadsheet className="w-3 h-3" />
              CSV
            </button>
          </div>
          <Button 
            variant="secondary" 
            icon={isFetching ? RefreshCw : Download} 
            onClick={handleExport}
            disabled={isFetching}
          >
            {isFetching ? t("common.loading", { defaultValue: "加载中..." }) : t("teacher.exportData")}
          </Button>
        </div>
      </div>

      <Card padding="md">
        <h2 className="mb-4 text-lg font-semibold text-stone-800">{t("teacher.masteryHeatmap")}</h2>
        <MasteryHeatmap rows={rows} columns={kus} getCell={getCell} className="min-h-[300px]" />
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-stone-800">{t("teacher.misconceptionRanking")}</h2>
          <MisconceptionRanking counts={analytics?.active_misconception_counts ?? {}} />
        </Card>
        <Card padding="md">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-stone-800">{t("teacher.teachingCoverage")}</h2>
            {/* M-32: Truncation notice for radar chart */}
            {kus.length > 6 && (
              <span className="text-xs text-stone-500">
                {t("teacher.showingFirstN", { n: 6, total: kus.length, defaultValue: `显示前6项（共${kus.length}项）` })}
              </span>
            )}
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name={t("teacher.teachingCoverage")} dataKey="value" stroke="#0D9488" fill="#0D9488" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {trendData.length > 0 && (
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-stone-800">{t("teacher.masteryTrendDays")}</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(v: number) => [`${v}%`, t("teacher.avgMasteryLabel")]} />
                <Line type="monotone" dataKey="mastery" stroke="#0D9488" strokeWidth={2} dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {(analytics?.recent_activity?.length ?? 0) > 0 && (
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-stone-800">{t("teacher.recentActivity")}</h2>
          <ul className="space-y-2">
            {(analytics?.recent_activity ?? []).slice(0, 10).map((a: { student?: string; action?: string; result?: string; timestamp?: string }, i: number) => (
              <li key={i} className="flex flex-wrap items-center gap-2 rounded-lg border border-stone-100 px-3 py-2 text-sm">
                <span className="font-medium text-stone-800">{a.student}</span>
                <span className="text-stone-600">{a.action}</span>
                {a.result != null && <span className="text-stone-500">{a.result}</span>}
                <span className="ml-auto text-xs text-stone-400">{a.timestamp ?? ""}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
