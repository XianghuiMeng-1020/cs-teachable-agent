import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { BookOpenCheck, Loader2, ChevronRight, Puzzle, ListChecks, ScanEye, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import { listAssessmentItems, getAssessmentStats, type AssessmentItemSummary, type AssessmentStats } from "@/api/assessment";
import { AssessmentProgress } from "@/components/assessment";
import { QuickStartGuide } from "@/components/assessment/QuickStartGuide";
import { getSessionId, setupSessionTelemetry } from "@/lib/telemetry";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import type { TFunction } from "i18next";

function getItemTypeLabel(t: TFunction, itemType: string): string {
  switch (itemType) {
    case "parsons":
      return t("practice.parsonsPuzzle");
    case "dropdown":
      return t("practice.fillBlanks");
    case "execution-trace":
      return t("practice.executionTrace");
    default:
      return itemType;
  }
}

const ITEM_TYPE_META: Record<string, { icon: typeof Puzzle; color: string; bg: string }> = {
  parsons: { icon: Puzzle, color: "text-violet-700", bg: "bg-violet-50 border-violet-200" },
  dropdown: { icon: ListChecks, color: "text-sky-700", bg: "bg-sky-50 border-sky-200" },
  "execution-trace": { icon: ScanEye, color: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200" },
};

export function PracticePage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [items, setItems] = useState<AssessmentItemSummary[]>([]);
  const [stats, setStats] = useState<AssessmentStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>("");
  const [maxAiPassRate, setMaxAiPassRate] = useState(75);
  const [total, setTotal] = useState(0);

  const buildSessionState = useCallback((currentId: number) => {
    const itemIds = items.map((it) => it.id);
    const currentIndex = itemIds.indexOf(currentId);
    return {
      itemIds,
      currentIndex: currentIndex >= 0 ? currentIndex : 0,
      sessionId: getSessionId(),
    };
  }, [items]);

  useEffect(() => {
    return setupSessionTelemetry();
  }, []);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [itemsRes, statsRes] = await Promise.all([
        listAssessmentItems({
          item_type: filterType || undefined,
          max_ai_pass_rate: maxAiPassRate,
          limit: 100,
        }),
        getAssessmentStats(),
      ]);
      setItems(itemsRes.items);
      setTotal(itemsRes.items.length);
      setStats(statsRes);
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }, [filterType, maxAiPassRate]);

  useEffect(() => { loadData(); }, [loadData]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">{t("practice.title")}</h1>
        <p className="mt-1 text-stone-500">
          {t("practice.desc")}
        </p>
      </div>

      {stats && (
        <AssessmentProgress
          totalAttempts={stats.total_attempts}
          correctAttempts={stats.correct_attempts}
          accuracy={stats.accuracy}
          uniqueItemsSolved={stats.unique_items_solved}
          totalItemsAvailable={stats.total_items_available}
        />
      )}

      {/* Quick Start Guide */}
      <QuickStartGuide />

      {/* AI Resistance Filter */}
      <div className="rounded-xl border border-stone-200/80 bg-white p-4 shadow-card">
        <div className="flex items-center gap-2 mb-3">
          <ShieldAlert className="h-4 w-4 text-brand-700" />
          <span className="text-sm font-semibold text-stone-800">{t("practice.aiResistanceFilter")}</span>
          <span className="ml-auto text-xs font-medium text-brand-700">
            {t("practice.maxAiPassRate", { rate: maxAiPassRate })}
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={100}
          step={5}
          value={maxAiPassRate}
          onChange={(e) => setMaxAiPassRate(Number(e.target.value))}
          className="w-full h-1.5 rounded-full appearance-none bg-stone-200 accent-brand-700 cursor-pointer"
        />
        <div className="mt-1.5 flex justify-between text-[10px] text-stone-400">
          <span>{t("practice.harder")}</span>
          <span>{t("practice.easier")}</span>
        </div>
      </div>

      {/* Type Filters */}
      <div className="flex items-center gap-2 flex-wrap">
        {[
          { value: "", labelKey: "practice.allTypes" as const },
          { value: "parsons", labelKey: "practice.parsons" as const },
          { value: "dropdown", labelKey: "practice.fillBlanks" as const },
          { value: "execution-trace", labelKey: "practice.trace" as const },
        ].map((f) => (
          <button
            key={f.value}
            onClick={() => setFilterType(f.value)}
            className={cn(
              "rounded-full border px-3.5 py-1.5 text-xs font-medium transition-all",
              filterType === f.value
                ? "border-brand-600 bg-brand-50 text-brand-800"
                : "border-stone-200 bg-white text-stone-600 hover:border-stone-300"
            )}
          >
            {t(f.labelKey)}
          </button>
        ))}
        <span className="text-xs text-stone-400 ml-auto">{t("practice.itemCount", { count: total })}</span>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-6 w-6 animate-spin text-brand-600" />
        </div>
      ) : items.length === 0 ? (
        <div className="rounded-xl border-2 border-dashed border-stone-200 py-16 text-center">
          <BookOpenCheck className="mx-auto h-10 w-10 text-stone-300" />
          <p className="mt-3 text-sm font-medium text-stone-500">{t("practice.noItems")}</p>
          <p className="mt-1 text-xs text-stone-400">{t("practice.tryChangingFilter")}</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => {
            const meta = ITEM_TYPE_META[item.item_type] ?? ITEM_TYPE_META.parsons;
            const TypeIcon = meta.icon;
            return (
              <button
                key={item.id}
                onClick={() => navigate(`/practice/${item.id}`, { state: buildSessionState(item.id) })}
                className="group relative rounded-xl border border-stone-200/80 bg-white p-5 text-left shadow-card transition-all hover:shadow-card-hover hover:-translate-y-0.5"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className={cn("flex h-9 w-9 items-center justify-center rounded-lg border", meta.bg)}>
                    <TypeIcon className={cn("h-4 w-4", meta.color)} />
                  </div>
                  <ChevronRight className="h-4 w-4 text-stone-300 transition-colors group-hover:text-brand-500 mt-1" />
                </div>
                <h3 className="mt-3 text-sm font-semibold text-stone-900 group-hover:text-brand-800 line-clamp-2">
                  {item.title}
                </h3>
                <div className="mt-2 flex items-center gap-2 flex-wrap">
                  <span className={cn("rounded-md px-2 py-0.5 text-[11px] font-medium border", meta.bg, meta.color)}>
                    {getItemTypeLabel(t, item.item_type)}
                  </span>
                  {item.theme && (
                    <span className="text-[11px] text-stone-400">{item.theme}</span>
                  )}
                </div>
                {item.concepts && item.concepts.length > 0 && (
                  <div className="mt-2.5 flex gap-1 flex-wrap">
                    {item.concepts.slice(0, 3).map((c) => (
                      <span key={c} className="rounded-md bg-stone-50 px-1.5 py-0.5 text-[10px] font-medium text-stone-500">
                        {c}
                      </span>
                    ))}
                    {item.concepts.length > 3 && (
                      <span className="text-[10px] text-stone-400">+{item.concepts.length - 3}</span>
                    )}
                  </div>
                )}
                {item.ai_pass_rate != null && (
                  <div className="mt-3">
                    <div className="flex items-center justify-between text-[10px] text-stone-400">
                      <span>{t("practice.difficulty")}</span>
                      <span>{Math.round((1 - item.ai_pass_rate / 100) * 100)}%</span>
                    </div>
                    <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-stone-100">
                      <div
                        className="h-full rounded-full bg-amber-400"
                        style={{ width: `${Math.round((1 - item.ai_pass_rate / 100) * 100)}%` }}
                      />
                    </div>
                  </div>
                )}
              </button>
            );
          })}
        </div>
      )}
      <ContextualHelp pageKey="practice" />
    </div>
  );
}
