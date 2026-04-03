import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bug, CheckCircle2, AlertCircle, Zap, Play } from "lucide-react";
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
        }, 600);
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
  const progressPercent = totalBugs > 0 ? (fixedCount / totalBugs) * 100 : 0;

  return (
    <div className="flex flex-col h-full">
      {/* Problem Statement - Enhanced */}
      <div className="px-4 py-4 border-b border-stone-200 bg-stone-50">
        {/* Type badge */}
        <div className="flex items-center gap-2 mb-2">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-red-50 border border-red-200">
            <Bug className="w-3.5 h-3.5 text-red-600" />
            <span className="text-xs font-semibold text-red-700">Find the Bug</span>
          </div>
          
          {/* Fix progress */}
          {totalBugs > 0 && (
            <div className="flex-1 flex items-center gap-2">
              <div className="flex-1 h-1.5 bg-stone-200 rounded-full overflow-hidden max-w-[100px]">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${progressPercent}%` }}
                  className="h-full bg-emerald-500 rounded-full"
                />
              </div>
              <span className={`text-xs font-medium ${fixedCount === totalBugs ? "text-emerald-600" : "text-stone-500"}`}>
                {fixedCount}/{totalBugs} fixed
              </span>
            </div>
          )}
        </div>
        
        <p className="text-base text-stone-700 leading-relaxed font-medium">{problemStatement}</p>
        
        {fixedCount === totalBugs && totalBugs > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 flex items-center gap-2 text-sm text-emerald-700 bg-emerald-50 px-3 py-2 rounded-lg border border-emerald-200"
          >
            <Zap className="w-4 h-4 fill-emerald-500" />
            <span className="font-medium">All bugs found! Great job!</span>
          </motion.div>
        )}
      </div>

      {/* Code Area - Enhanced styling */}
      <div className="flex-1 overflow-auto bg-[#1a1a2e] select-none relative" style={{ userSelect: "none", WebkitUserSelect: "none" }}>
        {userId && <CanvasWatermark userId={userId} username={username} />}
        <table className="w-full text-sm font-mono">
          <tbody>
            {lines.map((line) => {
              const isSelected = selectedLine === line.lineNum;
              
              return (
                <tr
                  key={line.lineNum}
                  onClick={() => {
                    setSelectedLine(line.lineNum);
                    onLineClick?.(line.lineNum, line.original);
                  }}
                  className="group transition-colors duration-150"
                >
                  {/* Line number gutter - Enhanced */}
                  <td 
                    className={`w-12 px-3 py-1.5 text-right text-xs font-medium border-r transition-colors ${
                      isSelected 
                        ? "text-blue-400 bg-blue-500/10 border-blue-500/30" 
                        : "text-stone-500 border-stone-700/50 group-hover:text-stone-400"
                    }`}
                  >
                    {line.lineNum}
                  </td>
                  
                  {/* Code content - Enhanced with accent bars */}
                  <td className="relative px-4 py-1.5 whitespace-pre">
                    {/* Accent bar for bug/fixed lines */}
                    {!line.isFixed && line.isBugLine && (
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500" />
                    )}
                    {line.isFixed && (
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500" />
                    )}
                    {isSelected && !line.isBugLine && !line.isFixed && (
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500" />
                    )}
                    
                    {/* Background highlight */}
                    <div className={`absolute inset-0 -z-10 transition-colors ${
                      line.isFixed ? "bg-emerald-500/8" : 
                      line.isBugLine ? "bg-red-500/8 group-hover:bg-red-500/12" : 
                      isSelected ? "bg-blue-500/8" : 
                      "group-hover:bg-white/5"
                    }`} />
                    
                    <AnimatePresence mode="wait">
                      {line.isFixed && line.fixed != null ? (
                        <motion.span
                          key={`fixed-${line.lineNum}`}
                          initial={{ opacity: 0, x: -8 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: 8 }}
                          transition={{ duration: 0.3 }}
                          className="text-emerald-300"
                        >
                          {line.fixed}
                        </motion.span>
                      ) : (
                        <motion.span
                          key={`orig-${line.lineNum}`}
                          exit={{ opacity: 0.5 }}
                          className={`transition-colors duration-200 ${
                            line.isBugLine ? "text-red-300" : "text-stone-200"
                          }`}
                        >
                          {line.original}
                        </motion.span>
                      )}
                    </AnimatePresence>
                  </td>
                  
                  {/* Indicator column */}
                  <td className="w-8 px-2">
                    {line.isFixed ? (
                      <motion.div
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ type: "spring", stiffness: 500, damping: 15 }}
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      </motion.div>
                    ) : line.isBugLine ? (
                      <div className="opacity-50 group-hover:opacity-100 transition-opacity">
                        <AlertCircle className="w-4 h-4 text-red-400" />
                      </div>
                    ) : null}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Fix explanations */}
      <AnimatePresence>
        {modifications.filter((m) => appliedMods.has(m.line_number) && m.explanation).length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="px-4 py-3 border-t border-emerald-200 bg-emerald-50 space-y-2"
          >
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 mb-2">
              <Zap className="w-3.5 h-3.5" />
              Bug Fixes
            </div>
            {modifications
              .filter((m) => appliedMods.has(m.line_number) && m.explanation)
              .map((m) => (
                <div 
                  key={m.line_number} 
                  className="flex items-start gap-2 text-sm text-emerald-800"
                >
                  <span className="shrink-0 text-xs font-bold bg-emerald-200 text-emerald-700 px-1.5 py-0.5 rounded">
                    L{m.line_number}
                  </span>
                  <span className="leading-relaxed">{m.explanation}</span>
                </div>
              ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Code execution preview */}
      <CodeRunPreview code={code} />
    </div>
  );
}
