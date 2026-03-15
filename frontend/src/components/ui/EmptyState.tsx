import type { LucideIcon } from "lucide-react";
import { Button } from "./Button";
import { cn } from "@/lib/utils";

export interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  action?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  className?: string;
  size?: "sm" | "md" | "lg";
  variant?: "default" | "compact" | "card";
}

const sizeClasses = {
  sm: { container: "py-8 px-4", icon: "h-8 w-8", title: "text-base", desc: "text-xs" },
  md: { container: "py-12 px-6", icon: "h-12 w-12", title: "text-lg", desc: "text-sm" },
  lg: { container: "py-16 px-8", icon: "h-16 w-16", title: "text-xl", desc: "text-base" },
};

const variantClasses = {
  default: "border border-dashed border-slate-200 bg-slate-50/50",
  compact: "border-0 bg-transparent",
  card: "border border-slate-200 bg-white shadow-sm",
};

export function EmptyState({ 
  icon: Icon, 
  title, 
  description, 
  action, 
  secondaryAction,
  className,
  size = "md",
  variant = "default",
}: EmptyStateProps) {
  const sizes = sizeClasses[size];
  
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl text-center",
        sizes.container,
        variantClasses[variant],
        className
      )}
      role="status"
      aria-live="polite"
    >
      <div className="relative">
        <div className="absolute inset-0 bg-brand-100 rounded-full blur-xl opacity-50" aria-hidden />
        <Icon className={cn("relative text-brand-400", sizes.icon)} aria-hidden />
      </div>
      <h3 className={cn("mt-4 font-semibold text-slate-700", sizes.title)}>{title}</h3>
      <p className={cn("mt-2 max-w-sm text-slate-500", sizes.desc)}>{description}</p>
      {(action || secondaryAction) && (
        <div className="mt-6 flex flex-col sm:flex-row gap-3">
          {action && (
            <Button variant="primary" size={size === "sm" ? "sm" : "md"} onClick={action.onClick}>
              {action.label}
            </Button>
          )}
          {secondaryAction && (
            <Button variant="ghost" size={size === "sm" ? "sm" : "md"} onClick={secondaryAction.onClick}>
              {secondaryAction.label}
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
