import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip as RTooltip } from "recharts";
import { useAppStore } from "@/stores/appStore";
import { getState, getMastery, getMisconceptions, getHistory, getConfig, getGamification, getLearningPath, listTA } from "@/api/client";
import { getRecommendedItems, getAssessmentStats } from "@/api/assessment";
import {
  BookOpen, BookOpenCheck, CheckCircle, AlertTriangle, MessageCircle,
  Sparkles, BrainCircuit, Bot, MessageSquare, Play, X, ChevronRight, ArrowRight,
} from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { TimelineView } from "@/components/state/TimelineView";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { PointsSystem } from "@/components/gamification/PointsSystem";
import { AchievementSystem } from "@/components/gamification/AchievementSystem";
import { SmartLearningPath } from "@/components/learning/SmartLearningPath";
import { MisconceptionAI } from "@/components/diagnosis/MisconceptionAI";
import { DomainSelector } from "@/components/onboarding/DomainSelector";
import { useAuthStore } from "@/stores/authStore";
import { ROUTES } from "@/lib/constants";
import type { TimelineEvent } from "@/components/state/TimelineView";

const DASHBOARD_HINT_KEY = "cs-ta-dashboard-hint-dismissed";

function useActivityTrend(taId: number | null) {
  const { data: historyData } = useQuery({
    queryKey: ["ta", taId, "history-trend", 1, 50],
    queryFn: () => getHistory(taId!, { page: 1, per_page: 50 }),
    enabled: taId != null && taId > 0,
  });
  const items = historyData?.items ?? [];
  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return d.toISOString().slice(0, 10);
  });
  const byDay: Record<string, number> = {};
  last7Days.forEach((day) => (byDay[day] = 0));
  items.forEach((evt) => {
    const day = (evt.timestamp || "").slice(0, 10);
    if (day in byDay) byDay[day]++;
  });
  return last7Days.map((date) => ({ date: date.slice(5), count: byDay[date] ?? 0 }));
}

const ONBOARDING_KEY = "cs-ta-onboarding-completed";

