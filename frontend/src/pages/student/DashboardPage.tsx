import { useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";
import { useAppStore } from "@/stores/appStore";
import { getState, getMastery, getMisconceptions, getHistory, getConfig, getGamification, getLearningPath } from "@/api/client";
import { BookOpen, CheckCircle, AlertTriangle, MessageCircle, Sparkles, BrainCircuit, Bot, MessageSquare, Play, X } from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { TimelineView } from "@/components/state/TimelineView";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { PointsSystem } from "@/components/gamification/PointsSystem";
import { AchievementSystem } from "@/components/gamification/AchievementSystem";
import { LearningPath } from "@/components/learning/LearningPath";
import { MisconceptionAI } from "@/components/diagnosis/MisconceptionAI";
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

export function DashboardPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const user = useAuthStore((s) => s.user);
  const [hintDismissed, setHintDismissed] = useState(() =>
    typeof localStorage !== "undefined" && localStorage.getItem(DASHBOARD_HINT_KEY) === "1"
  );
  const activityTrend = useActivityTrend(currentTaId);

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

  const { data: config } = useQuery({
    queryKey: ["config"],
    queryFn: getConfig,
  });
  const { data: gamification } = useQuery({
    queryKey: ["gamification"],
    queryFn: getGamification,
  });
  const { data: learningPath } = useQuery({
    queryKey: ["ta", currentTaId, "learning-path"],
    queryFn: () => getLearningPath(currentTaId!),
    enabled: currentTaId != null && currentTaId > 0,
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
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-slate-500">Welcome back, {user?.username}</p>
        <Card padding="lg" className="border-dashed border-slate-200">
          <EmptyState
            icon={Bot}
            title="No Teachable Agent selected"
            description="A new TA is usually created automatically. If you don't see one, use the dropdown above to create one, then return here."
          />
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stub mode notification banner */}
      {isStubMode && (
        <Card padding="md" className="bg-gradient-to-r from-slate-50 to-zinc-50 border-slate-200">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-slate-100 rounded-lg">
              <BrainCircuit className="w-5 h-5 text-slate-600" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-slate-900">Demo Mode Active</h3>
              <p className="mt-1 text-sm text-slate-600">
                The TA is running in demo mode with pre-defined responses. 
                To enable intelligent AI conversations, configure an LLM API key (OpenAI or DeepSeek) 
                in the backend environment variables.
              </p>
              <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
                <Sparkles className="w-4 h-4" />
                <span>System is fully functional for testing and research without LLM.</span>
              </div>
            </div>
          </div>
        </Card>
      )}

      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-slate-500">Welcome back, {user?.username}</p>
      </div>

      {!hintDismissed && (
        <Card padding="md" className="bg-brand-50 border-brand-200">
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <h3 className="font-semibold text-slate-900">Quick tip</h3>
              <p className="mt-1 text-sm text-slate-600">
                Teach your TA a concept first (e.g. variables or print), then run a test to see how well it learned.
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                setHintDismissed(true);
                try { localStorage.setItem(DASHBOARD_HINT_KEY, "1"); } catch {}
              }}
              className="rounded p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600"
              aria-label="Dismiss"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </Card>
      )}

      <div className="flex flex-wrap gap-2">
        <Link to={ROUTES.teach}>
          <Button icon={MessageSquare} variant="primary">Start teaching</Button>
        </Link>
        <Link to={ROUTES.test}>
          <Button icon={Play} variant="secondary">Run a test</Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Concepts Learned"
          value={`${learnedCount} / ${totalKus}`}
          icon={BookOpen}
          iconColor="bg-brand-50 text-brand-500"
        />
        <StatCard
          label="Test Pass Rate"
          value={mastery?.pass_rate != null ? `${Math.round(mastery.pass_rate * 100)}%` : "—"}
          icon={CheckCircle}
          iconColor="bg-emerald-50 text-success"
        />
        <StatCard
          label="Active Misconceptions"
          value={misconceptions.length}
          icon={AlertTriangle}
          iconColor="bg-amber-50 text-warning"
        />
        <StatCard
          label="Tests Run"
          value={mastery?.test_count != null ? String(mastery.test_count) : "—"}
          icon={MessageCircle}
          iconColor="bg-accent-50 text-accent-500"
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4">
          {activityTrend.some((d) => d.count > 0) && (
            <Card padding="md">
              <h2 className="text-lg font-semibold text-slate-900">Activity (last 7 days)</h2>
              <div className="mt-2 h-[120px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={activityTrend} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
                    <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 10 }} width={24} />
                    <Tooltip />
                    <Bar dataKey="count" fill="var(--color-brand-500, #6366f1)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}
          <Card padding="md">
            <h2 className="text-lg font-semibold text-slate-900">Recent Activity</h2>
            {recentEvents.length === 0 ? (
              <p className="mt-4 text-sm text-slate-500">No recent activity. Teach or run a test to see events.</p>
            ) : (
              <TimelineView events={recentEvents} className="mt-4" />
            )}
          </Card>
        </div>
        <div className="space-y-4">
          {gamification && (
            <>
              <PointsSystem points={gamification.points} level={gamification.level} />
              <AchievementSystem achievements={gamification.achievements} />
            </>
          )}
          {learningPath && (
            <LearningPath
              recommended={learningPath.recommended}
              learnedCount={learningPath.learned_count}
              totalCount={learningPath.total_count}
              estimatedMinutesRemaining={learningPath.estimated_minutes_remaining}
            />
          )}
          <Card padding="md">
            <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
          </Card>
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
