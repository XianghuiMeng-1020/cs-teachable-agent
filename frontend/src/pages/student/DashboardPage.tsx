import { useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getState, getMastery, getMisconceptions, getHistory } from "@/api/client";
import { BookOpen, CheckCircle, AlertTriangle, MessageCircle } from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { TimelineView } from "@/components/state/TimelineView";
import { useAuthStore } from "@/stores/authStore";
import type { TimelineEvent } from "@/components/state/TimelineView";

export function DashboardPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const user = useAuthStore((s) => s.user);

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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-slate-500">Welcome back, {user?.username}</p>
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
        <div className="lg:col-span-2">
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
          <Card padding="md">
            <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
          </Card>
          {misconceptions.length > 0 ? (
            misconceptions.slice(0, 2).map((m) => (
              <MisconceptionCard
                key={m.id}
                misconceptionId={m.id}
                description={m.description}
                affectedUnits={m.affected_units}
                remediationHint={m.remediation_hint}
                status={m.status as "active" | "correcting" | "resolved"}
              />
            ))
          ) : (
            <MisconceptionCardEmpty />
          )}
        </div>
      </div>
    </div>
  );
}
