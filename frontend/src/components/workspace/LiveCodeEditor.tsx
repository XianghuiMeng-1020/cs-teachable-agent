import { useState } from "react";
import { Play, Loader2, Terminal } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { runPythonSandbox } from "@/api/client";
import { cn } from "@/lib/utils";

export interface LiveCodeEditorProps {
  initialCode?: string;
  language?: string;
  maxHeight?: string;
  className?: string;
}

const DEFAULT_CODE = `# Try some Python
print("Hello from the TA!")
x = 2 + 2
print(f"2 + 2 = {x}")
`;

export function LiveCodeEditor({
  initialCode = DEFAULT_CODE,
  language = "python",
  maxHeight = "240px",
  className,
}: LiveCodeEditorProps) {
  const [code, setCode] = useState(initialCode);
  const [stdin, setStdin] = useState("");
  const [output, setOutput] = useState<{ stdout: string; stderr: string; returncode: number } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    setOutput(null);
    try {
      const result = await runPythonSandbox(code, stdin);
      setOutput(result);
    } catch (err) {
      setOutput({
        stdout: "",
        stderr: err instanceof Error ? err.message : "Failed to run code",
        returncode: -1,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={cn("flex flex-col rounded-xl border border-slate-200 bg-white shadow-card", className)}>
      <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-3 py-2">
        <span className="flex items-center gap-2 text-sm font-medium text-slate-700">
          <Terminal className="h-4 w-4 text-brand-500" />
          Live Python
        </span>
        <Button
          icon={loading ? Loader2 : Play}
          size="sm"
          onClick={handleRun}
          disabled={loading}
          loading={loading}
        >
          Run
        </Button>
      </div>
      <div className="grid gap-0 border-b border-slate-100">
        <div className="border-b border-slate-100">
          <label className="block px-3 py-1.5 text-xs font-medium text-slate-500">Code</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full resize-y rounded-none border-0 bg-slate-900/5 px-3 py-2 font-mono text-sm text-slate-800 focus:ring-2 focus:ring-brand-500/20"
            style={{ minHeight: "120px", maxHeight: "300px" }}
            spellCheck={false}
          />
        </div>
        <div>
          <label className="block px-3 py-1.5 text-xs font-medium text-slate-500">Stdin (optional)</label>
          <input
            type="text"
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            placeholder="Input for your program"
            className="w-full border-0 border-t border-slate-100 bg-slate-50/50 px-3 py-2 text-sm focus:ring-2 focus:ring-brand-500/20"
          />
        </div>
      </div>
      {output && (
        <div className="flex flex-col p-3">
          <span className="mb-1 text-xs font-medium text-slate-500">Output</span>
          <pre className="rounded-lg bg-slate-900 px-3 py-2 font-mono text-xs text-slate-100 overflow-x-auto">
            {output.stdout || "(no stdout)"}
          </pre>
          {output.stderr && (
            <pre className="mt-2 rounded-lg bg-amber-950/30 px-3 py-2 font-mono text-xs text-amber-800 overflow-x-auto">
              {output.stderr}
            </pre>
          )}
          {output.returncode !== 0 && output.returncode !== -1 && (
            <p className="mt-1 text-xs text-slate-500">Exit code: {output.returncode}</p>
          )}
        </div>
      )}
    </div>
  );
}
