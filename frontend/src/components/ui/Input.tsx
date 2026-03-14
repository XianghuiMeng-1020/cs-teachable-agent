import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, leftIcon, rightIcon, id: idProp, ...props }, ref) => {
    const generatedId = React.useId();
    const inputId = idProp ?? generatedId;
    const errorId = `${inputId}-error`;
    return (
      <div className="w-full">
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">{leftIcon}</div>
          )}
          <input
            type={type}
            ref={ref}
            id={inputId}
            aria-invalid={error ? true : undefined}
            aria-describedby={error ? errorId : undefined}
            className={cn(
              "flex h-9 w-full rounded-lg border bg-white px-3 py-2 text-sm transition-colors",
              "placeholder:text-slate-400",
              "focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 focus:outline-none",
              error && "border-danger ring-2 ring-danger/20",
              !error && "border-slate-300",
              leftIcon && "pl-9",
              rightIcon && "pr-9",
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">{rightIcon}</div>
          )}
        </div>
        {error && (
          <p id={errorId} className="mt-1 text-xs text-danger" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
