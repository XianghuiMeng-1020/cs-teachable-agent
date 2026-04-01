import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import { motion, AnimatePresence } from "framer-motion";
import { useAppStore } from "@/stores/appStore";
import { getProblems, getTA, runTest, runTestComprehensive } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProblemSelector } from "@/components/workspace/ProblemSelector";
import { TestResultCard } from "@/components/workspace/TestResultCard";
import { ComprehensiveReport } from "@/components/workspace/ComprehensiveReport";
import { ProblemUnlockPanel } from "@/components/workspace/ProblemUnlockPanel";
import { 
  Play, 
  Zap, 
  FileText, 
  Target,
  CheckCircle,
  XCircle,
  Trophy,
  Sparkles,
  BarChart3,
  AlertCircle,
  Clock,
} from "lucide-react";
import { toast } from "sonner";

// Animation variants
const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const scaleIn = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.3 } },
};

export function TestPage() {
  const { t } = useTranslation();
  const currentTaId = useAppStore((s) => s.currentTaId);
  const [selectedProblemId, setSelectedProblemId] = useState<string | null>(null);
  const [testMode, setTestMode] = useState<"single" | "comprehensive">("single");
  const [singleResult, setSingleResult] = useState<{
    problem_id: string;
    problem_statement: string;
    ta_code: string;
    passed: boolean;
    details: { input?: string; expected?: string; got?: string; passed?: boolean }[];
    reflection_prompt?: string | null;
  } | null>(null);
  const [comprehensiveResult, setComprehensiveResult] = useState<{
    total_run: number;
    total_passed: number;
    results: { problem_id: string; passed: boolean; problem_statement: string }[];
    overall_summary: string;
  } | null>(null);

  const queryClient = useQueryClient();

  const { data: taData } = useQuery({
    queryKey: ["ta", currentTaId],
    queryFn: () => getTA(currentTaId!),
    enabled: currentTaId != null,
  });
  const domainId = (taData?.domain_id as "python" | "database" | "ai_literacy") ?? "python";

  const { data: problemsData } = useQuery({
    queryKey: ["ta", currentTaId, "problems"],
    queryFn: () => getProblems(currentTaId!),
    enabled: currentTaId != null,
  });

  const problems = problemsData?.problems ?? [];
  const outputLabel =
    domainId === "database"
      ? t("test.taSQL")
      : domainId === "ai_literacy"
        ? t("test.taAnswer")
        : t("test.taCode");
  const selectedProblem = selectedProblemId
    ? problems.find((p: { problem_id: string }) => p.problem_id === selectedProblemId)
    : null;

  const runTestMutation = useMutation({
    mutationFn: (problemId: string | null) =>
      runTest(currentTaId!, problemId ?? undefined),
    onSuccess: (data) => {
      setSingleResult({
        problem_id: data.problem_id,
        problem_statement: data.problem_statement,
        ta_code: data.ta_code,
        passed: data.passed,
        details: data.details ?? [],
        reflection_prompt: data.reflection_prompt ?? null,
      });
      setComprehensiveResult(null);
      setTestMode("single");
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "state"] });
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "mastery"] });
      toast.success(data.passed ? t("test.testPassed") : t("test.testFailed"), {
        duration: 3000,
      });
    },
    onError: (err) => toast.error(err instanceof Error ? err.message : t("test.testFailed")),
  });

  const runComprehensiveMutation = useMutation({
    mutationFn: () => runTestComprehensive(currentTaId!),
    onSuccess: (data) => {
      setComprehensiveResult(data);
      setSingleResult(null);
      setTestMode("comprehensive");
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "state"] });
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "mastery"] });
      const percentage = Math.round((data.total_passed / data.total_run) * 100);
      toast.success(
        <div>
          <div className="font-semibold">{t("test.comprehensiveReport")}</div>
          <div className="text-sm">
            {data.total_passed}/{data.total_run} {t("test.passed")} ({percentage}%)
          </div>
        </div>,
        { duration: 4000 }
      );
    },
    onError: (err) => toast.error(err instanceof Error ? err.message : t("test.testFailed")),
  });

  const eligibleIds = problemsData?.eligible_ids ?? [];
  const learnedUnitIds = problemsData?.learned_unit_ids ?? [];
  const requiredKus = problemsData?.required_kus ?? [];

  const passRate = comprehensiveResult 
    ? Math.round((comprehensiveResult.total_passed / comprehensiveResult.total_run) * 100)
    : singleResult?.passed ? 100 : 0;

  return (
    <motion.div 
      variants={fadeIn}
      initial="hidden"
      animate="visible"
      className="space-y-6 max-w-6xl mx-auto"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg">
            <Target className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-stone-900">{t("test.title")}</h1>
            <p className="text-sm text-stone-500">
              {t("test.desc")}
            </p>
          </div>
        </div>
        
        {/* Stats Badge */}
        {(singleResult || comprehensiveResult) && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`flex items-center gap-2 px-4 py-2 rounded-full ${
              (comprehensiveResult?.total_passed === comprehensiveResult?.total_run) || singleResult?.passed
                ? "bg-emerald-100 text-emerald-700"
                : "bg-amber-100 text-amber-700"
            }`}
          >
            {(comprehensiveResult?.total_passed === comprehensiveResult?.total_run) || singleResult?.passed
              ? <CheckCircle className="w-5 h-5" />
              : <AlertCircle className="w-5 h-5" />
            }
            <span className="font-semibold">
              {comprehensiveResult 
                ? t("test.passRateLabel", { rate: passRate })
                : singleResult?.passed ? t("test.testPassed") : t("test.testFailed")
              }
            </span>
          </motion.div>
        )}
      </div>

      {/* Problem Unlock Panel */}
      {currentTaId && (
        <ProblemUnlockPanel
          problems={problems}
          eligibleIds={eligibleIds}
          learnedUnitIds={learnedUnitIds}
          requiredKus={requiredKus}
          currentTaId={currentTaId}
        />
      )}

      {/* Test Controls Card */}
      <Card padding="lg" className="bg-gradient-to-br from-stone-50 to-white">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Problem Selection */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-stone-700 flex items-center gap-2">
              <FileText className="w-4 h-4 text-brand-600" />
              {t("test.selectProblem")}
            </label>
            <ProblemSelector
              problems={problems}
              value={selectedProblemId}
              onValueChange={setSelectedProblemId}
              disabled={!currentTaId}
            />
            {selectedProblem && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                className="mt-3 p-3 bg-brand-50 rounded-lg border border-brand-100"
              >
                <p className="text-sm text-brand-800">{selectedProblem.problem_statement}</p>
              </motion.div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col justify-end">
            <label className="mb-2 block text-sm font-semibold text-stone-700 flex items-center gap-2">
              <Play className="w-4 h-4 text-brand-600" />
              {t("test.runTest")}
            </label>
            <div className="flex gap-3">
              <Button
                icon={Play}
                loading={runTestMutation.isPending}
                onClick={() => runTestMutation.mutate(selectedProblemId)}
                disabled={!currentTaId}
                className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
              >
                Run Single Test
              </Button>
              <Button
                variant="outline"
                icon={Zap}
                loading={runComprehensiveMutation.isPending}
                onClick={() => runComprehensiveMutation.mutate()}
                disabled={!currentTaId}
                className="flex-1"
              >
                {t("test.runAll")}
              </Button>
            </div>
            <p className="mt-2 text-xs text-stone-500">
              {t("test.singleDesc")} • {t("test.allDesc")}
            </p>
          </div>
        </div>
      </Card>

      {/* Results Section */}
      <AnimatePresence mode="wait">
        {testMode === "single" && singleResult && (
          <motion.div
            key="single"
            variants={scaleIn}
            initial="hidden"
            animate="visible"
            exit={{ opacity: 0, scale: 0.95 }}
          >
            <TestResultCard
              problemId={singleResult.problem_id}
              problemStatement={singleResult.problem_statement}
              taCode={singleResult.ta_code}
              passed={singleResult.passed}
              details={singleResult.details}
              defaultExpanded
              outputLabel={outputLabel}
              reflectionPrompt={singleResult.reflection_prompt}
            />
          </motion.div>
        )}

        {testMode === "comprehensive" && comprehensiveResult && (
          <motion.div
            key="comprehensive"
            variants={scaleIn}
            initial="hidden"
            animate="visible"
            exit={{ opacity: 0, scale: 0.95 }}
            className="space-y-6"
          >
            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl p-4 text-white">
                <div className="flex items-center gap-2 mb-1">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm font-medium text-emerald-100">{t("test.passed")}</span>
                </div>
                <div className="text-3xl font-bold">{comprehensiveResult.total_passed}</div>
              </div>
              <div className="bg-gradient-to-br from-rose-500 to-pink-600 rounded-xl p-4 text-white">
                <div className="flex items-center gap-2 mb-1">
                  <XCircle className="w-5 h-5" />
                  <span className="text-sm font-medium text-rose-100">{t("test.failed")}</span>
                </div>
                <div className="text-3xl font-bold">
                  {comprehensiveResult.total_run - comprehensiveResult.total_passed}
                </div>
              </div>
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-4 text-white">
                <div className="flex items-center gap-2 mb-1">
                  <BarChart3 className="w-5 h-5" />
                  <span className="text-sm font-medium text-blue-100">{t("test.total")}</span>
                </div>
                <div className="text-3xl font-bold">{comprehensiveResult.total_run}</div>
              </div>
              <div className={`rounded-xl p-4 text-white ${
                passRate >= 80 
                  ? "bg-gradient-to-br from-amber-400 to-orange-500"
                  : passRate >= 50
                  ? "bg-gradient-to-br from-violet-500 to-purple-600"
                  : "bg-gradient-to-br from-stone-500 to-stone-600"
              }`}>
                <div className="flex items-center gap-2 mb-1">
                  <Trophy className="w-5 h-5" />
                  <span className="text-sm font-medium text-white/80">{t("dashboard.passRate")}</span>
                </div>
                <div className="text-3xl font-bold">{passRate}%</div>
              </div>
            </div>

            {/* Detailed Report */}
            <Card padding="lg">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-brand-100 flex items-center justify-center">
                  <FileText className="w-5 h-5 text-brand-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-stone-900">{t("test.comprehensiveReport")}</h3>
                  <p className="text-sm text-stone-500">{t("test.comprehensiveReportDesc")}</p>
                </div>
              </div>
              <ComprehensiveReport
                totalRun={comprehensiveResult.total_run}
                totalPassed={comprehensiveResult.total_passed}
                results={comprehensiveResult.results}
                overallSummary={comprehensiveResult.overall_summary}
              />
            </Card>
          </motion.div>
        )}

        {!singleResult && !comprehensiveResult && (
          <motion.div
            key="empty"
            variants={fadeIn}
            initial="hidden"
            animate="visible"
          >
            <Card padding="xl" className="text-center border-dashed border-2 border-stone-200">
              <div className="py-12">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-stone-100 to-stone-50 flex items-center justify-center mx-auto mb-6">
                  <Play className="w-10 h-10 text-stone-300" />
                </div>
                <h3 className="text-xl font-semibold text-stone-900 mb-2">{t("test.readyTitle")}</h3>
                <p className="text-stone-500 mb-2 max-w-md mx-auto">
                  {t("test.readyDesc")}
                </p>
                <p className="text-sm text-stone-400 mb-6">
                  {t("test.readyHint")}
                </p>
                <div className="flex items-center justify-center gap-4 text-sm text-stone-500">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    <span>{t("test.testsRealtime")}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    <span>{t("test.instantFeedback")}</span>
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
      <ContextualHelp pageKey="test" />
    </motion.div>
  );
}