export function DashboardPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();
  const [hintDismissed, setHintDismissed] = useState(() =>
    typeof localStorage !== "undefined" && localStorage.getItem(DASHBOARD_HINT_KEY) === "1"
  );
  const [showDomainSelector, setShowDomainSelector] = useState(false);
  const activityTrend = useActivityTrend(currentTaId);

  const { data: taList, isLoading: isLoadingTAs } = useQuery({
    queryKey: ["ta", "list"],
    queryFn: listTA,
  });

  useEffect(() => {
    if (!isLoadingTAs && taList && taList.length === 0) {
      const hasCompletedOnboarding = typeof localStorage !== "undefined" &&
        localStorage.getItem(ONBOARDING_KEY) === "1";
      if (!hasCompletedOnboarding) setShowDomainSelector(true);
    }
  }, [taList, isLoadingTAs]);

  const handleOnboardingComplete = () => {
    try { localStorage.setItem(ONBOARDING_KEY, "1"); } catch {}
    setShowDomainSelector(false);
  };

  const { data: state } = useQuery({
    queryKey: ["ta", currentTaId, "state"],
    queryFn: () => getState(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: mastery } = useQuery({
    queryKey: ["ta", currentTaId, "mastery"],
    queryFn: () => getMastery(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: misconceptionsData } = useQuery({
    queryKey: ["ta", currentTaId, "misconceptions"],
    queryFn: () => getMisconceptions(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: historyData } = useQuery({
    queryKey: ["ta", currentTaId, "history", 1, 5],
    queryFn: () => getHistory(currentTaId!, { page: 1, per_page: 5 }),
    enabled: currentTaId != null,
  });
  const { data: config } = useQuery({ queryKey: ["config"], queryFn: getConfig });
  const { data: gamification } = useQuery({ queryKey: ["gamification"], queryFn: getGamification });
  const { data: learningPath } = useQuery({
    queryKey: ["ta", currentTaId, "learning-path"],
    queryFn: () => getLearningPath(currentTaId!),
    enabled: currentTaId != null && currentTaId > 0,
  });
  const { data: practiceRecs } = useQuery({
    queryKey: ["assessment", "recommend", currentTaId],
    queryFn: () => getRecommendedItems({ ta_id: currentTaId ?? undefined, count: 3 }),
  });
  const { data: assessStats } = useQuery({
    queryKey: ["assessment", "stats"],
    queryFn: getAssessmentStats,
  });

  const learnedCount = state?.learned_unit_ids?.length ?? 0;
  const totalKus = state?.units ? Object.keys(state.units).length : 20;
  const misconceptions = misconceptionsData?.misconceptions ?? [];
  const recentEvents: TimelineEvent[] = (historyData?.items ?? []).map((i) => ({
    id: i.id,
    type: (i.type as TimelineEvent["type"]) ?? "teach",
    title: i.title,
    description: i.description,
    timestamp: i.timestamp,
    metadata: i.metadata,
  }));
  const isStubMode = !config?.llm_configured;

  if (currentTaId == null) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="font-serif text-display-sm text-stone-900">Dashboard</h1>
          <p className="mt-1 text-stone-500">Welcome, {user?.username}</p>
        </div>
        <Card padding="lg" className="border-dashed">
          <EmptyState
            icon={Bot}
            title="No Teachable Agent selected"
            description="A new TA is usually created automatically. If you don't see one, use the dropdown above to create one."
          />
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <DomainSelector
        open={showDomainSelector}
        onOpenChange={setShowDomainSelector}
        onComplete={handleOnboardingComplete}
      />

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="font-serif text-display-sm text-stone-900">Dashboard</h1>
          <p className="mt-1 text-stone-500">Welcome back, {user?.username}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link to={ROUTES.teach}>
            <Button icon={MessageSquare} size="sm">Teach</Button>
          </Link>
          <Link to={ROUTES.test}>
            <Button icon={Play} variant="outline" size="sm">Test</Button>
          </Link>
          <Link to={ROUTES.practice}>
            <Button icon={BookOpenCheck} variant="outline" size="sm">Practice</Button>
          </Link>
        </div>
      </div>

      {/* Stub mode notification */}
      {isStubMode && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
          <div className="flex items-start gap-3">
            <BrainCircuit className="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-amber-900">Demo Mode</p>
              <p className="mt-0.5 text-sm text-amber-700">
                Running with pre-defined responses. Configure an LLM API key for intelligent conversations.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tip card */}
      {!hintDismissed && (
        <div className="rounded-xl border border-brand-200 bg-brand-50 p-4">
          <div className="flex items-start gap-3">
            <Sparkles className="mt-0.5 h-5 w-5 shrink-0 text-brand-600" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-brand-900">Getting started</p>
              <p className="mt-0.5 text-sm text-brand-700">
                Teach your agent a concept (e.g. variables), then run a test to see how well it learned.
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                setHintDismissed(true);
                try { localStorage.setItem(DASHBOARD_HINT_KEY, "1"); } catch {}
              }}
              className="rounded-lg p-1 text-brand-400 hover:text-brand-600"
              aria-label="Dismiss"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        <StatCard
          label="Concepts Learned"
          value={`${learnedCount} / ${totalKus}`}
          icon={BookOpen}
          iconColor="bg-brand-50 text-brand-700"
        />
        <StatCard
          label="Test Pass Rate"
          value={mastery?.pass_rate != null ? `${Math.round(mastery.pass_rate * 100)}%` : "—"}
          icon={CheckCircle}
          iconColor="bg-emerald-50 text-emerald-700"
        />
        <StatCard
          label="Misconceptions"
          value={misconceptions.length}
          icon={AlertTriangle}
          iconColor="bg-amber-50 text-amber-700"
        />
        <StatCard
          label="Tests Run"
          value={mastery?.test_count != null ? String(mastery.test_count) : "—"}
          icon={MessageCircle}
          iconColor="bg-sky-50 text-sky-700"
        />
      </div>

      {/* Main content grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Left column */}
        <div className="space-y-6 lg:col-span-2">
          {activityTrend.some((d) => d.count > 0) && (
            <Card padding="md">
              <h2 className="font-serif text-heading text-stone-900">Activity</h2>
              <p className="mt-0.5 text-sm text-stone-500">Last 7 days</p>
              <div className="mt-4 h-[140px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={activityTrend} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
                    <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#78716C" }} axisLine={false} tickLine={false} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: "#78716C" }} width={28} axisLine={false} tickLine={false} />
                    <RTooltip
                      contentStyle={{ borderRadius: "8px", border: "1px solid #E7E5E4", fontSize: "12px" }}
                    />
                    <Bar dataKey="count" fill="#0D9488" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          <Card padding="md">
            <div className="flex items-center justify-between">
              <h2 className="font-serif text-heading text-stone-900">Recent Activity</h2>
              <Link
                to={ROUTES.history}
                className="text-xs font-medium text-brand-700 hover:text-brand-800 flex items-center gap-1"
              >
                View all <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
            {recentEvents.length === 0 ? (
              <p className="mt-6 text-center text-sm text-stone-400">
                No activity yet. Start by teaching your agent a concept.
              </p>
            ) : (
              <TimelineView events={recentEvents} className="mt-4" />
            )}
          </Card>
        </div>

        {/* Right column */}
        <div className="space-y-6">
          {gamification && (
            <>
              <PointsSystem points={gamification.points} level={gamification.level} />
              <AchievementSystem achievements={gamification.achievements} />
            </>
          )}
          {learningPath && (
            <SmartLearningPath
              recommended={learningPath.recommended}
              pathSummary={learningPath.path_summary}
              learnedCount={learningPath.learned_count}
              totalCount={learningPath.total_count}
              onStartLearning={(nodeId) => navigate(`${ROUTES.teach}?focus=${nodeId}`)}
            />
          )}
          <Card padding="md">
            <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
          </Card>

          {/* Recommended practice */}
          {practiceRecs && practiceRecs.recommended.length > 0 && (
            <Card padding="md">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-stone-900 flex items-center gap-2">
                  <BookOpenCheck className="h-4 w-4 text-brand-600" />
                  Recommended Practice
                </h3>
                <Link to={ROUTES.practice} className="text-xs font-medium text-brand-700 hover:text-brand-800 flex items-center gap-0.5">
                  All <ChevronRight className="h-3 w-3" />
                </Link>
              </div>
              {assessStats && (
                <div className="mb-3 flex gap-4 text-xs text-stone-500">
                  <span>{assessStats.unique_items_solved} solved</span>
                  <span>{Math.round(assessStats.accuracy * 100)}% accuracy</span>
                </div>
              )}
              <div className="space-y-2">
                {practiceRecs.recommended.slice(0, 3).map((item) => (
                  <Link
                    key={item.id}
                    to={`/practice/${item.id}`}
                    className="block rounded-lg border border-stone-100 p-3 transition-all hover:border-brand-200 hover:bg-brand-50/40"
                  >
                    <div className="text-sm font-medium text-stone-800 line-clamp-1">{item.title}</div>
                    <div className="mt-1.5 flex items-center gap-2">
                      <span className="rounded-md bg-stone-100 px-2 py-0.5 text-[11px] font-medium text-stone-600">
                        {item.item_type === "parsons" ? "Parsons" : item.item_type === "dropdown" ? "Fill Blanks" : "Trace"}
                      </span>
                      {item.concepts?.slice(0, 2).map((c) => (
                        <span key={c} className="text-[11px] text-stone-400">{c}</span>
                      ))}
                    </div>
                  </Link>
                ))}
              </div>
            </Card>
          )}

          {/* Misconceptions */}
          {misconceptions.length > 0 ? (
            <>
              <MisconceptionAI misconceptions={misconceptions} />
              {misconceptions.slice(0, 2).map((m) => (
                <MisconceptionCard
                  key={m.id}
                  misconceptionId={m.id}
                  description={m.description}
                  affectedUnits={m.affected_units}
                  remediationHint={m.remediation_hint}
                  status={m.status as "active" | "correcting" | "resolved"}
                />
              ))}
            </>
          ) : (
            <MisconceptionCardEmpty />
          )}
        </div>
      </div>
    </div>
  );
}
