import { cn } from "@/lib/utils";
import { emitTelemetry } from "@/lib/telemetry";
import type { ExecutionTraceCheckpoint } from "@/api/assessment";

interface ExecutionTraceProps {
  functionName: string;
  functionSource: string;
  callExpression: string;
  checkpoints: ExecutionTraceCheckpoint[];
  selectedAnswers: Record<string, string>;
  onAnswerChange: (checkpointId: string, value: string) => void;
  disabled?: boolean;
  feedback?: { correct: boolean; feedback: string } | null;
}

export function ExecutionTrace({
  functionName,
  functionSource,
  callExpression,
  checkpoints,
  selectedAnswers,
  onAnswerChange,
  disabled = false,
  feedback,
}: ExecutionTraceProps) {
  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-stone-200 bg-stone-900 p-4 text-stone-100">
        <div className="mb-2 text-xs text-stone-400 font-sans">
          Function: <span className="text-brand-300 font-medium">{functionName}</span>
        </div>
        <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed">{functionSource}</pre>
      </div>

      <div className="rounded-lg border border-brand-200 bg-brand-50 px-4 py-3">
        <div className="text-xs text-stone-500 font-sans mb-1">Call expression:</div>
        <code className="font-mono text-sm text-brand-800 font-medium">{callExpression}</code>
      </div>

      <div className="space-y-3">
        <h4 className="text-sm font-medium text-stone-700">
          Checkpoints — fill in each variable value after the line executes:
        </h4>
        {checkpoints.map((cp) => (
          <div
            key={cp.checkpoint_id}
            className="flex items-start gap-3 rounded-lg border border-stone-200 bg-white p-3"
          >
            <div className="shrink-0 mt-1 flex h-6 w-6 items-center justify-center rounded-full bg-brand-100 text-xs font-medium text-brand-700">
              {cp.line_number}
            </div>
            <div className="flex-1 min-w-0">
              <code className="text-xs text-stone-500 block truncate">{cp.line_excerpt}</code>
              <div className="mt-1.5 flex items-center gap-2">
                <label className="text-sm text-stone-600 shrink-0">
                  <code className="font-medium text-brand-700">{cp.variable_name}</code> =
                </label>
                <input
                  type="text"
                  value={selectedAnswers[cp.checkpoint_id] || ""}
                  onChange={(e) => onAnswerChange(cp.checkpoint_id, e.target.value)}
                  onBlur={(e) => {
                    emitTelemetry("checkpoint_blurred", {
                      checkpointId: cp.checkpoint_id,
                      valueLength: e.target.value.length,
                    });
                  }}
                  disabled={disabled}
                  placeholder="value after execution"
                  className={cn(
                    "flex-1 rounded border border-stone-300 px-2 py-1 font-mono text-sm",
                    "focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500",
                    disabled && "cursor-not-allowed opacity-60 bg-stone-100"
                  )}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-xs text-stone-500">
        {checkpoints.filter((cp) => (selectedAnswers[cp.checkpoint_id] || "").trim()).length} /{" "}
        {checkpoints.length} checkpoints filled
      </div>

      {feedback && (
        <div
          className={cn(
            "rounded-lg border px-4 py-3 text-sm",
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
