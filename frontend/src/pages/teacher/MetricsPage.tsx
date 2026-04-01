import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { BarChart3, Activity, ShieldCheck, Zap, Database, Target, PieChart, Layers } from "lucide-react";
import { cn } from "@/lib/utils";
import { getMetricsDashboard, type MetricsDashboardData } from "@/api/assessment";
import { Card } from "@/components/ui/Card";

function formatPercent(v: number | null): string {
  if (v == null || Number.isNaN(v)) return "—";
  return `${v.toFixed(1)}%`;
}

function barW(value: number, max: number): string {
  if (max <= 0) return "0%";
  return `${Math.min((value / max) * 100, 100)}%`;
}

const TYPE_COLORS: Record<string, { bg: string; text: string; bar: string }> = {
  parsons: { bg: "bg-violet-50", text: "text-violet-700", bar: "bg-violet-500" },
  dropdown: { bg: "bg-sky-50", text: "text-sky-700", bar: "bg-sky-500" },
  execution_trace: { bg: "bg-emerald-50", text: "text-emerald-700", bar: "bg-emerald-500" },
};

function StatBox({ label, value, helper, icon: Icon }: { label: string; value: string; helper?: string; icon: React.ElementType }) {
  return (
    <Card padding="md">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wider text-stone-400">{label}</p>
          <p className="mt-1 text-2xl font-bold text-stone-900">{value}</p>
          {helper && <p className="mt-0.5 text-xs text-stone-500">{helper}</p>}
        </div>
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50">
          <Icon className="h-4.5 w-4.5 text-brand-700" />
        </div>
      </div>
    </Card>
  );
}

