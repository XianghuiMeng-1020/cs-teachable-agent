import { useQuery } from "@tanstack/react-query";
import { teacherTranscriptDetail } from "@/api/client";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { ExportCSVButton } from "./ExportCSVButton";
import { formatDate } from "@/lib/utils";

interface TranscriptDetailProps {
  sessionId: number;
  onBack: () => void;
}

export function TranscriptDetail({ sessionId, onBack }: TranscriptDetailProps) {
  const { data, isLoading } = useQuery({
    queryKey: ["teacher", "transcripts", sessionId],
    queryFn: () => teacherTranscriptDetail(sessionId),
  });

  if (isLoading || !data) {
    return <p className="text-sm text-slate-500">Loading...</p>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <button type="button" onClick={onBack} className="text-sm font-medium text-brand-600 hover:underline">
          ← Back to list
        </button>
        <ExportCSVButton sessionId={sessionId} />
      </div>
      <div className="flex items-center gap-2">
        <h1 className="text-xl font-bold text-slate-900">
          {data.student.username} — {formatDate(data.started_at)}
        </h1>
      </div>
      <Card padding="none">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-xs font-medium uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-4 py-3 text-left w-12">#</th>
                <th className="px-4 py-3 text-left w-28">Speaker</th>
                <th className="px-4 py-3 text-left">Content</th>
                <th className="px-4 py-3 text-left w-40">Interpreted KUs</th>
                <th className="px-4 py-3 text-left w-20">Quality</th>
              </tr>
            </thead>
            <tbody>
              {data.messages.map((msg, i) => (
                <tr key={i} className={`border-b border-slate-100 ${i % 2 === 0 ? "bg-white" : "bg-slate-50/50"}`}>
                  <td className="px-4 py-3">{msg.seq}</td>
                  <td className="px-4 py-3">
                    <Badge variant={msg.speaker === "student" ? "info" : msg.speaker === "ta" ? "default" : "outline"}>
                      {msg.speaker}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 whitespace-pre-wrap">{msg.content}</td>
                  <td className="px-4 py-3">
                    {msg.interpreted_units?.length ? (
                      <div className="flex flex-wrap gap-1">
                        {msg.interpreted_units.map((ku) => (
                          <Badge key={ku} variant="outline" size="sm">{ku}</Badge>
                        ))}
                      </div>
                    ) : (
                      "N/A"
                    )}
                  </td>
                  <td className="px-4 py-3">{msg.quality_score != null ? msg.quality_score : "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
