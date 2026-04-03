import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/30 dark:focus-visible:ring-brand-400/30 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-surfaceDark tap-target",
  {
    variants: {
      variant: {
        primary: "bg-brand-700 dark:bg-brand-600 text-white shadow-sm hover:bg-brand-800 dark:hover:bg-brand-500 active:bg-brand-900 dark:active:bg-brand-700",
        secondary: "bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700 active:bg-stone-300 dark:active:bg-stone-600",
        ghost: "bg-transparent text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800 active:bg-stone-200 dark:active:bg-stone-700",
        danger: "bg-danger text-white hover:bg-red-700 active:bg-red-800",
        success: "bg-success text-white hover:bg-emerald-700 active:bg-emerald-800",
        outline: "border border-stone-300 dark:border-stone-600 bg-transparent text-stone-700 dark:text-stone-300 hover:bg-stone-50 dark:hover:bg-stone-800 hover:border-stone-400 dark:hover:border-stone-500 active:bg-stone-100 dark:active:bg-stone-700",
        link: "bg-transparent text-brand-700 dark:text-brand-400 underline-offset-4 hover:underline active:text-brand-800 dark:active:text-brand-300 p-0 h-auto",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-9 px-4 text-sm",
        lg: "h-11 px-6 text-sm",
        xl: "h-12 px-8 text-base",
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
        {loading && <Loader2 className="h-4 w-4 animate-spin shrink-0" aria-hidden="true" />}
        {Icon && !loading && <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />}
        {children != null && (
          <span className={loading ? "invisible" : undefined}>{children}</span>
        )}
        {IconRight && !loading && <IconRight className="h-4 w-4 shrink-0" aria-hidden="true" />}
      </button>
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
