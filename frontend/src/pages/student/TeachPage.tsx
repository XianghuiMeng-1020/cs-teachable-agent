import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronDown, ChevronUp, Code } from "lucide-react";
import { useAppStore } from "@/stores/appStore";
import { getState, getMisconceptions, getTA } from "@/api/client";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { LiveCodeEditor } from "@/components/workspace/LiveCodeEditor";
import { LearningObjectives } from "@/components/workspace/LearningObjectives";
import { PromptLab } from "@/components/ai-experiments/PromptLab";
import { ModelComparison } from "@/components/ai-experiments/ModelComparison";
import type { UnitNode } from "@/components/state/KnowledgeGraph";

export function TeachPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const [playgroundOpen, setPlaygroundOpen] = useState(false);

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
  const { data: taData } = useQuery({
    queryKey: ["ta", currentTaId],
    queryFn: () => getTA(currentTaId!),
    enabled: currentTaId != null,
  });
  const domainId = (taData?.domain_id as string) ?? "python";

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
    <div className="grid h-[calc(100vh-var(--topbar-height)-48px)] gap-5 grid-cols-1 lg:grid-cols-[1fr_360px]">
      {/* Chat panel */}
      <div className="min-h-0 overflow-hidden rounded-xl border border-stone-200/80 bg-white shadow-card order-2 lg:order-1">
        <ChatPanel taId={currentTaId} />
      </div>

      {/* Sidebar panel */}
      <div className="flex min-h-0 flex-col gap-4 overflow-y-auto order-1 lg:order-2 pr-1">
        <KnowledgeGraph
          units={units}
          knowledgeUnitDefinitions={(state as { knowledge_unit_definitions?: unknown })?.knowledge_unit_definitions ?? undefined}
          className="min-h-[200px] flex-shrink-0"
        />

        <div className="rounded-xl border border-stone-200/80 bg-white p-4">
          <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
        </div>

        <LearningObjectives learnedUnitIds={state?.learned_unit_ids ?? []} compact />

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

        <div className="rounded-xl border border-stone-200/80 bg-white overflow-hidden">
          <button
            type="button"
            onClick={() => setPlaygroundOpen((o) => !o)}
            className="flex w-full items-center justify-between px-4 py-3 text-sm font-medium text-stone-700 hover:bg-stone-50 transition-colors"
          >
            <span className="flex items-center gap-2">
              <Code className="h-4 w-4 text-brand-600" />
              Code Playground
            </span>
            {playgroundOpen ? <ChevronUp className="h-4 w-4 text-stone-400" /> : <ChevronDown className="h-4 w-4 text-stone-400" />}
          </button>
          {playgroundOpen && (
            <div className="border-t border-stone-100 p-3">
              <LiveCodeEditor maxHeight="200px" />
            </div>
          )}
        </div>

        {domainId === "ai_literacy" && (
          <div className="space-y-4">
            <PromptLab taId={currentTaId} />
            <ModelComparison taId={currentTaId} />
          </div>
        )}
      </div>
    </div>
  );
}
