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
    fill: u.status === "learned" ? "#059669" : u.status === "partially_learned" ? "#D97706" : "#E7E5E4",
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

  const learnedCount = units.filter((u) => u.status === "learned").length;
  const partialCount = units.filter((u) => u.status === "partially_learned").length;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">Mastery</h1>
        <p className="mt-1 text-stone-500">
          {learnedCount} concepts mastered, {partialCount} in progress, {units.length} total
        </p>
      </div>

      <Card padding="md">
        <h2 className="font-serif text-heading text-stone-900 mb-4">Knowledge Graph</h2>
        <KnowledgeGraph
          units={units}
          knowledgeUnitDefinitions={defs ?? undefined}
          className="min-h-[400px]"
        />
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card padding="md">
          <h2 className="font-serif text-heading text-stone-900 mb-4">Per Concept</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} layout="vertical" margin={{ left: 100 }}>
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: "#78716C" }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" width={96} tick={{ fontSize: 11, fill: "#57534E" }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid #E7E5E4", fontSize: "12px" }} />
                <Bar dataKey="mastery" radius={[0, 4, 4, 0]}>
                  {barData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card padding="md">
          <h2 className="font-serif text-heading text-stone-900 mb-4">Topic Coverage</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#D6D3D1" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: "#57534E" }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10, fill: "#A8A29E" }} />
                <Radar name="Mastery" dataKey="value" stroke="#0D9488" fill="#0D9488" fillOpacity={0.2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
