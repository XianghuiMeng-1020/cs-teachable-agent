import { useQuery } from "@tanstack/react-query";
import { ResponsiveContainer, Tooltip, PieChart, Pie, Cell } from "recharts";
import { ClipboardList, Users, Target, TrendingUp, Loader2 } from "lucide-react";
import { getTeacherAssessmentOverview, listAssessmentItems } from "@/api/assessment";
import { Card } from "@/components/ui/Card";
import { cn } from "@/lib/utils";

const TYPE_COLORS: Record<string, string> = {
  parsons: "#7C3AED",
  dropdown: "#0284C7",
  "execution-trace": "#059669",
};

const TYPE_LABELS: Record<string, string> = {
  parsons: "Parsons",
  dropdown: "Dropdown",
  "execution-trace": "Exec Trace",
};

function StatBox({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <Card padding="md">
      <div className="flex items-center gap-2.5 mb-2">
        {icon}
        <span className="text-xs font-medium text-stone-500">{label}</span>
      </div>
      <div className="text-2xl font-bold text-stone-900">{value}</div>
    </Card>
  );
}

export function AssessmentManagePage() {
  const { data: overview, isLoading } = useQuery({
    queryKey: ["teacher", "assessment", "overview"],
    queryFn: getTeacherAssessmentOverview,
  });

  const { data: itemsData } = useQuery({
    queryKey: ["assessment", "items", "all"],
    queryFn: () => listAssessmentItems({ limit: 200 }),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="h-7 w-7 animate-spin text-brand-600" />
      </div>
    );
  }

  const stats = overview as Record<string, unknown> | undefined;
  const totalItems = Number(stats?.total_items ?? 0);
  const totalAttempts = Number(stats?.total_attempts ?? 0);
  const overallAccuracy = Number(stats?.overall_accuracy ?? 0);
  const uniqueStudents = Number(stats?.unique_students ?? 0);
  const itemsByType = (stats?.items_by_type as Record<string, number>) ?? {};
  const hardestItems = (stats?.hardest_items as Array<Record<string, unknown>>) ?? [];

  const pieData = Object.entries(itemsByType).map(([type, count]) => ({
    name: TYPE_LABELS[type] || type,
    value: count,
    color: TYPE_COLORS[type] || "#A8A29E",
  }));

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">Assessments</h1>
        <p className="mt-1 text-stone-500">Item management and performance overview</p>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <StatBox icon={<ClipboardList className="h-5 w-5 text-brand-600" />} label="Total Items" value={totalItems} />
        <StatBox icon={<Users className="h-5 w-5 text-sky-600" />} label="Students" value={uniqueStudents} />
        <StatBox icon={<Target className="h-5 w-5 text-emerald-600" />} label="Attempts" value={totalAttempts} />
        <StatBox icon={<TrendingUp className="h-5 w-5 text-amber-600" />} label="Accuracy" value={`${Math.round(overallAccuracy * 100)}%`} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h3 className="font-serif text-heading text-stone-900 mb-4">Items by Type</h3>
          {pieData.length > 0 ? (
            <div className="h-[220px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={75}
                    innerRadius={40}
                    label={({ name, value }) => `${name}: ${value}`}
                    labelLine={{ stroke: "#A8A29E" }}
                  >
                    {pieData.map((entry, i) => (
                      <Cell key={`cell-${i}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid #E7E5E4", fontSize: "12px" }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-sm text-stone-400 py-8 text-center">No items yet</p>
          )}
        </Card>

        <Card padding="md">
          <h3 className="font-serif text-heading text-stone-900 mb-4">Hardest Items</h3>
          {hardestItems.length === 0 ? (
            <p className="text-sm text-stone-400 py-8 text-center">No attempt data yet</p>
          ) : (
            <div className="space-y-2 max-h-[240px] overflow-y-auto">
              {hardestItems.map((item, i) => (
                <div key={i} className="flex items-center justify-between rounded-lg border border-stone-100 px-3.5 py-2.5">
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-medium text-stone-800 truncate">{String(item.title)}</div>
                    <div className="mt-0.5 flex items-center gap-2 text-xs text-stone-500">
                      <span className={cn(
                        "rounded-md px-1.5 py-0.5 text-[10px] font-medium",
                        String(item.item_type) === "parsons" ? "bg-violet-50 text-violet-700" :
                        String(item.item_type) === "dropdown" ? "bg-sky-50 text-sky-700" :
                        "bg-emerald-50 text-emerald-700"
                      )}>
                        {TYPE_LABELS[String(item.item_type)] || String(item.item_type)}
                      </span>
                      <span>{Number(item.attempts)} attempts</span>
                    </div>
                  </div>
                  <div className="text-right shrink-0 ml-3">
                    <div className="text-sm font-bold text-stone-900">
                      {Math.round(Number(item.pass_rate) * 100)}%
                    </div>
                    <div className="text-[10px] text-stone-400">pass rate</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Items table */}
      <Card padding="md">
        <h3 className="font-serif text-heading text-stone-900 mb-4">
          All Items
          <span className="ml-2 text-sm font-normal text-stone-400">({itemsData?.total ?? 0})</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-100 text-left">
                <th className="pb-3 text-xs font-semibold text-stone-500">Title</th>
                <th className="pb-3 text-xs font-semibold text-stone-500">Type</th>
                <th className="pb-3 text-xs font-semibold text-stone-500">Theme</th>
                <th className="pb-3 text-xs font-semibold text-stone-500">Concepts</th>
                <th className="pb-3 text-xs font-semibold text-stone-500 text-right">AI Pass Rate</th>
              </tr>
            </thead>
            <tbody>
              {(itemsData?.items ?? []).map((item) => (
                <tr key={item.id} className="border-b border-stone-50 hover:bg-stone-50 transition-colors">
                  <td className="py-3 pr-3 font-medium text-stone-800 max-w-[220px] truncate">
                    {item.title}
                  </td>
                  <td className="py-3 pr-3">
                    <span className={cn(
                      "rounded-md px-2 py-0.5 text-[11px] font-medium",
                      item.item_type === "parsons" ? "bg-violet-50 text-violet-700" :
                      item.item_type === "dropdown" ? "bg-sky-50 text-sky-700" :
                      "bg-emerald-50 text-emerald-700"
                    )}>
                      {TYPE_LABELS[item.item_type] || item.item_type}
                    </span>
                  </td>
                  <td className="py-3 pr-3 text-stone-500">{item.theme || "—"}</td>
                  <td className="py-3 pr-3">
                    <div className="flex gap-1 flex-wrap max-w-[200px]">
                      {(item.concepts ?? []).slice(0, 2).map((c) => (
                        <span key={c} className="rounded-md bg-stone-100 px-1.5 py-0.5 text-[10px] font-medium text-stone-600">{c}</span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 text-right text-stone-600">
                    {item.ai_pass_rate != null ? `${Math.round(item.ai_pass_rate)}%` : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
