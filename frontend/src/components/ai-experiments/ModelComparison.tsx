import { Info } from "lucide-react";
import { cn } from "@/lib/utils";

export function ModelComparison({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-xl border border-slate-200 bg-slate-50/80 p-4 text-center",
        className
      )}
    >
      <Info className="mx-auto h-8 w-8 text-slate-400" />
      <h3 className="mt-2 text-sm font-semibold text-slate-700">Model comparison</h3>
      <p className="mt-1 text-xs text-slate-500">
        Compare responses from different AI models (e.g. GPT vs others) to learn about model behavior and bias.
        Available when multiple backends are configured.
      </p>
    </div>
  );
}
