import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight, SkipForward, BookOpen, Bug, Code, Brain, FileText, ListChecks, Puzzle, Eye, Terminal, Star, Zap, Target, RefreshCw, GitCompare, Database } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { MasteryBar } from "./MasteryBar";
import { ProblemRenderer, type TeachProblem, type CodeModification } from "./ProblemRenderer";

const DIFFICULTY_CONFIG: Record<string, { label: string; labelKey: string; stars: number; color: string; bg: string; border: string; darkBg: string; darkBorder: string }> = {
  easy: { label: "简单", labelKey: "difficulty.easy", stars: 1, color: "text-emerald-700 dark:text-emerald-400", bg: "bg-emerald-50", border: "border-emerald-200", darkBg: "dark:bg-emerald-900/30", darkBorder: "dark:border-emerald-800" },
  remember: { label: "记忆", labelKey: "difficulty.remember", stars: 1, color: "text-emerald-700 dark:text-emerald-400", bg: "bg-emerald-50", border: "border-emerald-200", darkBg: "dark:bg-emerald-900/30", darkBorder: "dark:border-emerald-800" },
  medium: { label: "中等", labelKey: "difficulty.medium", stars: 2, color: "text-amber-700 dark:text-amber-400", bg: "bg-amber-50", border: "border-amber-200", darkBg: "dark:bg-amber-900/30", darkBorder: "dark:border-amber-800" },
  apply: { label: "应用", labelKey: "difficulty.apply", stars: 2, color: "text-amber-700 dark:text-amber-400", bg: "bg-amber-50", border: "border-amber-200", darkBg: "dark:bg-amber-900/30", darkBorder: "dark:border-amber-800" },
  hard: { label: "困难", labelKey: "difficulty.hard", stars: 3, color: "text-red-700 dark:text-red-400", bg: "bg-red-50", border: "border-red-200", darkBg: "dark:bg-red-900/30", darkBorder: "dark:border-red-800" },
  analyze: { label: "分析", labelKey: "difficulty.analyze", stars: 3, color: "text-red-700 dark:text-red-400", bg: "bg-red-50", border: "border-red-200", darkBg: "dark:bg-red-900/30", darkBorder: "dark:border-red-800" },
  transfer: { label: "迁移", labelKey: "difficulty.transfer", stars: 3, color: "text-purple-700 dark:text-purple-400", bg: "bg-purple-50", border: "border-purple-200", darkBg: "dark:bg-purple-900/30", darkBorder: "dark:border-purple-800" },
};

