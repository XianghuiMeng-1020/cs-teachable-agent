import type { LucideIcon } from "lucide-react";
import { Card } from "./Card";
import { Skeleton } from "./Skeleton";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown } from "lucide-react";

export interface StatCardProps {
  label: string;
  value: string | number;
  change?: { value: number; label: string };
  icon: LucideIcon;
  iconColor: string;
  loading?: boolean;
  className?: string;
}

export function StatCard({
  label,
  value,
  change,
  icon: Icon,
  iconColor,
  loading = false,
  className,
}: StatCardProps) {
  return (
    <Card padding="md" className={cn(className)}>
      <div className="flex items-start gap-4">
        <div
          className={cn(
            "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
            iconColor
          )}
        >
          <Icon className="h-5 w-5" aria-hidden />
        </div>
        <div className="min-w-0 flex-1">
          {loading ? (
            <Skeleton variant="line" className="mb-1 h-7 w-20" />
          ) : (
            <p className="text-2xl font-bold text-stone-900">{value}</p>
          )}
          <p className="text-sm text-stone-500">{label}</p>
          {change != null && !loading && (
            <p
              className={cn(
                "mt-1 flex items-center gap-1 text-xs font-medium",
                change.value >= 0 ? "text-success" : "text-danger"
              )}
            >
              {change.value >= 0 ? (
                <TrendingUp className="h-3.5 w-3.5" />
              ) : (
                <TrendingDown className="h-3.5 w-3.5" />
              )}
              {change.value >= 0 ? "+" : ""}
              {change.value}% {change.label}
            </p>
          )}
        </div>
      </div>
    </Card>
  );
}
