import { useState } from "react";
import { FileCode } from "lucide-react";

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
      <div className="px-4 py-3 border-b border-stone-200 bg-stone-50">
        <div className="flex items-center gap-2 mb-1">
          <FileCode className="w-4 h-4 text-teal-500" />
          <span className="text-xs font-semibold text-teal-700 uppercase tracking-wide">
            Short Code Answer
          </span>
        </div>
        <p className="text-sm text-stone-700 whitespace-pre-wrap">{problemStatement}</p>
      </div>

      <div className="flex-1 p-4">
        <textarea
          value={code}
          onChange={(e) => {
            setCode(e.target.value);
            onAnswer?.(e.target.value);
          }}
          disabled={disabled}
          spellCheck={false}
          className="w-full h-full min-h-[120px] rounded-lg border border-stone-300 bg-[#1e1e2e] text-stone-200 px-4 py-3 text-sm font-mono placeholder:text-stone-500 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 focus:outline-none resize-none disabled:opacity-50"
          placeholder="Write your code here..."
        />
      </div>
    </div>
  );
}
