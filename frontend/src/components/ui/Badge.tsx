import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full font-medium border",
  {
    variants: {
      variant: {
        default: "bg-stone-100 text-stone-700 border-stone-200/60",
        success: "bg-emerald-50 text-emerald-700 border-emerald-200/60",
        warning: "bg-amber-50 text-amber-700 border-amber-200/60",
        danger: "bg-red-50 text-red-700 border-red-200/60",
        info: "bg-brand-50 text-brand-800 border-brand-200/60",
        outline: "bg-transparent text-stone-600 border-stone-300",
      },
      size: {
        sm: "px-2 py-0.5 text-xs",
        md: "px-2.5 py-1 text-xs",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
}

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, size, dot, children, ...props }, ref) => (
    <span
      ref={ref}
      className={cn(badgeVariants({ variant, size }), className)}
      {...props}
    >
      {dot && <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-current" aria-hidden />}
      {children}
    </span>
  )
);
Badge.displayName = "Badge";

export { Badge, badgeVariants };
