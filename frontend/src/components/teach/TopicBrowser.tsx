import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { ChevronDown, ChevronRight, Bug, Code, Brain, FileText, ListChecks, Puzzle, Eye, Terminal, CheckCircle2 } from "lucide-react";
import type { TeachProblem } from "./ProblemRenderer";

interface TopicGroup {
  name: string;
  label: string;
  count: number;
  mastery_percent: number;
  problem_types: string[];
}

interface TopicBrowserProps {
  problems: TeachProblem[];
  topicGroups: TopicGroup[];
  selectedProblemId: string | null;
  onSelectProblem: (problemId: string) => void;
  className?: string;
}

const TYPE_ICONS: Record<string, typeof Bug> = {
  "buggy-code": Bug,
  "output-prediction": Eye,
  "code-completion": Code,
  "multiple-choice": ListChecks,
  "short-answer": FileText,
  parsons: Puzzle,
  dropdown: Terminal,
  "execution-trace": Brain,
};

const TYPE_COLORS: Record<string, string> = {
  "buggy-code": "text-red-500",
  "output-prediction": "text-blue-500",
  "code-completion": "text-purple-500",
  "multiple-choice": "text-emerald-500",
  "short-answer": "text-amber-500",
  parsons: "text-orange-500",
  dropdown: "text-teal-500",
  "execution-trace": "text-indigo-500",
};

const DIFFICULTY_DOT: Record<string, string> = {
  easy: "bg-emerald-400",
  medium: "bg-amber-400",
  hard: "bg-red-400",
};

export function TopicBrowser({ problems, topicGroups, selectedProblemId, onSelectProblem, className = "" }: TopicBrowserProps) {
  const { t } = useTranslation();
  const [expandedTopics, setExpandedTopics] = useState<Set<string>>(new Set());

  const problemsByTopic = useMemo(() => {
    const map = new Map<string, TeachProblem[]>();
    for (const p of problems) {
      const tg = p.topic_group || "general";
      if (!map.has(tg)) map.set(tg, []);
      map.get(tg)!.push(p);
    }
    return map;
  }, [problems]);

  const toggleTopic = (name: string) => {
    setExpandedTopics((prev) => {
      const next = new Set(prev);
      if (next.has(name)) next.delete(name);
      else next.add(name);
      return next;
    });
  };

  // Auto-expand topic containing selected problem
  const selectedTopic = useMemo(() => {
    if (!selectedProblemId) return null;
    const p = problems.find((p) => p.problem_id === selectedProblemId);
    return p?.topic_group || "general";
  }, [selectedProblemId, problems]);

  if (selectedTopic && !expandedTopics.has(selectedTopic)) {
    setExpandedTopics((prev) => new Set([...prev, selectedTopic]));
  }

  return (
    <div className={`flex flex-col h-full bg-stone-50/80 ${className}`}>
      <div className="px-3 py-2.5 border-b border-stone-200 bg-white">
        <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
          {t("teach.problemBank", { defaultValue: "Problem Bank" })}
        </h3>
        <p className="text-[10px] text-stone-400 mt-0.5">
          {problems.length} {t("teach.problemsAvailable", { defaultValue: "problems" })}
        </p>
      </div>

      <div className="flex-1 overflow-y-auto">
        {topicGroups.map((tg) => {
          const isExpanded = expandedTopics.has(tg.name);
          const topicProblems = problemsByTopic.get(tg.name) || [];
          const isMastered = tg.mastery_percent >= 80;

          return (
            <div key={tg.name} className="border-b border-stone-100">
              <button
                onClick={() => toggleTopic(tg.name)}
                className={`w-full flex items-center gap-2 px-3 py-2 text-left hover:bg-stone-100 transition-colors ${
                  selectedTopic === tg.name ? "bg-brand-50" : ""
                }`}
              >
                {isExpanded ? (
                  <ChevronDown className="w-3.5 h-3.5 text-stone-400 shrink-0" />
                ) : (
                  <ChevronRight className="w-3.5 h-3.5 text-stone-400 shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className={`text-xs font-medium truncate ${isMastered ? "text-emerald-600" : "text-stone-800"}`}>
                      {tg.label}
                    </span>
                    {isMastered && <CheckCircle2 className="w-3 h-3 text-emerald-500 shrink-0" />}
                  </div>
                  {/* Mastery bar */}
                  <div className="flex items-center gap-1.5 mt-1">
                    <div className="flex-1 h-1 bg-stone-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          tg.mastery_percent >= 80 ? "bg-emerald-500" : tg.mastery_percent >= 40 ? "bg-amber-500" : "bg-red-400"
                        }`}
                        style={{ width: `${Math.min(100, tg.mastery_percent)}%` }}
                      />
                    </div>
                    <span className="text-[9px] text-stone-400 w-7 text-right shrink-0">{Math.round(tg.mastery_percent)}%</span>
                  </div>
                </div>
                <span className="text-[10px] text-stone-400 shrink-0">{tg.count}</span>
              </button>

              {isExpanded && (
                <div className="pb-1">
                  {topicProblems.map((p) => {
                    const Icon = TYPE_ICONS[p.problem_type] || FileText;
                    const color = TYPE_COLORS[p.problem_type] || "text-stone-500";
                    const isSelected = p.problem_id === selectedProblemId;

                    return (
                      <button
                        key={p.problem_id}
                        onClick={() => onSelectProblem(p.problem_id)}
                        className={`w-full flex items-center gap-2 pl-8 pr-3 py-1.5 text-left transition-colors ${
                          isSelected ? "bg-brand-100 text-brand-800" : "hover:bg-stone-100 text-stone-600"
                        }`}
                      >
                        <Icon className={`w-3.5 h-3.5 shrink-0 ${isSelected ? "text-brand-600" : color}`} />
                        <span className="text-[11px] truncate flex-1">{p.problem_statement?.slice(0, 50) || p.problem_id}</span>
                        <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${DIFFICULTY_DOT[p.difficulty ?? ""] || "bg-stone-300"}`} />
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        {topicGroups.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-stone-400">
            <Brain className="w-8 h-8 mb-2 opacity-50" />
            <p className="text-xs">{t("teach.noTopics", { defaultValue: "No topics available" })}</p>
          </div>
        )}
      </div>
    </div>
  );
}
