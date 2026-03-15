import { useState } from "react";
import * as Collapsible from "@radix-ui/react-collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { CodeEditor } from "./CodeEditor";
import { SQLVisualizer } from "./SQLVisualizer";
import { cn } from "@/lib/utils";

export interface TestResultCardProps {
  problemId: string;
  problemStatement: string;
  taCode: string;
  passed: boolean;
  details: { input?: string; expected?: string; got?: string; passed?: boolean }[];
  masteryReport?: Record<string, unknown>;
  defaultExpanded?: boolean;
  outputLabel?: string;
  reflectionPrompt?: string | null;
  /** For database domain: optional result set to visualize */
  resultRows?: Record<string, unknown>[];
  resultColumns?: string[];
}

export function TestResultCard({
  problemId,
  problemStatement,
  taCode,
  passed,
  details,
  defaultExpanded = false,
  outputLabel = "TA's code",
  reflectionPrompt,
  resultRows,
  resultColumns,
}: TestResultCardProps) {
  const [open, setOpen] = useState(defaultExpanded);

  return (
    <Card padding="none" className="overflow-hidden">
      <Collapsible.Root open={open} onOpenChange={setOpen}>
        <button
          type="button"
          className="flex w-full items-center justify-between gap-2 px-5 py-4 text-left hover:bg-slate-50/50"
          onClick={() => setOpen(!open)}
        >
          <div className="flex min-w-0 flex-1 items-center gap-2">
            <Badge variant={passed ? "success" : "danger"} size="md">
              {passed ? "PASS" : "FAIL"}
            </Badge>
            <span className="truncate text-sm font-medium text-slate-800">
              {problemId}: {problemStatement.slice(0, 60)}
              {problemStatement.length > 60 ? "..." : ""}
            </span>
          </div>
          {open ? (
            <ChevronDown className="h-4 w-4 shrink-0 text-slate-400" />
          ) : (
            <ChevronRight className="h-4 w-4 shrink-0 text-slate-400" />
          )}
        </button>
        <Collapsible.Content>
          <div className="space-y-4 border-t border-slate-100 px-5 pb-5 pt-2">
            <div>
              <h4 className="mb-1 text-xs font-medium uppercase tracking-wider text-slate-500">{outputLabel}</h4>
              <CodeEditor code={taCode} copyButton maxHeight="200px" />
            </div>
            {resultColumns && resultRows && (
              <div>
                <h4 className="mb-2 text-xs font-medium uppercase tracking-wider text-slate-500">Result set</h4>
                <SQLVisualizer columns={resultColumns} rows={resultRows} showChart />
              </div>
            )}
            <div>
              <h4 className="mb-2 text-xs font-medium uppercase tracking-wider text-slate-500">
                Test cases
              </h4>
              <ul className="space-y-2">
                {details.map((d, i) => (
                  <li
                    key={i}
                    className={cn(
                      "rounded-lg border px-3 py-2 text-sm",
                      d.passed
                        ? "border-emerald-200 bg-emerald-50/50"
                        : "border-red-200 bg-red-50/50"
                    )}
                  >
                    {d.input != null && <span className="font-mono text-xs text-slate-500">input: {d.input}</span>}
                    {d.input != null && <br />}
                    {d.expected != null && <span>expected: {d.expected}</span>}
                    {d.expected != null && <br />}
                    {d.got != null && <span>got: {d.got}</span>}
                  </li>
                ))}
              </ul>
            </div>
            {reflectionPrompt && (
              <div className="rounded-lg border border-amber-200 bg-amber-50/50 px-3 py-2 text-sm text-amber-900">
                <strong>Reflect:</strong> {reflectionPrompt}
              </div>
            )}
          </div>
        </Collapsible.Content>
      </Collapsible.Root>
    </Card>
  );
}
