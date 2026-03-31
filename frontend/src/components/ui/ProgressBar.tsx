import { cn } from "@/lib/utils";

interface ProgressBarProps {
  value: number;
  max?: number;
  className?: string;
  color?: "brand" | "success" | "warning" | "error" | "slate";
  showLabel?: boolean;
}

export function ProgressBar({
  value,
  max = 100,
  className,
  color = "brand",
  showLabel = false,
}: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  const colorClasses = {
    brand: "bg-brand-500",
    success: "bg-emerald-500",
    warning: "bg-amber-500",
    error: "bg-rose-500",
    slate: "bg-stone-500",
  };

  return (
    <div className={cn("w-full bg-stone-200 rounded-full overflow-hidden", className)}>
      <div
        className={cn("h-full transition-all duration-300 ease-out", colorClasses[color])}
        style={{ width: `${percentage}%` }}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      />
      {showLabel && (
        <span className="text-xs text-stone-500 mt-1">
          {Math.round(percentage)}%
        </span>
      )}
    </div>
  );
}
