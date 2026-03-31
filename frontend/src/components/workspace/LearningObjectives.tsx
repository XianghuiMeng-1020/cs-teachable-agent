/**
 * Session learning objectives based on Bloom levels: Understand → Apply → Analyze.
 * Shows progress for the current session or learned units.
 */

import { CheckCircle, Circle } from "lucide-react";

export type BloomLevel = "understand" | "apply" | "analyze";

interface LearningObjectivesProps {
  /** Learned unit IDs (or from session). */
  learnedUnitIds?: string[];
  /** Which levels are considered achieved (e.g. from state or session). */
  achievedLevels?: BloomLevel[];
  /** Compact display. */
  compact?: boolean;
}

const LEVELS: { id: BloomLevel; label: string; description: string }[] = [
  { id: "understand", label: "Understand", description: "Explain concepts and restate in own words" },
  { id: "apply", label: "Apply", description: "Use concepts in examples and exercises" },
  { id: "analyze", label: "Analyze", description: "Compare, contrast, and debug" },
];

export function LearningObjectives({
  learnedUnitIds = [],
  achievedLevels = [],
  compact,
}: LearningObjectivesProps) {
  const hasLearned = learnedUnitIds.length > 0;
  const understandDone = achievedLevels.includes("understand") || (hasLearned && achievedLevels.length === 0);
  const applyDone = achievedLevels.includes("apply") || (hasLearned && learnedUnitIds.length >= 3);
  const analyzeDone = achievedLevels.includes("analyze");

  if (compact) {
    return (
      <div className="flex items-center gap-3 text-xs text-stone-600 dark:text-stone-400">
        {LEVELS.map((level, i) => {
          const done = level.id === "understand" ? understandDone : level.id === "apply" ? applyDone : analyzeDone;
          return (
            <span key={level.id} className="flex items-center gap-1">
              {done ? <CheckCircle className="h-3.5 w-3.5 text-green-600" /> : <Circle className="h-3.5 w-3.5 text-stone-300" />}
              <span className={done ? "font-medium text-stone-800 dark:text-stone-200" : ""}>{level.label}</span>
            </span>
          );
        })}
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-stone-200 bg-stone-50/50 p-3 dark:border-stone-700 dark:bg-stone-900/30">
      <p className="mb-2 text-xs font-medium text-stone-600 dark:text-stone-400">Session learning objectives</p>
      <ul className="space-y-2">
        {LEVELS.map((level) => {
          const done = level.id === "understand" ? understandDone : level.id === "apply" ? applyDone : analyzeDone;
          return (
            <li key={level.id} className="flex items-start gap-2">
              {done ? (
                <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-600 dark:text-green-400" />
              ) : (
                <Circle className="mt-0.5 h-4 w-4 shrink-0 text-stone-300 dark:text-stone-600" />
              )}
              <div>
                <p className={`text-sm font-medium ${done ? "text-stone-800 dark:text-stone-200" : "text-stone-500 dark:text-stone-400"}`}>
                  {level.label}
                </p>
                <p className="text-xs text-stone-500 dark:text-stone-400">{level.description}</p>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
