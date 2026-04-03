import { useState } from "react";
import { FileCode, Terminal, Sparkles } from "lucide-react";

interface ShortCodeAnswerProps {
  problemStatement: string;
  starterCode: string;
  onAnswer?: (code: string) => void;
  disabled?: boolean;
}

export function ShortCodeAnswer({ problemStatement, starterCode, onAnswer, disabled }: ShortCodeAnswerProps) {
  const [code, setCode] = useState(starterCode);

  return (
    <div className="flex flex-col h-full">
      {/* Problem statement (if provided directly) */}
      {problemStatement && (
        <p className="text-base text-stone-700 font-medium leading-relaxed mb-4">{problemStatement}</p>
      )}
      
      {/* Code editor area */}
      <div className="flex-1 flex flex-col min-h-0 rounded-xl border border-stone-300 bg-[#1a1a2e] overflow-hidden">
        {/* Toolbar */}
        <div className="flex items-center justify-between px-3 py-2 bg-stone-800 border-b border-stone-700">
          <div className="flex items-center gap-2 text-xs text-stone-400">
            <Terminal className="w-3.5 h-3.5" />
            <span>code_editor.py</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
          </div>
        </div>
        
        {/* Editor */}
        <textarea
          value={code}
          onChange={(e) => {
            setCode(e.target.value);
            onAnswer?.(e.target.value);
          }}
          disabled={disabled}
          spellCheck={false}
          className="flex-1 w-full min-h-[160px] bg-[#1a1a2e] text-stone-200 px-4 py-3 text-sm font-mono placeholder:text-stone-600 focus:outline-none resize-none disabled:opacity-50 leading-relaxed"
          placeholder="# Write your solution here\n# The agent will learn from your approach\n\ndef solution():\n    pass"
        />
        
        {/* Footer */}
        <div className="px-3 py-1.5 bg-stone-800/50 border-t border-stone-700 flex items-center justify-between text-[10px] text-stone-500">
          <div className="flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            <span>AI will check your code for correctness</span>
          </div>
          <span>{code.length} chars</span>
        </div>
      </div>
    </div>
  );
}
