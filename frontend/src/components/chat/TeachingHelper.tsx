/**
 * Teaching Helper: shows real-time metacognitive feedback (antipattern detection).
 * Displays pattern (good / commanding / spoon_feeding / under_teaching), feedback, and suggestions.
 */

import { AlertCircle, CheckCircle, Lightbulb } from "lucide-react";

export interface TeachingHelperResult {
  pattern: string;
  feedback: string;
  suggestions: string[];
}

interface TeachingHelperProps {
  result: TeachingHelperResult | null;
  onSendAnyway?: () => void;
  onDismiss?: () => void;
  compact?: boolean;
}

const PATTERN_LABELS: Record<string, string> = {
  good: "Good teaching",
  commanding: "Commanding (only instructions)",
  spoon_feeding: "Spoon-feeding (giving answer directly)",
  under_teaching: "Under-teaching (too vague)",
};

export function TeachingHelper({ result, onSendAnyway, onDismiss, compact }: TeachingHelperProps) {
  if (!result) return null;
  const isGood = result.pattern === "good";
  const hasSuggestions = result.suggestions && result.suggestions.length > 0;

  if (compact && isGood) return null;

  return (
    <div
      className={`rounded-lg border p-3 text-sm ${
        isGood
          ? "border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-950/40"
          : "border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-950/40"
      }`}
    >
      <div className="flex items-start gap-2">
        {isGood ? (
          <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-600 dark:text-green-400" />
        ) : (
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
        )}
        <div className="min-w-0 flex-1">
          <p className="font-medium text-stone-800 dark:text-stone-200">
            {PATTERN_LABELS[result.pattern] ?? result.pattern}
          </p>
          {result.feedback && (
            <p className="mt-1 text-stone-600 dark:text-stone-400">{result.feedback}</p>
          )}
          {hasSuggestions && (
            <ul className="mt-2 flex flex-col gap-1">
              <li className="flex items-start gap-1.5">
                <Lightbulb className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-600 dark:text-amber-400" />
                <span className="text-stone-600 dark:text-stone-400">Suggestions:</span>
              </li>
              {result.suggestions.map((s, i) => (
                <li key={i} className="ml-5 list-disc text-stone-600 dark:text-stone-400">
                  {s}
                </li>
              ))}
            </ul>
          )}
          {!isGood && (onSendAnyway || onDismiss) && (
            <div className="mt-3 flex gap-2">
              {onSendAnyway && (
                <button
                  type="button"
                  onClick={onSendAnyway}
                  className="rounded bg-amber-200 px-2 py-1 text-xs font-medium text-amber-900 hover:bg-amber-300 dark:bg-amber-800 dark:text-amber-100 dark:hover:bg-amber-700"
                >
                  Send anyway
                </button>
              )}
              {onDismiss && (
                <button
                  type="button"
                  onClick={onDismiss}
                  className="rounded bg-stone-200 px-2 py-1 text-xs font-medium text-stone-700 hover:bg-stone-300 dark:bg-stone-700 dark:text-stone-200 dark:hover:bg-stone-600"
                >
                  Dismiss
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
