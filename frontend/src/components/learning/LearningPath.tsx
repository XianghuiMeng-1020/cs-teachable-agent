import { Link } from "react-router-dom";
import { BookOpen, Clock, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";
import type { LearningPathItem } from "@/api/client";

interface LearningPathProps {
  recommended: LearningPathItem[];
  learnedCount: number;
  totalCount: number;
  estimatedMinutesRemaining: number;
  className?: string;
}

export function LearningPath({
  recommended,
  learnedCount,
  totalCount,
  estimatedMinutesRemaining,
  className,
}: LearningPathProps) {
  const pct = totalCount ? Math.round((learnedCount / totalCount) * 100) : 0;
  return (
    <div className={cn("rounded-xl border border-slate-200 bg-white p-4", className)}>
      <h3 className="flex items-center gap-2 text-sm font-semibold text-slate-800">
        <BookOpen className="h-4 w-4 text-brand-500" />
        Your learning path
      </h3>
      <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
        <span>{learnedCount} / {totalCount} concepts</span>
        <span className="text-slate-300">·</span>
        <span className="flex items-center gap-1">
          <Clock className="h-3.5 w-3.5" />
          ~{estimatedMinutesRemaining} min left
        </span>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-brand-500 transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      {recommended.length > 0 && (
        <div className="mt-4">
          <p className="text-xs font-medium text-slate-500">Recommended next</p>
          <ul className="mt-1 space-y-1">
            {recommended.slice(0, 3).map((ku) => (
              <li key={ku.id}>
                <Link
                  to={ROUTES.teach}
                  className="flex items-center justify-between rounded-lg px-2 py-1.5 text-sm text-slate-700 hover:bg-slate-50"
                >
                  <span>{ku.name || ku.id}</span>
                  <ChevronRight className="h-4 w-4 text-slate-400" />
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
