/**
 * Timeline of a misconception lifecycle: activated → diagnosed → corrected → verified.
 */

import { Circle, CheckCircle, AlertCircle } from "lucide-react";

export interface MisconceptionEvent {
  type: "activated" | "diagnosed" | "corrected" | "verified";
  at: string;
  label?: string;
  detail?: string;
}

interface MisconceptionTimelineProps {
  misconceptionId: string;
  events: MisconceptionEvent[];
  confidenceCurve?: { at: string; value: number }[];
  className?: string;
}

export function MisconceptionTimeline({
  misconceptionId,
  events,
  confidenceCurve,
  className = "",
}: MisconceptionTimelineProps) {
  return (
    <div className={className}>
      <p className="text-sm font-medium text-stone-700 dark:text-stone-300">{misconceptionId}</p>
      <div className="mt-3 space-y-0">
        {events.map((evt, i) => (
          <div key={i} className="flex gap-3">
            <div className="flex flex-col items-center">
              {evt.type === "activated" || evt.type === "diagnosed" ? (
                <AlertCircle className="h-4 w-4 text-amber-500" />
              ) : (
                <CheckCircle className="h-4 w-4 text-green-500" />
              )}
              {i < events.length - 1 && <div className="w-px flex-1 min-h-[8px] bg-stone-200 dark:bg-stone-600" />}
            </div>
            <div className="pb-4">
              <p className="text-xs font-medium text-stone-600 dark:text-stone-400 capitalize">{evt.type}</p>
              <p className="text-xs text-stone-500">{evt.at}</p>
              {evt.label && <p className="text-sm text-stone-700 dark:text-stone-300">{evt.label}</p>}
              {evt.detail && <p className="text-xs text-stone-500 mt-0.5">{evt.detail}</p>}
            </div>
          </div>
        ))}
      </div>
      {confidenceCurve && confidenceCurve.length > 1 && (
        <p className="mt-2 text-xs text-stone-500">Confidence over time: {confidenceCurve.length} points</p>
      )}
    </div>
  );
}
