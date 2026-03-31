import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getProblems, getTA, runTest, runTestComprehensive } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProblemSelector } from "@/components/workspace/ProblemSelector";
import { TestResultCard } from "@/components/workspace/TestResultCard";
import { ComprehensiveReport } from "@/components/workspace/ComprehensiveReport";
import { ProblemUnlockPanel } from "@/components/workspace/ProblemUnlockPanel";
import { Play, Zap, FileText } from "lucide-react";
import { toast } from "sonner";

export function TestPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const [selectedProblemId, setSelectedProblemId] = useState<string | null>(null);
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
  const outputLabel = domainId === "database" ? "TA's SQL" : domainId === "ai_literacy" ? "TA's answer" : "TA's code";
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
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "state"] });
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "mastery"] });
      toast.success(data.passed ? "Test passed" : "Test failed");
    },
    onError: (err) => toast.error(err instanceof Error ? err.message : "Test failed"),
  });

  const runComprehensiveMutation = useMutation({
    mutationFn: () => runTestComprehensive(currentTaId!),
    onSuccess: (data) => {
      setComprehensiveResult(data);
      setSingleResult(null);
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "state"] });
      queryClient.invalidateQueries({ queryKey: ["ta", currentTaId, "mastery"] });
      toast.success(`Completed: ${data.total_passed}/${data.total_run} passed`);
    },
    onError: (err) => toast.error(err instanceof Error ? err.message : "Comprehensive test failed"),
  });

  const eligibleIds = problemsData?.eligible_ids ?? [];
  const learnedUnitIds = problemsData?.learned_unit_ids ?? [];
  const requiredKus = problemsData?.required_kus ?? [];

  return (
    <div className="space-y-6">
      {/* Unlock panel */}
      {currentTaId && (
        <ProblemUnlockPanel
          problems={problems}
          eligibleIds={eligibleIds}
          learnedUnitIds={learnedUnitIds}
          requiredKus={requiredKus}
          currentTaId={currentTaId}
        />
      )}

      {/* Controls */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="flex-1">
          <label className="mb-1.5 block text-sm font-medium text-stone-700">Problem</label>
          <ProblemSelector
            problems={problems}
            value={selectedProblemId}
            onValueChange={setSelectedProblemId}
            disabled={!currentTaId}
            className="max-w-md"
          />
        </div>
        <div className="flex gap-2 shrink-0">
          <Button
            icon={Play}
            loading={runTestMutation.isPending}
            onClick={() => runTestMutation.mutate(selectedProblemId)}
            disabled={!currentTaId}
          >
            Run Test
          </Button>
          <Button
            variant="outline"
            icon={Zap}
            loading={runComprehensiveMutation.isPending}
            onClick={() => runComprehensiveMutation.mutate()}
            disabled={!currentTaId}
          >
            Run All
          </Button>
        </div>
      </div>

      {/* Selected problem preview */}
      {selectedProblem && (
        <Card padding="md">
          <div className="flex items-center gap-2 mb-2">
            <FileText className="h-4 w-4 text-stone-400" />
            <h3 className="text-sm font-semibold text-stone-800">Problem Description</h3>
          </div>
          <p className="text-sm leading-relaxed text-stone-600">{selectedProblem.problem_statement}</p>
        </Card>
      )}

      {/* Results */}
      <div className="grid gap-5 lg:grid-cols-2">
        <div>
          {singleResult && (
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
          )}
          {comprehensiveResult && (
            <Card padding="md">
              <ComprehensiveReport
                totalRun={comprehensiveResult.total_run}
                totalPassed={comprehensiveResult.total_passed}
                results={comprehensiveResult.results}
                overallSummary={comprehensiveResult.overall_summary}
              />
            </Card>
          )}
          {!singleResult && !comprehensiveResult && (
            <Card padding="lg" className="text-center">
              <div className="py-8">
                <Play className="mx-auto h-10 w-10 text-stone-300" />
                <p className="mt-3 text-sm font-medium text-stone-500">
                  Select a problem and run a test to see results
                </p>
                <p className="mt-1 text-xs text-stone-400">
                  Or use "Run All" for a comprehensive evaluation
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