export function MetricsPage() {
  const { t } = useTranslation();
  const [data, setData] = useState<MetricsDashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  const itemTypeLabel = (itemType: string) => {
    if (itemType === "execution_trace" || itemType === "execution-trace") return t("practice.executionTrace");
    if (itemType === "parsons") return t("practice.parsons");
    if (itemType === "dropdown") return t("teacher.typeDropdown", { defaultValue: "Dropdown" });
    return itemType.charAt(0).toUpperCase() + itemType.slice(1);
  };

  useEffect(() => {
    getMetricsDashboard()
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-24 animate-pulse rounded-xl bg-stone-100" />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <Card padding="lg" className="text-center py-12">
        <BarChart3 className="mx-auto h-10 w-10 text-stone-300" />
        <p className="mt-3 text-sm font-medium text-stone-500">{t("teacher.unableToLoadMetrics")}</p>
      </Card>
    );
  }

  const { totals, type_overview, ai_pass_distribution, theme_overview, telemetry } = data;
  const maxTypeItems = Math.max(...type_overview.map((row) => row.total_items), 1);
  const maxBucketTotal = Math.max(
    ...ai_pass_distribution.map((b) => b.parsons + b.dropdown + b.execution_trace),
    1
  );
  const maxThemeItems = Math.max(...theme_overview.map((row) => row.total_items), 1);
  const maxEventCount = telemetry.available
    ? Math.max(...telemetry.event_breakdown.map((e) => e.count), 1)
    : 1;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">{t("teacher.metricsTitle")}</h1>
        <p className="mt-1 text-stone-500">{t("teacher.metricsDesc")}</p>
      </div>

      {/* Top stats */}
      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        <StatBox
          label={t("teacher.inventory")}
          value={String(totals.total_items)}
          helper={t("teacher.evaluated", { count: totals.evaluated_items })}
          icon={Database}
        />
        <StatBox
          label={t("teacher.lowAiItems")}
          value={String(totals.low_ai_items)}
          helper={t("teacher.lowAiHint")}
          icon={ShieldCheck}
        />
        <StatBox
          label={t("teacher.avgAiPass")}
          value={formatPercent(totals.avg_ai_pass_rate)}
          helper={t("teacher.studentAttempts", { count: totals.total_attempts })}
          icon={Target}
        />
        <StatBox
          label={t("teacher.telemetry")}
          value={String(totals.telemetry_events)}
          helper={t("teacher.focusExits", { count: telemetry.focus_loss_count })}
          icon={Activity}
        />
      </div>

      {/* Type overview + AI pass buckets */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Item type mix */}
        <Card padding="md">
          <div className="flex items-center gap-2 mb-4">
            <PieChart className="h-4 w-4 text-brand-700" />
            <h2 className="font-serif text-heading text-stone-900">{t("teacher.itemTypeMix")}</h2>
          </div>
          <div className="space-y-3">
            {type_overview.map((row) => {
              const colors = TYPE_COLORS[row.item_type] ?? TYPE_COLORS.parsons;
              const evalShare = row.total_items > 0 ? (row.evaluated_items / row.total_items) * 100 : 0;
              return (
                <div key={row.item_type} className="rounded-lg border border-stone-100 p-3">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className={cn("rounded-md px-2 py-0.5 text-[11px] font-medium", colors.bg, colors.text)}>
                        {itemTypeLabel(row.item_type)}
                      </span>
                      <span className="text-xs text-stone-500">
                        {row.total_items} {t("teacher.items")}
                      </span>
                    </div>
                    <span className="text-xs font-semibold text-stone-700">
                      AI {formatPercent(row.avg_ai_pass_rate)}
                    </span>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <span className="w-10 text-[10px] text-stone-400">{t("teacher.load")}</span>
                      <div className="flex-1 h-2 rounded-full bg-stone-100 overflow-hidden">
                        <div className={cn("h-full rounded-full", colors.bar)} style={{ width: barW(row.total_items, maxTypeItems) }} />
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="w-10 text-[10px] text-stone-400">{t("teacher.eval")}</span>
                      <div className="flex-1 h-2 rounded-full bg-stone-100 overflow-hidden">
                        <div className="h-full rounded-full bg-brand-500" style={{ width: `${evalShare}%` }} />
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Card>

        {/* AI pass buckets */}
        <Card padding="md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Layers className="h-4 w-4 text-brand-700" />
              <h2 className="font-serif text-heading text-stone-900">{t("teacher.aiPassBuckets")}</h2>
            </div>
            <div className="flex gap-2">
              <span className="rounded-md bg-violet-50 px-2 py-0.5 text-[10px] font-medium text-violet-600">{t("practice.parsons")}</span>
              <span className="rounded-md bg-sky-50 px-2 py-0.5 text-[10px] font-medium text-sky-600">{t("teacher.typeDropdown", { defaultValue: "Dropdown" })}</span>
              <span className="rounded-md bg-emerald-50 px-2 py-0.5 text-[10px] font-medium text-emerald-600">{t("practice.trace")}</span>
            </div>
          </div>
          <div className="space-y-3">
            {ai_pass_distribution.map((bucket) => {
              const total = bucket.parsons + bucket.dropdown + bucket.execution_trace;
              return (
                <div key={bucket.bucket} className="flex items-center gap-3">
                  <span className="w-14 text-sm font-bold text-stone-800">{bucket.bucket}</span>
                  <div className="flex-1 flex gap-0.5 h-4">
                    {bucket.parsons > 0 && (
                      <div className="bg-violet-500 rounded-full" style={{ width: barW(bucket.parsons, maxBucketTotal) }} />
                    )}
                    {bucket.dropdown > 0 && (
                      <div className="bg-sky-500 rounded-full" style={{ width: barW(bucket.dropdown, maxBucketTotal) }} />
                    )}
                    {bucket.execution_trace > 0 && (
                      <div className="bg-emerald-500 rounded-full" style={{ width: barW(bucket.execution_trace, maxBucketTotal) }} />
                    )}
                  </div>
                  <span className="w-8 text-right text-xs text-stone-500">{total}</span>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      {/* Theme spread */}
      <Card padding="md">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="h-4 w-4 text-brand-700" />
          <h2 className="font-serif text-heading text-stone-900">{t("teacher.themeSpread")}</h2>
          <div className="ml-auto flex gap-2">
            <span className="rounded-md bg-brand-50 px-2 py-0.5 text-[10px] font-medium text-brand-700">{t("teacher.total")}</span>
            <span className="rounded-md bg-emerald-50 px-2 py-0.5 text-[10px] font-medium text-emerald-700">{t("teacher.lowAi")}</span>
          </div>
        </div>
        <div className="space-y-2">
          {theme_overview.slice(0, 10).map((row) => (
            <div key={row.theme} className="flex items-center gap-3">
              <span className="w-28 text-sm font-medium text-stone-700 truncate">{row.theme}</span>
              <div className="flex-1 flex gap-0.5 h-3.5">
                <div className="bg-brand-500 rounded-full" style={{ width: barW(row.total_items, maxThemeItems) }} />
                <div className="bg-emerald-500 rounded-full" style={{ width: barW(row.low_ai_items, maxThemeItems) }} />
              </div>
              <span className="w-14 text-right text-xs text-stone-500">
                AI {formatPercent(row.avg_ai_pass_rate)}
              </span>
            </div>
          ))}
        </div>
      </Card>

      {/* Telemetry panel */}
      <Card padding="md">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="h-4 w-4 text-brand-700" />
          <h2 className="font-serif text-heading text-stone-900">{t("teacher.studentTelemetry")}</h2>
        </div>

        {!telemetry.available ? (
          <div className="rounded-xl border-2 border-dashed border-stone-200 px-6 py-10 text-center">
            <Activity className="mx-auto h-8 w-8 text-stone-300" />
            <p className="mt-3 text-sm text-stone-500">{t("teacher.noTelemetryData")}</p>
          </div>
        ) : (
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Integrity signals */}
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-lg border border-stone-200 p-3">
                  <p className="text-[10px] font-semibold uppercase text-stone-400">{t("teacher.totalEvents")}</p>
                  <p className="mt-1 text-xl font-bold text-brand-700">{telemetry.total_events}</p>
                </div>
                <div className="rounded-lg border border-stone-200 p-3">
                  <p className="text-[10px] font-semibold uppercase text-stone-400">{t("teacher.studentAttemptsLabel")}</p>
                  <p className="mt-1 text-xl font-bold text-stone-900">{totals.total_attempts}</p>
                  <p className="text-[10px] text-stone-400">{t("teacher.correctLabel", { count: totals.correct_attempts })}</p>
                </div>
              </div>
              <div className="rounded-lg border border-amber-200 bg-amber-50/50 p-3">
                <h3 className="text-sm font-semibold text-stone-800 mb-2">{t("teacher.integritySignals")}</h3>
                <div className="grid grid-cols-2 gap-2">
                  <div className="rounded-md bg-white border border-amber-100 p-2.5">
                    <p className="text-[10px] text-stone-400">{t("teacher.focusExitsLabel")}</p>
                    <p className="text-lg font-bold text-amber-700">{telemetry.focus_loss_count}</p>
                  </div>
                  <div className="rounded-md bg-white border border-amber-100 p-2.5">
                    <p className="text-[10px] text-stone-400">{t("teacher.resumes")}</p>
                    <p className="text-lg font-bold text-brand-700">{telemetry.resume_count}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Event breakdown */}
            <div>
              <h3 className="text-sm font-semibold text-stone-800 mb-3">{t("teacher.eventVolume")}</h3>
              <div className="space-y-1.5 max-h-[260px] overflow-y-auto">
                {telemetry.event_breakdown.slice(0, 12).map((ev) => (
                  <div key={ev.event_type} className="flex items-center gap-2">
                    <span className="w-36 text-xs text-stone-600 font-mono truncate">{ev.event_type}</span>
                    <div className="flex-1 h-2.5 rounded-full bg-stone-100 overflow-hidden">
                      <div className="h-full rounded-full bg-brand-500" style={{ width: barW(ev.count, maxEventCount) }} />
                    </div>
                    <span className="w-10 text-right text-xs font-medium text-stone-700">{ev.count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
