import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { getHistory } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { TimelineView } from "@/components/state/TimelineView";
import type { TimelineEvent } from "@/components/state/TimelineView";
import { formatRelative } from "@/lib/utils";

export function HistoryPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["ta", currentTaId, "history", page, typeFilter],
    queryFn: () =>
      getHistory(currentTaId!, { page, per_page: 20, type: typeFilter !== "all" ? typeFilter : undefined }),
    enabled: currentTaId != null,
  });

  const events: TimelineEvent[] = (data?.items ?? []).map((i) => ({
    id: i.id,
    type: i.type as TimelineEvent["type"],
    title: i.title,
    description: i.description,
    timestamp: formatRelative(i.timestamp),
    metadata: i.metadata,
  }));

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-stone-900">History</h1>
        <div className="flex gap-2">
          {["all", "teach", "test_pass", "test_fail"].map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => { setTypeFilter(t); setPage(1); }}
              className={`rounded-lg border px-3 py-1.5 text-sm font-medium ${
                typeFilter === t
                  ? "border-brand-700 bg-brand-50 text-brand-700"
                  : "border-stone-200 text-stone-600 hover:bg-stone-50"
              }`}
            >
              {t === "all" ? "All" : t === "teach" ? "Teaching" : t === "test_pass" ? "Passed" : "Failed"}
            </button>
          ))}
        </div>
      </div>

      <Card padding="md">
        {isLoading ? (
          <p className="text-sm text-stone-500">Loading...</p>
        ) : events.length === 0 ? (
          <p className="text-sm text-stone-500">No events yet. Teach or run tests to see history.</p>
        ) : (
          <>
            <TimelineView events={events} />
            {data && data.total > data.per_page && (
              <div className="mt-4 flex justify-center gap-2">
                <button
                  type="button"
                  className="rounded-lg border border-stone-200 px-3 py-1.5 text-sm disabled:opacity-50"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}
                >
                  Previous
                </button>
                <span className="py-1.5 text-sm text-stone-600">
                  Page {data.page} of {Math.ceil(data.total / data.per_page)}
                </span>
                <button
                  type="button"
                  className="rounded-lg border border-stone-200 px-3 py-1.5 text-sm disabled:opacity-50"
                  disabled={page >= Math.ceil(data.total / data.per_page)}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </Card>
    </div>
  );
}
