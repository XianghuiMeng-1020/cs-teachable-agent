import { useState } from "react";
import { Terminal } from "lucide-react";

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
      <div className="px-4 py-3 border-b border-stone-200 bg-stone-50">
        <div className="flex items-center gap-2 mb-1">
          <Terminal className="w-4 h-4 text-blue-500" />
          <span className="text-xs font-semibold text-blue-700 uppercase tracking-wide">
            Output Prediction
          </span>
        </div>
        <p className="text-sm text-stone-700">{problemStatement}</p>
      </div>

      <div className="flex-1 overflow-auto bg-[#1e1e2e] select-none p-4" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        <pre className="text-sm font-mono text-stone-200 whitespace-pre-wrap">{code}</pre>
      </div>

      <div className="px-4 py-3 border-t border-stone-200 bg-white">
        <label className="block text-xs font-medium text-stone-600 mb-1">
          What will this code output?
        </label>
        <textarea
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            onAnswer?.(e.target.value);
          }}
          disabled={disabled}
          placeholder="Type the expected output..."
          className="w-full rounded-lg border border-stone-300 bg-stone-50 px-3 py-2 text-sm font-mono placeholder:text-stone-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none disabled:opacity-50"
          rows={3}
        />
      </div>
    </div>
  );
}
