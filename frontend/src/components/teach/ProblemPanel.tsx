import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight, SkipForward, BookOpen, Bug, Code, Brain, FileText, ListChecks, Puzzle, Eye, Terminal, Star, Zap, Target } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { MasteryBar } from "./MasteryBar";
import { ProblemRenderer, type TeachProblem, type CodeModification } from "./ProblemRenderer";

const DIFFICULTY_CONFIG: Record<string, { label: string; stars: number; color: string; bg: string; border: string }> = {
  easy: { label: "Easy", stars: 1, color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200" },
  remember: { label: "Remember", stars: 1, color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200" },
  medium: { label: "Medium", stars: 2, color: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200" },
  apply: { label: "Apply", stars: 2, color: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200" },
  hard: { label: "Hard", stars: 3, color: "text-red-700", bg: "bg-red-50", border: "border-red-200" },
  analyze: { label: "Analyze", stars: 3, color: "text-red-700", bg: "bg-red-50", border: "border-red-200" },
  transfer: { label: "Transfer", stars: 3, color: "text-purple-700", bg: "bg-purple-50", border: "border-purple-200" },
};

const TYPE_CONFIG: Record<string, { label: string; icon: typeof Bug; color: string; bg: string; border: string; desc: string }> = {
  "buggy-code": { 
    label: "Find the Bug", 
    icon: Bug, 
    color: "text-red-700", 
    bg: "bg-red-50", 
    border: "border-red-200",
    desc: "Identify and explain the error"
  },
  "output-prediction": { 
    label: "Predict Output", 
    icon: Eye, 
    color: "text-blue-700", 
    bg: "bg-blue-50", 
    border: "border-blue-200",
    desc: "What will this code print?"
  },
  "code-completion": { 
    label: "Complete Code", 
    icon: Code, 
    color: "text-purple-700", 
    bg: "bg-purple-50", 
    border: "border-purple-200",
    desc: "Fill in the missing parts"
  },
  "multiple-choice": { 
    label: "Concept Check", 
    icon: ListChecks, 
    color: "text-emerald-700", 
    bg: "bg-emerald-50", 
    border: "border-emerald-200",
    desc: "Test your understanding"
  },
  "short-answer": { 
    label: "Write Code", 
    icon: FileText, 
    color: "text-amber-700", 
    bg: "bg-amber-50", 
    border: "border-amber-200",
    desc: "Solve by writing code"
  },
  parsons: { 
    label: "Parsons Puzzle", 
    icon: Puzzle, 
    color: "text-orange-700", 
    bg: "bg-orange-50", 
    border: "border-orange-200",
    desc: "Reorder the code blocks"
  },
  dropdown: { 
    label: "Fill Blanks", 
    icon: Terminal, 
    color: "text-teal-700", 
    bg: "bg-teal-50", 
    border: "border-teal-200",
    desc: "Select the correct options"
  },
  "execution-trace": { 
    label: "Trace Code", 
    icon: Brain, 
    color: "text-indigo-700", 
    bg: "bg-indigo-50", 
    border: "border-indigo-200",
    desc: "Follow the execution flow"
  },
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
      <div className="flex flex-col h-full items-center justify-center text-stone-400 bg-white">
        <div className="w-10 h-10 border-3 border-stone-200 border-t-brand-500 rounded-full animate-spin mb-4" />
        <p className="text-sm font-medium text-stone-500">{t("common.loading", { defaultValue: "Loading problems..." })}</p>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex flex-col h-full items-center justify-center text-stone-400 bg-white px-8">
        <div className="w-16 h-16 bg-stone-100 rounded-2xl flex items-center justify-center mb-4">
          <BookOpen className="w-8 h-8 text-stone-300" />
        </div>
        <p className="text-base font-semibold text-stone-600 mb-2">
          {t("teach.selectTopic", { defaultValue: "Select a topic to begin" })}
        </p>
        <p className="text-sm text-center text-stone-400 max-w-xs leading-relaxed">
          {t("teach.selectTopicDesc", { defaultValue: "Choose a topic from the sidebar to browse problems. Each topic contains different problem types to help you learn." })}
        </p>
      </div>
    );
  }

  const typeConf = TYPE_CONFIG[problem.problem_type] || { 
    label: problem.problem_type, 
    icon: FileText, 
    color: "text-stone-700", 
    bg: "bg-stone-50", 
    border: "border-stone-200",
    desc: ""
  };
  const TypeIcon = typeConf.icon;
  const diffConf = DIFFICULTY_CONFIG[problem.difficulty || "medium"];

  // Limit KU display to 3 + more indicator
  const kuList = problem.knowledge_units_tested || [];
  const displayKUs = kuList.slice(0, 3);
  const moreKUs = kuList.length - 3;

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header - Two rows */}
      <div className="px-4 py-3 border-b border-stone-200 shrink-0 space-y-3">
        {/* Row 1: Topic + Mastery + Progress */}
        <div className="flex items-center gap-4">
          <div className="flex-1 min-w-0">
            {topicLabel && (
              <p className="text-xs font-medium text-stone-400 uppercase tracking-wider mb-1">
                {topicLabel}
              </p>
            )}
          </div>
          
          {/* Progress indicator */}
          <div className="flex items-center gap-2 text-xs text-stone-500 bg-stone-100 px-3 py-1.5 rounded-lg shrink-0">
            <Target className="w-3.5 h-3.5" />
            <span className="font-medium">{problemIndex + 1}</span>
            <span className="text-stone-400">/</span>
            <span>{totalProblems}</span>
          </div>
        </div>

        {/* Mastery bar */}
        <MasteryBar percent={masteryPercent} showLabel={true} />

        {/* Row 2: Badges */}
        <div className="flex items-center gap-2 flex-wrap">
          {/* Difficulty badge with stars */}
          <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border ${diffConf.bg} ${diffConf.border} ${diffConf.color}`}>
            <div className="flex gap-0.5">
              {Array.from({ length: diffConf.stars }).map((_, i) => (
                <Star key={i} className="w-3 h-3 fill-current" />
              ))}
            </div>
            <span className="text-xs font-semibold">{diffConf.label}</span>
          </div>

          {/* Type badge */}
          <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border ${typeConf.bg} ${typeConf.border}`}>
            <TypeIcon className={`w-3.5 h-3.5 ${typeConf.color}`} />
            <span className={`text-xs font-semibold ${typeConf.color}`}>{typeConf.label}</span>
          </div>

          {/* Knowledge unit chips */}
          {displayKUs.map((ku, i) => (
            <span 
              key={i} 
              className="text-[10px] bg-stone-100 text-stone-500 px-2 py-0.5 rounded-full border border-stone-200"
            >
              {ku.replace(/_/g, " ")}
            </span>
          ))}
          {moreKUs > 0 && (
            <span className="text-[10px] bg-stone-100 text-stone-500 px-2 py-0.5 rounded-full border border-stone-200">
              +{moreKUs}
            </span>
          )}
        </div>
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

      {/* Bottom navigation bar */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-stone-200 bg-white shrink-0">
        <Button 
          variant="outline" 
          icon={ChevronLeft} 
          onClick={onPrev} 
          disabled={problemIndex <= 0}
          className="text-sm"
        >
          {t("teach.prev", { defaultValue: "Previous" })}
        </Button>
        
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            icon={SkipForward} 
            onClick={onSkip} 
            disabled={totalProblems <= 1}
            className="text-xs text-stone-500 hover:text-stone-700"
          >
            {t("teach.skip", { defaultValue: "Skip" })}
          </Button>
        </div>
        
        <Button 
          icon={ChevronRight} 
          onClick={onNext} 
          disabled={problemIndex >= totalProblems - 1}
          className="text-sm"
        >
          {t("teach.next", { defaultValue: "Next" })}
        </Button>
      </div>
    </div>
  );
}
