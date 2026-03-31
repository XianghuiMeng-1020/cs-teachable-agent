import { cn } from "@/lib/utils";
import { CheckCircle2, Circle, Target } from "lucide-react";

interface AssessmentProgressProps {
  totalAttempts: number;
  correctAttempts: number;
  accuracy: number;
  uniqueItemsSolved: number;
  totalItemsAvailable: number;
  className?: string;
}

export function AssessmentProgress({
  totalAttempts,
  correctAttempts,
  accuracy,
  uniqueItemsSolved,
  totalItemsAvailable,
  className,
}: AssessmentProgressProps) {
  const progressPercent = totalItemsAvailable > 0
    ? Math.round((uniqueItemsSolved / totalItemsAvailable) * 100)
    : 0;

  return (
    <div className={cn("grid grid-cols-2 gap-3 sm:grid-cols-4", className)}>
      <StatCard
        icon={<Target className="h-4 w-4 text-brand-600" />}
        label="Solved"
        value={`${uniqueItemsSolved}/${totalItemsAvailable}`}
        sub={`${progressPercent}%`}
      />
      <StatCard
        icon={<CheckCircle2 className="h-4 w-4 text-green-600" />}
        label="Correct"
        value={String(correctAttempts)}
        sub={`${Math.round(accuracy * 100)}% accuracy`}
      />
      <StatCard
        icon={<Circle className="h-4 w-4 text-stone-400" />}
        label="Attempts"
        value={String(totalAttempts)}
        sub="total"
      />
      <div className="rounded-lg border border-stone-200 bg-white p-3">
        <div className="text-xs text-stone-500 mb-1">Progress</div>
        <div className="h-2 w-full rounded-full bg-stone-100 overflow-hidden">
          <div
            className="h-full rounded-full bg-brand-500 transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <div className="mt-1 text-xs text-stone-500 text-right">{progressPercent}%</div>
      </div>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  sub,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub: string;
}) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-3">
      <div className="flex items-center gap-1.5 mb-1">
        {icon}
        <span className="text-xs text-stone-500">{label}</span>
      </div>
      <div className="text-lg font-semibold text-stone-900">{value}</div>
      <div className="text-xs text-stone-500">{sub}</div>
    </div>
  );
}
