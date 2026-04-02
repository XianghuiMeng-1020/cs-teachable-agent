import { useTranslation } from "react-i18next";
import { ChevronLeft, ChevronRight, SkipForward, Lock } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { MasteryThermometer } from "./MasteryThermometer";
import { ProblemRenderer, type TeachProblem, type CodeModification } from "./ProblemRenderer";

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-emerald-100 text-emerald-700",
  remember: "bg-emerald-100 text-emerald-700",
  medium: "bg-amber-100 text-amber-700",
  apply: "bg-amber-100 text-amber-700",
  hard: "bg-red-100 text-red-700",
  analyze: "bg-red-100 text-red-700",
};

const TYPE_LABELS: Record<string, string> = {
  "buggy-code": "Debug",
  "output-prediction": "Predict Output",
  "code-completion": "Complete Code",
  "multiple-choice": "Concept",
  "short-answer": "Code Answer",
  parsons: "Parsons Puzzle",
  dropdown: "Fill in Blanks",
  "execution-trace": "Trace Execution",
};

interface ProblemPanelProps {
  problem: TeachProblem | null;
  masteryPercent: number;
  codeModifications: CodeModification[];
  problemIndex: number;
  totalProblems: number;
  onPrev: () => void;
  onNext: () => void;
  onSkip: () => void;
  loading?: boolean;
  userId?: number;
  username?: string;
  onLineClick?: (lineNum: number, lineContent: string) => void;
}

export function ProblemPanel({
  problem,
  masteryPercent,
  codeModifications,
  problemIndex,
  totalProblems,
  onPrev,
  onNext,
  onSkip,
  loading,
  userId,
  username,
  onLineClick,
}: ProblemPanelProps) {
  const { t } = useTranslation();

  if (loading || !problem) {
    return (
      <div className="flex flex-col h-full items-center justify-center text-stone-400">
        <Lock className="w-8 h-8 mb-2" />
        <p className="text-sm">{loading ? t("common.loading", { defaultValue: "Loading..." }) : t("teach.noProblem", { defaultValue: "No problem available" })}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Top bar: mastery + problem info */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-stone-200 bg-white shrink-0">
        <MasteryThermometer percent={masteryPercent} className="h-14" />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wide ${DIFFICULTY_COLORS[problem.difficulty ?? ""] ?? "bg-stone-100 text-stone-600"}`}>
              {problem.difficulty ?? "?"}
            </span>
            <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-700 text-[10px] font-semibold uppercase tracking-wide">
              {TYPE_LABELS[problem.problem_type] ?? problem.problem_type}
            </span>
            {problem.topic_group && (
              <span className="text-[10px] text-stone-500 font-medium">{problem.topic_group}</span>
            )}
          </div>
          <p className="text-xs text-stone-500 mt-0.5 truncate">
            {problem.knowledge_units_tested?.join(", ")}
          </p>
        </div>

        <span className="text-xs text-stone-400 shrink-0">
          {problemIndex + 1} / {totalProblems}
        </span>
      </div>

      {/* Problem content */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <ProblemRenderer
          problem={problem}
          codeModifications={codeModifications}
          userId={userId}
          username={username}
          onLineClick={onLineClick}
        />
      </div>

      {/* Bottom nav */}
      <div className="flex items-center justify-between px-4 py-2 border-t border-stone-200 bg-white shrink-0">
        <Button variant="outline" icon={ChevronLeft} onClick={onPrev} disabled={problemIndex <= 0}>
          {t("teach.prev", { defaultValue: "Prev" })}
        </Button>
        <Button variant="outline" icon={SkipForward} onClick={onSkip}>
          {t("teach.skip", { defaultValue: "Skip" })}
        </Button>
        <Button icon={ChevronRight} onClick={onNext} disabled={problemIndex >= totalProblems - 1}>
          {t("teach.next", { defaultValue: "Next" })}
        </Button>
      </div>
    </div>
  );
}
