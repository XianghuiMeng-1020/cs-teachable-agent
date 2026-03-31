import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import * as Tabs from "@radix-ui/react-tabs";
import { ArrowLeft } from "lucide-react";
import { teacherStudentDetail } from "@/api/client";
import { Avatar } from "@/components/ui/Avatar";
import { Card } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { BookOpen, Target, MessageSquare } from "lucide-react";
import { ROUTES } from "@/lib/constants";
import { formatDate } from "@/lib/utils";
import type { UnitNode } from "@/components/state/KnowledgeGraph";

export function StudentDetailPage() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const id = userId ? parseInt(userId, 10) : NaN;

  const { data, isLoading } = useQuery({
    queryKey: ["teacher", "student", id],
    queryFn: () => teacherStudentDetail(id),
    enabled: !Number.isNaN(id),
  });

  const [selectedTaIndex, setSelectedTaIndex] = useState(0);

  if (Number.isNaN(id) || isLoading || !data) {
    return <p className="text-sm text-stone-500">Loading...</p>;
  }

  const taInstances = data.ta_instances ?? [];
  const primary = taInstances[selectedTaIndex] ?? taInstances[0];
  const units: UnitNode[] = primary?.units
    ? Object.entries(primary.units).map(([unit_id, rec]) => ({
        unit_id,
        status: (rec?.status as UnitNode["status"]) ?? "unknown",
        topic_group: (rec as { topic_group?: string })?.topic_group,
      }))
    : [];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button type="button" onClick={() => navigate(ROUTES.teacher.students)} className="rounded-lg p-1 hover:bg-stone-100">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <Avatar fallback={data.user.username} size="lg" />
        <div>
          <h1 className="text-2xl font-bold text-stone-900">{data.user.username}</h1>
          <p className="text-sm text-stone-500">Joined {data.user.created_at ? formatDate(data.user.created_at) : "—"}</p>
        </div>
      </div>

      {taInstances.length > 1 && (
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-stone-600">TA:</span>
          <select
            value={selectedTaIndex}
            onChange={(e) => setSelectedTaIndex(Number(e.target.value))}
            className="rounded border border-stone-300 bg-white px-2 py-1 text-sm"
          >
            {taInstances.map((ta, i) => (
              <option key={ta.id ?? i} value={i}>
                {(ta as { name?: string; domain_id?: string }).name ?? (ta as { domain_id?: string }).domain_id ?? `TA ${i + 1}`}
              </option>
            ))}
          </select>
        </div>
      )}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <StatCard label="Learned KUs" value={primary ? `${primary.learned_count}/${primary.total_kus}` : "—"} icon={BookOpen} iconColor="bg-brand-50 text-brand-700" />
        <StatCard label="Mastery %" value={primary ? `${primary.mastery_percent}%` : "—"} icon={Target} iconColor="bg-emerald-50 text-success" />
        <StatCard label="Sessions / Tests" value={primary ? `${primary.test_count} tests` : "—"} icon={MessageSquare} iconColor="bg-accent-50 text-accent-500" />
      </div>

      <Tabs.Root defaultValue="knowledge">
        <Tabs.List className="mb-4 flex gap-2 border-b border-stone-200">
          <Tabs.Trigger value="knowledge" className="border-b-2 border-transparent px-4 py-2 text-sm font-medium data-[state=active]:border-brand-700 data-[state=active]:text-brand-600">Knowledge State</Tabs.Trigger>
          <Tabs.Trigger value="misconceptions" className="border-b-2 border-transparent px-4 py-2 text-sm font-medium data-[state=active]:border-brand-700 data-[state=active]:text-brand-600">Misconceptions</Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="knowledge">
          <Card padding="md">
            <KnowledgeGraph units={units} className="min-h-[300px]" />
            {units.length === 0 && <p className="py-4 text-center text-sm text-stone-500">No knowledge state data. Student may not have taught yet.</p>}
          </Card>
        </Tabs.Content>
        <Tabs.Content value="misconceptions">
          {primary?.active_misconceptions?.length ? (
            primary.active_misconceptions.map((mid: string) => (
              <MisconceptionCard
                key={mid}
                misconceptionId={mid}
                description="Active for this TA instance."
                affectedUnits={[]}
                remediationHint="Have the student teach the correct concept."
                status="active"
              />
            ))
          ) : (
            <MisconceptionCardEmpty />
          )}
        </Tabs.Content>
      </Tabs.Root>
    </div>
  );
}
