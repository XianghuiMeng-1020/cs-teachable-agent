import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/30 focus-visible:ring-offset-2 active:scale-[0.97] active:duration-75",
  {
    variants: {
      variant: {
        primary: "bg-brand-500 text-white shadow-sm hover:bg-brand-600 hover:shadow-md active:bg-brand-700",
        secondary: "bg-slate-100 text-slate-700 hover:bg-slate-200 hover:shadow-sm active:bg-slate-300",
        ghost: "bg-transparent text-slate-600 hover:bg-slate-100 active:bg-slate-200",
        danger: "bg-danger text-white hover:bg-red-600 hover:shadow-md active:bg-red-700",
        success: "bg-success text-white hover:bg-emerald-600 hover:shadow-md active:bg-emerald-700",
        outline: "border border-slate-300 bg-transparent text-slate-700 hover:bg-slate-50 hover:border-slate-400 active:bg-slate-100",
        link: "bg-transparent text-brand-500 underline-offset-4 hover:underline active:text-brand-600",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-9 px-4 text-sm",
        lg: "h-11 px-6 text-base",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
  icon?: LucideIcon;
  iconRight?: LucideIcon;
  fullWidth?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      loading = false,
      icon: Icon,
      iconRight: IconRight,
      fullWidth,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), fullWidth && "w-full", className)}
        disabled={disabled ?? loading}
        {...props}
      >
        {loading && <Loader2 className="h-4 w-4 animate-spin shrink-0" aria-hidden />}
        {Icon && !loading && <Icon className="h-4 w-4 shrink-0" aria-hidden />}
        {children != null && (
          <span className={loading ? "invisible" : undefined}>{children}</span>
        )}
        {IconRight && !loading && <IconRight className="h-4 w-4 shrink-0" aria-hidden />}
      </button>
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
