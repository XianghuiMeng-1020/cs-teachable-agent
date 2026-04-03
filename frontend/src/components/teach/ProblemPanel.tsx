import { useTranslation } from "react-i18next";
import { ChevronLeft, ChevronRight, SkipForward, BookOpen, Bug, Code, Brain, FileText, ListChecks, Puzzle, Eye, Terminal } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { MasteryThermometer } from "./MasteryThermometer";
import { ProblemRenderer, type TeachProblem, type CodeModification } from "./ProblemRenderer";

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-emerald-100 text-emerald-700 border-emerald-200",
  remember: "bg-emerald-100 text-emerald-700 border-emerald-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  apply: "bg-amber-100 text-amber-700 border-amber-200",
  hard: "bg-red-100 text-red-700 border-red-200",
  analyze: "bg-red-100 text-red-700 border-red-200",
};

const TYPE_CONFIG: Record<string, { label: string; icon: typeof Bug; color: string }> = {
  "buggy-code": { label: "Debug", icon: Bug, color: "bg-red-50 text-red-700 border-red-200" },
  "output-prediction": { label: "Predict Output", icon: Eye, color: "bg-blue-50 text-blue-700 border-blue-200" },
  "code-completion": { label: "Complete Code", icon: Code, color: "bg-purple-50 text-purple-700 border-purple-200" },
  "multiple-choice": { label: "Concept", icon: ListChecks, color: "bg-emerald-50 text-emerald-700 border-emerald-200" },
  "short-answer": { label: "Code Answer", icon: FileText, color: "bg-amber-50 text-amber-700 border-amber-200" },
  parsons: { label: "Parsons Puzzle", icon: Puzzle, color: "bg-orange-50 text-orange-700 border-orange-200" },
  dropdown: { label: "Fill in Blanks", icon: Terminal, color: "bg-teal-50 text-teal-700 border-teal-200" },
  "execution-trace": { label: "Trace Execution", icon: Brain, color: "bg-indigo-50 text-indigo-700 border-indigo-200" },
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
  topicLabel?: string;
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
  topicLabel,
}: ProblemPanelProps) {
  const { t } = useTranslation();

  if (loading) {
    return (
      <div className="flex flex-col h-full items-center justify-center text-stone-400">
        <div className="w-8 h-8 border-2 border-stone-300 border-t-brand-600 rounded-full animate-spin mb-3" />
        <p className="text-sm">{t("common.loading", { defaultValue: "Loading problems..." })}</p>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex flex-col h-full items-center justify-center text-stone-400 px-6">
        <BookOpen className="w-12 h-12 mb-3 opacity-40" />
        <p className="text-sm font-medium text-stone-600 mb-1">
          {t("teach.selectTopic", { defaultValue: "Select a topic to start" })}
        </p>
        <p className="text-xs text-center text-stone-400 max-w-[240px]">
          {t("teach.selectTopicDesc", { defaultValue: "Choose a topic from the sidebar to browse problems. Each topic contains different problem types to help you learn." })}
        </p>
      </div>
    );
  }

  const typeConf = TYPE_CONFIG[problem.problem_type] || { label: problem.problem_type, icon: FileText, color: "bg-stone-50 text-stone-700 border-stone-200" };
  const TypeIcon = typeConf.icon;

  return (
    <div className="flex flex-col h-full">
      {/* Top bar: mastery + problem info */}
      <div className="flex items-center gap-3 px-4 py-2.5 border-b border-stone-200 bg-white shrink-0">
        <MasteryThermometer percent={masteryPercent} className="h-14" />

        <div className="flex-1 min-w-0">
          {topicLabel && (
            <p className="text-[10px] font-medium text-stone-500 uppercase tracking-wider mb-0.5">{topicLabel}</p>
          )}
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded border text-[10px] font-semibold ${DIFFICULTY_COLORS[problem.difficulty ?? ""] ?? "bg-stone-100 text-stone-600 border-stone-200"}`}>
              {problem.difficulty ?? "?"}
            </span>
            <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded border text-[10px] font-semibold ${typeConf.color}`}>
              <TypeIcon className="w-3 h-3" />
              {typeConf.label}
            </span>
          </div>
          <p className="text-[10px] text-stone-400 mt-0.5 truncate">
            {problem.knowledge_units_tested?.join(", ")}
          </p>
        </div>

        <span className="text-xs text-stone-400 shrink-0 bg-stone-100 px-2 py-0.5 rounded-full">
          {problemIndex + 1}/{totalProblems}
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
        <Button variant="outline" icon={SkipForward} onClick={onSkip} disabled={totalProblems <= 1}>
          {t("teach.skip", { defaultValue: "Skip" })}
        </Button>
        <Button icon={ChevronRight} onClick={onNext} disabled={problemIndex >= totalProblems - 1}>
          {t("teach.next", { defaultValue: "Next" })}
        </Button>
      </div>
    </div>
  );
}