const TYPE_CONFIG: Record<string, { label: string; labelKey: string; icon: typeof Bug; color: string; bg: string; border: string; darkBg: string; darkBorder: string; desc: string; descKey: string }> = {
  "buggy-code": {
    label: "找Bug",
    labelKey: "type.buggyCode",
    icon: Bug,
    color: "text-red-700 dark:text-red-400",
    bg: "bg-red-50",
    border: "border-red-200",
    darkBg: "dark:bg-red-900/30",
    darkBorder: "dark:border-red-800",
    desc: "找出并解释错误",
    descKey: "type.buggyCodeDesc"
  },
  "output-prediction": {
    label: "预测输出",
    labelKey: "type.outputPrediction",
    icon: Eye,
    color: "text-blue-700 dark:text-blue-400",
    bg: "bg-blue-50",
    border: "border-blue-200",
    darkBg: "dark:bg-blue-900/30",
    darkBorder: "dark:border-blue-800",
    desc: "这段代码会输出什么?",
    descKey: "type.outputPredictionDesc"
  },
  "code-completion": {
    label: "补全代码",
    labelKey: "type.codeCompletion",
    icon: Code,
    color: "text-purple-700 dark:text-purple-400",
    bg: "bg-purple-50",
    border: "border-purple-200",
    darkBg: "dark:bg-purple-900/30",
    darkBorder: "dark:border-purple-800",
    desc: "填补缺失的部分",
    descKey: "type.codeCompletionDesc"
  },
  "multiple-choice": {
    label: "概念检查",
    labelKey: "type.multipleChoice",
    icon: ListChecks,
    color: "text-emerald-700 dark:text-emerald-400",
    bg: "bg-emerald-50",
    border: "border-emerald-200",
    darkBg: "dark:bg-emerald-900/30",
    darkBorder: "dark:border-emerald-800",
    desc: "测试你的理解",
    descKey: "type.multipleChoiceDesc"
  },
  "short-answer": {
    label: "写代码",
    labelKey: "type.shortAnswer",
    icon: FileText,
    color: "text-amber-700 dark:text-amber-400",
    bg: "bg-amber-50",
    border: "border-amber-200",
    darkBg: "dark:bg-amber-900/30",
    darkBorder: "dark:border-amber-800",
    desc: "通过写代码解决",
    descKey: "type.shortAnswerDesc"
  },
  parsons: {
    label: "Parsons拼图",
    labelKey: "type.parsons",
    icon: Puzzle,
    color: "text-orange-700 dark:text-orange-400",
    bg: "bg-orange-50",
    border: "border-orange-200",
    darkBg: "dark:bg-orange-900/30",
    darkBorder: "dark:border-orange-800",
    desc: "重新排序代码块",
    descKey: "type.parsonsDesc"
  },
  dropdown: {
    label: "填空",
    labelKey: "type.dropdown",
    icon: Terminal,
    color: "text-teal-700 dark:text-teal-400",
    bg: "bg-teal-50",
    border: "border-teal-200",
    darkBg: "dark:bg-teal-900/30",
    darkBorder: "dark:border-teal-800",
    desc: "选择正确的选项",
    descKey: "type.dropdownDesc"
  },
  "execution-trace": {
    label: "追踪代码",
    labelKey: "type.executionTrace",
    icon: Brain,
    color: "text-indigo-700 dark:text-indigo-400",
    bg: "bg-indigo-50",
    border: "border-indigo-200",
    darkBg: "dark:bg-indigo-900/30",
    darkBorder: "dark:border-indigo-800",
    desc: "跟随执行流程",
    descKey: "type.executionTraceDesc"
  },
  refactoring: {
    label: "重构代码",
    labelKey: "type.refactoring",
    icon: RefreshCw,
    color: "text-cyan-700 dark:text-cyan-400",
    bg: "bg-cyan-50",
    border: "border-cyan-200",
    darkBg: "dark:bg-cyan-900/30",
    darkBorder: "dark:border-cyan-800",
    desc: "改进代码质量",
    descKey: "type.refactoringDesc"
  },
  matching: {
    label: "概念配对",
    labelKey: "type.matching",
    icon: GitCompare,
    color: "text-pink-700 dark:text-pink-400",
    bg: "bg-pink-50",
    border: "border-pink-200",
    darkBg: "dark:bg-pink-900/30",
    darkBorder: "dark:border-pink-800",
    desc: "连接概念与定义",
    descKey: "type.matchingDesc"
  },
  "schema-design": {
    label: "设计Schema",
    labelKey: "type.schemaDesign",
    icon: Database,
    color: "text-sky-700 dark:text-sky-400",
    bg: "bg-sky-50",
    border: "border-sky-200",
    darkBg: "dark:bg-sky-900/30",
    darkBorder: "dark:border-sky-800",
    desc: "创建数据库结构",
    descKey: "type.schemaDesignDesc"
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
      <div className="flex flex-col h-full items-center justify-center text-stone-400 dark:text-stone-500 bg-white dark:bg-surfaceDark-card" role="status" aria-live="polite">
        <div className="w-10 h-10 border-3 border-stone-200 dark:border-stone-700 border-t-brand-500 rounded-full animate-spin mb-4" aria-hidden="true" />
        <p className="text-sm font-medium text-stone-500 dark:text-stone-400">{t("common.loading", { defaultValue: "加载问题中..." })}</p>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex flex-col h-full items-center justify-center text-stone-400 dark:text-stone-500 bg-white dark:bg-surfaceDark-card px-8" role="status">
        <div className="w-16 h-16 bg-stone-100 dark:bg-stone-800 rounded-2xl flex items-center justify-center mb-4" aria-hidden="true">
          <BookOpen className="w-8 h-8 text-stone-300 dark:text-stone-600" />
        </div>
        <p className="text-base font-semibold text-stone-600 dark:text-stone-300 mb-2">
          {t("teach.selectTopic", { defaultValue: "选择主题开始" })}
        </p>
        <p className="text-sm text-center text-stone-400 dark:text-stone-500 max-w-xs leading-relaxed">
          {t("teach.selectTopicDesc", { defaultValue: "从侧边栏选择主题来浏览问题。每个主题包含不同类型的问题帮助你学习。" })}
        </p>
      </div>
    );
  }

  const typeConf = TYPE_CONFIG[problem.problem_type] || {
    label: problem.problem_type,
    labelKey: "",
    icon: FileText,
    color: "text-stone-700 dark:text-stone-300",
    bg: "bg-stone-50",
    border: "border-stone-200",
    darkBg: "dark:bg-stone-800",
    darkBorder: "dark:border-stone-700",
    desc: "",
    descKey: ""
  };
  const TypeIcon = typeConf.icon;
  const diffConf = DIFFICULTY_CONFIG[problem.difficulty || "medium"];

  // Limit KU display to 3 + more indicator
  const kuList = problem.knowledge_units_tested || [];
  const displayKUs = kuList.slice(0, 3);
  const moreKUs = kuList.length - 3;

  return (
    <div className="flex flex-col h-full bg-white dark:bg-surfaceDark-card transition-colors duration-300">
      {/* Header - Two rows */}
      <div className="px-4 py-3 border-b border-stone-200 dark:border-stone-700 shrink-0 space-y-3">
        {/* Row 1: Topic + Mastery + Progress */}
        <div className="flex items-center gap-4">
          <div className="flex-1 min-w-0">
            {topicLabel && (
              <p className="text-xs font-medium text-stone-400 dark:text-stone-500 uppercase tracking-wider mb-1">
                {topicLabel}
              </p>
            )}
          </div>

          {/* Progress indicator */}
          <div
            className="flex items-center gap-2 text-xs text-stone-500 dark:text-stone-400 bg-stone-100 dark:bg-stone-800 px-3 py-1.5 rounded-lg shrink-0"
            role="progressbar"
            aria-valuenow={problemIndex + 1}
            aria-valuemin={1}
            aria-valuemax={totalProblems}
            aria-label={`问题进度: ${problemIndex + 1} / ${totalProblems}`}
          >
            <Target className="w-3.5 h-3.5" aria-hidden="true" />
            <span className="font-medium">{problemIndex + 1}</span>
            <span className="text-stone-400 dark:text-stone-500">/</span>
            <span>{totalProblems}</span>
          </div>
        </div>

        {/* Mastery bar */}
        <MasteryBar percent={masteryPercent} showLabel={true} />

        {/* Row 2: Badges */}
        <div className="flex items-center gap-2 flex-wrap" role="list" aria-label="问题属性">
          {/* Difficulty badge with stars */}
          <div
            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border ${diffConf.bg} ${diffConf.darkBg} ${diffConf.border} ${diffConf.darkBorder} ${diffConf.color}`}
            role="listitem"
            aria-label={`难度: ${diffConf.label}, ${diffConf.stars}星`}
          >
            <div className="flex gap-0.5" aria-hidden="true">
              {Array.from({ length: diffConf.stars }).map((_, i) => (
                <Star key={i} className="w-3 h-3 fill-current" />
              ))}
            </div>
            <span className="text-xs font-semibold">{diffConf.label}</span>
          </div>

          {/* Type badge with tooltip description */}
          <div
            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border ${typeConf.bg} ${typeConf.darkBg} ${typeConf.border} ${typeConf.darkBorder}`}
            role="listitem"
            aria-label={`问题类型: ${typeConf.label}. ${typeConf.desc}`}
            title={typeConf.desc}
          >
            <TypeIcon className={`w-3.5 h-3.5 ${typeConf.color}`} aria-hidden="true" />
            <span className={`text-xs font-semibold ${typeConf.color}`}>{typeConf.label}</span>
          </div>

          {/* Knowledge unit chips */}
          {displayKUs.map((ku, i) => (
            <span
              key={i}
              className="text-[10px] bg-stone-100 dark:bg-stone-800 text-stone-500 dark:text-stone-400 px-2 py-0.5 rounded-full border border-stone-200 dark:border-stone-700"
              role="listitem"
              aria-label={`知识点: ${ku.replace(/_/g, " ")}`}
            >
              {ku.replace(/_/g, " ")}
            </span>
          ))}
          {moreKUs > 0 && (
            <span
              className="text-[10px] bg-stone-100 dark:bg-stone-800 text-stone-500 dark:text-stone-400 px-2 py-0.5 rounded-full border border-stone-200 dark:border-stone-700"
              role="listitem"
              aria-label={`还有 ${moreKUs} 个知识点`}
            >
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
      <div className="flex items-center justify-between px-4 py-3 border-t border-stone-200 dark:border-stone-700 bg-white dark:bg-surfaceDark-card shrink-0">
        <Button
          variant="outline"
          icon={ChevronLeft}
          onClick={onPrev}
          disabled={problemIndex <= 0}
          className="text-sm tap-target"
          aria-label="上一个问题"
        >
          {t("teach.prev", { defaultValue: "上一题" })}
        </Button>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            icon={SkipForward}
            onClick={onSkip}
            disabled={totalProblems <= 1}
            className="text-xs text-stone-500 dark:text-stone-400 hover:text-stone-700 dark:hover:text-stone-300 tap-target"
            aria-label="跳过当前问题"
          >
            {t("teach.skip", { defaultValue: "跳过" })}
          </Button>
        </div>

        <Button
          icon={ChevronRight}
          onClick={onNext}
          disabled={problemIndex >= totalProblems - 1}
          className="text-sm tap-target"
          aria-label="下一个问题"
        >
          {t("teach.next", { defaultValue: "下一题" })}
        </Button>
      </div>
    </div>
  );
}
