import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, label, leftIcon, rightIcon, id: idProp, ...props }, ref) => {
    const generatedId = React.useId();
    const inputId = idProp ?? generatedId;
    const errorId = `${inputId}-error`;
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="mb-1.5 block text-sm font-medium text-stone-700">
            {label}
          </label>
        )}
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-400">{leftIcon}</div>
          )}
          <input
            type={type}
            ref={ref}
            id={inputId}
            aria-invalid={error ? true : undefined}
            aria-describedby={error ? errorId : undefined}
            className={cn(
              "flex h-10 w-full rounded-lg border bg-white px-3.5 py-2.5 text-sm text-ink transition-colors duration-150",
              "placeholder:text-stone-400",
              "hover:border-stone-400",
              "focus:border-brand-600 focus:ring-2 focus:ring-brand-600/10 focus:outline-none",
              error && "border-danger ring-2 ring-danger/10",
              !error && "border-stone-300",
              leftIcon && "pl-10",
              rightIcon && "pr-10",
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400">{rightIcon}</div>
          )}
        </div>
        {error && (
          <p id={errorId} className="mt-1.5 text-xs text-danger" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
