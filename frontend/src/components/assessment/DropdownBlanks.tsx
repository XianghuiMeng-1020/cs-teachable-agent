import { useMemo } from "react";
import { cn } from "@/lib/utils";
import { emitTelemetry } from "@/lib/telemetry";
import type { DropdownBlank } from "@/api/assessment";

interface DropdownBlanksProps {
  promptTemplate: string;
  blanks: DropdownBlank[];
  selectedAnswers: Record<string, string>;
  onAnswerChange: (blankId: string, value: string) => void;
  disabled?: boolean;
  feedback?: { correct: boolean; feedback: string } | null;
}

function shuffleArray<T>(arr: T[]): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function DropdownBlanks({
  promptTemplate,
  blanks,
  selectedAnswers,
  onAnswerChange,
  disabled = false,
  feedback,
}: DropdownBlanksProps) {
  const blankMap = new Map(blanks.map((b) => [b.placeholder, b]));
  const parts = promptTemplate.split(/(__BLANK_\d+__)/g);

  const shuffledOptions = useMemo(() => {
    const map: Record<string, string[]> = {};
    blanks.forEach((b) => {
      map[b.blank_id] = shuffleArray(b.options);
    });
    return map;
  }, [blanks]);

  const handleChange = (blankId: string, value: string) => {
    onAnswerChange(blankId, value);
    emitTelemetry("blank_changed", { blankId, hasValue: !!value });
  };

  const filledCount = blanks.filter((b) => selectedAnswers[b.blank_id]).length;

  return (
    <div className="space-y-5">
      {/* Code template preview with inline selected values */}
      <div>
        <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-stone-400">
          Code Preview
        </h4>
        <div className="rounded-lg border border-stone-200 bg-stone-900 p-4 overflow-x-auto">
          <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-stone-100">
            {parts.map((part, i) => {
              const blank = blankMap.get(part);
              if (!blank) {
                return <span key={i}>{part}</span>;
              }
              const val = selectedAnswers[blank.blank_id];
              return (
                <span
                  key={i}
                  className={cn(
                    "inline-block rounded px-1 mx-0.5 font-semibold",
                    val
                      ? "bg-brand-800/50 text-brand-300"
                      : "bg-stone-700 text-stone-500"
                  )}
                >
                  {val || `___`}
                </span>
              );
            })}
          </pre>
        </div>
      </div>

      {/* Interactive blanks with button groups */}
      <div>
        <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-stone-400">
          Fill in the Blanks ({filledCount}/{blanks.length})
        </h4>
        <div className="space-y-3">
          {blanks.map((blank) => {
            const options = shuffledOptions[blank.blank_id] ?? blank.options;
            const selected = selectedAnswers[blank.blank_id];
            return (
              <div key={blank.blank_id} className="rounded-lg border border-stone-200 bg-white p-3">
                <div className="mb-2 flex items-center gap-2">
                  <span className="rounded-md bg-stone-100 px-2 py-0.5 font-mono text-xs text-stone-600">
                    {blank.placeholder}
                  </span>
                  {selected && (
                    <span className="text-xs text-brand-700 font-medium">= {selected}</span>
                  )}
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {options.map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => handleChange(blank.blank_id, opt)}
                      disabled={disabled}
                      className={cn(
                        "rounded-md border px-3 py-1.5 text-xs font-mono font-medium transition-all",
                        selected === opt
                          ? "border-brand-600 bg-brand-50 text-brand-800 ring-1 ring-brand-600/20"
                          : "border-stone-200 bg-white text-stone-700 hover:border-stone-300 hover:bg-stone-50",
                        disabled && "cursor-not-allowed opacity-60"
                      )}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {feedback && (
        <div
          className={cn(
            "rounded-xl border px-4 py-3 text-sm",
            feedback.correct
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-amber-200 bg-amber-50 text-amber-800"
          )}
        >
          {feedback.feedback}
        </div>
      )}
    </div>
  );
}
