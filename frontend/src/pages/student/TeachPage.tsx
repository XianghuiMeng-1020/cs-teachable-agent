import { useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getState, getMisconceptions } from "@/api/client";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import type { UnitNode } from "@/components/state/KnowledgeGraph";

export function TeachPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);

  const { data: state } = useQuery({
    queryKey: ["ta", currentTaId, "state"],
    queryFn: () => getState(currentTaId!),
    enabled: currentTaId != null,
  });

  const { data: misconceptionsData } = useQuery({
    queryKey: ["ta", currentTaId, "misconceptions"],
    queryFn: () => getMisconceptions(currentTaId!),
    enabled: currentTaId != null,
  });

  const defs = (state as { knowledge_unit_definitions?: { id: string; topic_group?: string }[] })?.knowledge_unit_definitions;
  const units: UnitNode[] = state?.units
    ? Object.entries(state.units).map(([unit_id, rec]) => ({
        unit_id,
        status: (rec as { status?: string }).status as UnitNode["status"] ?? "unknown",
        topic_group: (rec as { topic_group?: string }).topic_group ?? defs?.find((d) => d.id === unit_id)?.topic_group,
      }))
    : [];

  const learnedCount = state?.learned_unit_ids?.length ?? 0;
  const totalKus = units.length || 20;
  const misconceptions = misconceptionsData?.misconceptions ?? [];

  return (
    <div
      className="grid h-[calc(100vh-var(--topbar-height)-40px)] gap-4"
      style={{ gridTemplateColumns: "1fr 380px" }}
    >
      <div className="min-h-0 overflow-hidden rounded-xl border border-slate-200/60 bg-white shadow-card">
        <ChatPanel taId={currentTaId} />
      </div>
      <div className="flex min-h-0 flex-col gap-4 overflow-y-auto">
        <KnowledgeGraph
          units={units}
          knowledgeUnitDefinitions={(state as { knowledge_unit_definitions?: unknown })?.knowledge_unit_definitions ?? undefined}
          className="min-h-[200px] flex-shrink-0"
        />
        <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
        {misconceptions.length > 0 ? (
          misconceptions.map((m) => (
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
  );
}
