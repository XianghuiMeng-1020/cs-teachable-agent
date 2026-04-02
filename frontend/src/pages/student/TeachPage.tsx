import { useState, useCallback, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { GripVertical, Trophy, ArrowRight } from "lucide-react";
import { useAppStore } from "@/stores/appStore";
import { getState, getProblems, getTA, me } from "@/api/client";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { ProblemPanel } from "@/components/teach/ProblemPanel";
import { AntiCheatShell } from "@/components/assessment/AntiCheatShell";
import { AntiCaptureOverlay } from "@/components/assessment/AntiCaptureOverlay";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import { Button } from "@/components/ui/Button";
import type { TeachProblem, CodeModification } from "@/components/teach/ProblemRenderer";

const MASTERY_THRESHOLD = 80;
const MIN_LEFT_WIDTH = 30;
const MAX_LEFT_WIDTH = 70;

export function TeachPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const currentTaId = useAppStore((s) => s.currentTaId);

  // Resizable split
  const [leftPercent, setLeftPercent] = useState(50);
  const dragging = useRef(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Problem state
  const [problemIndex, setProblemIndex] = useState(0);
  const [codeModifications, setCodeModifications] = useState<CodeModification[]>([]);
  const [showMasteredBanner, setShowMasteredBanner] = useState(false);

  // Queries
  const { data: state } = useQuery({
    queryKey: ["ta", currentTaId, "state"],
    queryFn: () => getState(currentTaId!),
    enabled: currentTaId != null,
    refetchInterval: 5000,
  });

  const { data: taData } = useQuery({
    queryKey: ["ta", currentTaId],
    queryFn: () => getTA(currentTaId!),
    enabled: currentTaId != null,
  });

  const { data: problemsData, isLoading: problemsLoading } = useQuery({
    queryKey: ["ta", currentTaId, "problems"],
    queryFn: () => getProblems(currentTaId!),
    enabled: currentTaId != null,
  });

  const { data: userData } = useQuery({ queryKey: ["me"], queryFn: me });

  const domainId = (taData?.domain_id as string) ?? "python";

  // Build problem list from API or fallback
  const problems: TeachProblem[] = (problemsData?.problems ?? []).map((p: Record<string, unknown>) => ({
    problem_id: p.problem_id as string,
    problem_type: (p as { problem_type?: string }).problem_type ?? "buggy-code",
    problem_statement: p.problem_statement as string,
    difficulty: (p.difficulty as string) ?? "easy",
    difficulty_order: (p as { difficulty_order?: number }).difficulty_order ?? 0,
    topic_group: (p as { topic_group?: string }).topic_group,
    knowledge_units_tested: (p.knowledge_units_required ?? p.knowledge_units_tested ?? []) as string[],
    code: (p as { code?: string }).code,
    bug_lines: (p as { bug_lines?: number[] }).bug_lines,
    correct_code: (p as { correct_code?: string }).correct_code,
    bug_explanation: (p as { bug_explanation?: string }).bug_explanation,
    code_template: (p as { code_template?: string }).code_template,
    completion_slots: (p as { completion_slots?: { line: number; placeholder: string }[] }).completion_slots,
    choices: (p as { choices?: { id: string; text: string }[] }).choices,
    correct_choice_ids: (p as { correct_choice_ids?: string[] }).correct_choice_ids,
    starter_code: (p as { starter_code?: string }).starter_code,
    expected_output: (p as { expected_output?: string }).expected_output,
    options: (p as { options?: string[] }).options,
    required_block_count: (p as { required_block_count?: number }).required_block_count,
    blanks: (p as { blanks?: TeachProblem["blanks"] }).blanks,
    prompt_template: (p as { prompt_template?: string }).prompt_template,
    function_name: (p as { function_name?: string }).function_name,
    function_source: (p as { function_source?: string }).function_source,
    call_expression: (p as { call_expression?: string }).call_expression,
    checkpoints: (p as { checkpoints?: TeachProblem["checkpoints"] }).checkpoints,
  }));

  const currentProblem = problems[problemIndex] ?? null;

  // Compute mastery for current problem's knowledge units
  const computeMastery = useCallback(() => {
    if (!state?.units || !currentProblem?.knowledge_units_tested?.length) return 0;
    const kus = currentProblem.knowledge_units_tested;
    let sum = 0;
    for (const ku of kus) {
      const unit = (state.units as Record<string, { bkt_p_know?: number }>)[ku];
      sum += (unit?.bkt_p_know ?? 0);
    }
    return Math.round((sum / kus.length) * 100);
  }, [state, currentProblem]);

  const masteryPercent = computeMastery();

  // Check mastery threshold
  useEffect(() => {
    if (masteryPercent >= MASTERY_THRESHOLD && !showMasteredBanner) {
      setShowMasteredBanner(true);
    }
  }, [masteryPercent, showMasteredBanner]);

  // Line click -> pre-fill chat reference
  const [lineRef, setLineRef] = useState<string | null>(null);
  const handleLineClick = useCallback((lineNum: number, lineContent: string) => {
    setLineRef(`[Line ${lineNum}] ${lineContent.trim()}`);
  }, []);

  // Reset modifications when problem changes
  useEffect(() => {
    setCodeModifications([]);
    setShowMasteredBanner(false);
    setLineRef(null);
  }, [problemIndex]);

  // Listen for code_modification events from ChatPanel
  useEffect(() => {
    const handler = (e: CustomEvent<{ modification: CodeModification }>) => {
      setCodeModifications((prev) => [...prev, e.detail.modification]);
    };
    window.addEventListener("ta-code-modification" as string, handler as EventListener);
    return () => window.removeEventListener("ta-code-modification" as string, handler as EventListener);
  }, []);

  // Drag-to-resize
  const handleMouseDown = useCallback(() => { dragging.current = true; }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!dragging.current || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const pct = ((e.clientX - rect.left) / rect.width) * 100;
      setLeftPercent(Math.min(MAX_LEFT_WIDTH, Math.max(MIN_LEFT_WIDTH, pct)));
    };
    const handleMouseUp = () => { dragging.current = false; };
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  const goNext = () => {
    setShowMasteredBanner(false);
    setProblemIndex((i) => Math.min(i + 1, problems.length - 1));
  };
  const goPrev = () => setProblemIndex((i) => Math.max(i - 1, 0));
  const goSkip = () => goNext();

  return (
    <AntiCaptureOverlay>
      <AntiCheatShell enabled>
        <div
          ref={containerRef}
          className="h-[calc(100vh-var(--topbar-height)-24px)] flex relative select-none"
        >
          {/* LEFT: Problem Panel */}
          <div
            className="flex flex-col min-h-0 border-r border-stone-200 bg-white overflow-hidden rounded-l-2xl shadow-lg"
            style={{ width: `${leftPercent}%` }}
          >
            {/* Domain badge */}
            <div className="flex items-center gap-2 px-4 py-2 border-b border-stone-100 bg-stone-50/50">
              <span className="px-2 py-0.5 text-xs font-medium bg-emerald-100 text-emerald-700 rounded-full">{domainId}</span>
              <span className="text-xs text-stone-400">{t("teach.title", { defaultValue: "Teach" })}</span>
            </div>
            <ProblemPanel
              problem={currentProblem}
              masteryPercent={masteryPercent}
              codeModifications={codeModifications}
              problemIndex={problemIndex}
              totalProblems={problems.length || 1}
              onPrev={goPrev}
              onNext={goNext}
              onSkip={goSkip}
              loading={problemsLoading}
              userId={userData?.id}
              username={userData?.username}
              onLineClick={handleLineClick}
            />
          </div>

          {/* DRAG HANDLE */}
          <div
            onMouseDown={handleMouseDown}
            className="w-2 flex-shrink-0 cursor-col-resize bg-stone-100 hover:bg-brand-200 transition-colors flex items-center justify-center z-10"
          >
            <GripVertical className="w-3 h-3 text-stone-400" />
          </div>

          {/* RIGHT: Chat Panel */}
          <div
            className="flex flex-col min-h-0 bg-white overflow-hidden rounded-r-2xl shadow-lg"
            style={{ width: `${100 - leftPercent}%` }}
          >
            <ChatPanel
              taId={currentTaId}
              problemContext={currentProblem ? { problem_id: currentProblem.problem_id, problem_type: currentProblem.problem_type } : undefined}
              lineRef={lineRef}
              onLineRefUsed={() => setLineRef(null)}
            />
          </div>

          {/* MASTERED BANNER */}
          <AnimatePresence>
            {showMasteredBanner && (
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 30 }}
                className="absolute bottom-8 left-1/2 -translate-x-1/2 z-50"
              >
                <div className="flex items-center gap-3 bg-emerald-600 text-white px-6 py-3 rounded-2xl shadow-xl">
                  <Trophy className="w-6 h-6 text-yellow-300" />
                  <div>
                    <p className="font-semibold">
                      {t("teach.masteredBanner", { defaultValue: "Topic Mastered!" })}
                    </p>
                    <p className="text-sm text-emerald-100">
                      {t("teach.masteredDesc", { defaultValue: "You've reached 80% mastery. Ready for the next challenge?" })}
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    icon={ArrowRight}
                    onClick={goNext}
                    className="ml-2 border-white/30 text-white hover:bg-white/20"
                  >
                    {t("teach.nextTopic", { defaultValue: "Next" })}
                  </Button>
                  <button
                    onClick={() => setShowMasteredBanner(false)}
                    className="ml-1 text-emerald-200 hover:text-white text-sm"
                  >
                    ✕
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <ContextualHelp pageKey="teach" />
        </div>
      </AntiCheatShell>
    </AntiCaptureOverlay>
  );
}
