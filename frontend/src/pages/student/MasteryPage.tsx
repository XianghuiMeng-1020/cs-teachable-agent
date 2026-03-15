import { useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getState } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import type { UnitNode } from "@/components/state/KnowledgeGraph";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Cell } from "recharts";
import { KU_DISPLAY_NAMES } from "@/lib/constants";

export function MasteryPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);

  const { data: state } = useQuery({
    queryKey: ["ta", currentTaId, "state"],
    queryFn: () => getState(currentTaId!),
    enabled: currentTaId != null,
  });

  const defs = (state as { knowledge_unit_definitions?: { id: string; name?: string }[] })?.knowledge_unit_definitions;
  const nameById = defs ? Object.fromEntries(defs.map((d) => [d.id, d.name ?? d.id])) : {};

  const units: UnitNode[] = state?.units
    ? Object.entries(state.units).map(([unit_id, rec]) => ({
        unit_id,
        status: (rec as { status?: string }).status as UnitNode["status"] ?? "unknown",
        topic_group: (rec as { topic_group?: string }).topic_group ?? defs?.find((d: { id: string; topic_group?: string }) => d.id === unit_id)?.topic_group,
      }))
    : [];

  const barData = units.map((u) => ({
    name: nameById[u.unit_id] ?? KU_DISPLAY_NAMES[u.unit_id] ?? u.unit_id,
    mastery: u.status === "learned" ? 100 : u.status === "partially_learned" ? 50 : u.status === "misconception" ? 0 : 0,
    fill: u.status === "learned" ? "#10B981" : u.status === "partially_learned" ? "#F59E0B" : "#F1F5F9",
  }));

  const byTopicGroup = units.reduce<Record<string, { learned: number; total: number }>>((acc, u) => {
    const g = u.topic_group ?? "other";
    if (!acc[g]) acc[g] = { learned: 0, total: 0 };
    acc[g].total += 1;
    if (u.status === "learned" || u.status === "partially_learned") acc[g].learned += 1;
    return acc;
  }, {});
  let radarData = Object.entries(byTopicGroup).map(([subject, v]) => ({
    subject: subject.replace(/_/g, " "),
    value: v.total ? Math.round((v.learned / v.total) * 100) : 0,
    fullMark: 100,
  }));
  if (radarData.length === 0) {
    radarData = [{ subject: "Knowledge", value: 0, fullMark: 100 }];
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Mastery</h1>

      <Card padding="md">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Knowledge state</h2>
        <KnowledgeGraph
          units={units}
          knowledgeUnitDefinitions={defs ?? undefined}
          className="min-h-[400px]"
        />
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Per concept</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} layout="vertical" margin={{ left: 100 }}>
                <XAxis type="number" domain={[0, 100]} />
                <YAxis type="category" dataKey="name" width={96} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="mastery" radius={[0, 2, 2, 0]}>
                  {barData.map((_, i) => (
                    <Cell key={i} fill={barData[i].fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card padding="md">
          <h2 className="mb-4 text-lg font-semibold text-slate-800">Topic coverage</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name="Mastery" dataKey="value" stroke="#6366F1" fill="#6366F1" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
