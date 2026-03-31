import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ChevronDown, 
  ChevronUp, 
  Code, 
  MessageSquare, 
  Brain, 
  Target,
  Sparkles,
  BookOpen,
  Lightbulb,
  Zap,
  GraduationCap,
} from "lucide-react";
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

// Animation variants
const slideIn = {
  hidden: { opacity: 0, x: 20 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.4 } },
};

const fadeIn = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
};

export function TeachPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const [playgroundOpen, setPlaygroundOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<"chat" | "playground" | "promptlab">("chat");

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
  
  const progressPercent = totalKus > 0 ? Math.round((learnedCount / totalKus) * 100) : 0;

  // Sample teaching tips
  const teachingTips = [
    "Explain concepts as if teaching a beginner",
    "Use specific examples to illustrate ideas",
    "Ask the TA questions to check understanding",
    "Connect new concepts to what TA already knows",
  ];

  return (
    <div className="h-[calc(100vh-var(--topbar-height)-24px)] flex flex-col lg:flex-row gap-4">
      {/* Main Content Area */}
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex-1 flex flex-col min-h-0"
      >
        {/* Header */}
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
              <MessageSquare className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-stone-900 flex items-center gap-2">
                Teach Your AI Agent
                <span className="px-2 py-0.5 text-xs font-medium bg-emerald-100 text-emerald-700 rounded-full">
                  {domainId}
                </span>
              </h1>
              <p className="text-sm text-stone-500">
                Explain concepts clearly — the agent starts with zero knowledge
              </p>
            </div>
          </div>
          
          {/* Tab Switcher */}
          <div className="hidden sm:flex items-center gap-1 bg-stone-100 rounded-lg p-1">
            {[
              { id: "chat", icon: MessageSquare, label: "Chat" },
              { id: "playground", icon: Code, label: "Code" },
              { id: "promptlab", icon: Sparkles, label: "AI Lab" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? "bg-white text-brand-700 shadow-sm"
                    : "text-stone-600 hover:text-stone-900"
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 min-h-0 rounded-2xl border border-stone-200 bg-white shadow-lg overflow-hidden">
          <AnimatePresence mode="wait">
            {activeTab === "chat" && (
              <motion.div
                key="chat"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full"
              >
                <ChatPanel taId={currentTaId} />
              </motion.div>
            )}
            {activeTab === "playground" && (
              <motion.div
                key="playground"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full p-4"
              >
                <LiveCodeEditor domainId={domainId} />
              </motion.div>
            )}
            {activeTab === "promptlab" && (
              <motion.div
                key="promptlab"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full overflow-auto"
              >
                <div className="p-4 space-y-4">
                  <PromptLab />
                  <ModelComparison />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Teaching Tips */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-4 flex items-start gap-3 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-3 border border-amber-200"
        >
          <div className="w-8 h-8 rounded-lg bg-amber-100 flex items-center justify-center flex-shrink-0">
            <Lightbulb className="w-4 h-4 text-amber-600" />
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-amber-900">Teaching Tip</div>
            <div className="text-sm text-amber-700">
              {teachingTips[Math.floor(Math.random() * teachingTips.length)]}
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Right Sidebar */}
      <motion.div 
        variants={slideIn}
        initial="hidden"
        animate="visible"
        className="w-full lg:w-80 flex-shrink-0 flex flex-col gap-4 overflow-y-auto"
      >
        {/* Progress Card */}
        <div className="rounded-xl bg-gradient-to-br from-brand-600 to-brand-700 p-4 text-white shadow-lg">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
              <GraduationCap className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="text-sm text-brand-100">Learning Progress</div>
              <div className="text-2xl font-bold">{progressPercent}%</div>
            </div>
          </div>
          <div className="h-2 bg-white/20 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progressPercent}%` }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="h-full bg-white rounded-full"
            />
          </div>
          <div className="mt-3 flex justify-between text-sm text-brand-100">
            <span>{learnedCount} concepts learned</span>
            <span>{totalKus - learnedCount} remaining</span>
          </div>
        </div>

        {/* Knowledge Graph */}
        <div className="rounded-xl border border-stone-200 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Brain className="w-5 h-5 text-violet-600" />
            <h3 className="font-semibold text-stone-900">Knowledge State</h3>
          </div>
          <KnowledgeGraph
            units={units}
            knowledgeUnitDefinitions={(state as { knowledge_unit_definitions?: unknown })?.knowledge_unit_definitions ?? undefined}
            className="min-h-[200px]"
          />
        </div>

        {/* Mastery Status */}
        <div className="rounded-xl border border-stone-200 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-emerald-600" />
            <h3 className="font-semibold text-stone-900">Mastery Status</h3>
          </div>
          <MasteryRadial learnedCount={learnedCount} totalCount={totalKus} />
        </div>

        {/* Learning Objectives */}
        <div className="rounded-xl border border-stone-200 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-stone-900">Next Objectives</h3>
          </div>
          <LearningObjectives learnedUnitIds={state?.learned_unit_ids ?? []} compact />
        </div>

        {/* Misconceptions */}
        <div className="rounded-xl border border-stone-200 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-amber-600" />
            <h3 className="font-semibold text-stone-900">
              Misconceptions
              {misconceptions.length > 0 && (
                <span className="ml-2 px-2 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-full">
                  {misconceptions.length}
                </span>
              )}
            </h3>
          </div>
          {misconceptions.length > 0 ? (
            <div className="space-y-3">
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
              {misconceptions.length > 2 && (
                <div className="text-center text-sm text-stone-500">
                  +{misconceptions.length - 2} more misconceptions
                </div>
              )}
            </div>
          ) : (
            <MisconceptionCardEmpty />
          )}
        </div>
      </motion.div>
    </div>
  );
}
