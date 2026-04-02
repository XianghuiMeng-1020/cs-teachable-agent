import { useState, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Play, Loader2, Terminal, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { getToken } from "@/api/client";

const API_BASE =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "/api" : "/api");

interface CodeRunPreviewProps {
  code: string;
  disabled?: boolean;
}

interface RunResult {
  stdout: string;
  stderr: string;
  returncode: number;
}

export function CodeRunPreview({ code, disabled }: CodeRunPreviewProps) {
  const { t } = useTranslation();
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [showPanel, setShowPanel] = useState(false);

  const runCode = useCallback(async () => {
    if (!code.trim()) return;
    setRunning(true);
    setShowPanel(true);
    try {
      const token = getToken();
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API_BASE}/sandbox/run-problem-code`, {
        method: "POST",
        headers,
        body: JSON.stringify({ code }),
      });
      if (!res.ok) {
        setResult({ stdout: "", stderr: `HTTP ${res.status}`, returncode: -1 });
        return;
      }
      const data: RunResult = await res.json();
      setResult(data);
    } catch (err) {
      setResult({
        stdout: "",
        stderr: err instanceof Error ? err.message : "Unknown error",
        returncode: -1,
      });
    } finally {
      setRunning(false);
    }
  }, [code]);

  return (
    <div className="border-t border-stone-200">
      <div className="flex items-center justify-between px-3 py-1.5 bg-stone-50">
        <button
          onClick={runCode}
          disabled={disabled || running || !code.trim()}
          className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md bg-stone-800 text-white hover:bg-stone-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {running ? (
            <Loader2 className="w-3 h-3 animate-spin" />
          ) : (
            <Play className="w-3 h-3" />
          )}
          {t("teach.runCode", { defaultValue: "Run" })}
        </button>
        {showPanel && (
          <button
            onClick={() => { setShowPanel(false); setResult(null); }}
            className="p-0.5 rounded hover:bg-stone-200 text-stone-400"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
      <AnimatePresence>
        {showPanel && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="bg-stone-900 px-3 py-2 font-mono text-xs max-h-32 overflow-auto">
              <div className="flex items-center gap-1.5 mb-1 text-stone-500">
                <Terminal className="w-3 h-3" />
                <span className="text-[10px] uppercase tracking-wide">
                  {t("teach.output", { defaultValue: "Output" })}
                </span>
              </div>
              {running ? (
                <div className="text-stone-400 animate-pulse">Running...</div>
              ) : result ? (
                <>
                  {result.stdout && (
                    <pre className="text-emerald-300 whitespace-pre-wrap break-all">{result.stdout}</pre>
                  )}
                  {result.stderr && (
                    <pre className="text-red-400 whitespace-pre-wrap break-all">{result.stderr}</pre>
                  )}
                  {!result.stdout && !result.stderr && (
                    <span className="text-stone-500 italic">
                      {t("teach.noOutput", { defaultValue: "(no output)" })}
                    </span>
                  )}
                  {result.returncode !== 0 && (
                    <div className="mt-1 text-[10px] text-red-500">
                      Exit code: {result.returncode}
                    </div>
                  )}
                </>
              ) : null}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
