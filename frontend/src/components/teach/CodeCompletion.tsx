import { useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PuzzleIcon, CheckCircle2, Code, Terminal } from "lucide-react";
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
      {/* Header */}
      <div className="px-4 py-3 border-b border-purple-200 bg-purple-50">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-7 h-7 rounded-lg bg-purple-100 border border-purple-200 flex items-center justify-center">
            <PuzzleIcon className="w-4 h-4 text-purple-600" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
            Complete Code
          </span>
          {filledCount > 0 && (
            <span className="ml-auto flex items-center gap-1.5 text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-200">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {filledCount}/{totalSlots} filled
            </span>
          )}
        </div>
        <p className="text-base text-stone-700 font-medium leading-relaxed">{problemStatement}</p>
      </div>

      {/* Code with completion slots */}
      <div className="flex-1 overflow-auto bg-[#1a1a2e] select-none" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        <div className="flex items-center gap-2 px-4 py-2 text-xs text-stone-500 border-b border-stone-800">
          <Code className="w-3.5 h-3.5" />
          <span>Fill in the highlighted blanks</span>
        </div>
        <table className="w-full text-sm font-mono">
          <tbody>
            {lines.map((line) => (
              <tr 
                key={line.lineNum} 
                className={line.isSlot ? (line.filled ? "bg-emerald-900/20" : "bg-amber-900/15") : "hover:bg-white/5 transition-colors"}
              >
                <td className="w-12 px-3 py-1.5 text-right text-xs font-medium text-stone-500 select-none border-r border-stone-700/50">
                  {line.lineNum}
                </td>
                <td className="px-4 py-1.5 whitespace-pre">
                  <AnimatePresence mode="wait">
                    {line.isSlot && line.filled ? (
                      <motion.span
                        key={`filled-${line.lineNum}`}
                        initial={{ opacity: 0, x: -8, backgroundColor: "rgba(52,211,153,0.4)" }}
                        animate={{ opacity: 1, x: 0, backgroundColor: "rgba(52,211,153,0)" }}
                        transition={{ duration: 0.4 }}
                        className="text-emerald-300 font-medium"
                      >
                        {line.filled}
                      </motion.span>
                    ) : line.isSlot ? (
                      <motion.span
                        key={`slot-${line.lineNum}`}
                        className="text-amber-300/70 italic bg-amber-500/10 px-2 py-0.5 rounded"
                      >
                        {line.placeholder || "# ???"}
                      </motion.span>
                    ) : (
                      <span className="text-stone-200">{line.content}</span>
                    )}
                  </AnimatePresence>
                </td>
                <td className="w-8 px-2">
                  {line.filled && (
                    <motion.div
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ type: "spring", stiffness: 500, damping: 15 }}
                    >
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    </motion.div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Progress hint */}
      {totalSlots > 0 && filledCount < totalSlots && (
        <div className="px-4 py-2 border-t border-stone-200 bg-stone-50">
          <p className="text-xs text-stone-500">
            <Terminal className="w-3 h-3 inline mr-1" />
            The agent is waiting for you to explain the missing code...
          </p>
        </div>
      )}
    </div>
  );
}
