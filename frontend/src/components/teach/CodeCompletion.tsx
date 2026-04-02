import { useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PuzzleIcon, CheckCircle2 } from "lucide-react";
import type { CodeModification } from "./ProblemRenderer";

interface CodeCompletionProps {
  codeTemplate: string;
  slots: { line: number; placeholder: string }[];
  modifications: CodeModification[];
  problemStatement: string;
}

export function CodeCompletion({ codeTemplate, slots, modifications, problemStatement }: CodeCompletionProps) {
  const lines = useMemo(() => {
    return codeTemplate.split("\n").map((line, idx) => {
      const lineNum = idx + 1;
      const slot = slots.find((s) => s.line === lineNum);
      const mod = modifications.find((m) => m.line_number === lineNum);
      return {
        lineNum,
        content: line,
        isSlot: slot != null,
        placeholder: slot?.placeholder ?? "",
        filled: mod?.new_code ?? null,
      };
    });
  }, [codeTemplate, slots, modifications]);

  const filledCount = lines.filter((l) => l.filled).length;
  const totalSlots = slots.length;

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-stone-200 bg-stone-50">
        <div className="flex items-center gap-2 mb-1">
          <PuzzleIcon className="w-4 h-4 text-violet-500" />
          <span className="text-xs font-semibold text-violet-700 uppercase tracking-wide">
            Code Completion
          </span>
          {filledCount > 0 && (
            <span className="ml-auto flex items-center gap-1 text-xs text-emerald-600">
              <CheckCircle2 className="w-3 h-3" />
              {filledCount}/{totalSlots} filled
            </span>
          )}
        </div>
        <p className="text-sm text-stone-700">{problemStatement}</p>
      </div>

      <div className="flex-1 overflow-auto bg-[#1e1e2e] select-none" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        <table className="w-full text-sm font-mono">
          <tbody>
            {lines.map((line) => (
              <tr key={line.lineNum} className={line.isSlot ? (line.filled ? "bg-emerald-900/30" : "bg-amber-900/20") : ""}>
                <td className="w-10 px-2 py-0.5 text-right text-stone-500 select-none border-r border-stone-700/50 align-top">
                  {line.lineNum}
                </td>
                <td className="px-3 py-0.5 whitespace-pre">
                  <AnimatePresence mode="wait">
                    {line.isSlot && line.filled ? (
                      <motion.span
                        key={`filled-${line.lineNum}`}
                        initial={{ opacity: 0, backgroundColor: "rgba(52,211,153,0.3)" }}
                        animate={{ opacity: 1, backgroundColor: "rgba(52,211,153,0)" }}
                        transition={{ duration: 1 }}
                        className="text-emerald-300"
                      >
                        {line.filled}
                      </motion.span>
                    ) : line.isSlot ? (
                      <motion.span
                        key={`slot-${line.lineNum}`}
                        className="text-amber-400/60 italic"
                      >
                        {line.placeholder || "# ???"}
                      </motion.span>
                    ) : (
                      <span className="text-stone-200">{line.content}</span>
                    )}
                  </AnimatePresence>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
