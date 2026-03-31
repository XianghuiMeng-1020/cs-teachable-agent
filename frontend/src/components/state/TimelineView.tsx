import { cn } from "@/lib/utils";
import { CodeEditor } from "@/components/workspace/CodeEditor";

export interface TimelineEvent {
  id: string;
  type: "teach" | "test_pass" | "test_fail" | "misconception_activated" | "correction" | "relearning";
  title: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

const typeDotColors: Record<TimelineEvent["type"], string> = {
  teach: "bg-brand-500",
  test_pass: "bg-success",
  test_fail: "bg-danger",
  misconception_activated: "bg-warning",
  correction: "bg-blue-500",
  relearning: "bg-accent-500",
};

interface TimelineViewProps {
  events: TimelineEvent[];
  className?: string;
}

export function TimelineView({ events, className }: TimelineViewProps) {
  return (
    <div className={cn("space-y-0", className)}>
      <div className="border-l-2 border-stone-200 pl-4">
        {events.map((evt) => (
          <div key={evt.id} className="relative pb-6 last:pb-0">
            <div
              className={cn(
                "absolute left-[-21px] top-1 h-3 w-3 rounded-full",
                typeDotColors[evt.type]
              )}
            />
            <div className="rounded-lg border border-stone-100 bg-white p-3">
              <p className="text-sm font-medium text-stone-800">{evt.title}</p>
              <p className="mt-1 text-xs text-stone-500">{evt.description}</p>
              <p className="mt-1 text-xs text-stone-400">{evt.timestamp}</p>
              {evt.type.startsWith("test_") && evt.metadata?.ta_code && (
                <div className="mt-2">
                  <CodeEditor
                    code={String(evt.metadata.ta_code)}
                    maxHeight="120px"
                    showLineNumbers={false}
                    copyButton={false}
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
