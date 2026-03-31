import { Link } from "react-router-dom";
import { AlertTriangle, BookOpen, Target } from "lucide-react";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";
import type { MisconceptionDetailDto } from "@/api/client";

interface MisconceptionAIProps {
  misconceptions: MisconceptionDetailDto[];
  className?: string;
}

export function MisconceptionAI({ misconceptions, className }: MisconceptionAIProps) {
  if (misconceptions.length === 0) {
    return (
      <div className={cn("rounded-xl border border-stone-200 bg-emerald-50/50 p-4", className)}>
        <p className="text-sm font-medium text-stone-700">No misconceptions detected</p>
        <p className="mt-1 text-xs text-stone-500">Your TA&apos;s knowledge state is consistent. Keep teaching and testing.</p>
      </div>
    );
  }

  return (
    <div className={cn("rounded-xl border border-amber-200 bg-amber-50/30 p-4", className)}>
      <h3 className="flex items-center gap-2 text-sm font-semibold text-stone-800">
        <AlertTriangle className="h-4 w-4 text-amber-600" />
        Misconception diagnosis
      </h3>
      <p className="mt-1 text-xs text-stone-600">
        The TA may have picked up these misconceptions. Teaching the correct concept and running tests helps correct them.
      </p>
      <div className="mt-3 space-y-3">
        {misconceptions.map((m) => (
          <div
            key={m.id}
            className="rounded-lg border border-amber-200/80 bg-white p-3"
          >
            <p className="text-sm font-medium text-stone-800">{m.description}</p>
            {m.affected_units?.length > 0 && (
              <p className="mt-1 text-xs text-stone-500">
                Affected: {m.affected_units.join(", ")}
              </p>
            )}
            <div className="mt-2 flex items-start gap-2 rounded bg-stone-50 p-2 text-xs text-stone-600">
              <Target className="h-3.5 w-3.5 shrink-0 mt-0.5" />
              <span>{m.remediation_hint}</span>
            </div>
          </div>
        ))}
      </div>
      <Link
        to={ROUTES.teach}
        className="mt-3 flex items-center gap-2 text-sm font-medium text-brand-600 hover:underline"
      >
        <BookOpen className="h-4 w-4" />
        Teach to correct
      </Link>
    </div>
  );
}
