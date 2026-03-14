import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getProblems, getTA, runTest, runTestComprehensive } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProblemSelector } from "@/components/workspace/ProblemSelector";
import { TestResultCard } from "@/components/workspace/TestResultCard";
import { ComprehensiveReport } from "@/components/workspace/ComprehensiveReport";
import { Play, Lightbulb, GraduationCap } from "lucide-react";
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

  // Check if TA needs more teaching to unlock problems
  const hasUnlockableProblems = problems.length > 0;
  const learnedCount = (problemsData?.learned_unit_ids?.length ?? 0);
  const requiredCount = (problemsData?.required_kus?.length ?? 0);

  return (
    <div className="space-y-6">
      {/* Educational hint for problem unlocking */}
      {!hasUnlockableProblems && currentTaId && (
        <Card padding="md" className="bg-gradient-to-r from-amber-50 to-orange-50 border-amber-200">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-amber-100 rounded-lg">
              <GraduationCap className="w-5 h-5 text-amber-600" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-amber-900">Teach More Concepts to Unlock Tests</h3>
              <p className="mt-1 text-sm text-amber-800">
                Your TA needs to learn more concepts before it can attempt problems. 
                Go to the <strong>Teach</strong> page and teach concepts like variables, loops, or functions.
              </p>
              <div className="mt-3 flex items-center gap-2 text-xs text-amber-700">
                <Lightbulb className="w-4 h-4" />
                <span>Tip: Try teaching &quot;variable_assignment&quot; or &quot;print_function&quot; first!</span>
              </div>
            </div>
          </div>
        </Card>
      )}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <ProblemSelector
          problems={problems}
          value={selectedProblemId}
          onValueChange={setSelectedProblemId}
          disabled={!currentTaId}
          className="max-w-md"
        />
        <div className="flex gap-2">
          <Button
            icon={Play}
            loading={runTestMutation.isPending}
            onClick={() => runTestMutation.mutate(selectedProblemId)}
            disabled={!currentTaId}
          >
            Run Test
          </Button>
          <Button
            variant="secondary"
            icon={Play}
            loading={runComprehensiveMutation.isPending}
            onClick={() => runComprehensiveMutation.mutate()}
            disabled={!currentTaId}
          >
            Run Comprehensive
          </Button>
        </div>
      </div>

      {selectedProblem && (
        <Card padding="md">
          <h3 className="text-sm font-semibold text-slate-700">Selected problem</h3>
          <p className="mt-2 text-sm text-slate-600">{selectedProblem.problem_statement}</p>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
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
            <Card padding="md">
              <p className="text-sm text-slate-500">
                Select a problem (or leave Auto-select) and click Run Test or Run Comprehensive.
              </p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
