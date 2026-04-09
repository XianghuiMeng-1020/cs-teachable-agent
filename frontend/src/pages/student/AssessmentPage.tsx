import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { ArrowLeft, Send, RotateCcw, Loader2, CheckCircle, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { getAssessmentItem, gradeAssessmentItem, type AssessmentItemDetail, type GradeResponse } from "@/api/assessment";
import { ParsonsBlock, DropdownBlanks, ExecutionTrace, HintPanel } from "@/components/assessment";
import { AntiCheatShell } from "@/components/assessment/AntiCheatShell";
import { AntiCaptureOverlay } from "@/components/assessment/AntiCaptureOverlay";
import { QuickStartGuide } from "@/components/assessment/QuickStartGuide";
import { Button } from "@/components/ui/Button";
import { emitTelemetry, generateAttemptId, getSessionId } from "@/lib/telemetry";
import type { FocusLossEvent } from "@/components/assessment/AntiCheatShell";

const ITEM_TYPE_LABELS: Record<string, string> = {
  parsons: "Parsons Puzzle",
  dropdown: "Fill in the Blanks",
  "execution-trace": "Execution Trace",
};

export function AssessmentPage() {
  const { itemId } = useParams<{ itemId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const [item, setItem] = useState<AssessmentItemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<GradeResponse | null>(null);
  const [attemptNumber, setAttemptNumber] = useState(1);
  const [startTime] = useState(Date.now());
  const [hintsUsed, setHintsUsed] = useState(0);
  const sessionState = (location.state as { itemIds?: number[]; currentIndex?: number } | null) ?? null;
  const itemIds = sessionState?.itemIds ?? [];
  const currentIndex = sessionState?.currentIndex ?? -1;
  const nextItemId = currentIndex >= 0 && currentIndex < itemIds.length - 1 ? itemIds[currentIndex + 1] : null;

  const [selectedBlocks, setSelectedBlocks] = useState<string[]>([]);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const attemptIdRef = useRef(generateAttemptId());
  const focusLossCountRef = useRef(0);

  useEffect(() => {
    if (!itemId) return;
    setLoading(true);
    getAssessmentItem(Number(itemId))
      .then((loadedItem) => {
        setItem(loadedItem);
        emitTelemetry("task_loaded", {
          itemId: loadedItem.id,
          itemType: loadedItem.item_type,
        }, { itemId: loadedItem.id, itemType: loadedItem.item_type, attemptId: attemptIdRef.current });
      })
      .catch(() => navigate("/practice"))
      .finally(() => setLoading(false));
  }, [itemId, navigate]);

  const handleSubmit = useCallback(async () => {
    if (!item || submitting) return;
    setSubmitting(true);
    emitTelemetry("submit_clicked", {
      itemId: item.id,
      attemptNumber,
      durationMs: Date.now() - startTime,
      focusLossCount: focusLossCountRef.current,
    }, { itemId: item.id, itemType: item.item_type, attemptId: attemptIdRef.current });
    try {
      const result = await gradeAssessmentItem(item.id, {
        selected_blocks: item.item_type === "parsons" ? selectedBlocks : undefined,
        selected_answers: item.item_type !== "parsons" ? selectedAnswers : undefined,
        duration_ms: Date.now() - startTime,
        hints_used: hintsUsed,
      });
      setFeedback(result);
      setAttemptNumber((n) => n + 1);
      const isCorrectResult = result.correct;
      emitTelemetry(
        isCorrectResult ? "graded_correct" : "graded_incorrect",
        {
          score: result.score,
          expected: result.expected_count,
          durationMs: Date.now() - startTime,
          focusLossCount: focusLossCountRef.current,
        },
        { itemId: item.id, itemType: item.item_type, attemptId: attemptIdRef.current }
      );
    } catch {
      // handle error
    } finally {
      setSubmitting(false);
    }
  }, [item, selectedBlocks, selectedAnswers, submitting, startTime, hintsUsed, attemptNumber]);

  const handleReset = useCallback(() => {
    setSelectedBlocks([]);
    setSelectedAnswers({});
    setFeedback(null);
    attemptIdRef.current = generateAttemptId();
    focusLossCountRef.current = 0;
    emitTelemetry("attempt_reset", {}, { itemId: item?.id, itemType: item?.item_type, attemptId: attemptIdRef.current });
  }, [item]);

  const handleAnswerChange = useCallback((id: string, value: string) => {
    setSelectedAnswers((prev) => ({ ...prev, [id]: value }));
    setFeedback(null);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="h-7 w-7 animate-spin text-brand-600" />
      </div>
    );
  }

  if (!item) {
    return (
      <div className="py-24 text-center text-stone-400">Item not found</div>
    );
  }

  const isCorrect = feedback?.correct;

  const handleFocusLost = useCallback((event: FocusLossEvent) => {
    focusLossCountRef.current += 1;
    emitTelemetry("focus_lost", {
      reason: event.reason,
      focusLossCountInAttempt: focusLossCountRef.current,
    }, { itemId: item?.id, itemType: item?.item_type, attemptId: attemptIdRef.current, eventTime: event.timestamp });
  }, [item]);

  const handleFocusResume = useCallback(() => {
    emitTelemetry("resume_clicked", {
      focusLossCountInAttempt: focusLossCountRef.current,
    }, { itemId: item?.id, itemType: item?.item_type, attemptId: attemptIdRef.current });
  }, [item]);

  return (
    <AntiCaptureOverlay>
    <AntiCheatShell
      enabled={true}
      onFocusLost={handleFocusLost}
      onResume={handleFocusResume}
    >
    <div className="mx-auto max-w-3xl space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate("/practice")}
          className="rounded-lg p-1.5 text-stone-400 hover:bg-stone-100 hover:text-stone-600 transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div className="flex-1 min-w-0">
          <h1 className="font-serif text-xl font-bold text-stone-900 truncate">{item.title}</h1>
          <div className="flex items-center gap-2 mt-1">
            <span className="rounded-md border border-brand-200 bg-brand-50 px-2 py-0.5 text-[11px] font-medium text-brand-800">
              {ITEM_TYPE_LABELS[item.item_type] || item.item_type}
            </span>
            {item.theme && (
              <span className="text-xs text-stone-500">{item.theme}</span>
            )}
          </div>
        </div>
        {currentIndex >= 0 && itemIds.length > 0 && (
          <span className="ml-auto rounded-md border border-stone-200 bg-white px-2 py-1 text-xs font-medium text-stone-600">
            Session {currentIndex + 1}/{itemIds.length}
          </span>
        )}
      </div>

      {/* Prompt */}
      <QuickStartGuide />

      <div className="rounded-xl border border-stone-200/80 bg-stone-50 px-5 py-4">
        <p className="text-sm leading-relaxed text-stone-700 whitespace-pre-wrap">{item.prompt}</p>
      </div>

      {/* Concepts */}
      {item.concepts && item.concepts.length > 0 && (
        <div className="flex gap-1.5 flex-wrap">
          {item.concepts.map((c) => (
            <span key={c} className="rounded-md bg-stone-100 px-2.5 py-1 text-xs font-medium text-stone-600">
              {c}
            </span>
          ))}
        </div>
      )}

      {/* Interactive area */}
      <div className="rounded-xl border border-stone-200/80 bg-white p-5">
        {item.item_type === "parsons" && item.options && (
          <ParsonsBlock
            options={item.options}
            distractors={item.distractors}
            requiredBlockCount={item.required_block_count || 0}
            selectedBlocks={selectedBlocks}
            onSelectedChange={(blocks) => { setSelectedBlocks(blocks); setFeedback(null); }}
            disabled={isCorrect === true}
            feedback={feedback}
          />
        )}
        {item.item_type === "dropdown" && item.blanks && (
          <DropdownBlanks
            promptTemplate={item.prompt_template || ""}
            blanks={item.blanks}
            selectedAnswers={selectedAnswers}
            onAnswerChange={handleAnswerChange}
            disabled={isCorrect === true}
            feedback={feedback}
          />
        )}
        {item.item_type === "execution-trace" && item.checkpoints && (
          <ExecutionTrace
            functionName={item.function_name || ""}
            functionSource={item.function_source || ""}
            callExpression={item.call_expression || ""}
            checkpoints={item.checkpoints}
            selectedAnswers={selectedAnswers}
            onAnswerChange={handleAnswerChange}
            disabled={isCorrect === true}
            feedback={feedback}
          />
        )}
      </div>

      {/* Hints */}
      <HintPanel
        itemDbId={item.id}
        selectedBlocks={item.item_type === "parsons" ? selectedBlocks : undefined}
        selectedAnswers={item.item_type !== "parsons" ? selectedAnswers : undefined}
        lastFeedback={feedback as unknown as Record<string, unknown>}
        attemptNumber={attemptNumber}
        onHintUsed={() => setHintsUsed((prev) => prev + 1)}
      />

      {/* Feedback banner */}
      {feedback && (
        <div className={cn(
          "rounded-xl border p-4 flex items-start gap-3",
          isCorrect
            ? "border-emerald-200 bg-emerald-50"
            : "border-amber-200 bg-amber-50"
        )}>
          {isCorrect ? (
            <CheckCircle className="h-5 w-5 shrink-0 text-emerald-600 mt-0.5" />
          ) : (
            <RotateCcw className="h-5 w-5 shrink-0 text-amber-600 mt-0.5" />
          )}
          <div>
            <p className={cn("text-sm font-semibold", isCorrect ? "text-emerald-900" : "text-amber-900")}>
              {isCorrect ? "Correct!" : "Not quite right"}
            </p>
            <p className={cn("mt-0.5 text-sm", isCorrect ? "text-emerald-700" : "text-amber-700")}>
              {isCorrect
                ? `Great work! You got ${feedback.correct_count} of ${feedback.expected_count} correct.`
                : `${feedback.correct_count ?? 0} of ${feedback.expected_count ?? "?"} correct. Try again or use a hint.`}
            </p>
            {!!feedback.next_action && (
              <p className="mt-1 text-xs text-stone-600">
                Next action: {feedback.next_action}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3 justify-end pb-4">
        <Button
          variant="outline"
          icon={RotateCcw}
          onClick={handleReset}
          disabled={isCorrect === true}
        >
          Reset
        </Button>
        {isCorrect ? (
          <Button
            icon={ChevronRight}
            onClick={() => {
              if (nextItemId != null) {
                navigate(`/practice/${nextItemId}`, {
                  state: {
                    itemIds,
                    currentIndex: currentIndex + 1,
                  },
                });
              } else {
                navigate("/practice");
              }
            }}
            className="bg-emerald-600 hover:bg-emerald-700"
          >
            {nextItemId != null ? "Next Exercise" : "Back to Practice"}
          </Button>
        ) : (
          <Button
            icon={submitting ? undefined : Send}
            loading={submitting}
            onClick={handleSubmit}
          >
            Submit
          </Button>
        )}
      </div>
    </div>
    </AntiCheatShell>
    </AntiCaptureOverlay>
  );
}
