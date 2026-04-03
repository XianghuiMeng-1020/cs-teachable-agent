import { useState, useMemo, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronRight, Search, Bug, Code, Brain, FileText, ListChecks, Puzzle, Eye, Terminal, CheckCircle2 } from "lucide-react";
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
  "buggy-code": "text-red-500 bg-red-50",
  "output-prediction": "text-blue-500 bg-blue-50",
  "code-completion": "text-purple-500 bg-purple-50",
  "multiple-choice": "text-emerald-500 bg-emerald-50",
  "short-answer": "text-amber-500 bg-amber-50",
  parsons: "text-orange-500 bg-orange-50",
  dropdown: "text-teal-500 bg-teal-50",
  "execution-trace": "text-indigo-500 bg-indigo-50",
};

const DIFFICULTY_LABEL: Record<string, string> = {
  easy: "E",
  remember: "E",
  medium: "M",
  apply: "M",
  hard: "H",
  analyze: "H",
  transfer: "T",
};

const DIFFICULTY_BADGE_COLORS: Record<string, string> = {
  easy: "bg-emerald-100 text-emerald-700 border-emerald-200",
  remember: "bg-emerald-100 text-emerald-700 border-emerald-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  apply: "bg-amber-100 text-amber-700 border-amber-200",
  hard: "bg-red-100 text-red-700 border-red-200",
  analyze: "bg-red-100 text-red-700 border-red-200",
  transfer: "bg-purple-100 text-purple-700 border-purple-200",
};

export function TopicBrowser({ problems, topicGroups, selectedProblemId, onSelectProblem, className = "" }: TopicBrowserProps) {
  const { t } = useTranslation();
  const [expandedTopics, setExpandedTopics] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState("");

  // Get selected topic - must be memoized to avoid render-loop setState
  const selectedTopic = useMemo(() => {
    if (!selectedProblemId) return null;
    const p = problems.find((p) => p.problem_id === selectedProblemId);
    return p?.topic_group || "general";
  }, [selectedProblemId, problems]);

  // Auto-expand selected topic using useEffect instead of during render
  useEffect(() => {
    if (selectedTopic && !expandedTopics.has(selectedTopic)) {
      setExpandedTopics((prev) => new Set([...prev, selectedTopic]));
    }
  }, [selectedTopic, expandedTopics]);

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

  const filteredTopicGroups = useMemo(() => {
    if (!searchQuery.trim()) return topicGroups;
    return topicGroups.filter(tg => 
      tg.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tg.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [topicGroups, searchQuery]);

  return (
    <div className={`flex flex-col h-full bg-stone-50/80 ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b border-stone-200 bg-white shrink-0">
        <h3 className="text-sm font-bold text-stone-700 uppercase tracking-wide mb-2">
          {t("teach.problemBank", { defaultValue: "Problem Bank" })}
        </h3>
        
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-stone-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t("teach.searchTopics", { defaultValue: "Search topics..." })}
            className="w-full pl-8 pr-3 py-1.5 text-xs bg-stone-100 border border-stone-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-200 focus:border-brand-300 transition-all"
          />
        </div>
        
        <p className="text-xs text-stone-500 mt-2">
          <span className="font-medium text-stone-700">{problems.length}</span> {t("teach.problemsAvailable", { defaultValue: "problems available" })}
        </p>
      </div>

      {/* Topic list */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {filteredTopicGroups.map((tg) => {
          const isExpanded = expandedTopics.has(tg.name);
          const topicProblems = problemsByTopic.get(tg.name) || [];
          const isMastered = tg.mastery_percent >= 80;
          const isSelectedTopic = selectedTopic === tg.name;

          return (
            <div key={tg.name} className="border-b border-stone-100 last:border-b-0">
              {/* Topic header */}
              <button
                onClick={() => toggleTopic(tg.name)}
                className={`w-full flex items-center gap-2 px-4 py-2.5 text-left transition-all duration-200 ${
                  isSelectedTopic 
                    ? "bg-brand-50/70 border-l-4 border-brand-400" 
                    : "hover:bg-stone-100 border-l-4 border-transparent"
                }`}
              >
                {/* Expand icon */}
                <div className="shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-stone-100 hover:bg-stone-200 transition-colors">
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5 text-stone-500" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5 text-stone-500" />
                  )}
                </div>

                {/* Topic info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`text-sm font-semibold truncate ${isMastered ? "text-emerald-700" : "text-stone-800"}`}>
                      {tg.label}
                    </span>
                    {isMastered && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="shrink-0"
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      </motion.div>
                    )}
                  </div>
                  
                  {/* Mastery bar - improved */}
                  <div className="flex items-center gap-2 mt-1.5">
                    <div className="flex-1 h-1.5 bg-stone-200 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(100, tg.mastery_percent)}%` }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                        className={`h-full rounded-full transition-colors ${
                          tg.mastery_percent >= 80 ? "bg-emerald-500" 
                          : tg.mastery_percent >= 50 ? "bg-amber-500" 
                          : "bg-red-400"
                        }`}
                      />
                    </div>
                    <span className="text-[10px] font-medium text-stone-500 w-8 text-right shrink-0">
                      {Math.round(tg.mastery_percent)}%
                    </span>
                  </div>
                </div>

                {/* Problem count badge */}
                <span className="shrink-0 text-[10px] font-medium text-stone-500 bg-stone-100 px-2 py-0.5 rounded-full">
                  {tg.count}
                </span>
              </button>

              {/* Expanded problem list */}
              <AnimatePresence>
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
                    className="overflow-hidden"
                  >
                    <div className="pb-2 pt-1">
                      {topicProblems.map((p) => {
                        const Icon = TYPE_ICONS[p.problem_type] || FileText;
                        const isSelected = p.problem_id === selectedProblemId;
                        const diffLabel = DIFFICULTY_LABEL[p.difficulty || "medium"] || "M";
                        const diffClass = DIFFICULTY_BADGE_COLORS[p.difficulty || "medium"];

                        return (
                          <button
                            key={p.problem_id}
                            onClick={() => onSelectProblem(p.problem_id)}
                            className={`w-full flex items-center gap-2 pl-11 pr-3 py-2 text-left transition-all duration-150 ${
                              isSelected 
                                ? "bg-brand-100 border-r-4 border-brand-400" 
                                : "hover:bg-stone-100"
                            }`}
                          >
                            {/* Type icon with colored bg */}
                            <div className={`shrink-0 w-6 h-6 rounded-lg flex items-center justify-center ${TYPE_COLORS[p.problem_type]?.split(" ")[1] || "bg-stone-100"}`}>
                              <Icon className={`w-3.5 h-3.5 ${TYPE_COLORS[p.problem_type]?.split(" ")[0] || "text-stone-500"}`} />
                            </div>

                            {/* Problem text */}
                            <span className={`text-xs truncate flex-1 ${isSelected ? "text-brand-800 font-medium" : "text-stone-600"}`}>
                              {p.problem_statement?.slice(0, 55) || p.problem_id}
                            </span>

                            {/* Difficulty badge */}
                            <span className={`shrink-0 text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded border ${diffClass}`}>
                              {diffLabel}
                            </span>
                          </button>
                        );
                      })}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}

        {filteredTopicGroups.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-stone-400">
            <Brain className="w-10 h-10 mb-3 opacity-40" />
            <p className="text-sm">{t("teach.noTopics", { defaultValue: "No topics available" })}</p>
            <p className="text-xs text-stone-400 mt-1">Try adjusting your search</p>
          </div>
        )}
      </div>
    </div>
  );
}
