import { useState } from "react";
import { HelpCircle, CheckSquare, Square } from "lucide-react";

interface ConceptMCQProps {
  problemStatement: string;
  choices: { id: string; text: string }[];
  onAnswer?: (selectedIds: string[]) => void;
  disabled?: boolean;
}

export function ConceptMCQ({ problemStatement, choices, onAnswer, disabled }: ConceptMCQProps) {
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    if (disabled) return;
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      onAnswer?.([...next]);
      return next;
    });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-stone-200 bg-stone-50">
        <div className="flex items-center gap-2 mb-1">
          <HelpCircle className="w-4 h-4 text-indigo-500" />
          <span className="text-xs font-semibold text-indigo-700 uppercase tracking-wide">
            Concept Question
          </span>
        </div>
        <p className="text-sm text-stone-700 whitespace-pre-wrap">{problemStatement}</p>
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-2">
        {choices.map((c) => {
          const isSelected = selected.has(c.id);
          return (
            <button
              key={c.id}
              onClick={() => toggle(c.id)}
              disabled={disabled}
              className={`w-full flex items-start gap-3 rounded-lg border p-3 text-left text-sm transition-all ${
                isSelected
                  ? "border-indigo-300 bg-indigo-50 text-indigo-900"
                  : "border-stone-200 bg-white text-stone-700 hover:border-stone-300 hover:bg-stone-50"
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isSelected ? (
                <CheckSquare className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
              ) : (
                <Square className="w-4 h-4 text-stone-400 shrink-0 mt-0.5" />
              )}
              <span>{c.text}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
