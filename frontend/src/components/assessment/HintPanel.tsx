import { useState, useCallback, useRef } from "react";
import { Lightbulb, ChevronUp, Loader2, ThumbsUp, ThumbsDown, Zap } from "lucide-react";
import { cn } from "@/lib/utils";
import { getAssessmentHint, type HintResponse } from "@/api/assessment";
import { emitTelemetry } from "@/lib/telemetry";

type HintType = "understand" | "next-step" | "check-one-issue";
type HintRating = "helpful" | "unhelpful" | null;

interface HintRecord extends HintResponse {
  rating: HintRating;
  requestedAt: string;
}

const HINT_LIMITS: Record<HintType, number> = {
  understand: 1,
  "next-step": 2,
  "check-one-issue": 2,
};

interface HintPanelProps {
  itemDbId: number;
  taId?: number;
  selectedBlocks?: string[];
  selectedAnswers?: Record<string, string>;
  lastFeedback?: Record<string, unknown> | null;
  attemptNumber?: number;
  disabled?: boolean;
}

const HINT_TYPES: { value: HintType; label: string; desc: string }[] = [
  { value: "understand", label: "Understand", desc: "Help me understand the task" },
  { value: "next-step", label: "Next Step", desc: "What should I try next?" },
  { value: "check-one-issue", label: "Check Issue", desc: "Check one specific issue" },
];

const LEVEL_SCOPE_LABELS: Record<number, { label: string; desc: string }> = {
  1: { label: "Conceptual", desc: "Broad concept only — no specific elements" },
  2: { label: "Regional", desc: "Points to a general area — no exact answers" },
  3: { label: "Targeted", desc: "Names one element — still no answer revealed" },
};

