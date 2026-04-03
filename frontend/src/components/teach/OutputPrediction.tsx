import { useState } from "react";
import { Eye, Terminal, ArrowRight } from "lucide-react";

interface OutputPredictionProps {
  code: string;
  problemStatement: string;
  onAnswer?: (value: string) => void;
  disabled?: boolean;
}

export function OutputPrediction({ code, problemStatement, onAnswer, disabled }: OutputPredictionProps) {
  const [value, setValue] = useState("");

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-3 border-b border-blue-200 bg-blue-50">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-7 h-7 rounded-lg bg-blue-100 border border-blue-200 flex items-center justify-center">
            <Eye className="w-4 h-4 text-blue-600" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
            Predict Output
          </span>
        </div>
        <p className="text-base text-stone-700 font-medium leading-relaxed">{problemStatement}</p>
        <p className="text-xs text-blue-600 mt-1">Read the code carefully before predicting</p>
      </div>

      {/* Code display */}
      <div className="flex-1 overflow-auto bg-[#1a1a2e] select-none p-4" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        <div className="flex items-center gap-2 mb-2 text-xs text-stone-500">
          <Terminal className="w-3.5 h-3.5" />
          <span>Python Code</span>
        </div>
        <pre className="text-sm font-mono text-stone-200 whitespace-pre-wrap leading-relaxed">{code}</pre>
      </div>

      {/* Answer input */}
      <div className="px-4 py-3 border-t border-stone-200 bg-white">
        <div className="flex items-center gap-2 mb-2">
          <ArrowRight className="w-4 h-4 text-blue-500" />
          <label className="text-sm font-medium text-stone-700">
            What will this code output?
          </label>
        </div>
        <textarea
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            onAnswer?.(e.target.value);
          }}
          disabled={disabled}
          placeholder="Type the expected output... (e.g., 'Hello World', 42, etc.)"
          className="w-full rounded-xl border border-stone-300 bg-stone-50 px-4 py-3 text-sm font-mono placeholder:text-stone-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none disabled:opacity-50 transition-all"
          rows={3}
        />
        <p className="text-xs text-stone-400 mt-1.5">Be precise - match spaces, newlines, and formatting</p>
      </div>
    </div>
  );
}
