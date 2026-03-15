import * as React from "react";
import { cn } from "@/lib/utils";

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "line" | "circle" | "rect";
  shimmer?: boolean;
}

const Skeleton = React.forwardRef<HTMLDivElement, SkeletonProps>(
  ({ className, variant = "line", shimmer = true, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "relative overflow-hidden bg-slate-200",
        shimmer && "before:absolute before:inset-0 before:-translate-x-full before:animate-shimmer before:bg-gradient-to-r before:from-transparent before:via-white/40 before:to-transparent",
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
    <div className="space-y-3 p-4">
      <Skeleton variant="rect" className="h-40 w-full" />
      <Skeleton variant="line" className="h-4 w-3/4" />
      <Skeleton variant="line" className="h-4 w-1/2" />
      <div className="flex gap-2 pt-2">
        <Skeleton variant="line" className="h-8 w-20" />
        <Skeleton variant="line" className="h-8 w-20" />
      </div>
    </div>
  );
}

export function SkeletonChat() {
  return (
    <div className="space-y-4 p-4">
      <div className="flex gap-3">
        <Skeleton variant="circle" className="h-10 w-10 shrink-0" />
        <div className="flex-1 space-y-2">
          <Skeleton variant="line" className="h-4 w-1/4" />
          <Skeleton variant="rect" className="h-20 w-full" />
        </div>
      </div>
      <div className="flex gap-3 justify-end">
        <div className="flex-1 space-y-2 max-w-[80%]">
          <Skeleton variant="rect" className="h-16 w-full" />
        </div>
      </div>
    </div>
  );
}

export function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-2 p-4">
      <div className="flex gap-4 pb-2">
        <Skeleton variant="line" className="h-6 w-1/4" />
        <Skeleton variant="line" className="h-6 w-1/4" />
        <Skeleton variant="line" className="h-6 w-1/4" />
        <Skeleton variant="line" className="h-6 w-1/4" />
      </div>
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <Skeleton variant="line" className="h-10 w-1/4" />
          <Skeleton variant="line" className="h-10 w-1/4" />
          <Skeleton variant="line" className="h-10 w-1/4" />
          <Skeleton variant="line" className="h-10 w-1/4" />
        </div>
      ))}
    </div>
  );
}

export function SkeletonDashboard() {
  return (
    <div className="space-y-6 p-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Skeleton variant="rect" className="h-24" />
        <Skeleton variant="rect" className="h-24" />
        <Skeleton variant="rect" className="h-24" />
        <Skeleton variant="rect" className="h-24" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Skeleton variant="rect" className="h-80 lg:col-span-2" />
        <Skeleton variant="rect" className="h-80" />
      </div>
    </div>
  );
}

export { Skeleton };