export function HintPanel({
  itemDbId,
  taId,
  selectedBlocks,
  selectedAnswers,
  lastFeedback,
  attemptNumber,
  disabled = false,
}: HintPanelProps) {
  const [hints, setHints] = useState<HintRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const usageCount = useRef<Record<HintType, number>>({
    understand: 0,
    "next-step": 0,
    "check-one-issue": 0,
  });

  const getRemainingForType = (type: HintType) => {
    return Math.max(0, HINT_LIMITS[type] - usageCount.current[type]);
  };

  const requestHint = useCallback(
    async (hintType: HintType) => {
      if (loading || disabled) return;
      if (getRemainingForType(hintType) <= 0) return;

      const level = Math.min(usageCount.current[hintType] + 1, 3) as 1 | 2 | 3;

      setLoading(true);
      emitTelemetry("hint_requested", { hintType, level, itemDbId });

      try {
        const hint = await getAssessmentHint(itemDbId, {
          ta_id: taId,
          hint_type: hintType,
          level,
          selected_blocks: selectedBlocks,
          selected_answers: selectedAnswers,
          last_feedback: lastFeedback ?? undefined,
          attempt_number: attemptNumber,
        });

        usageCount.current[hintType] += 1;

        const record: HintRecord = {
          ...hint,
          rating: null,
          requestedAt: new Date().toISOString(),
        };
        setHints((prev) => [record, ...prev]);
        setExpanded(true);
        emitTelemetry("hint_received", { hintType, level, hintId: hint.hint_id });
      } catch {
        emitTelemetry("hint_request_failed", { hintType, level });
      } finally {
        setLoading(false);
      }
    },
    [itemDbId, taId, selectedBlocks, selectedAnswers, lastFeedback, attemptNumber, loading, disabled]
  );

  const rateHint = (hintId: string, rating: HintRating) => {
    setHints((prev) =>
      prev.map((h) => (h.hint_id === hintId ? { ...h, rating } : h))
    );
    emitTelemetry(rating === "helpful" ? "hint_helpful" : "hint_unhelpful", { hintId });
  };

  const totalUsed = hints.length;
  const totalLimit = Object.values(HINT_LIMITS).reduce((a, b) => a + b, 0);

  return (
    <div className="rounded-xl border border-amber-200 bg-amber-50/40">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between px-4 py-3 text-sm font-medium text-amber-800 hover:bg-amber-100/50 transition-colors rounded-xl"
      >
        <span className="flex items-center gap-2">
          <Lightbulb className="h-4 w-4" />
          Hints
          {totalUsed > 0 && (
            <span className="text-xs text-amber-600">
              {totalUsed}/{totalLimit} used
            </span>
          )}
        </span>
        <ChevronUp className={cn("h-4 w-4 transition-transform", !expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="border-t border-amber-200 px-4 py-3 space-y-3">
          {/* Hint type buttons with remaining counts */}
          <div className="flex gap-2 flex-wrap">
            {HINT_TYPES.map(({ value, label }) => {
              const remaining = getRemainingForType(value);
              const exhausted = remaining <= 0;
              return (
                <button
                  key={value}
                  onClick={() => requestHint(value)}
                  disabled={loading || disabled || exhausted}
                  className={cn(
                    "rounded-full border px-3 py-1.5 text-xs font-medium transition-all",
                    exhausted
                      ? "border-stone-200 bg-stone-50 text-stone-400 cursor-not-allowed"
                      : "border-amber-300 bg-white text-amber-800 hover:bg-amber-100",
                    loading && "opacity-50 cursor-wait"
                  )}
                  title={exhausted ? `No ${label} hints remaining` : `${remaining} remaining`}
                >
                  {loading ? <Loader2 className="h-3 w-3 animate-spin inline mr-1" /> : null}
                  {label}
                  <span className="ml-1.5 text-[10px] opacity-70">
                    {remaining}/{HINT_LIMITS[value]}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Level scope indicator */}
          {(() => {
            const nextLevel = Math.min(
              Math.max(...Object.values(usageCount.current).map(v => v + 1)),
              3
            ) as 1 | 2 | 3;
            const scope = LEVEL_SCOPE_LABELS[nextLevel];
            return scope ? (
              <div className="flex items-center gap-2 rounded-md border border-amber-100 bg-amber-50/50 px-3 py-1.5">
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-600">
                  Level {nextLevel}: {scope.label}
                </span>
                <span className="text-[10px] text-amber-700/70">{scope.desc}</span>
              </div>
            ) : null;
          })()}

          {/* Hint history */}
          {hints.length > 0 && (
            <div className="space-y-2.5 max-h-72 overflow-y-auto">
              {hints.map((hint) => (
                <div
                  key={hint.hint_id}
                  className="rounded-lg border border-amber-200 bg-white px-3.5 py-2.5"
                >
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-xs font-semibold text-amber-700">{hint.title}</span>
                    <span className="rounded-md bg-amber-100 px-1.5 py-0.5 text-[10px] font-medium text-amber-600">
                      L{hint.level}
                    </span>
                    {hint.escalation_available && (
                      <button
                        onClick={() => {
                          const hintType = HINT_TYPES.find((t) =>
                            hint.title?.toLowerCase().includes(t.value)
                          )?.value ?? "next-step";
                          requestHint(hintType);
                          emitTelemetry("hint_stronger_requested", { hintId: hint.hint_id });
                        }}
                        className="ml-auto flex items-center gap-1 rounded-md border border-amber-300 px-2 py-0.5 text-[10px] font-medium text-amber-700 hover:bg-amber-50"
                      >
                        <Zap className="h-3 w-3" />
                        Stronger hint
                      </button>
                    )}
                  </div>
                  <p className="text-sm leading-relaxed text-stone-700">{hint.body}</p>
                  {hint.target && (
                    <p className="mt-1 text-xs text-stone-500">
                      Focus: <span className="font-medium">{hint.target.label}</span>
                    </p>
                  )}
                  {/* Rating */}
                  <div className="mt-2 flex items-center gap-2 border-t border-amber-100 pt-2">
                    <span className="text-[10px] text-stone-400">Was this helpful?</span>
                    <button
                      onClick={() => rateHint(hint.hint_id, "helpful")}
                      className={cn(
                        "rounded-md p-1 transition-colors",
                        hint.rating === "helpful"
                          ? "bg-emerald-100 text-emerald-700"
                          : "text-stone-400 hover:bg-stone-100 hover:text-stone-600"
                      )}
                    >
                      <ThumbsUp className="h-3 w-3" />
                    </button>
                    <button
                      onClick={() => rateHint(hint.hint_id, "unhelpful")}
                      className={cn(
                        "rounded-md p-1 transition-colors",
                        hint.rating === "unhelpful"
                          ? "bg-red-100 text-red-700"
                          : "text-stone-400 hover:bg-stone-100 hover:text-stone-600"
                      )}
                    >
                      <ThumbsDown className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {hints.length === 0 && (
            <p className="text-xs text-amber-600 py-1">
              Choose a hint type above. Hints are limited to help you learn independently.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
