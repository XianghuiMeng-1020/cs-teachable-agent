/**
 * Shows current TA mode: Help Receiver (passive) vs Questioner (asking why/how).
 * Every 3rd TA message is in Questioner mode (backend mode-shifting).
 */

import { MessageCircle, HelpCircle } from "lucide-react";

interface ModeIndicatorProps {
  /** Number of TA messages so far (0-based). Next message will be (taMessageCount + 1)-th. */
  taMessageCount: number;
  /** If true, the next TA response will be in Questioner mode. */
  isQuestionerTurn?: boolean;
  compact?: boolean;
}

export function ModeIndicator({ taMessageCount, isQuestionerTurn, compact }: ModeIndicatorProps) {
  const questioner = isQuestionerTurn ?? (taMessageCount + 1) % 3 === 0;
  if (compact) {
    return (
      <span
        className={`inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-xs font-medium ${
          questioner
            ? "bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200"
            : "bg-stone-100 text-stone-600 dark:bg-stone-800 dark:text-stone-300"
        }`}
        title={questioner ? "Questioner mode: TA will ask a thought-provoking question" : "Help Receiver mode"}
      >
        {questioner ? <HelpCircle className="h-3 w-3" /> : <MessageCircle className="h-3 w-3" />}
        {questioner ? "Questioner" : "Help Receiver"}
      </span>
    );
  }
  return (
    <div className="flex items-center gap-2 text-xs text-stone-500 dark:text-stone-400">
      <span>TA mode:</span>
      <span
        className={`inline-flex items-center gap-1 rounded px-2 py-0.5 font-medium ${
          questioner
            ? "bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200"
            : "bg-stone-100 text-stone-600 dark:bg-stone-800 dark:text-stone-300"
        }`}
      >
        {questioner ? <HelpCircle className="h-3.5 w-3.5" /> : <MessageCircle className="h-3.5 w-3.5" />}
        {questioner ? "Questioner" : "Help Receiver"}
      </span>
    </div>
  );
}
