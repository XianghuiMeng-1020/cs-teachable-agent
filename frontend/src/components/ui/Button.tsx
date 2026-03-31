import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/30 focus-visible:ring-offset-2",
  {
    variants: {
      variant: {
        primary: "bg-brand-700 text-white shadow-sm hover:bg-brand-800 active:bg-brand-900",
        secondary: "bg-stone-100 text-stone-700 hover:bg-stone-200 active:bg-stone-300",
        ghost: "bg-transparent text-stone-600 hover:bg-stone-100 active:bg-stone-200",
        danger: "bg-danger text-white hover:bg-red-700 active:bg-red-800",
        success: "bg-success text-white hover:bg-emerald-700 active:bg-emerald-800",
        outline: "border border-stone-300 bg-transparent text-stone-700 hover:bg-stone-50 hover:border-stone-400 active:bg-stone-100",
        link: "bg-transparent text-brand-700 underline-offset-4 hover:underline active:text-brand-800 p-0 h-auto",
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
