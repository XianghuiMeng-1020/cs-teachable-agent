import * as React from "react";
import { cn } from "@/lib/utils";

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "line" | "circle" | "rect";
}

const Skeleton = React.forwardRef<HTMLDivElement, SkeletonProps>(
  ({ className, variant = "line", ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "animate-pulse bg-slate-200",
        variant === "line" && "h-4 rounded",
        variant === "circle" && "rounded-full",
        variant === "rect" && "rounded-lg",
        className
      )}
      {...props}
    />
  )
);
Skeleton.displayName = "Skeleton";

export function SkeletonCard() {
  return (
    <div className="space-y-3">
      <Skeleton variant="rect" className="h-40 w-full" />
      <Skeleton variant="line" className="h-4 w-3/4" />
      <Skeleton variant="line" className="h-4 w-1/2" />
      <Skeleton variant="line" className="h-4 w-2/3" />
    </div>
  );
}

export { Skeleton };
