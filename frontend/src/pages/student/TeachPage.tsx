import { useState, useCallback, useEffect, useRef, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { GripVertical, Trophy, ArrowRight, PanelLeftClose, PanelLeft, Maximize2, Minimize2 } from "lucide-react";
import { useAppStore } from "@/stores/appStore";
import { getState, getProblems, getTA, me } from "@/api/client";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { ProblemPanel } from "@/components/teach/ProblemPanel";
import { TopicBrowser } from "@/components/teach/TopicBrowser";
import { ProctorBadge } from "@/components/teach/ProctorBadge";
import { AntiCheatShell } from "@/components/assessment/AntiCheatShell";
import { AntiCaptureOverlay } from "@/components/assessment/AntiCaptureOverlay";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import { Button } from "@/components/ui/Button";
import type { TeachProblem, CodeModification } from "@/components/teach/ProblemRenderer";

const MASTERY_THRESHOLD = 80;
const MOBILE_BREAKPOINT = 768;

interface TopicGroupInfo {
  name: string;
  label: string;
  count: number;
  mastery_percent: number;
  problem_types: string[];
}

type ViewMode = "split" | "problem" | "chat";

export function TeachPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const currentTaId = useAppStore((s) => s.currentTaId);

  // Mobile detection
  const [isMobile, setIsMobile] = useState(() =>
    typeof window !== "undefined" ? window.innerWidth < MOBILE_BREAKPOINT : false
  );
  const [mobileView, setMobileView] = useState<ViewMode>("split");

  // Sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Problem selection state
  const [selectedProblemId, setSelectedProblemId] = useState<string | null>(null);
  const [codeModifications, setCodeModifications] = useState<CodeModification[]>([]);
  const [showMasteredBanner, setShowMasteredBanner] = useState(false);

  // Drag resize between problem panel and chat
  const [splitPercent, setSplitPercent] = useState(50);
  const dragging = useRef(false);
  const rightRef = useRef<HTMLDivElement>(null);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < MOBILE_BREAKPOINT;
      setIsMobile(mobile);
      if (mobile) {
        setSidebarOpen(false);
        if (mobileView === "split") {
          setMobileView("problem");
        }
      } else {
        setSidebarOpen(true);
        setMobileView("split");
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, [mobileView]);

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

  // Build typed problem list
  const problems: TeachProblem[] = useMemo(() =>
    (problemsData?.problems ?? []).map((p: Record<string, unknown>) => ({
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
    })),
  [problemsData]);

  const topicGroups: TopicGroupInfo[] = useMemo(() =>
    (problemsData as Record<string, unknown>)?.topic_groups as TopicGroupInfo[] ?? [],
  [problemsData]);

  // Auto-select first problem if none selected
  useEffect(() => {
    if (!selectedProblemId && problems.length > 0) {
      setSelectedProblemId(problems[0].problem_id);
    }
  }, [problems, selectedProblemId]);

  const currentProblem = useMemo(() =>
    problems.find((p) => p.problem_id === selectedProblemId) ?? null,
  [problems, selectedProblemId]);

  const currentTopicGroup = currentProblem?.topic_group || "general";
  const problemsInTopic = useMemo(() =>
    problems.filter((p) => (p.topic_group || "general") === currentTopicGroup),
  [problems, currentTopicGroup]);
  const indexInTopic = problemsInTopic.findIndex((p) => p.problem_id === selectedProblemId);

  // Mastery for current problem's KUs
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

  useEffect(() => {
    if (masteryPercent >= MASTERY_THRESHOLD && !showMasteredBanner) {
      setShowMasteredBanner(true);
    }
  }, [masteryPercent, showMasteredBanner]);

  // Line click -> chat reference
  const [lineRef, setLineRef] = useState<string | null>(null);
  const handleLineClick = useCallback((lineNum: number, lineContent: string) => {
    setLineRef(`[Line ${lineNum}] ${lineContent.trim()}`);
    if (isMobile) {
      setMobileView("chat");
    }
  }, [isMobile]);

  // Reset when problem changes
  useEffect(() => {
    setCodeModifications([]);
    setShowMasteredBanner(false);
    setLineRef(null);
  }, [selectedProblemId]);

  // Listen for code_modification events
  useEffect(() => {
    const handler = (e: CustomEvent<{ modification: CodeModification }>) => {
      setCodeModifications((prev) => [...prev, e.detail.modification]);
    };
    window.addEventListener("ta-code-modification" as string, handler as EventListener);
    return () => window.removeEventListener("ta-code-modification" as string, handler as EventListener);
  }, []);

  // Navigation within topic
  const goNextInTopic = () => {
    if (indexInTopic < problemsInTopic.length - 1) {
      setSelectedProblemId(problemsInTopic[indexInTopic + 1].problem_id);
    }
  };
  const goPrevInTopic = () => {
    if (indexInTopic > 0) {
      setSelectedProblemId(problemsInTopic[indexInTopic - 1].problem_id);
    }
  };
  const goSkip = () => goNextInTopic();

  // Drag resize - disabled on mobile
  const handleMouseDown = useCallback(() => {
    if (!isMobile) {
      dragging.current = true;
    }
  }, [isMobile]);

  useEffect(() => {
    if (isMobile) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!dragging.current || !rightRef.current) return;
      const rect = rightRef.current.getBoundingClientRect();
      const pct = ((e.clientX - rect.left) / rect.width) * 100;
      setSplitPercent(Math.min(70, Math.max(30, pct)));
    };
    const handleMouseUp = () => { dragging.current = false; };
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isMobile]);

  const goNextTopic = () => {
    setShowMasteredBanner(false);
    const idx = topicGroups.findIndex((tg) => tg.name === currentTopicGroup);
    if (idx >= 0 && idx < topicGroups.length - 1) {
      const nextTg = topicGroups[idx + 1].name;
      const firstProblem = problems.find((p) => (p.topic_group || "general") === nextTg);
      if (firstProblem) setSelectedProblemId(firstProblem.problem_id);
    }
  };

  // Mobile view toggle button
  const MobileViewToggle = () => (
    <div className="flex items-center gap-1 bg-stone-100 dark:bg-stone-800 rounded-lg p-1">
      <button
        onClick={() => setMobileView("problem")}
        className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors tap-target ${
          mobileView === "problem"
            ? "bg-white dark:bg-stone-700 text-stone-900 dark:text-stone-100 shadow-sm"
            : "text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200"
        }`}
        aria-label="查看问题"
        aria-pressed={mobileView === "problem"}
      >
        问题
      </button>
      <button
        onClick={() => setMobileView("chat")}
        className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors tap-target ${
          mobileView === "chat"
            ? "bg-white dark:bg-stone-700 text-stone-900 dark:text-stone-100 shadow-sm"
            : "text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200"
        }`}
        aria-label="查看对话"
        aria-pressed={mobileView === "chat"}
      >
        对话
      </button>
    </div>
  );

  return (
    <AntiCaptureOverlay>
      <AntiCheatShell enabled>
        <div className="h-[calc(100vh-var(--topbar-height)-24px)] flex relative select-none">
          {/* LEFT SIDEBAR: Topic Browser - Hidden on mobile */}
          <AnimatePresence>
            {sidebarOpen && !isMobile && (
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: 256, opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
                className="shrink-0 border-r border-stone-200 dark:border-stone-700 bg-white dark:bg-surfaceDark-card overflow-hidden flex flex-col rounded-l-2xl shadow-lg"
              >
                <TopicBrowser
                  problems={problems}
                  topicGroups={topicGroups}
                  selectedProblemId={selectedProblemId}
                  onSelectProblem={setSelectedProblemId}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Mobile sidebar overlay */}
          <AnimatePresence>
            {sidebarOpen && isMobile && (
              <>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
                  onClick={() => setSidebarOpen(false)}
                />
                <motion.div
                  initial={{ x: "-100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "-100%" }}
                  transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
                  className="fixed left-0 top-0 bottom-0 z-50 w-[280px] bg-white dark:bg-surfaceDark-card shadow-elevated dark:shadow-elevated-dark"
                >
                  <div className="flex items-center justify-between p-4 border-b border-stone-200 dark:border-stone-700">
                    <h2 className="font-semibold text-stone-900 dark:text-stone-100">选择主题</h2>
                    <button
                      onClick={() => setSidebarOpen(false)}
                      className="p-2 rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800 tap-target"
                      aria-label="关闭侧边栏"
                    >
                      <Minimize2 className="w-4 h-4" />
                    </button>
                  </div>
                  <TopicBrowser
                    problems={problems}
                    topicGroups={topicGroups}
                    selectedProblemId={selectedProblemId}
                    onSelectProblem={(id) => {
                      setSelectedProblemId(id);
                      setSidebarOpen(false);
                    }}
                  />
                </motion.div>
              </>
            )}
          </AnimatePresence>

          {/* MAIN AREA: Problem + Chat */}
          <div ref={rightRef} className="flex-1 flex min-w-0 relative">
            {/* Problem Panel */}
            <div
              className={`flex flex-col min-h-0 border-r border-stone-200 dark:border-stone-700 bg-white dark:bg-surfaceDark-card overflow-hidden transition-all duration-300 ${
                isMobile ? (mobileView === "problem" ? "w-full" : "hidden") : ""
              }`}
              style={isMobile ? undefined : { width: `${splitPercent}%` }}
            >
              {/* Header bar - Enhanced */}
              <div className="flex items-center gap-3 px-4 py-2 border-b border-stone-200 dark:border-stone-700 bg-white dark:bg-surfaceDark-card shrink-0 shadow-sm">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-1.5 rounded-lg hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-300 transition-all tap-target"
                  title={sidebarOpen ? "收起侧边栏" : "展开侧边栏"}
                  aria-label={sidebarOpen ? "收起侧边栏" : "展开侧边栏"}
                >
                  {sidebarOpen ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeft className="w-4 h-4" />}
                </button>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 text-xs font-semibold bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 rounded-lg border border-brand-200 dark:border-brand-800">
                    {domainId.toUpperCase()}
                  </span>
                  <span className="text-xs text-stone-400 dark:text-stone-500 font-medium">{t("teach.title", { defaultValue: "教学" })}</span>
                </div>

                {/* Mobile view toggle */}
                {isMobile && <MobileViewToggle />}

                <div className="flex-1" />
                <ProctorBadge />
              </div>

              <ProblemPanel
                problem={currentProblem}
                masteryPercent={masteryPercent}
                codeModifications={codeModifications}
                problemIndex={indexInTopic}
                totalProblems={problemsInTopic.length}
                onPrev={goPrevInTopic}
                onNext={goNextInTopic}
                onSkip={goSkip}
                loading={problemsLoading}
                userId={userData?.id}
                username={userData?.username}
                onLineClick={handleLineClick}
                topicLabel={topicGroups.find((tg) => tg.name === currentTopicGroup)?.label}
              />
            </div>

            {/* DRAG HANDLE - Hidden on mobile */}
            {!isMobile && (
              <div
                onMouseDown={handleMouseDown}
                className="w-1.5 shrink-0 cursor-col-resize bg-stone-100 dark:bg-stone-800 hover:bg-brand-400 dark:hover:bg-brand-600 hover:w-2 transition-all duration-150 flex items-center justify-center z-10 group"
                role="separator"
                aria-orientation="vertical"
                aria-label="调整面板大小"
              >
                <GripVertical className="w-3 h-3 text-stone-400 dark:text-stone-600 group-hover:text-brand-600 dark:group-hover:text-brand-300 transition-colors" />
              </div>
            )}

            {/* Chat Panel */}
            <div
              className={`flex flex-col min-h-0 bg-white dark:bg-surfaceDark-card overflow-hidden rounded-r-2xl shadow-lg transition-all duration-300 ${
                isMobile ? (mobileView === "chat" ? "w-full" : "hidden") : ""
              }`}
              style={isMobile ? undefined : { width: `${100 - splitPercent}%` }}
            >
              {/* Mobile header for chat */}
              {isMobile && mobileView === "chat" && (
                <div className="flex items-center gap-3 px-4 py-2 border-b border-stone-200 dark:border-stone-700 bg-white dark:bg-surfaceDark-card shrink-0">
                  <MobileViewToggle />
                  <div className="flex-1" />
                </div>
              )}
              <ChatPanel
                taId={currentTaId}
                problemContext={currentProblem ? { problem_id: currentProblem.problem_id, problem_type: currentProblem.problem_type } : undefined}
                lineRef={lineRef}
                onLineRefUsed={() => setLineRef(null)}
              />
            </div>

            {/* MASTERED BANNER - Enhanced */}
            <AnimatePresence>
              {showMasteredBanner && (
                <motion.div
                  initial={{ opacity: 0, y: 30, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 30, scale: 0.95 }}
                  transition={{ type: "spring", damping: 20, stiffness: 300 }}
                  className="absolute bottom-8 left-1/2 -translate-x-1/2 z-50 px-4"
                >
                  <div className="flex items-center gap-4 bg-gradient-to-r from-emerald-600 to-emerald-500 text-white px-6 py-4 rounded-2xl shadow-2xl ring-1 ring-emerald-400/30 max-w-[90vw] sm:max-w-md">
                    <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center shrink-0">
                      <Trophy className="w-6 h-6 text-yellow-300" />
                    </div>
                    <div className="min-w-0">
                      <p className="font-bold text-base">
                        {t("teach.masteredBanner", { defaultValue: "主题已掌握!" })}
                      </p>
                      <p className="text-sm text-emerald-100/90 hidden sm:block">
                        {t("teach.masteredDesc", { defaultValue: "已达到 80% 掌握度。准备好迎接下一个挑战了吗?" })}
                      </p>
                    </div>
                    <Button
                      variant="outline"
                      icon={ArrowRight}
                      onClick={goNextTopic}
                      className="ml-2 border-white/40 text-white hover:bg-white/20 hover:border-white/60 shrink-0"
                    >
                      <span className="hidden sm:inline">{t("teach.nextTopic", { defaultValue: "下一主题" })}</span>
                      <span className="sm:hidden">下一</span>
                    </Button>
                    <button
                      onClick={() => setShowMasteredBanner(false)}
                      className="ml-1 p-1 text-emerald-200 hover:text-white hover:bg-white/10 rounded-lg transition-colors tap-target shrink-0"
                      aria-label="关闭"
                    >
                      ✕
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <ContextualHelp pageKey="teach" />
        </div>
      </AntiCheatShell>
    </AntiCaptureOverlay>
  );
}
