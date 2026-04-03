import { useState } from "react";
import { motion } from "framer-motion";
import { CheckSquare, Square } from "lucide-react";

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
    <div className="space-y-3">
      {/* Problem statement (if provided directly) */}
      {problemStatement && (
        <p className="text-base text-stone-700 font-medium leading-relaxed mb-4">{problemStatement}</p>
      )}
      
      {/* Choices as cards */}
      <div className="space-y-2">
        {choices.map((c, i) => {
          const isSelected = selected.has(c.id);
          return (
            <motion.button
              key={c.id}
              onClick={() => toggle(c.id)}
              disabled={disabled}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              whileHover={{ scale: disabled ? 1 : 1.01 }}
              whileTap={{ scale: disabled ? 1 : 0.99 }}
              className={`w-full flex items-start gap-3 rounded-xl border-2 p-4 text-left transition-all ${
                isSelected
                  ? "border-emerald-400 bg-emerald-50/50 shadow-sm"
                  : "border-stone-200 bg-white text-stone-700 hover:border-stone-300 hover:bg-stone-50/50"
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <div className={`shrink-0 w-6 h-6 rounded-md flex items-center justify-center transition-colors ${
                isSelected ? "bg-emerald-500" : "bg-stone-200"
              }`}>
                {isSelected ? (
                  <CheckSquare className="w-4 h-4 text-white" />
                ) : (
                  <Square className="w-4 h-4 text-stone-400" />
                )}
              </div>
              <span className={`text-sm leading-relaxed pt-0.5 ${isSelected ? "text-emerald-900 font-medium" : "text-stone-700"}`}>
                {c.text}
              </span>
            </motion.button>
          );
        })}
      </div>

      {/* Selection hint */}
      <p className="text-xs text-stone-400 text-center pt-2">
        {selected.size === 0 
          ? "Select one or more answers" 
          : `${selected.size} option${selected.size > 1 ? 's' : ''} selected`}
      </p>
    </div>
  );
}
