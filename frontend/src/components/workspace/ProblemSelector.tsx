import * as Select from "@radix-ui/react-select";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ProblemOption {
  problem_id: string;
  problem_statement: string;
  difficulty?: string;
}

interface ProblemSelectorProps {
  problems: ProblemOption[];
  value: string | null;
  onValueChange: (problemId: string | null) => void;
  disabled?: boolean;
  className?: string;
}

const AUTO_ID = "__auto__";

export function ProblemSelector({
  problems,
  value,
  onValueChange,
  disabled,
  className,
}: ProblemSelectorProps) {
  const displayValue =
    value === null || value === AUTO_ID
      ? "Auto-select"
      : (() => {
          const p = problems.find((x) => x.problem_id === value);
          return p ? `${p.problem_id}: ${p.problem_statement.slice(0, 40)}...` : value;
        })();

  return (
    <Select.Root
      value={value ?? AUTO_ID}
      onValueChange={(v) => onValueChange(v === AUTO_ID ? null : v)}
      disabled={disabled}
    >
      <Select.Trigger
        className={cn(
          "flex h-9 w-full min-w-0 items-center justify-between gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700",
          "hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-brand-500/20 disabled:opacity-50",
          className
        )}
      >
        <span className="truncate">{displayValue}</span>
        <ChevronDown className="h-4 w-4 shrink-0 text-slate-400" />
      </Select.Trigger>
      <Select.Portal>
        <Select.Content
          className="z-50 max-h-[280px] overflow-auto rounded-lg border border-slate-200 bg-white py-1 shadow-card"
          position="popper"
          sideOffset={4}
        >
          <Select.Item
            value={AUTO_ID}
            className="cursor-pointer px-3 py-2 text-sm outline-none hover:bg-slate-100 data-[highlighted]:bg-slate-100"
          >
            Auto-select
          </Select.Item>
          {problems.map((p) => (
            <Select.Item
              key={p.problem_id}
              value={p.problem_id}
              className="cursor-pointer px-3 py-2 text-sm outline-none hover:bg-slate-100 data-[highlighted]:bg-slate-100"
            >
              <span className="font-mono text-xs text-slate-500">{p.problem_id}</span>
              <span className="ml-2">{p.problem_statement.slice(0, 40)}...</span>
            </Select.Item>
          ))}
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
