import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bug, CheckCircle2 } from "lucide-react";
import { watermarkCode } from "@/lib/watermark";
import { CanvasWatermark } from "./CanvasWatermark";
import { CodeRunPreview } from "./CodeRunPreview";
import type { CodeModification } from "./ProblemRenderer";

interface BuggyCodeBlockProps {
  code: string;
  bugLines: number[];
  modifications: CodeModification[];
  problemStatement: string;
  userId?: number;
  username?: string;
  onLineClick?: (lineNum: number, lineContent: string) => void;
}

export function BuggyCodeBlock({ code, bugLines, modifications, problemStatement, userId, username, onLineClick }: BuggyCodeBlockProps) {
  const [appliedMods, setAppliedMods] = useState<Set<number>>(new Set());
  const [selectedLine, setSelectedLine] = useState<number | null>(null);

  useEffect(() => {
    if (modifications.length > appliedMods.size) {
      const unapplied = modifications.filter((m) => !appliedMods.has(m.line_number));
      if (unapplied.length > 0) {
        const timer = setTimeout(() => {
          setAppliedMods((prev) => {
            const next = new Set(prev);
            next.add(unapplied[0].line_number);
            return next;
          });
        }, 800);
        return () => clearTimeout(timer);
      }
    }
  }, [modifications, appliedMods]);

  const lines = useMemo(() => {
    const watermarked = userId ? watermarkCode(code, userId) : code;
    const original = watermarked.split("\n");
    return original.map((line, idx) => {
      const lineNum = idx + 1;
      const mod = modifications.find((m) => m.line_number === lineNum);
      const isApplied = appliedMods.has(lineNum);
      const isBugLine = bugLines.includes(lineNum);
      return {
        lineNum,
        original: line,
        fixed: mod?.new_code ?? null,
        isFixed: isApplied && mod != null,
        isBugLine,
        explanation: mod?.explanation,
      };
    });
  }, [code, bugLines, modifications, appliedMods, userId]);

  const fixedCount = lines.filter((l) => l.isFixed).length;
  const totalBugs = bugLines.length;

  return (
    <div className="flex flex-col h-full">
      {/* Problem Statement */}
      <div className="px-4 py-3 border-b border-stone-200 bg-stone-50">
        <div className="flex items-center gap-2 mb-1">
          <Bug className="w-4 h-4 text-red-500" />
          <span className="text-xs font-semibold text-red-700 uppercase tracking-wide">
            Buggy Code
          </span>
          {fixedCount > 0 && (
            <span className="ml-auto flex items-center gap-1 text-xs text-emerald-600">
              <CheckCircle2 className="w-3 h-3" />
              {fixedCount}/{totalBugs} fixed
            </span>
          )}
        </div>
        <p className="text-sm text-stone-700">{problemStatement}</p>
      </div>

      {/* Code Area */}
      <div className="flex-1 overflow-auto bg-[#1e1e2e] select-none relative" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        {userId && <CanvasWatermark userId={userId} username={username} />}
        <table className="w-full text-sm font-mono ocr-noise">
          <tbody>
            {lines.map((line) => (
              <tr
                key={line.lineNum}
                onClick={() => {
                  setSelectedLine(line.lineNum);
                  onLineClick?.(line.lineNum, line.original);
                }}
                className={`cursor-pointer transition-colors hover:bg-white/5 ${
                  selectedLine === line.lineNum ? "ring-1 ring-inset ring-blue-400/50" : ""
                } ${
                  line.isFixed ? "bg-emerald-900/30" : line.isBugLine ? "bg-red-900/20" : ""
                }`}
              >
                {/* Line number gutter */}
                <td className="w-10 px-2 py-0.5 text-right text-stone-500 select-none border-r border-stone-700/50 align-top">
                  {line.lineNum}
                </td>
                {/* Code */}
                <td className="px-3 py-0.5 whitespace-pre">
                  <AnimatePresence mode="wait">
                    {line.isFixed && line.fixed != null ? (
                      <motion.span
                        key={`fixed-${line.lineNum}`}
                        initial={{ opacity: 0, backgroundColor: "rgba(52,211,153,0.3)" }}
                        animate={{ opacity: 1, backgroundColor: "rgba(52,211,153,0)" }}
                        transition={{ duration: 1.2 }}
                        className="text-emerald-300"
                      >
                        {line.fixed}
                      </motion.span>
                    ) : (
                      <motion.span
                        key={`orig-${line.lineNum}`}
                        exit={{ opacity: 0 }}
                        className={line.isBugLine ? "text-red-300" : "text-stone-200"}
                      >
                        {line.original}
                      </motion.span>
                    )}
                  </AnimatePresence>
                </td>
                {/* Indicator */}
                <td className="w-6 px-1">
                  {line.isFixed && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                  {!line.isFixed && line.isBugLine && <Bug className="w-3.5 h-3.5 text-red-400 opacity-50" />}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedLine && lines.find((l) => l.lineNum === selectedLine && l.isFixed) && (
        <div className="px-4 py-2 border-t border-stone-700 bg-stone-800/50 font-mono text-xs">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-stone-400 font-sans text-[10px] uppercase tracking-wide">Line {selectedLine} Diff</span>
          </div>
          <div className="text-red-400 line-through opacity-70">
            - {lines.find((l) => l.lineNum === selectedLine)?.original}
          </div>
          <div className="text-emerald-400">
            + {lines.find((l) => l.lineNum === selectedLine)?.fixed}
          </div>
        </div>
      )}

      {/* Fix explanations */}
      {modifications.filter((m) => appliedMods.has(m.line_number) && m.explanation).length > 0 && (
        <div className="px-4 py-2 border-t border-stone-200 bg-emerald-50 space-y-1">
          {modifications
            .filter((m) => appliedMods.has(m.line_number) && m.explanation)
            .map((m) => (
              <p key={m.line_number} className="text-xs text-emerald-800">
                <span className="font-semibold">Line {m.line_number}:</span> {m.explanation}
              </p>
            ))}
        </div>
      )}

      {/* Code execution preview */}
      <CodeRunPreview code={code} />
    </div>
  );
}
